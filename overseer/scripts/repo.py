#!/usr/bin/env python3
"""Per-repository setup for the overseer skill.

  repo.py inspect <checkout>               read-only: what this repo normally uses
  repo.py slots <checkout>                 FREE or BUSY for each standing worktree <repo>-wt<N>
  repo.py init-slots <checkout> --count N  create missing <repo>-wt1..wtN (detached at the default branch)

<checkout> is any checkout of the repo; the primary one is found from it.
`inspect` and `slots` change nothing. `init-slots` only adds worktrees.
"""
import argparse, collections, glob, json, os, re, subprocess, sys

# Files that show which agent harness a repo is set up for. AGENTS.md is read
# by several harnesses, so it is not evidence for any one of them.
MARKERS = {"claude": ["CLAUDE.md", ".claude"], "codex": [".codex"], "cursor": [".cursor", ".cursorrules"],
           "gemini": ["GEMINI.md", ".gemini"], "opencode": [".opencode", "opencode.json"], "copilot": [".github/copilot-instructions.md"]}
INSTRUCTIONS = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules", ".github/copilot-instructions.md"]

def run(cmd, cwd=None, timeout=30):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout).stdout.strip()
    except Exception:
        return ""

def git(wt, *args):
    return run(["git", "-C", wt, *args])

def herdr(*args):
    try:
        return json.loads(run(["herdr", *args])).get("result", {})
    except Exception:
        return {}

def primary(checkout):
    out = git(os.path.abspath(os.path.expanduser(checkout)), "worktree", "list", "--porcelain")
    if not out:
        sys.exit(f"{checkout} is not a git checkout")
    return out.splitlines()[0].split(" ", 1)[1]

def base_ref(repo):
    """Remote default branch as a ref, e.g. origin/main."""
    ref = git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if ref:
        return ref
    for cand in ("origin/main", "origin/master"):
        if git(repo, "rev-parse", "--verify", "-q", cand):
            return cand
    sys.exit("cannot find the remote default branch; run `git remote set-head origin --auto`")

def slot_paths(repo):
    found = [w for w in glob.glob(repo.rstrip("/") + "-wt*") if re.search(r"-wt\d+$", w)]
    return sorted(found, key=lambda w: int(re.search(r"(\d+)$", w).group(1)))

def agents_in(repo):
    return [a for a in herdr("agent", "list").get("agents", [])
            if (a.get("cwd") or "") == repo or (a.get("cwd") or "").startswith(repo + "-")]

def inspect(repo):
    base = base_ref(repo)
    slots_ = slot_paths(repo)
    live = collections.Counter(a.get("agent") for a in agents_in(repo))
    marked = [k for k, files in MARKERS.items() if any(os.path.exists(os.path.join(repo, f)) for f in files)]
    me = next((a.get("agent") for a in herdr("agent", "list").get("agents", [])
               if a.get("pane_id") == os.environ.get("HERDR_PANE_ID")), None)
    harness = (live.most_common(1)[0][0] if live else None) or me or (marked[0] if marked else None)
    remote = git(repo, "remote", "get-url", "origin")
    host = "github" if "github.com" in remote else "gitlab" if "gitlab" in remote else "other"
    hooks = git(repo, "config", "core.hooksPath") or ".git/hooks"
    others = [l.split(" ", 1)[1] for l in git(repo, "worktree", "list", "--porcelain").splitlines()
              if l.startswith("worktree ")][1:]
    print(f"repo: {repo}")
    print(f"default branch: {base}")
    print(f"harness: {harness or 'unknown'}  (live sessions here: {dict(live) or 'none'}; "
          f"repo files: {marked or 'none'}; this session: {me or 'unknown'})")
    print(f"standing slots: {', '.join(os.path.basename(s) for s in slots_) or 'none'}")
    print(f"other worktrees: {len([o for o in others if o not in slots_])}")
    print(f"instruction files: {[f for f in INSTRUCTIONS if os.path.exists(os.path.join(repo, f))] or 'none'}")
    print(f"PR host: {host} ({remote or 'no origin remote'}); gh cli: {'yes' if run(['gh', '--version']) else 'no'}")
    print(f"hooks: {hooks}")

def slots(repo):
    base = base_ref(repo)
    paths = slot_paths(repo)
    if not paths:
        print(f"no standing slots for {repo}; use one-off worktrees, or `repo.py init-slots` to create some")
        return
    agents = collections.defaultdict(list)
    for ag in agents_in(repo):
        agents[ag.get("cwd", "")].append(ag)
    open_ws = {w.get("path"): w.get("open_workspace_id")
               for w in herdr("worktree", "list", "--cwd", repo).get("worktrees", [])}
    for wt in paths:
        branch = git(wt, "branch", "--show-current")
        dirty = len(git(wt, "status", "--porcelain").splitlines())
        unpushed = git(wt, "rev-list", "--count", "@{u}..HEAD") or "no upstream"
        ahead = git(wt, "rev-list", "--count", f"{base}..HEAD") or "?"
        pr = []
        if branch:
            try:
                pr = json.loads(run(["gh", "pr", "list", "--head", branch, "--state", "all", "--limit", "1",
                                     "--json", "number,state"], cwd=wt) or "[]")
            except ValueError:
                pr = []
        state = pr[0]["state"] if pr else "NONE"
        ags = agents.get(wt, [])
        status = ",".join(f"{a['pane_id']}:{a.get('agent')}:{a.get('agent_status')}" for a in ags) or "no agent"
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
              f"{branch or '(detached)'} | {prs} | {'; '.join(why) or 'clean, nothing in flight'}")

def init_slots(repo, count):
    base = base_ref(repo)
    remote, branch = base.split("/", 1)
    git(repo, "fetch", "-q", remote, branch)
    for n in range(1, count + 1):
        path = f"{repo.rstrip('/')}-wt{n}"
        if os.path.exists(path):
            print(f"exists   {path}")
            continue
        r = subprocess.run(["git", "-C", repo, "worktree", "add", "--detach", path, base], capture_output=True, text=True)
        print(f"{'created' if r.returncode == 0 else 'FAILED '}  {path}  {r.stderr.strip().splitlines()[-1] if r.returncode else ''}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["inspect", "slots", "init-slots"])
    ap.add_argument("checkout")
    ap.add_argument("--count", type=int)
    a = ap.parse_args()
    repo = primary(a.checkout)
    if a.command == "inspect":
        inspect(repo)
    elif a.command == "slots":
        slots(repo)
    elif not a.count or a.count < 1:
        sys.exit("init-slots needs --count N")
    else:
        init_slots(repo, a.count)

if __name__ == "__main__":
    main()
