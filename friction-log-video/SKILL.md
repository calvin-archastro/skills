---
name: friction-log-video
description: >
  Produce a recorded friction-log video of a product journey, five minutes at
  most: write the scenario, storyboard it as beats in Splice, write a script for
  the screen take and a full numbered transcript, record the screen journey and
  the narration (face and voice) separately, then cut the narration into lines,
  lay each on its beat and finish the video with a pre-roll intro, the person's
  face in frame, fades, click zooms, annotations and clear persona handoffs.
  Scenarios, scripts and transcripts
  are kept in the project's docs/friction-logs/ for reuse, and each can run
  against the local stack or staging. Needs the Splice video editor and its
  splice skill. Use when the user asks for a friction log video, a recorded
  walkthrough or demo of a flow, a script to record, or to re-run or re-cut a
  saved friction log.
---

# Friction log video

A friction log video shows one person using the product for real and saying
what they expected, what happened, and where it cost them time. The person
records twice: the screen journey first, then the narration, read from a full
transcript. You plan before, fill the transcript between the takes, and cut
after.

```text
1 Scenario ─> 2 Storyboard ─> 3 Script and ─> 4 Screen ─> 5 Narration ─> 6 Cut ─> 7 Finish ─> 8 Findings
  repo file    Splice beats    transcript      take        take           lines    intro, zoom,  repo file
                               repo files     (person)    (person reads)  onto     notes, fades
                                                                          beats
```

Why two takes: the narration is written, so it fits each beat's time and says
the friction plainly. The screen take stays a real, unrehearsed use of the
product, and its scratch voice track is the raw friction evidence.

Load the **splice** skill before step 2. It is the reference for every
`splice ctl` command used here; this skill only says which ones to use and in
what order. Recipes for the intro, persona cards and annotation scenes are in
[references/splice-recipes.md](references/splice-recipes.md).

## Where things live

| What | Where | Committed |
|---|---|---|
| Scenario, script, transcript, findings | `docs/friction-logs/<slug>/` | yes |
| Index of scenarios, environments | `docs/friction-logs/README.md` | yes |
| Splice project, raw take, exported video | `~/Movies/Splice/friction-logs/` | no |

```text
docs/friction-logs/<slug>/
  scenario.md              # goal, personas, environments, beats (the plan)
  script.md                # what the person does in the screen take
  transcript.md            # every narration line, numbered, read in the narration take
  runs/<date>-<env>.md     # findings from one recording, with timestamps
```

- Slugs are kebab-case and name the journey: `invite-teammate`,
  `thread-handoff-to-agent`.
- Start from `templates/scenario.md`, `templates/script.md` and
  `templates/transcript.md` in this skill.
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
| The script and transcript only | Steps 1 and 3 |
| To re-run a saved scenario | Read its files, then steps 2 to 8 |
| To re-record only the narration | Step 5, then 6 to 8 |
| To re-cut footage already recorded | Steps 6 to 8 |
| To see what exists | Read `docs/friction-logs/README.md` |

## 1. Scenario

Write `docs/friction-logs/<slug>/scenario.md` from the template. Settle these
with the person before anything else:

1. **Goal.** One sentence naming what the user is trying to get done.
2. **Personas.** Each has a name, a role, an accent colour and its own browser
   window. Two or more personas means the handoff rules in step 3 and step 7
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
5. Staging can show other people's data. Note what must be hidden; step 7
   redacts it.
6. Write the date and time (UTC) of the recording in the findings file, since
   staging moves.

## 2. Storyboard it in Splice

1. Check Splice (`splice ctl status`). If it is not running, ask the person to
   open it.
2. Ask the person to make a new project saved as
   `~/Movies/Splice/friction-logs/<slug>-<date>-<env>.splice`.
3. Confirm `status` names that project and its `duration` is 0. If any other
   project is open, pass `--project <name>` on every command. Never edit a
   project the person did not make for this video.
4. Set the canvas: `splice ctl canvas --aspect 16:9 --fps 30`.
5. Write the transcript (step 3) first, so the board can carry it. Then add
   one beat per row of the scenario, in order, with its planned length:
   - `--story`: the beat's transcript lines, with their numbers, exactly as in
     `transcript.md`;
   - `--capture`: what the screen take shows, and how the face appears.

   ```sh
   splice ctl story add --title "Hook" --duration 12 \
     --story "L1 I'm Dana, an admin at Acme. I want to invite Sam ..." \
     --capture "Narration camera full frame"
   splice ctl story add --title "Dana · Open members" --duration 30 \
     --story "L2 First, the members page. L3 [after take] ..." \
     --capture "Screen: Settings > Members. Face bubble"
   ```

   Put the persona's name first in every beat title. Lines marked
   `[after take]` are filled in step 5; update the beat's `--story` with
   `story set` then.
6. Add a cue at each persona change: `splice ctl cue add --at 96 --label
   "HANDOFF Dana -> Sam"`.
7. `splice ctl story read`: the beats must end at or before 300 s. Fix the plan
   in `scenario.md` first, then the board, so the two stay the same.
8. `splice ctl view story` and ask the person to approve the board.

## 3. Script and transcript

Two files. The script is for the screen take; the transcript is everything
the finished video says.

### `script.md`: the screen take

Write it from `templates/script.md`. The person reads it while driving the
product, so it must work at a glance.

- One block per beat: persona, **ANCHOR**, **DO**, **NOTICE**.
- **ANCHOR** is a short line the person says out loud to open the beat, and it
  appears nowhere else in the script ("Next, the members page."). The mic
  records a scratch track; you find beats by these lines in its captions.
- **DO** is the clicks, one per line, with the exact labels on screen.
- **NOTICE** is a prompt: "Say what you expected here, then what you got."
  The person says it to the scratch track in their own words. These raw
  reactions are the evidence for the findings and the source for the
  transcript's friction lines. They are not used in the video.

Rules the person follows, printed at the top of the script:

1. Record the journey in one take. Do not stop the recording.
2. Pause for a full second between beats.
3. After a mistake, pause, say "again", and repeat the beat from its anchor
   line. The last attempt is the one kept.
4. While a page loads, keep quiet or say what you are waiting for.
5. At a handoff, say the handoff line, then switch windows.

Handoffs in the script:

- A full-width banner between the beats: `HANDOFF  Dana (admin, window 1) ->
  Sam (member, window 2)`.
- One browser window per persona, each visibly different (profile colour or
  theme), so the footage itself shows who is acting.

### `transcript.md`: the narration

Write it from `templates/transcript.md`. It is every word of the finished
video's voice, in order, as numbered lines.

- Number every line `L1`, `L2`, ... across the whole video; never reuse a
  number. One line is one to three sentences about one thing on screen.
- Group the lines under the beat they play over, with the beat's length and a
  word budget: about 2.2 words per second of the beat, less where the screen
  needs a moment to read. Add the words up per beat; over budget means cut
  words, not speed up the voice.
- Write it the way the person talks: short sentences, first person, no
  product marketing. Read it aloud once; anything that trips gets rewritten.
- The hook, every handoff, and the verdict are lines like any other.
- A handoff line names both people: "That is Dana's side done. Now I am Sam,
  a new member, opening the invite."
- Where a line depends on what happens in the screen take (how long a wait
  took, what broke, which option the agent offered), write the expected line
  and mark it `[after take]`. The verdict's three frictions are always
  `[after take]`.
- Leave room for one extra line per beat for a friction nobody predicted.

## 4. Screen take

1. Preflight with the person:
   - personas signed in, each in its own window, at the starting page;
   - notifications off, bookmarks bar hidden, unrelated tabs closed;
   - browser zoom at 110 to 125 percent so text reads at 1080p;
   - the script on a second display, a phone or paper, not on the recorded
     display.
2. Set up the take. Read `splice ctl record sources` first and check that
   screen and microphone access are granted. No camera: the face comes from
   the narration take.

   ```sh
   # one persona: record the browser window
   splice ctl record setup --screen window:Chrome --camera none --microphone default \
     --no-system --layout screen --clicks --cursor
   # two or more personas, or a terminal too: record the display
   splice ctl record setup --screen display:1 --camera none --microphone default \
     --no-system --layout screen --clicks --cursor
   ```

3. Ask before starting. Then `splice ctl record start --at 0`.
4. The person runs the script once, start to finish.
5. `splice ctl record stop --wait`. Keep the reply: it lists the screen and
   microphone clips and the take's folder.
6. Mute the scratch track: `splice ctl volume --clip <mic clip> --value 0`.
   Keep it on the timeline; it lines up with the screen and is cut with it.
7. `splice ctl save --label "screen take"`.

## 5. Narration take

### Fill the transcript from the screen take

1. Transcribe the scratch track: `splice ctl captions --clip <mic clip>
   --wait`, then `splice ctl read`. Find each beat by its anchor line.
2. Read the person's NOTICE reactions and look at frames where they named a
   problem (`splice ctl frame`).
3. Replace every `[after take]` line with what actually happened: real wait
   times, what broke, the three frictions for the verdict. Add a line for any
   friction the transcript did not predict, and drop lines about things that
   did not happen.
4. Check each beat's word budget again, then delete the scratch caption
   clips.
5. Update the board: `story set --beat <id> --story "<lines>"` for each beat
   whose lines changed. Show the person the final transcript and get their
   OK before they read it.

### Record it

1. Set up for camera and voice only:

   ```sh
   splice ctl record setup --screen none --camera default --microphone default \
     --no-system --layout camera --mirror --clean
   ```

   Ask the person to turn on Voice Isolation (`splice ctl record mic-mode`).
   They look at the camera; the transcript sits just under or beside the
   lens.
2. `splice ctl record start --into media`, so the take does not land on the
   timeline yet.
3. Rules for the reading, printed at the top of the transcript:
   1. Say the line's number ("L3"), pause, read the line, pause about two
      seconds.
   2. After a flub, say the number again and reread the whole line. The last
      reading of each number is the one kept.
   3. Read at a relaxed pace. Do not rush to fit a beat; the picture is fitted
      to the voice.
4. `splice ctl record stop --wait`. The take has a camera clip and a
   microphone clip that start together.
5. `splice ctl save --label "narration take"`.

## 6. Cut

### The screen take

1. From the scratch captions (or by scanning `frame`s; every beat starts with
   a click), mark each beat's range in the screen take.
2. Drop the person's own mistakes ("again"), dead air, and the head and tail.
3. Apply the drops from the end of the timeline to the start, so earlier times
   stay valid. Split the screen clip and the scratch mic at the same times and
   delete both pieces with `--ripple`:

   ```sh
   splice ctl split --at 212.4
   splice ctl split --at 219.8
   splice ctl delete --clip 31,32 --ripple
   ```

Waiting is friction. Do not cut out a slow load, a spinner or an error. Shorten
it with `splice ctl speed --clip <piece> --rate 6` on the screen piece and the
scratch piece, and add a label with the real time ("waited 14 s"). For waits of
many minutes, speed the piece to land at about 3 s. Cut only the person's own
mistakes and dead air.

### The narration

1. Add the narration's camera and mic clips to the timeline after everything
   else (`splice ctl add --media <id>`), on their own tracks.
2. Transcribe the mic clip (`captions --wait`, then `read`). Find every spoken
   line number; keep the last reading of each.
3. Split camera and mic together at each kept line's start and end, keeping
   about 0.2 s of room on each side. Delete the spoken numbers, the retakes
   and the pauses. Delete the caption clips.
4. Each line is now a camera piece and a mic piece of the same length. Move
   both to the line's beat with `splice ctl move --clip <id> --to <t>`, the
   same `--to` for both, starting about 0.3 s after the action the line talks
   about. Never move one without the other.

### Fit the picture to the voice

1. A beat runs as long as its lines plus about a second. If the lines run
   longer than the beat's screen footage, slow a sped-up wait or keep more of
   a pause. If they are much shorter, trim the beat so there is no idle
   screen under silence.
2. `read` after each beat: lines must not overlap each other, and each line
   must sit over the screen it describes. Check with `frame` at each line's
   start.

## 7. Finish

Work in this order. Check each with `splice ctl frame` before the next.

1. **Intro pre-roll, 4 to 6 s.** Use the `Friction log intro` symbol; make it
   once from the recipe if `splice ctl symbol list` does not have it. Run
   `symbol read` on the use and fill the labels it reports: one with the
   journey, one with product, environment and date. Make room first by moving
   the cut to start after it.
2. **Face in frame.** The face is the narration's camera pieces, so it shows
   only while a line is spoken.
   - Hook and verdict: the camera pieces fill the frame (they come in full
     frame from the `camera` layout). Hide the screen under them for those
     sections (`look --opacity 0` on that screen piece).
   - Journey: set each camera piece to a round bubble in a corner
     (`look --scale 0.26 --x 0.36 --y 0.3 --mask ellipse`). Where it covers the
     control being used, move it to another corner.
   - Every beat has at least one line, so the face is never missing for a
     whole beat.
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
   value per clip. Each line already starts and ends in a pause.
7. **Redact.** Blur anything private or not the team's to show: emails of real
   people, tokens, other customers' names (`look --redact blur` on that piece).
8. **Sound.** Narration at 1; the scratch track stays at 0. If there is intro
   music, keep it under 0.4 and end it before the hook's first word.
9. **Captions**, if the person wants them: `captions --clip <narration mic
   pieces>` on the finished cut, then fix misheard product names against
   `transcript.md`.
10. **End card, 3 to 4 s:** the three frictions as text, and where the findings
    file is.

Before export:

0. Make the board match the cut. `story remove` the beats from last to first
   (removing an earlier beat pulls later footage left), then `story add` them
   again in order, intro and cards included, with the real lengths and the
   final transcript lines as each beat's `--story`. `read`
   after the first removal: if any clip moved, `undo` and leave the board.
1. `splice ctl status`: `duration` is 300 or less. If it is over, shorten waits
   and silences first, then drop the weakest beat. Do not speed up speech.
2. Export a draft and ask the person to watch it:
   `splice ctl export ~/Movies/Splice/friction-logs/<slug>-<date>-<env>-draft.mp4 --draft --wait`.
3. Apply their notes, then export the final with `--high --wait`.
4. You cannot hear the result. Say so, and ask the person to check the voice
   level and the music.

Do not upload or share the video unless the person asks.

## 8. Findings

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
5. Anything in the scenario, script or transcript that should change for the
   next run.
6. The frictions come from the scratch track's reactions, with the final
   video's timestamp of the line that names each one.

Update the scenario's row in `docs/friction-logs/README.md` with the date and
environment of this run.

## Checks before calling it done

1. The video is 300 s or shorter and opens with the intro.
2. Every transcript line is in the video once, on its beat, with its camera
   and voice together. The face is visible in every beat and full frame in
   the hook and verdict.
3. No `[after take]` marker is left in `transcript.md`.
4. Every handoff has a card, a spoken line and a badge.
5. Every friction in the findings file has an annotation at its timestamp.
6. No waits were removed; shortened waits show the real time.
7. Nothing private is readable in any frame you sampled.
8. `scenario.md`, `script.md`, `transcript.md` and the findings file are in
   `docs/friction-logs/<slug>/` and the README index lists the scenario.
9. The findings file has "How this was run" with the commands used, and the
   README's "Environments" section agrees with it.
