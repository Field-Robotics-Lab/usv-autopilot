# usv-autopilot

Tools, environments and documentation for tuning and analyzing ArduPilot Rover on small single-prop, single-rudder unmanned surface vehicles. The first platform is the me2801 USV, but the methods are meant to carry over to other vessels.

The audience is collaborators, not beginners.  The requirement is that a technical user should be able to run and modify the experimetns **without** communicating directly with to the author. 

## Layout

The work splits into three efforts, one directory each:

| Directory | Effort | Status | Next |
|---|---|---|---|
| [usv-analysis/](usv-analysis/) | Analytical: MATLAB transfer-function models of the plant and of the ArduPilot speed and steering loops | started | linear speed-loop model from the ArduPilot source, then steering |
| [usv-sitl/](usv-sitl/) | Numerical: a reproducible ArduPilot SITL environment (Linux/WSL2, MATLAB, Mission Planner) and the tooling to run parameter sets in it | started | settle the architecture in `docs/reference/`, then the first verified setup page |
| `usv-field/` | Field tests: trial params, post-processing | deferred | contents decided when field work starts |

## Docs conventions

Docs are plain Markdown, rendered by GitHub, with no build step. Each effort has its own `docs/`, using the same three folders:

| Folder | Holds |
|---|---|
| `getting-started/` | setup to a first working run |
| `walkthroughs/` | one task per page, step by step |
| `reference/` | architecture, derivations and the reasons behind them; parameters, tables |

A walkthrough has:
- one or two sentences of purpose;
- Prerequisites, as links to the pages that must pass first;
- copy-paste steps, each with a sentence of why;
- pinned versions (tag or commit) where it matters;
- the environment it was tested in.

Where several components meet, use a pieces table: what each piece is, how it is installed and where it goes. Diagrams are Mermaid blocks. Write each paragraph as one line, with no hard wrapping.

## Outside this repo

- Thesis specific code: parameter sensitivity analysis lives in separate own repo(s) and uses this one. Findings that generalize, such as the parameter-to-control-element map and the tuning order, come back here.  This repo is a the reusable part of the project and a contribution to the community.  
- [me2801](https://github.com/bsb808/me2801): the course uses the same boat. Related material there: the log pipeline (`utils/ardu_utils/`, `book/w03_lab_usv_sysid/code/`, `book/w07_lab_usv_pid/code/`), the boat params (`utils/ardu_params/`) and the provisioning guide (`site/weeks/w03_lab_usv_sysid/provisioning.qmd`). Some docs may be shared or combined. 