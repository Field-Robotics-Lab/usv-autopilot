# usv-autopilot

Tools, environments and documentation for tuning and analyzing ArduPilot Rover on small single-prop, single-rudder unmanned surface vehicles. The first platform is a Pro Boat Blackjack 42 running ArduPilot Rover on a Cube Orange+. The methods are meant to carry over to other vessels.

The audience is collaborating faculty, researchers and engineering students. The bar is that someone else can reproduce the work from the docs and code.

## Layout

The work splits into three efforts, one directory each:

| Directory | Effort | Status |
|---|---|---|
| [usv-analysis/](usv-analysis/) | Analytical: MATLAB transfer-function models of the plant and of the ArduPilot speed and steering loops | started |
| [usv-sitl/](usv-sitl/) | Numerical: a reproducible ArduPilot SITL environment and the tooling to run parameter sets in it | started |
| `usv-field/` | Field tests: trial params, post-processing | deferred |

Code lives in the directory of the effort it serves. Nothing is centralized up front. When a second effort needs something, we decide then whether to share it. [ROADMAP.md](ROADMAP.md) summarizes what is where and how this repo relates to other work.

## Docs conventions

Docs are plain Markdown, rendered by GitHub, with no build step. Each effort has its own `docs/`, using the same four folders:

| Folder | Holds |
|---|---|
| `getting-started/` | setup to a first working run |
| `how-to/` | one task per page |
| `design/` | architecture, derivations, and the reasons behind them |
| `reference/` | parameters, tables |

A walkthrough page has:
- one or two sentences of purpose;
- Prerequisites, as links to the pages that must pass first;
- copy-paste steps, each with a sentence of why;
- pinned versions (tag or commit) where it matters;
- the environment it was tested in.

Where several components meet, use a pieces table: what each piece is, how it is installed and where it goes. Diagrams are Mermaid blocks. Add a page only when there is something to reproduce. Write each paragraph as one line, with no hard wrapping.
