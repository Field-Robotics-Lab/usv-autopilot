#!/usr/bin/env python3
"""Check that MAVLink messages from a running SITL arrive on UDP 14551.

The Python counterpart of matlab/Check_SITL_Link.m. Needs pymavlink, which
ArduPilot's install script installs (setup guide, Step 3), and SITL running
with the 14551 output (setup guide, Step 5).
"""
import sys
import time

from pymavlink import mavutil

PORT = 14551
LISTEN_S = 3.0

# Listen on UDP port 14551, as a ground station would
link = mavutil.mavlink_connection(f"udpin:127.0.0.1:{PORT}")

# Keep the most recent HEARTBEAT from the autopilot (sent once per second).
# Heartbeats from other components, such as a ground station, are skipped.
latest = None
deadline = time.time() + LISTEN_S
while time.time() < deadline:
    msg = link.recv_match(type="HEARTBEAT", blocking=True, timeout=0.5)
    if msg is not None and msg.type != mavutil.mavlink.MAV_TYPE_GCS:
        latest = msg

link.close()

if latest is None:
    print(f"No HEARTBEAT received. Check that SITL is running and 'output' lists 127.0.0.1:{PORT}.")
    sys.exit(1)

vehicle = mavutil.mavlink.enums["MAV_TYPE"][latest.type].name.removeprefix("MAV_TYPE_")
mode = mavutil.mode_string_v10(latest)
armed = bool(latest.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
print(f"HEARTBEAT from SystemID {latest.get_srcSystem()}, ComponentID {latest.get_srcComponent()}:"
      f" {vehicle}, mode {mode}, {'armed' if armed else 'disarmed'}")
print("Python is receiving messages from SITL.")
