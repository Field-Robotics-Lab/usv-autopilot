# Roadmap

What is where, what comes next, and how this repo relates to other work.

## In this repo

| Directory | What it holds | Next |
|---|---|---|
| `usv-analysis/` | MATLAB TF models of the plant and the ArduPilot speed and steering loops | linear speed-loop model from the ArduPilot source, then steering |
| `usv-sitl/` | reproducible SITL environment (Linux/WSL2, MATLAB, Mission Planner) and the tooling to run parameter sets | settle the architecture in `docs/design/`, then the first verified setup page |
| `usv-field/` | field trials: params, post-processing | deferred; contents decided when field work starts |

## Outside this repo

- Thesis: parameter sensitivity analysis of ArduPilot Rover on the Blackjack 42. It lives in the student's own repo and uses this one. Findings that generalize, such as the parameter-to-control-element map and the tuning order, come back here.
- [me2801](https://github.com/bsb808/me2801): the course uses the same boat. Related material there: the log pipeline (`utils/ardu_utils/`, `book/w03_lab_usv_sysid/code/`, `book/w07_lab_usv_pid/code/`), the boat params (`utils/ardu_params/`) and the provisioning guide (`site/weeks/w03_lab_usv_sysid/provisioning.qmd`). Some docs may be shared or combined. Whether anything moves is decided when a directory here first needs it.
- [oceans2026](https://github.com/Field-Robotics-Lab/oceans2026): Python model identification of the Blackjack 42.
- [ird-autopilot-maritime](https://github.com/HonuRobotics/ird-autopilot-maritime): internal R&D proposal and report.
- [ardu_utils](https://github.com/bsb808/ardu_utils): an older copy of the log tools, which has diverged from the me2801 copy.

## Open items

1. Log reading (`bin2mat`, `load_and_prep`) is needed first by SITL. Recommend starting it in `usv-sitl/matlab/`, and moving it only if field work needs it too.
