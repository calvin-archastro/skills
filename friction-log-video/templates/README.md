# Friction logs

Recorded friction-log videos: one person walks a product journey, then
narrates it on camera from a written transcript, saying where it cost them
time. Each journey keeps its scenario and script here
so it can be recorded again on another environment or after a fix.

The `friction-log-video` skill writes and uses these files.

## Layout

```text
docs/friction-logs/<slug>/
  scenario.md              # goal, personas, local and staging setup, beats
  script.md                # what the person does in the screen take
  transcript.md            # every narration line, numbered
  runs/<date>-<env>.md     # findings from one recording, with timestamps
```

- Videos and Splice projects are not committed. They are in
  `~/Movies/Splice/friction-logs/` on the machine that recorded them; each
  findings file gives the path or link.
- No passwords, tokens or magic links in these files. Name the env var or
  vault item.

## Environments

| Product | Local | Staging |
|---|---|---|
| <app> | <URL, and how the port is found> | <URL> |

- Start the local stack: <command>.
- Local sign-in for a persona: <route or steps, with how the role is set>.
- Staging sign-in: <where test accounts are kept>.

## Scenarios

| Slug | Journey | Product | Personas | Last recorded |
|---|---|---|---|---|
| | | | | |
