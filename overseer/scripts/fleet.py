#!/usr/bin/env python3
"""Fleet snapshot for the overseer skill. Read-only.

Joins `herdr agent list` + `herdr workspace list` with each agent's Claude
transcript and prints, per session: pane, workspace label, status, worktree,
branch, the user's last prompts, and the tail of the session's last reply.

  fleet.py                 one block per live agent
  fleet.py --brief         one line per live agent
  fleet.py --find TEXT     only sessions whose prompts/replies mention TEXT
  fleet.py --prs           also list my open PRs by branch (one REST call)
  fleet.py -n 6 -t 900     prompts shown / reply tail chars
"""
import argparse, glob, json, os, subprocess, sys

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
            # Skip tool results, harness notices and compaction summaries: only what the user typed.
            if d.get("isMeta") or txt.startswith("<") or txt.startswith("This session is being continued"):
                continue
            prompts.append((ts, txt))
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--find")
    ap.add_argument("--prs", action="store_true")
    ap.add_argument("-n", type=int, default=8)
    ap.add_argument("-t", type=int, default=1400)
    a = ap.parse_args()

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
