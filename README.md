# swirl

Parallel Claude Code agents that never stop. Pick a folder, a number of
agents, and an instruction. Each agent works in a fresh Claude session,
finishes a pass, resets, and goes again — until you stop it.

## Use

```bash
./swirl ui
```

Opens a browser page with three boxes: **folder · how many agents · what
they should do**. Hit **LAUNCH**. One live card appears per agent; type into
a card to steer that agent (**Say** = next pass, **Poke** = interrupt now).
**Stop** ends everything. Closing the page changes nothing — agents keep
going until you stop them.

## Terminal

```bash
./swirl run "instruction" /path/to/project --agents 20   # launch
./swirl watch --target /path/to/project                  # tmux wall (one pane per agent)
./swirl status --live --target /path/to/project          # fleet table
./swirl say 3 "message" --target /path/to/project        # lands at agent 3's next pass
./swirl poke 3 "message" --target /path/to/project       # interrupts agent 3 now
./swirl stop --target /path/to/project                   # the off switch
./swirl fix /path/to/project                             # bounded variant: fix all lint
                                                         # problems to zero, then stop
```

## How it works

Each agent loops: fresh headless Claude Code session → does a pass → session
ends → a new one starts in its place, cold. Agents divide the work instead
of duplicating it: before touching anything, an agent claims its piece of the
task — an atomic symlink in `<target>/.swirl/claims/` — and skips pieces
other agents hold. When its pass ends the claims are released and the agent
logs what it finished to `<target>/.swirl/worklog`, so the next cold session
builds on it instead of redoing it. Everything each agent does is written to
`<target>/.swirl/` — live feeds, fleet state, claims, worklog, a report. The
browser page and the tmux wall are read-only views of those files.

## Requirements

- `claude` CLI, logged in (agents run with `--dangerously-skip-permissions`
  inside the target folder — point it only at projects you trust it with)
- Python 3.9+, no packages
- `tmux` only if you want the terminal wall

MIT license.
