#!/usr/bin/env python3
"""Drive the SITL motorboat on one straight guided run, which records one log.

The scripted form of setup guide Step 7: set WP_SPEED, switch to Guided, arm,
send the boat DIST_M metres north, wait until it stops there, and disarm.
Arming opens a new .BIN log and disarming closes it. Needs pymavlink
(installed by ArduPilot's install script, guide Step 3) and SITL running with
the UDP 14551 output (guide Step 5).
"""
import math
import sys
import time

from pymavlink import mavutil

PORT = 14551
WP_SPEED = 2.0   # m/s, speed in Guided and Auto modes
DIST_M = 50.0    # m, distance of the target point, due north of the start
TIMEOUT_S = 120

link = mavutil.mavlink_connection(f"udpin:127.0.0.1:{PORT}")
if link.wait_heartbeat(timeout=10) is None:
    sys.exit(f"No HEARTBEAT on UDP {PORT}. Is SITL running with --out=udp:127.0.0.1:{PORT}?")
link.target_system, link.target_component = 1, 1

pos = link.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout=10)
if pos is None:
    sys.exit("No position from the autopilot yet. Wait for 'EKF3 IMU0 is using GPS'.")
lat0, lon0 = pos.lat / 1e7, pos.lon / 1e7
lat1 = lat0 + DIST_M / 111_320.0  # metres north to degrees latitude
print(f"Start {lat0:.6f} {lon0:.6f}; target {DIST_M:.0f} m north at {WP_SPEED} m/s")

link.param_set_send("WP_SPEED", WP_SPEED)
link.set_mode("GUIDED")
link.arducopter_arm()          # MAV_CMD_COMPONENT_ARM_DISARM; works for every vehicle type
link.motors_armed_wait()
print("Armed: log started")

# Go to the target: a position-only SET_POSITION_TARGET_GLOBAL_INT, the
# message a ground station's "Fly To" sends.
link.mav.set_position_target_global_int_send(
    0, 1, 1, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
    0b110111111000,  # use position only
    int(lat1 * 1e7), int(lon0 * 1e7), 0, 0, 0, 0, 0, 0, 0, 0, 0)

t0 = time.time()
top = 0.0
while time.time() - t0 < TIMEOUT_S:
    p = link.recv_match(type="GLOBAL_POSITION_INT", blocking=True, timeout=2)
    if p is None:
        continue
    left = math.hypot((p.lat / 1e7 - lat1) * 111_320.0,
                      (p.lon / 1e7 - lon0) * 111_320.0 * math.cos(math.radians(lat0)))
    speed = math.hypot(p.vx, p.vy) / 100.0
    top = max(top, speed)
    if left < 3.0 and speed < 0.3:
        break
else:
    print(f"Did not arrive within {TIMEOUT_S} s; disarming anyway.")

print(f"Arrived after {time.time() - t0:.0f} s, top speed {top:.2f} m/s, {left:.1f} m from the target")
link.arducopter_disarm()
link.motors_disarmed_wait()
print("Disarmed: log closed")
