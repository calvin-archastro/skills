# Environments: how to run the product for a recording

Read from step 1 of the product-video skill. The scenario lists both
environments so the same script runs on either; the script uses `$APP_URL`
and the run picks the value.

## Research how to run it

Do this before writing beats, for every environment the scenario lists. A
scenario nobody can start is not reusable.

1. Read what is already known: the "Environments" section of
   `docs/videos/README.md` and the "How this was run" section of the latest
   run file for this scenario or a neighbouring one.
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
   - facts that hold for every video go in the "Environments" section of
     `docs/videos/README.md`;
   - facts for this journey (data to create, starting pages, cleanup) go in
     the scenario's Environment section.

Do not guess a URL, a port or a sign-in route. If something could not be
found, write "unknown" with what you tried, and resolve it with the person
before recording.

## Local

1. The person starts the stack. Do not start it for them.
2. Resolve the URL and ports the way the project documents, and check the
   app answers before recording.
3. Sign each persona in, one browser window per persona. Use the project's
   development sign-in if it has one, and set each persona's role explicitly.
4. Local shows the code in this checkout. Write the commit (`git rev-parse
   --short HEAD`) in the run file.

## Staging

1. Each persona signs in for real, with a test account kept for this purpose.
   The scenario names where the credentials are kept, not the credentials.
2. Sign in before recording starts, so no password or magic link is on screen.
3. Data made on staging stays there. Name everything the run creates with a
   tag (`vid-<date>`), and list the cleanup in the scenario.
4. Do not change staging infrastructure for a recording.
5. Staging can show other people's data. Note what must be hidden; step 7
   redacts it.
6. Write the date and time (UTC) of the recording in the run file, since
   staging moves.
