#!/usr/bin/env python3
"""Fleet snapshot for the overseer skill. Read-only.

Joins `herdr agent list` + `herdr workspace list` with each agent's Claude
transcript and prints, per session: pane, workspace label, status, worktree,
branch, the last prompts entered in the pane, and the tail of the session's
last reply. A prompt sent by another agent through `herdr agent prompt` is
recorded like a paste by the user; those are tagged [pasted] or [relay], and
only an untagged prompt is certainly the user's own typing.

  fleet.py                 one block per live agent
  fleet.py --brief         one line per live agent
  fleet.py --find TEXT     only sessions whose prompts/replies mention TEXT
  fleet.py --prs           also list my open PRs by branch (one REST call)
  fleet.py -n 6 -t 900     prompts shown / reply tail chars
  fleet.py --slots REPO    FREE or BUSY for each standing worktree REPO-wt<N>
                           (git state, PR state, agent state; one gh call each)
"""
import argparse, glob, json, os, re, subprocess, sys

def herdr(*args):
    try:
        out = subprocess.run(["herdr", *args], capture_output=True, text=True, timeout=20).stdout
        return json.loads(out).get("result", {})
    except Exception as e:
        sys.exit(f"herdr {' '.join(args)} failed: {e}")

def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""

QUIET_COMMANDS = {"/clear", "/model", "/fast", "/effort", "/status", "/usage", "/login", "/compact", "/resume"}
RELAY = re.compile(r"relayed (by|from)|^(Lead|Parent|Overseer) here|^From .{0,40}'s session in ", re.I)
PASTE = re.compile(r"</?pasted_content[^>]*>")

def entered_prompt(d, txt):
    """Return the prompt entered in the pane, or None for harness-generated turns."""
    if d.get("isMeta") or d.get("isCompactSummary") or txt.startswith("[Request interrupted"):
        return None
    cmd = re.search(r"<command-name>(/[\w:-]+)</command-name>", txt)
    if cmd:
        if cmd.group(1) in QUIET_COMMANDS:
            return None
        args = re.search(r"<command-args>(.*?)</command-args>", txt, re.S)
        return (cmd.group(1) + " " + (args.group(1).strip() if args else "")).strip()
    origin = d.get("origin")
    if isinstance(origin, dict) and origin.get("kind") != "human":
        return None
    pasted = bool(PASTE.search(txt))
    txt = PASTE.sub("", txt).strip()
    if not isinstance(origin, dict) and (txt.startswith("<") or txt.startswith("This session is being continued")):
        return None  # older transcripts carry no origin field
    tag = "[relay] " if RELAY.search(txt[:300]) else "[pasted] " if pasted else ""
    return tag + txt

def read_session(sid):
    hits = glob.glob(os.path.expanduser(f"~/.claude/projects/*/{sid}.jsonl"))
    if not hits:
        return None
    prompts, last, last_ts, branch = [], "", "", ""
    for line in open(hits[0], errors="ignore"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("isSidechain"):
            continue
        branch = d.get("gitBranch") or branch
        msg = d.get("message") or {}
        txt = text_of(msg.get("content")).strip()
        if not txt:
            continue
        ts = (d.get("timestamp") or "")[5:16]
        if d.get("type") == "user":
            p = entered_prompt(d, txt)
            if p:
                prompts.append((ts, p))
        elif d.get("type") == "assistant":
            last, last_ts = txt, ts
    return {"branch": branch, "prompts": prompts, "last": last, "last_ts": last_ts,
            "kb": os.path.getsize(hits[0]) // 1000}

def my_prs():
    try:
        out = subprocess.run(["gh", "api", "--paginate", "search/issues?q=is:pr+is:open+author:@me&per_page=100",
                              "--jq", ".items[] | [.number, .draft, .title, .repository_url] | @tsv"],
                             capture_output=True, text=True, timeout=40).stdout
    except Exception:
        return []
    return [l.split("\t") for l in out.splitlines() if l]

def git(wt, *args):
    return subprocess.run(["git", "-C", wt, *args], capture_output=True, text=True).stdout.strip()

def slots(repo):
    """Standing worktrees <repo>-wt1..wt9: which can take a new feature."""
    agents = {}
    for ag in herdr("agent", "list").get("agents", []):
        agents.setdefault(ag.get("cwd", ""), []).append(ag)
    open_ws = {w.get("path"): w.get("open_workspace_id")
               for w in herdr("worktree", "list", "--cwd", repo).get("worktrees", [])}
    for wt in sorted(w for w in glob.glob(repo.rstrip("/") + "-wt*") if re.search(r"-wt\d+$", w)):
        branch = git(wt, "branch", "--show-current") or "(detached)"
        dirty = len(git(wt, "status", "--porcelain").splitlines())
        unpushed = git(wt, "rev-list", "--count", "@{u}..HEAD") or "no upstream"
        ahead = git(wt, "rev-list", "--count", "origin/main..HEAD") or "?"
        try:
            pr = json.loads(subprocess.run(
                ["gh", "pr", "list", "--head", branch, "--state", "all", "--limit", "1", "--json", "number,state,isDraft"],
                capture_output=True, text=True, timeout=30, cwd=wt).stdout or "[]")
        except Exception:
            pr = []
        state = pr[0]["state"] if pr else "NONE"
        ags = agents.get(wt, [])
        status = ",".join(f"{a['pane_id']}:{a.get('agent_status')}" for a in ags) or "no agent"
        why = []
        if any(a.get("agent_status") in ("working", "blocked") for a in ags):
            why.append("agent busy")
        if dirty:
            why.append(f"{dirty} dirty files")
        if state == "OPEN":
            why.append(f"PR {pr[0]['number']} open")
        if state == "NONE" and ahead not in ("0", "?"):
            why.append(f"{ahead} commits with no PR")
        if unpushed not in ("0", "no upstream"):
            why.append(f"{unpushed} unpushed")
        prs = f"PR {pr[0]['number']} {state}" if pr else "no PR"
        print(f"{'FREE' if not why else 'BUSY'} | {os.path.basename(wt)} | ws {open_ws.get(wt) or 'not open'} | {status} | "
              f"{branch} | {prs} | {'; '.join(why) or 'clean, feature finished'}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--find")
    ap.add_argument("--prs", action="store_true")
    ap.add_argument("--slots", metavar="REPO", help="primary checkout, e.g. ~/code/myrepo")
    ap.add_argument("-n", type=int, default=8)
    ap.add_argument("-t", type=int, default=1400)
    a = ap.parse_args()
    if a.slots:
        return slots(os.path.abspath(os.path.expanduser(a.slots)))

    labels = {w["workspace_id"]: (w.get("number"), w.get("label")) for w in herdr("workspace", "list").get("workspaces", [])}
    me = os.environ.get("HERDR_PANE_ID")
    for ag in herdr("agent", "list").get("agents", []):
        sid = (ag.get("agent_session") or {}).get("value", "")
        s = read_session(sid) if sid else None
        num, label = labels.get(ag.get("workspace_id"), ("?", "?"))
        if a.find:
            hay = " ".join(p for _, p in (s or {}).get("prompts", [])) + (s or {}).get("last", "") + (label or "")
            if a.find.lower() not in hay.lower():
                continue
        cwd = ag.get("cwd", "").replace(os.path.expanduser("~") + "/", "")
        head = (f"{ag['pane_id']}{' (me)' if ag['pane_id'] == me else ''} | ws {num} \"{label}\" | {ag.get('agent')} "
                f"{ag.get('agent_status')} | {cwd} | {(s or {}).get('branch', '?')} | {sid[:8]}")
        if a.brief:
            lastp = s["prompts"][-1] if s and s["prompts"] else ("", "")
            print(f"{head} | last ask [{lastp[0]}]: {lastp[1][:110]!r}")
            continue
        print(f"\n######## {head}")
        if not s:
            print("  (no transcript found)")
            continue
        for ts, p in s["prompts"][-a.n:]:
            print(f"  U[{ts}Z] {p[:400]}")
        print(f"  LAST REPLY [{s['last_ts']}Z] ({s['kb']}KB transcript):")
        print("    " + s["last"][-a.t:].replace("\n", "\n    "))
    if a.prs:
        print("\n######## my open PRs (number, draft, title, repo)")
        for row in my_prs():
            print("  " + " | ".join(row))

if __name__ == "__main__":
    main()
