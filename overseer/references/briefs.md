# Briefs and messages

The user gives the role and the pass condition ("use a subagent adversary to
make sure the UI works and doesn't regress", "one subagent/worktree per issue -
get prs out"). You write the brief. These templates come from about 1,900
briefs written in real sessions; the weak spots found in them are fixed here.

## 1. Every brief contains

1. Situation and role in one sentence, with repo and worktree path.
2. Siblings, if any: who else is running, which region each owns, who merges.
3. Authority line with its source (see `standing-rules.md`). Default: no commit,
   no push.
4. Evidence block: observed numbers, run ids, shas, exact error text, log paths.
   Hypotheses in a separate block labelled unproven.
5. Goal in the system's terms, and the harm if it is wrong.
6. Numbered steps with a preference order and stop conditions.
7. Exact focused verification commands.
8. Scope fences: files owned, files off limits.
9. Output contract: section names, word cap, `file:line`, "confirmed by running"
   versus "suspected from reading", what was checked and found sound, where to
   write it, what to return (HEAD sha, branch, worktree).
10. Self-containedness check: could a cold agent do this from the brief and the
    files it names? If the brief points at a shared file, still inline the
    authority line, the scope fence and the report shape.

Pass the model on every subagent call. Give every editing agent a real
worktree (harness isolation, or `git worktree add` with the path in the brief);
otherwise its `git checkout` switches your checkout. Reviewers are new agents each round; use
a follow-up message only to continue the same agent on the same task.

## 2. Templates

### T1. Read-only investigation

```
Read-only research in <repo path> (ignore sibling worktrees). Do not edit or run builds.
Goal: <the decision this feeds>. Breadth: <medium | very thorough>.
Answer each with file:line and short verbatim excerpts. If something is absent, say so.
1. <exact question naming the artifact wanted>
2. <how Y flows from A to B: entry point, hand-offs, fallbacks>
3. <what already exists to mirror (exemplar file) and what is missing>
Separate what you observed from what you infer. Flag what you could not determine.
Report as numbered sections matching the questions, under <N> words.
```

### T2. Independent review of a diff

```
Independent code review of <uncommitted change in <worktree> | commit <sha> on <branch>>.
Pin: confirm `git log -1` is <sha>; if not, report and stop.
Read-only: no edits, commits, pushes or stash. You may run: <focused commands>.
Intent (what must be true): <invariants in system terms; harm if wrong>.
Author's claims (unverified): 1. ... 2. ...
Verify each claim, then spend at least half your effort on what is not on that list:
callers of changed signatures, behaviour changes for callers that did not opt in,
tenancy and viewer boundaries, races, tests that assert less than their names say,
deleted tests or features.
Try to refute each finding yourself before reporting it.
Report, under <N> words:
1. Ranked defects: file:line, concrete trigger, what happens, suggested fix,
   and "confirmed by running" or "suspected from reading".
2. What you checked and found sound.
3. Verdict: SHIP | REVISE | BLOCKED. SHIP needs no unresolved major defect and enough evidence.
No style preferences.
```

Do not hand the reviewer the author's reasoning as context; it belongs in the
claims block. Do not let the reviewer fix.

### T3. RCA of a failure

```
Repo: <org/repo>. Read the repo instruction file. Load the `rca` skill.
You are in your own worktree <path> (confirm with `git rev-parse --show-toplevel`; if it is <lead checkout>, stop).
Then: git fetch origin <default> && git checkout -B <branch> origin/<default>.
Observed: <workflow/lane>, run <id>, job <id>, sha <sha>: <exact error, failing test names>.
Logs: <command to fetch>. Also check whether it fails on other PR runs and on older main runs.
Hypothesis (unproven): <...>.
Goal: the mechanism (real bug, test race, or environment change), proven by a repro, then a fix at the cause.
No retries, timeout bumps or skips.
Repro: <exact command>.
<authority line>
Report, under <N> words: root cause with evidence (observed versus inferred), files changed,
test results before and after, worktree path and branch.
```

### T4. Implement one change among parallel agents

```
You are implementing <one change> in <repo>, in your own worktree <path>.
<N> other agents are editing <regions> in their own worktrees; I merge.
Keep edits inside <named files/regions>. Do not reformat or reorder anything else.
First confirm `git rev-parse --show-toplevel` is <your worktree path>, not <lead checkout>; if it is not, stop.
Then: git fetch origin <default> && git checkout -B <branch> origin/<default>.
<rule block from standing-rules.md>
## Observed
<numbers, ids, log paths>
## Hypothesis to verify first (unproven)
<...>
## Do
1. Establish the facts: <where to look>.
2. Smallest sound change. Preference: a, then b, then c. Stop and report if <condition>.
3. Keep working: <edge cases>.
## Verify
<exact commands>. Measure; do not estimate. Say what only CI can confirm.
## Report (under <N> words)
Evidence, what changed and why it is correct, commands and results,
what you left alone and why, HEAD sha and branch.
```

### T5. Fix-check round

```
Role: <reviewer role>, round <n>. You have not seen this before. Review only.
Do not trust this brief's claims.
Artifact: <path or sha>; verify it first.
Prior issues, each to be marked FIXED | PARTIAL | NOT FIXED with evidence:
<ID>: <symptom>. Claimed change: <...>.
Then look for anything new: regressions, edges, limits.
If you cannot check something, say so; the verdict for it is BLOCKED.
Report: 1. Verdict 2. Coverage 3. Fix check by ID 4. New issues
[ID | major/minor | bug/taste | where | evidence] 5. What to keep.
```

### T6. Cold-read check of a task node (cheap model, one round)

```
You will not see the conversation that produced this task. Read only <node file>.
Could an engineer implement and verify it from this text alone?
Return JSON: {"ready": bool, "gaps": [{"field", "blocking": bool, "question", "why"}]}.
An empty gaps list is a valid answer. Do not propose solutions.
```

### T7. Persona or adversarial panel (design, copy, UX, media)

```
Role: <master interaction designer | brand designer | technical editor | adversary trying to break X>.
You have not seen this before. Assume the author thinks it is finished and is wrong.
Artifact: <URL or path, how to capture your own evidence>.
Bar: <the user's words, e.g. "indistinguishable from an agency">. Compare against <named exemplars>.
Separate "this is broken" from "this is taste".
Report a table: issue | where | evidence | severity | concrete change. Then verdict SHIP | REVISE.
```

Run two or three roles per round, apply the proven items, and send a fresh
panel (T5) until the verdict is SHIP.

## 3. Fan-out shapes

| Work | Agents | Partition |
|---|---|---|
| Subsystem mapping | 3 to 4 read-only | one per subsystem |
| CI or incident RCA | one per independent failure | by failure |
| Independent fixes, flakes | one per issue, about four at once | own worktree, branch and PR each |
| Shared hot file | one per region | named regions; lead merges staged diffs |
| Port or batch waves | 5 to 8, then one reviewer each | by batch; later waves read the notes file |
| Task-node checks | one cheap agent per node | by node |
| Design or media review | 2 to 3 roles per round | by role |

Outputs come back as a staged diff or one local commit. The lead pushes.

## 4. Messages

To a subagent or a pane (`herdr agent prompt`). Open with state
and ids, never "as discussed". Number two or more asks. Restate the git
boundary. Say what to report.

- Relay a decision: `From <user>, relayed by the overseer session: "<their words>". This applies to <PR/branch>. Keep <...>; drop <...>.`
- Scope change: `Lead here. <PR/branch/sha>. Change: <add | drop | replace X> because <evidence or who decided>. Keep: <...>. Still: <git boundary>. Report: HEAD sha and test results.`
- CI red: `<PR> run <id>, job <name>, fails <test>: <error>. Pull gh run view --log-failed, fix the cause (no skips), new commit on top of <sha>. <push or not>. Report the new HEAD.`
- Review blockers to the author: `<PR> at <sha>: an independent review found blocking issues. Fix as new commits on top; do not amend. BLOCKING: 1. ... 2. ...`
- Stop: `Received your report. I own <loop> now. Stop any monitor on <run> and do not rerun it.`
- Nudge: `Read your output file <path> now; notifications will not resume you. Send the final report in one message: <fields>.`
- Resume: `You were stopped by <limit>, not by a mistake. State: <file>. New evidence: <...>. Pick up at <step>.`
- Cross-session handoff: `From <user>'s session in <worktree> (they asked me to hand this to you): <task>. Findings to verify: <...>. Overseer proposal, not confirmed by the user: <...>. Open question to raise with them: <...>. PR handling: <...>.`
