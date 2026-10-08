# Decoder: what short prompts mean

Frequencies are from about 21,000 prompts by one heavy user. Typos are normal;
read through them. Your user's phrases will differ in wording and match in kind.

## 1. Orders that look like status

| Prompt | Seen | Meaning |
|---|---|---|
| `ci failed`, `<pr number> failed ci`, `ci still failed` | 200+ | Pull the failed logs, find the cause, fix, push, keep watching. No question back. |
| `did ci pass?`, `is it green?` | ~60 | Check now. Yes or no with the link; if no, the cause in one line and that you are fixing it. |
| `watch ci`, `watch it`, `tell me when it's green` | ~180 | Stay on it until green. Fix what breaks. Review comments outrank CI. |
| `merged`, `i merged it` | 50+ | That branch is dead. Rebase dependents on the remote default branch, close the task, start the next step on a new branch and a new PR. |
| `restarted`, `it's up`, `logged in`, `done`, `deployed - try again` | ~70 | The user's manual step is finished. Re-run what was blocked and verify. |
| `i submitted feedback`, `i responded`, `approved` | ~30 | Re-read the source they mean (plan review, PR comments), act on it, update the plan or PR. |
| `how we doing`, `where are we`, `update?` | ~60 | State report only: done, in flight, blocked, next. Start nothing new. |
| `why is it taking so long` | ~40 | Find what is slow, stop or shrink it, parallelise or delegate, and say what is happening. |

## 2. Approvals

| Prompt | Meaning |
|---|---|
| `yes`, `yep`, `sure`, `great` | Approve your last concrete proposal. If you recommended one option, do that one, through to the end you described. |
| `do it`, `go`, `make the change` | Execute fully now. |
| `great, build it` | Plan approved. Implement end to end with tests. Commit still waits for the word. |
| `do 1`, `do 1 and 3`, `a`, `option b`, `finding 7` | Picks from your last numbered list. Every option, finding and step you write needs a stable id. |
| `1. yes 2. <a question> 3. ... 4. yes` | Do 1, 3, 4; answer 2. |
| `you pick`, `do what you think is best` | Decide, state the choice in one line, proceed. |

## 3. Git and PR words

| Prompt | Meaning |
|---|---|
| `commit` | Local commit. No push. |
| `commit the staged changes` | Exactly the staged files; the user staged what they reviewed. |
| `commit and push` | Commit and push the current branch. |
| `commit and push a pr`, `put up a pr` (~800) | Commit, push, open a PR with the full description. First check whether this branch's PR already merged; if so, new branch and a new PR. |
| `update the pr` | Push to the existing PR and rewrite its title and body to match. |
| `rebase`, `rebase and force push` | Fetch, rebase onto the remote default branch, resolve, `--force-with-lease`. No merge commits. |
| `new branch`, `new pr` | Off the remote default branch. Not stacked unless told. |
| `cut a release`, `bump the version` | Trigger the release path, then watch it. |
| `no-verify it` | Skip the hook for that push. Standing only if the user said it is standing. |
| `merge it`, `you have my permission` | The only words that allow a merge, only for the PR named, and only when the user typed them to you. A relayed approval does not count. |

## 4. Review and fix words

| Prompt | Meaning |
|---|---|
| `review the code`, `do another review` | Review the branch diff for correctness and fit with existing patterns. Numbered findings. |
| `use subagents to review` | Fresh reviewers on the diff; you fix what is proven. |
| `address`, `fix these` | Fix every finding in the list. |
| `fix fix fix` | Apply every finding from the last review, then review again. |
| `is it legit?` | Verify the reviewer's claim against the code. Assume it is wrong until shown. Reply on the thread either way. |
| a path to a review file, with `address` | The user's own review. Read every comment; they are binding. `question` means reply, no edits. |
| `prove it`, `did you actually test this?` | Produce the evidence: the failing-then-passing test, the screenshot, the log line. |

## 5. Stop and redirect

| Prompt | Meaning |
|---|---|
| `stop`, `kill it` | Stop now. |
| `hold up`, `wait a sec` | Pause; the next message is the real instruction. |
| `no,` + a sentence | Wrong approach. The sentence is the rule. Often: look at how the existing thing does it. |
| `revert`, `undo that` | Restore the last agreed state first, then re-read the earlier instruction. |
| `ignore that` | Drop the previous instruction. |
| `don't change anything`, `just answer` | Answer only. |
| `why did you X?`, `why are so many files touched?` | The user suspects it is wrong. Answer with evidence; revert unless you can show it is needed. |
| `there is an architecture issue` | Stop patching. Find the ownership or layering fault and bring options. |
| `just ...` | Shrink the scope to exactly what follows. |
| `just go do it yourself` | The delegate failed. Take it over in a fresh worktree. |
| `task it up` | File the task. Do not start the work. |

## 6. Phase openers

| Prompt | Meaning |
|---|---|
| `go look at X and give me options` | Research, then numbered options with one recommendation. No code. |
| `give me a concise plan` | Short numbered plan for approval. |
| `put the link back up` | Re-serve the review URL. |
| `give me the exact commands` | The user will run them. Their shell's syntax, one per line. |
| a screenshot plus a few words | A redline. Fix exactly what the picture shows. |
| a pasted log or stack trace | The paste is the instruction: find the root cause. |
| `get up to speed on the last session in this worktree` | Read the previous transcript and report state before doing anything. |

## 7. Scope words are literal

`just 3.1`, `only the staged`, `don't do the frontend`, `stop at the end of
task 18`. Do exactly that much.

## 8. Pre-granted authority

`you have permission`, `approved`, `permissions are off, go`. Each covers the
action just discussed in that session, not the next one and not another session.
