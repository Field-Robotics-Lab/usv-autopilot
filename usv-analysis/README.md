# usv-analysis

MATLAB transfer-function models of a small USV and of the ArduPilot speed and steering loops that control it. The models are linear approximations, derived from the ArduPilot source. They predict how each autopilot parameter shapes the closed-loop speed and heading response before any simulation or water time.

This is the effort closest to the NPS ME2801 course, which uses the same boat.

```
models/             TF models of the plant and the ArduPilot speed + steering loops (each cites the ArduPilot source it follows)
examples/           live scripts showing each model's response to parameter changes
docs/walkthroughs/  task pages, e.g. evaluate a parameter change on the linear model
docs/reference/     how the ArduPilot loops reduce to the linear models (derivation, assumptions); parameter → control element map
```

No quick start yet. One is added with the first model that runs end to end.
