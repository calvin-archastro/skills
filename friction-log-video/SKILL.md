---
name: friction-log-video
description: >
  Produce a recorded friction-log video of a product journey, five minutes at
  most: write the scenario, stage it as beats in Splice, write a script the
  person records in one take (screen, face and voice), then cut that take into a
  finished video with a pre-roll intro, the person's face in frame, fades,
  click zooms, annotations and clear persona handoffs. Scenarios and scripts
  are kept in the project's docs/friction-logs/ for reuse, and each can run
  against the local stack or staging. Needs the Splice video editor and its
  splice skill. Use when the user asks for a friction log video, a recorded
  walkthrough or demo of a flow, a script to record, or to re-run or re-cut a
  saved friction log.
---

# Friction log video

A friction log video shows one person using the product for real and saying
what they expected, what happened, and where it cost them time. The person
records once. You plan before the take and cut after it.

```text
1 Scenario ──> 2 Stage ──> 3 Script ──> 4 Record ──> 5 Cut ──> 6 Finish ──> 7 Findings
  repo file     Splice      repo file    one take     slice     intro, zoom,   repo file
                beats                    (person)     (you)     notes, fades
```

Load the **splice** skill before step 2. It is the reference for every
`splice ctl` command used here; this skill only says which ones to use and in
what order. Recipes for the intro, persona cards and annotation scenes are in
[references/splice-recipes.md](references/splice-recipes.md).

## Where things live

| What | Where | Committed |
|---|---|---|
| Scenario, script, findings | `docs/friction-logs/<slug>/` | yes |
| Index of scenarios, environments | `docs/friction-logs/README.md` | yes |
| Splice project, raw take, exported video | `~/Movies/Splice/friction-logs/` | no |

```text
docs/friction-logs/<slug>/
  scenario.md              # goal, personas, environments, beats (the plan)
  script.md                # what the person says and does, one take
  runs/<date>-<env>.md     # findings from one recording, with timestamps
```

- Slugs are kebab-case and name the journey: `invite-teammate`,
  `thread-handoff-to-agent`.
- Start from `templates/scenario.md` and `templates/script.md` in this skill.
  If `docs/friction-logs/README.md` does not exist, create it from
  `templates/README.md`.
- Before writing a new scenario, read `docs/friction-logs/README.md`. If the
  journey exists, reuse it: re-run it on another environment, or update it.
- Add a row to the README index for each new scenario.
- No secrets, passwords or tokens in any of these files. Name the env var or
  vault item that holds them.

## Choose the mode

| The person wants | Do |
|---|---|
| A new friction log video | Steps 1 to 7 |
| The script only | Steps 1 and 3 |
| To re-run a saved scenario | Read its files, then steps 2 to 7 |
| To re-cut footage already recorded | Steps 5 to 7 |
| To see what exists | Read `docs/friction-logs/README.md` |

## 1. Scenario

Write `docs/friction-logs/<slug>/scenario.md` from the template. Settle these
with the person before anything else:

1. **Goal.** One sentence naming what the user is trying to get done.
2. **Personas.** Each has a name, a role, an accent colour and its own browser
   window. Two or more personas means the handoff rules in step 3 and step 6
   apply.
3. **Environment.** Local, staging, or both. See "Environments" below.
4. **Beats.** The journey as 4 to 9 beats. Each beat has one persona, one user
   action, what done looks like, and a length in seconds.

Time budget, 300 seconds in total:

| Part | Seconds |
|---|---|
| Intro pre-roll | 4 to 6 |
| Hook: who I am, what I am trying to do | 10 to 15 |
| Journey beats | 200 to 230 |
| Persona cards, about 2 s each | as needed |
| Verdict: top three frictions | 20 to 30 |
| End card | 3 to 4 |

- Add the beat lengths up in the scenario file. If the plan is over 300 s, cut
  a beat or split the journey into two slugs. Do not plan to speed-talk.
- Walk the journey yourself first when you can (agent-browser against the same
  environment). You learn where the friction is, how long pages take, and what
  data must exist. If the project already has a written walkthrough of this
  journey, reuse its steps.

### Environments

The scenario lists both environments so the same script runs on either. The
script uses `$APP_URL`; the run picks the value.

#### Research how to run it

Do this before writing beats, for every environment the scenario lists. A
scenario nobody can start is not reusable.

1. Read what is already known: the "Environments" section of
   `docs/friction-logs/README.md` and the "How this was run" section of the
   latest findings file for this scenario or a neighbouring one.
2. Fill the gaps from the project, in this order: README, AGENTS.md and
   CLAUDE.md, the project's own skills, service and task-runner config,
   test and synthetic-check config (it usually names the staging URLs), and
   the sign-in route's source.
3. Find, for each environment:
   - the base URL, and for local, how the port is found;
   - the command that starts the stack and how long it takes to be ready;
   - a check that the app answers (health URL or page);
   - how a persona signs in and how its role is set;
   - how the data the journey needs is created;
   - how to reset or clean up afterwards.
4. Try what you can without changing anything: resolve the port, call the
   health check, open the sign-in page. Mark each fact as **checked** (you ran
   it and it worked) or **from docs** (read, not run).
5. Ask the person only for what the project cannot tell you, such as where
   staging test accounts are kept.
6. Write the result in two places:
   - facts that hold for every scenario go in the "Environments" section of
     `docs/friction-logs/README.md`;
   - facts for this journey (data to create, starting pages, cleanup) go in
     the scenario's Environment section.

Do not guess a URL, a port or a sign-in route. If something could not be
found, write "unknown" with what you tried, and resolve it with the person
before recording.

**Local**

1. The person starts the stack. Do not start it for them.
2. Resolve the URL and ports the way the project documents, and check the
   app answers before recording.
3. Sign each persona in, one browser window per persona. Use the project's
   development sign-in if it has one, and set each persona's role explicitly.
4. Local shows the code in this checkout. Write the commit (`git rev-parse
   --short HEAD`) in the findings file.

**Staging**

1. Each persona signs in for real, with a test account kept for this purpose.
   The scenario names where the credentials are kept, not the credentials.
2. Sign in before recording starts, so no password or magic link is on screen.
3. Data made on staging stays there. Name everything the run creates with a
   tag (`fl-<date>`), and list the cleanup in the scenario.
4. Do not change staging infrastructure for a recording.
5. Staging can show other people's data. Note what must be hidden; step 6
   redacts it.
6. Write the date and time (UTC) of the recording in the findings file, since
   staging moves.

## 2. Stage it in Splice

1. Check Splice (`splice ctl status`). If it is not running, ask the person to
   open it.
2. Ask the person to make a new project saved as
   `~/Movies/Splice/friction-logs/<slug>-<date>-<env>.splice`.
3. Confirm `status` names that project and its `duration` is 0. If any other
   project is open, pass `--project <name>` on every command. Never edit a
   project the person did not make for this video.
4. Set the canvas: `splice ctl canvas --aspect 16:9 --fps 30`.
5. Add one beat per row of the scenario, in order, with its planned length:

   ```sh
   splice ctl story add --title "Hook" --duration 12 \
     --story "Dana, admin at Acme, wants to invite Sam" --capture "Camera full frame"
   splice ctl story add --title "Dana · Open members" --duration 30 \
     --story "Find the invite button" --capture "Screen: Settings > Members, face bubble"
   ```

   Put the persona's name first in every beat title.
6. Add a cue at each persona change: `splice ctl cue add --at 96 --label
   "HANDOFF Dana -> Sam"`.
7. `splice ctl story read`: the beats must end at or before 300 s. Fix the plan
   in `scenario.md` first, then the board, so the two stay the same.
8. `splice ctl view story` and ask the person to approve the board.

## 3. Script

Write `docs/friction-logs/<slug>/script.md` from the template. The person
reads it while recording, so it must work at a glance.

- One block per beat: persona, **SAY**, **DO**, **REACT**.
- **SAY** is written out for the hook, the handoffs and the verdict. Keep it to
  about 2.2 words per second of the beat.
- **DO** is the clicks, one per line, with the exact labels on screen.
- **REACT** is a prompt, not a line: "Say what you expected here, then what you
  got." The reactions are the friction log. Do not write them for the person.
- Each beat opens with a short **anchor line** that appears nowhere else in
  the script ("Next, the members page."). You find beats by these lines in the
  transcript.

Rules the person follows, printed at the top of the script:

1. Record everything in one take. Do not stop the recording.
2. Pause for a full second between beats.
3. After a mistake, pause, say "again", and repeat the beat from its anchor
   line. The last attempt is the one kept.
4. While a page loads, keep quiet or say what you are waiting for. Do not fill.
5. At a handoff, say the handoff line, then switch windows.

Handoffs in the script:

- A full-width banner between the beats: `HANDOFF  Dana (admin, window 1) ->
  Sam (member, window 2)`.
- A spoken line that names both people: "That is Dana's side done. Now I am
  Sam, a new member, opening the invite."
- One browser window per persona, each visibly different (profile colour or
  theme), so the footage itself shows who is acting.

## 4. Record

1. Preflight with the person:
   - personas signed in, each in its own window, at the starting page;
   - notifications off, bookmarks bar hidden, unrelated tabs closed;
   - browser zoom at 110 to 125 percent so text reads at 1080p;
   - the script on a second display, a phone or paper, not on the recorded
     display.
2. Set up the take. Read `splice ctl record sources` first and check that
   screen, camera and microphone access are granted.

   ```sh
   # one persona: record the browser window
   splice ctl record setup --screen window:Chrome --camera default --microphone default \
     --layout bubble --corner br --size 0.26 --shape circle --mirror --clean --clicks --cursor
   # two or more personas: record the display, so every window is in the take
   splice ctl record setup --screen display:1 --camera default --microphone default \
     --layout bubble --corner br --size 0.26 --shape circle --mirror --clean --clicks --cursor
   ```

3. Ask before starting. Then `splice ctl record start --at 0`, so the take
   starts at the beginning of the timeline.
4. The person runs the script once, start to finish.
5. `splice ctl record stop --wait`. Keep the reply: it lists the screen, camera
   and microphone clips and the take's folder.
6. `splice ctl save --label "raw take"`, so the uncut take can be restored.

## 5. Cut the take

The take is three or four clips that start together (screen, camera,
microphone, sometimes system sound). Every cut applies to all of them at the
same times, or the face and voice drift from the screen.

1. Transcribe: `splice ctl captions --clip <microphone clip> --wait`, then
   `splice ctl read`. Each caption is a clip with its words, `start` and `end`.
2. Build the cut list from the captions:
   - find each beat by its anchor line;
   - where "again" was said, keep only the attempt after the last one;
   - mark silences over 1.5 s between beats;
   - mark the head before the hook and the tail after the verdict.
3. Write the cut list as a table (keep or drop, from, to, beat) and check the
   kept time: it must fit the budget with room for the intro, cards and end
   card.
4. Delete the caption clips. They were for timing; their times are wrong once
   the take is cut.
5. Apply the drops from the end of the timeline to the start, so earlier times
   stay valid. For each range:

   ```sh
   splice ctl split --at 212.4          # every clip under that time
   splice ctl split --at 219.8
   splice ctl delete --clip 31,32,33 --ripple   # every layer's piece of that range
   ```

   Include the system-sound piece when the take has one. A layer left out
   keeps its length and drifts.

6. After each ripple, `read` and check that every layer's pieces of each
   section still share a start time. If they do not, `undo`
   and close the gap with `move` instead.
7. Look at a frame from the middle of every kept section (`splice ctl frame`).

Waiting is friction. Do not cut out a slow load, a spinner or an error. Shorten
it with `splice ctl speed --clip <piece> --rate 6` on every layer's piece,
sound included, set the sound pieces' volume to 0, and add a label with the
real time ("waited 14 s"). Cut only the person's own mistakes and dead air.

## 6. Finish

Work in this order. Check each with `splice ctl frame` before the next.

1. **Intro pre-roll, 4 to 6 s.** Use the `Friction log intro` symbol; make it
   once from the recipe if `splice ctl symbol list` does not have it. Run
   `symbol read` on the use and fill the labels it reports: one with the
   journey, one with product, environment and date. Make room first by moving
   the cut to start after it.
2. **Face in frame.**
   - Hook and verdict: the camera fills the frame. Split the camera clip at
     the section's edges and set that piece to full size with `look`.
   - Journey: the camera stays a round bubble in a corner. Where it covers the
     control being used, move that piece of the camera clip to another corner.
   - The face is never hidden for a whole beat.
3. **Click zooms.** `splice ctl zoom --clip <screen piece> --to 1.8` on each
   screen piece. Scan frames: remove the zoom (`--none`) where it hides
   something the person is talking about, and add a keyframed push-in where
   they point at something without clicking. `--none` clears every zoom on
   that piece; to drop one zoom, split the piece around it first.
4. **Annotations.** One per friction, as a see-through scene over the screen:
   a ring or box on the spot, an arrow, and a label of six words at most.
   - Colour by kind: red for friction, green for a good moment, amber for a
     wait.
   - Show each for 3.5 s, starting as the person names the problem. For
     another length, patch each layer's `exit.at` to 0.4 s before the end.
   - Place it where the zoom is steady, and check frames at its start, middle
     and end.
5. **Persona handoffs.** At each handoff cue:
   - a full-frame persona card for about 2 s, in the persona's colour, with
     name and role ("Sam · new member");
   - the card on the screen's track, touching the clips before and after it,
     with a `push-left` transition into it and a `dissolve` out of it;
   - a persona badge (name, role, colour) in the top-left corner for the whole
     of every beat, so any paused frame shows who is acting;
   - the same colour on that persona's annotations' label background.
6. **Fades.** A `dissolve` transition from the intro into the hook,
   `dip-black` between major sections, plain cuts inside a beat, and
   `look --exit fade` on the end card. Sound cannot be faded: `volume` is one
   value per clip. Start and end the voice clips in a pause instead.
7. **Redact.** Blur anything private or not the team's to show: emails of real
   people, tokens, other customers' names (`look --redact blur` on that piece).
8. **Sound.** Voice at 1. If there is intro music, keep it under 0.4 and end
   it before the hook's first word.
9. **Captions**, if the person wants them: `captions --clip <mic pieces>` on
   the finished cut, then fix misheard product names.
10. **End card, 3 to 4 s:** the three frictions as text, and where the findings
    file is.

Before export:

0. Make the board match the cut. `story remove` the beats from last to first
   (removing an earlier beat pulls later footage left), then `story add` them
   again in order, intro and cards included, with the real lengths. `read`
   after the first removal: if any clip moved, `undo` and leave the board.
1. `splice ctl status`: `duration` is 300 or less. If it is over, shorten waits
   and silences first, then drop the weakest beat. Do not speed up speech.
2. Export a draft and ask the person to watch it:
   `splice ctl export ~/Movies/Splice/friction-logs/<slug>-<date>-<env>-draft.mp4 --draft --wait`.
3. Apply their notes, then export the final with `--high --wait`.
4. You cannot hear the result. Say so, and ask the person to check the voice
   level and the music.

Do not upload or share the video unless the person asks.

## 7. Findings

Write `docs/friction-logs/<slug>/runs/<date>-<env>.md` from `templates/run.md`:

1. Environment, commit or recording time, personas, and the path of the video.
2. **How this was run**: the commands and steps actually used for this
   recording, in order, so the next person can repeat it without research.
   - starting the stack, or the staging URL;
   - the readiness check;
   - each persona's sign-in, with its role;
   - the data created before recording;
   - the cleanup done afterwards;
   - anything that differed from the README or the scenario, and what failed
     before the working way was found.
   Then correct the README's "Environments" section and the scenario where
   they were wrong.
3. A table of frictions: timestamp in the final video, persona, what happened,
   what the person expected, severity (blocker, slows, cosmetic).
4. What worked well, in two or three lines.
5. Anything in the scenario or script that should change for the next run.

Update the scenario's row in `docs/friction-logs/README.md` with the date and
environment of this run.

## Checks before calling it done

1. The video is 300 s or shorter and opens with the intro.
2. The face is visible in every beat, and full frame in the hook and verdict.
3. Every handoff has a card, a spoken line and a badge.
4. Every friction in the findings file has an annotation at its timestamp.
5. No waits were removed; shortened waits show the real time.
6. Nothing private is readable in any frame you sampled.
7. `scenario.md`, `script.md` and the findings file are in
   `docs/friction-logs/<slug>/` and the README index lists the scenario.
8. The findings file has "How this was run" with the commands used, and the
   README's "Environments" section agrees with it.
