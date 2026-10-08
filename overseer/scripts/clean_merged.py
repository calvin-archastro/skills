#!/usr/bin/env python3
"""Discard leftover changes in a worktree that are already on origin/main.

A dirty path is proven merged when what is on disk is byte-for-byte what
origin/main has at that path (same blob and mode), or the path is gone on disk
and also absent from origin/main. Discarding such a path loses nothing.
Everything else is left alone and listed.

  clean_merged.py <worktree>           dry run: verdict per dirty path
  clean_merged.py <worktree> --apply   discard the proven paths only

Refuses to apply while a Herdr agent in that worktree is working or blocked.
"""
import argparse, json, os, subprocess, sys

def git(wt, *args, stdin=None, check=False):
    r = subprocess.run(["git", "-C", wt, *args], capture_output=True, input=stdin)
    if check and r.returncode:
        sys.exit(f"git {' '.join(args)} failed: {r.stderr.decode().strip()}")
    return r.stdout

def dirty_paths(wt):
    out = git(wt, "status", "--porcelain=v1", "-z", "--untracked-files=all", check=True).decode()
    parts, paths, i = out.split("\0"), [], 0
    while i < len(parts) and parts[i]:
        code, path = parts[i][:2], parts[i][3:]
        paths.append(path)
        if code[0] in "RC":  # the next field is the path it was renamed or copied from
            i += 1
            paths.append(parts[i])
        i += 1
    return sorted(set(paths))

def on_disk(wt, path):
    full = os.path.join(wt, path)
    if os.path.islink(full):
        return "120000", git(wt, "hash-object", "--stdin", stdin=os.readlink(full).encode()).decode().strip()
    if os.path.isfile(full):
        mode = "100755" if os.access(full, os.X_OK) else "100644"
        return mode, git(wt, "hash-object", "--", path).decode().strip()
    return None

def on_main(wt, path):
    out = git(wt, "ls-tree", "origin/main", "--", path).decode().strip()
    if not out:
        return None
    mode, kind, blob = out.split("\t")[0].split()
    return (mode, blob) if kind == "blob" else ("other", blob)

def agent_busy(wt):
    try:
        out = subprocess.run(["herdr", "agent", "list"], capture_output=True, text=True, timeout=20).stdout
        agents = json.loads(out)["result"]["agents"]
    except Exception:
        return False
    return any(a.get("cwd") == wt and a.get("agent_status") in ("working", "blocked") for a in agents)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("worktree")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    wt = os.path.abspath(os.path.expanduser(a.worktree))
    git(wt, "fetch", "-q", "origin", "main", check=True)

    proven, kept = [], []
    for p in dirty_paths(wt):
        disk, main_ = on_disk(wt, p), on_main(wt, p)
        if os.path.isdir(os.path.join(wt, p)) and not os.path.islink(os.path.join(wt, p)):
            kept.append((p, "directory or submodule"))
        elif disk == main_:
            proven.append((p, "identical to origin/main" if disk else "absent here and on origin/main"))
        elif disk is None:
            kept.append((p, "deleted here, still on origin/main"))
        elif main_ is None:
            kept.append((p, "not on origin/main"))
        else:
            kept.append((p, "differs from origin/main"))

    for p, why in proven:
        print(f"MERGED  {p}  ({why})")
    for p, why in kept:
        print(f"KEEP    {p}  ({why})")
    print(f"{os.path.basename(wt)}: {len(proven)} proven merged, {len(kept)} kept")

    if not a.apply or not proven:
        return
    if agent_busy(wt):
        sys.exit("an agent in this worktree is working or blocked; nothing discarded")
    for p, _ in proven:
        if git(wt, "ls-tree", "HEAD", "--", p):
            git(wt, "restore", "--source=HEAD", "--staged", "--worktree", "--", p, check=True)
        else:
            git(wt, "rm", "-q", "--cached", "--ignore-unmatch", "--", p, check=True)
            full = os.path.join(wt, p)
            if os.path.lexists(full):
                os.remove(full)
    left = git(wt, "status", "--porcelain").decode().splitlines()
    print(f"discarded {len(proven)}; {len(left)} dirty paths remain")

if __name__ == "__main__":
    main()
