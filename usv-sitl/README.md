# usv-sitl

A reproducible ArduPilot software-in-the-loop (SITL) environment for small USVs, plus the scripts and MATLAB that run parameter sets in it and post-process the logs. ArduPilot simulates both the control and the plant for now.

The environment spans ArduPilot SITL on Linux or Windows WSL2, MATLAB on Windows and/or Linux, and Mission Planner on Windows. That architecture is under design. Its working record goes in `docs/design/architecture.md` (which process runs where, how they connect, a Mermaid diagram and a pieces table). The setup pages under `docs/getting-started/` are added as each configuration is verified through a smoke test.

```
docs/design/          architecture: living design record
docs/getting-started/ setup per platform (Linux, WSL2, Windows) through a smoke test
docs/how-to/          task pages, e.g. run a param set from MATLAB, retrieve the log
vehicles/             SITL params and frame config for the boat
scripts/              launch SITL, run a param set, collect the log
matlab/               MATLAB that drives SITL and post-processes its logs
```

No quick start yet. One is added with the first verified setup.
