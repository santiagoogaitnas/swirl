# farm2

**Headless rebuild of the [Claude Code Agent Farm](https://github.com/Dicklesworthstone/claude_code_agent_farm) ("bigclaude").**
Parallel Claude Code agents grinding a codebase until an external oracle says
it's clean — without tmux screen-scraping, and without a babysitter.

The og farm drove Claude Code through its human TUI: it typed keystrokes into
tmux panes and pattern-matched screen text to guess state ("is the welcome
message visible yet?"). Every Claude Code UI update broke it. farm2 keeps
everything that made the farm valuable and replaces the guessing with a
contract: agents run headless (`claude -p --output-format stream-json`) and
report structured events.

## The three principles

1. **The ratchet.** An external oracle (linter / type-checker / any command
   whose stdout lines are problems) decides whether work continues. An agent's
   own "done" never terminates the loop. Every cycle is a fresh session — cold
   context, no memory of previous excuses. Claude satisfices; the farm doesn't
   let it.
2. **Events → files → screen. Never screen → farm.** The runner writes
   structured state to `.farm/`; the wall renders it. tmux is a TV, not a
   steering wheel. Resize it, kill it, reopen it — nothing breaks.
3. **Casual.** One command, zero authored config. Stack auto-detected, agent
   count derived from problem count, report at the end.

## Quickstart

```bash
./farm demo                 # self-contained: copies examples/brokenpkg into
                            # runs/, launches 2 agents, builds the wall
tmux attach -t farm-demo-…  # watch the wall (exact name is printed)

./farm fix ~/code/myproject # the real thing: auto-detect oracle, grind to zero
```

What a launch looks like — every decision is printed:

```
→ oracle: `uvx ruff check -q --output-format concise .` → 29 problems
→ fleet: 2 agents (auto-sized: 1 agent per ~12 problems, min 2, cap 8)
→ plan: each agent loops fresh Claude sessions over its own slice of files, max 10 cycles each
→ stops when: oracle reports 0 problems · or cycles exhausted · or `farm stop`
→ runner pid 57316 · 2 agents · max 10 cycles/agent
wall ready → tmux attach -t farm-myproject
→ steer: farm say <n> "msg" (next cycle) · farm poke <n> "msg" (interrupt now) · farm status --live
→ logs: …/.farm/  ·  report lands at …/.farm/report.md
```

Fleet sizing: `agents = min(8, max(2, problems // 12))`, override with
`--agents N`. Each agent's cycle prompt = its file slice + the ratchet rules
(root causes only, no suppressions, verify each fix against the oracle, no
questions, no summaries) + any queued operator message.

## Commands

| Command | What it does |
|---|---|
| `farm fix [path]` | Ratchet the oracle to zero problems. Flags: `--agents N`, `--max-cycles M`, `--oracle 'cmd'`, `--fg`, `--no-wall` |
| `farm run "task" [path]` | Free-form standing task with oracle as backstop |
| `farm demo` | Run the built-in demo on a disposable copy of `examples/brokenpkg` |
| `farm status --target P [--live]` | Fleet table (live = refreshing) |
| `farm watch --target P` | (Re)build the tmux wall for a running farm |
| `farm say <n\|all> "msg" --target P` | Message an agent; lands at its next cycle start |
| `farm poke <n\|all> "msg" --target P` | Interrupt the agent's current cycle; message lands immediately in a fresh cycle |
| `farm stop --target P` | Stop the runner and close the wall |

`--target` defaults to `.`, so from inside the target repo it's just `farm status --live`.

## How it works

```
farm fix .
  └─ detects oracle (ruff / tsc / --oracle 'cmd'), counts problems
  └─ spawns detached RUNNER (survives your terminal)
       └─ one thread per agent, each looping:
            oracle → slice of problems → fresh `claude -p` session
            (stream-json events → .farm/agents/N/cycle-M.jsonl
                                → .farm/agents/N/feed.log   [rendered]
                                → .farm/state.json          [fleet state])
            → process exits → oracle again → repeat
       └─ loop ends only when: oracle returns zero, max-cycles hit, or farm stop
  └─ builds the WALL: tmux grid = live fleet status + one pane tailing each feed
  └─ final report → .farm/report.md
```

State contract (everything the wall or any other UI needs):

```
<target>/.farm/
  state.json        fleet state (atomic writes)
  agents/N/feed.log human-rendered activity stream (tail -f me)
  agents/N/cycle-M.jsonl  raw structured events per cycle
  inbox/N.txt       operator message, consumed at next cycle start
  poke/N            flag: interrupt current cycle now
  oracle.log        problem counts over time
  report.md         end-of-run summary
```

## Requirements

- `claude` CLI on PATH (or `FARM_CLAUDE_BIN=/path/to/claude`) with subscription
  or API auth — agents run with `--dangerously-skip-permissions`
- `tmux` (only for the wall; runner works without it)
- Python 3.9+ (stdlib only, no installs)
- For the Python oracle: `ruff` on PATH, else falls back to `uvx ruff`

## Status: walking skeleton

Built to prove the architecture end-to-end (runner + ratchet + wall + steering).
Known simplifications, roughly in the order they'd matter:

- Problems are partitioned by file, so agents don't collide within a cycle —
  except at the endgame, when a starved agent steals the tail file. Worktree
  isolation would remove even that.
- Oracle auto-detection covers Python (ruff) and TypeScript (tsc); everything
  else needs `--oracle`
- No notification on completion yet (report.md + status only)
- `farm run` free-form mode is minimal
- One farm per target directory at a time

## Lineage

- Original: [Dicklesworthstone/claude_code_agent_farm](https://github.com/Dicklesworthstone/claude_code_agent_farm)
- Local og copy: `~/0DEVELOPMENT/bigclaude copy` (kept pristine as reference)
- This rebuild keeps the og farm's soul — the forced-cycle ratchet that stops
  Claude from satisficing — and discards its transport (TUI scraping).
