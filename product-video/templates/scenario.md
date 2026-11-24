# <Journey title>

| | |
|---|---|
| Type | <demo, friction log, tutorial or release clip> |
| Slug | `<slug>` |
| Product | <which app> |
| Runs on | local, staging |
| Planned length | <sum> s of <the type's cap> |
| Last recorded | never |

## Goal

<One sentence: what the user gets done, or, for a release clip, what changed.>

## Personas

| Name | Role | Colour | Window | Local sign-in | Staging account |
|---|---|---|---|---|---|
| Dana | Admin at Acme | `#2f6fed` | 1 | `dana@example.test`, admin | vault item `<name>` |
| Sam | New member | `#8e4ec6` | 2 | `sam@example.test`, member | vault item `<name>` |

## Environment

Each line is marked **checked** (run and it worked) or **from docs** (read,
not run). Shared facts are in `../README.md` under "Environments".

### Local

- Start: <the command the person runs>.
- `APP_URL`: <local URL, and how the port is found>.
- Sign-in: <the development sign-in for a persona, with its role>.
- Data to create before recording: <list, with the command or page for each>.

### Staging

- `APP_URL`: <staging URL>
- Sign-in: real sign-in, before recording starts.
- Tag for anything created: `vid-<date>`.
- Hide in the edit: <emails, other customers' names, tokens>.
- Cleanup after recording: <what to delete, and where>.

## Preconditions

1. <What must be true before beat 1: accounts exist, the inbox is empty, ...>

## Beats

| # | Persona | Beat | The user does | Done when | Seconds |
|---|---|---|---|---|---|
| 0 | | Intro | (pre-roll) | | 5 |
| 1 | Dana | Hook | Says who they are, what the product is, the scenario (sample app and the change wanted), and what the video shows | | 30 |
| 2 | Dana | <title> | <one action> | <what is on screen> | 35 |
| 3 | Dana | <title> | <one action> | <what is on screen> | 40 |
| | | Handoff card: Sam | | | 2 |
| 4 | Sam | <title> | <one action> | <what is on screen> | 45 |
| 5 | Sam | <title> | <one action> | <what is on screen> | 40 |
| | | Handoff card: Dana | | | 2 |
| 6 | Dana | <Close, Verdict or Recap, by type> | <closing line; three frictions; the steps> | | 25 |
| 7 | | End card | | | 4 |
| | | **Total** | | | **228** |

## Music and branding

<Mood of the score for the hook, the journey and the ending, or "none".
Branded intro and transitions: yes or no.>

## Driver

<Agent (default) or person drives the screen take.>

## Watch for

<What the dry run found: where it is slow, where it breaks, what data it
needs. A friction log slows down and reacts here; the other types make sure
it passes before recording. Leave empty if nobody has walked it yet.>

## Out of scope

<What this video does not cover.>
