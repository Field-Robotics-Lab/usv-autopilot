#!/usr/bin/env python3
"""Plot ground speed from the newest SITL .BIN log and save the run's parameters.

The Python counterpart of matlab/Read_SITL_Run.m (setup guide, Step 8). Finds
the newest log in the ArduPilot clone next to this repo in the working
directory, <working dir>/ardupilot/Rover/logs, plots GPS ground speed against
time, and writes the parameters recorded in the log as a .parm file next to it,
one NAME,VALUE per line. Needs pymavlink and matplotlib, both in the container.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from pymavlink import mavutil

here = Path(__file__).resolve().parent                  # .../usv-autopilot/usv-sitl/python
folder = here.parents[2] / "ardupilot" / "Rover" / "logs"
logs = sorted(folder.glob("*.BIN"), key=lambda p: p.stat().st_mtime)
if not logs:
    raise SystemExit(f"No .BIN logs in {folder}")
log = logs[-1]                                          # newest log
print(f"Reading {log}")

t, spd, params = [], [], {}
reader = mavutil.mavlink_connection(str(log))
while (m := reader.recv_match(type=["GPS", "PARM"])) is not None:
    if m.get_type() == "GPS":
        t.append(m.TimeUS / 1e6)
        spd.append(m.Spd)
    else:
        params[m.Name] = m.Value                        # last value wins, as in the MATLAB script

parm = log.with_suffix(".parm")
parm.write_text("".join(f"{name},{value:.7g}\n" for name, value in sorted(params.items())))
print(f"Wrote {len(params)} parameters to {parm}")

png = log.with_suffix(".png")
plt.plot([x - t[0] for x in t], spd)
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
plt.title(log.name)
plt.grid(True)
plt.savefig(png, dpi=100)
print(f"Saved the plot to {png}; top speed {max(spd):.2f} m/s")
plt.show()
