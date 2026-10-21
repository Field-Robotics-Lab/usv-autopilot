# ArduPilot Rover SITL Setup: Stock Motorboat

How to run ArduPilot's stock motorboat in SITL (software-in-the-loop) on Ubuntu, following ArduPilot's own documentation, pinned to release **Rover-4.7.2**.

**Prerequisites**

* A working Ubuntu 22.04 install, native or [WSL2 on Windows 11](https://learn.microsoft.com/en-us/windows/wsl/install).
* MATLAB with the [UAV Toolbox](https://www.mathworks.com/products/uav.html) (Steps 6–7) on Windows.
* Optional: [Mission Planner](https://ardupilot.org/planner/docs/mission-planner-installation.html) on Windows (Step 5b). SITL's own map and console are enough for every step.

**Tested on**

* Windows 11, WSL2 Ubuntu 22.04 with mirrored networking
* ArduPilot Rover-4.7.2 (commit `fb77356789`)
* MATLAB R2026b with the UAV Toolbox
* Mission Planner-1.3.83 (optional)

!\[SITL architecture and default network ports](https://ardupilot.org/dev/\_images/sitl-architecture.svg)

Source: ArduPilot \[1], [Setting up the Build Environment (Linux/Ubuntu)](https://ardupilot.org/dev/docs/building-setup-linux.html)

\---

## Quick setup

To do Steps 1–4 in one go on a fresh Ubuntu 22.04, download [Linux\_script.sh](../../scripts/Linux_script.sh) and run:

```bash
bash Linux\\\_script.sh
```

## Step 1. Get the ArduPilot code

Source: ArduPilot \[1], [Setting up the Build Environment (Linux/Ubuntu)](https://ardupilot.org/dev/docs/building-setup-linux.html)

```bash
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
# Download a full copy of ArduPilot's source code from GitHub into a new folder, \\\~/ardupilot.

cd ardupilot
# Move into the new ArduPilot folder. Every later command runs from here.

git checkout Rover-4.7.2
# Switch the code from ArduPilot's latest development version to release Rover-4.7.2.

git submodule update --init --recursive
# The clone downloaded the separate projects (submodules) at the versions the development
# code uses. This updates them to the versions release 4.7.2 was built with.
```

**Check:** `git status` prints:

```
HEAD detached at Rover-4.7.2
nothing to commit, working tree clean
```

\---

## Step 2. Install the build tools

Source: ArduPilot \[1], [Setting up the Build Environment (Linux/Ubuntu)](https://ardupilot.org/dev/docs/building-setup-linux.html)

```bash
Tools/environment\\\_install/install-prereqs-ubuntu.sh -y
# Run ArduPilot's install script. The script is part of the code downloaded in Step 1
# (folder \\\~/ardupilot/Tools/environment\\\_install). It reads its own list of requirements
# and downloads them from the internet:
#   - compilers that turn the C++ code into programs (one for this computer, used by SITL;
#     one for ARM autopilot boards such as the Cube)
#   - Python tools, including MAVProxy
#   - the folders that hold these tools, added to the PATH so Linux can find them by name

. \\\~/.profile
# Reload the PATH settings the script just added, so this terminal can find the new tools.
```

**Check:** in a new terminal, run `which sim\\\_vehicle.py`. It prints a path ending in `ardupilot/Tools/autotest/sim\\\_vehicle.py`, which means the SITL launcher is installed and on the PATH.

\---

## Step 3. Build SITL

Source: ArduPilot \[2], [Building ArduPilot (BUILD.md, Rover-4.7.2)](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/BUILD.md).

```bash
./waf configure --board sitl
# waf is ArduPilot's build tool (downloaded in Step 1).

./waf rover
# Compile the Rover firmware, which ArduPilot uses for both ground rovers and surface boats.
# The result is one program, build/sitl/bin/ardurover: the same autopilot that runs on a
# flight controller, built for this computer.
```

**Check:** the build ends with `'rover' finished successfully`.

\---

## Step 4. Launch the motorboat

Source: ArduPilot \[3], [SITL Simulator (Software in the Loop)](https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html); \[4], [SITL on Windows using WSL](https://ardupilot.org/dev/docs/sitl-on-windows-wsl.html).

ArduPilot's example launches a Copter from the `ArduCopter` folder. For a boat, launch from the `Rover` folder and choose the motorboat:

```bash
cd \\\~/ardupilot/Rover
# Go into the Rover folder. sim\\\_vehicle.py picks the vehicle firmware from the folder.

../Tools/autotest/sim\\\_vehicle.py -f motorboat --map --console
# Start the ardurover program from Step 3, connect it to a physics model of the vehicle,
# and start MAVProxy to pass messages to ground stations.
```

> \\\[!NOTE]
> \\\*\\\*WSL2 with mirrored networking only:\\\*\\\* add `--no-wsl2-network` to the launch command (from ArduPilot \\\[4], \\\[SITL on Windows using WSL](https://ardupilot.org/dev/docs/sitl-on-windows-wsl.html)). Without it, SITL sends its messages to the Windows host address instead of `127.0.0.1`, and ground stations on Windows cannot connect. Native Linux does not need it.

**Check:** the console prints `EKF3 IMU0 is using GPS` (the simulated GPS and navigation filter are ready), the prompt shows `MANUAL>` (the current mode), and the boat appears on the map.

\---

## Step 5. Start at the test lake, connect a ground station, and drive

Source: ArduPilot \[4], [SITL on Windows using WSL](https://ardupilot.org/dev/docs/sitl-on-windows-wsl.html); \[5], [Using SITL](https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html)

### 5a. Start the boat at the test lake

By default SITL starts at ArduPilot's test site in Canberra, Australia. ArduPilot's documented way to change it is to save a named location and launch with `-L`. Stop SITL with **Ctrl+C** first.

```bash
mkdir -p \\\~/.config/ardupilot
# Create ArduPilot's folder for personal settings (no error if it already exists).

echo "LAKE=36.5986135,-121.8689162,0,0" >> \\\~/.config/ardupilot/locations.txt
# Save the test lake as a location named LAKE, in the format LAT,LON,ALT,HEADING:

cd \\\~/ardupilot/Rover
# Go into the Rover folder.

../Tools/autotest/sim\\\_vehicle.py -f motorboat --map --console -L LAKE
# Same launch as Step 4, plus -L LAKE to start at the saved location.
```

**Check:** the console prints `Set HOME to 36.59861 -121.86892` and the map shows the boat at the lake.

### 5b. Connect a ground station (Optional)

To connect Mission Planner, choose **UDP**, click **Connect**, and enter **14550**. A ground station on another computer uses that computer's IP address instead.

### 5c. Drive the boat

Type at the `MANUAL>` prompt:

```
mode guided
# Guided mode: the boat drives to whatever point it is sent to.

arm throttle
# Arm the motor. The boat will not move until it is armed.
```

Then right-click the map and choose **Fly To** (in Mission Planner: **Fly To Here**, altitude 0, since altitude does not apply to a boat). The boat drives to that point.

```
disarm
# Disarm the motor when the boat arrives.
```

Leave SITL running for Step 6.

**Check:** the boat moves on the map toward the clicked point.

\---

## Step 6. Connect MATLAB to SITL

MATLAB talks to SITL both ways through MAVProxy: it reads telemetry and sends commands such as parameter changes, mode changes, and arming while the boat runs. After a run, MATLAB reads the `.BIN` log file that SITL saves in `\\\~/ardupilot/Rover/logs`; a `.parm` file can also set parameters when SITL starts.

Source: ArduPilot \[4], [SITL on Windows using WSL](https://ardupilot.org/dev/docs/sitl-on-windows-wsl.html); MathWorks \[6], [mavlinkio](https://www.mathworks.com/help/uav/ref/mavlinkio.html)

Needs MATLAB with the UAV Toolbox. SITL sends its messages only to port 14550 by default, which a ground station uses. MATLAB needs its own port, 14551, so a second output is added.

### 6a. Add an output for MATLAB

Option 1, while SITL is running. Type at the `MANUAL>` prompt:

```
output add 127.0.0.1:14551
# Tell MAVProxy to also send every message to port 14551 on this computer.

output
# List the outputs. Both 127.0.0.1:14550 and 127.0.0.1:14551 should appear.
```

Option 2, at launch. Add `--out` to the launch command from Step 5a:

```bash
cd \\\~/ardupilot/Rover
# Go into the Rover folder.

../Tools/autotest/sim\\\_vehicle.py -f motorboat --map --console -L LAKE --out=udp:127.0.0.1:14551
# Same launch as Step 5a, plus a second output to UDP port 14551 for MATLAB.
# On WSL2 with mirrored networking, also add --no-wsl2-network.
```

**Check:** `output` lists both `127.0.0.1:14550` and `127.0.0.1:14551`.

### 6b. Receive SITL messages in MATLAB

Download [Check\_SITL\_Link.m](../../matlab/Check_SITL_Link.m). With SITL running, run in MATLAB:

```matlab
Check\\\_SITL\\\_Link
```

The script listens on UDP port 14551 for 3 seconds, prints the most recent HEARTBEAT message from the autopilot, and closes the connection.

If Windows Firewall asks about MATLAB, click **Allow**.

**Check:** the script prints a struct with `MsgID: 0` (HEARTBEAT), `SystemID: 1`, `ComponentID: 1`, `Payload`, and `Seq`. MATLAB is now receiving ArduPilot's messages from SITL.

\---

## Step 7. Read a SITL log in MATLAB

Source: MathWorks \[7], [ardupilotreader](https://www.mathworks.com/help/uav/ref/ardupilotreader.html)

SITL saves a `.BIN` log in `\\\~/ardupilot/Rover/logs` each time the boat is armed, and closes it when the boat is disarmed. MATLAB reads the file directly from Linux.

### 7a. Make a log

With SITL running type at the `MANUAL>` prompt:

```
param set WP\\\_SPEED 2
# Speed in Guided and Auto modes: 2 m/s.

mode guided
arm throttle
# Arming starts a new log.
```

Right-click the map and choose **Fly To**, about 50 m from the boat (about 20 s at 2 m/s). When the boat arrives:

```
disarm
# After the boat arrives. Disarming closes the log.
```

In a second Ubuntu terminal (or after stopping SITL with **Ctrl+C**):

```bash
ls -lt \\\~/ardupilot/Rover/logs
# List the logs, newest first.
```

### 7b. Read the log in MATLAB

Download [Read\_SITL\_Run.m](../../matlab/Read_SITL_Run.m). In its settings, change `<user>` to your Linux user name. After each SITL run, run in MATLAB:

```matlab
Read\\\_SITL\\\_Run
```

The script:

1. Opens the newest `.BIN` log in `\\\~/ardupilot/Rover/logs`.
2. Lists the message types recorded in the log.
3. Plots ground speed versus time.
4. Reads every parameter recorded in the log and saves them as a `.parm` file with the same name as the log (for example, `00000003.parm`), one `NAME,VALUE` per line.
5. Opens the `.parm` file in a new Editor tab.

**Check:** the plot shows the speed rising to about 2 m/s, holding, and returning to zero, and the `.parm` file contains `WP\\\_SPEED,2`.

\---

## References

1. ArduPilot, [Setting up the Build Environment (Linux/Ubuntu)](https://ardupilot.org/dev/docs/building-setup-linux.html)
2. ArduPilot, [Building ArduPilot (BUILD.md, Rover-4.7.2)](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/BUILD.md)
3. ArduPilot, [SITL Simulator (Software in the Loop)](https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html)
4. ArduPilot, [SITL on Windows using WSL](https://ardupilot.org/dev/docs/sitl-on-windows-wsl.html)
5. ArduPilot, [Using SITL](https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html)
6. MathWorks, [mavlinkio: Connect with MAVLink clients to exchange messages (UAV Toolbox)](https://www.mathworks.com/help/uav/ref/mavlinkio.html)
7. MathWorks, [ardupilotreader: Read ArduPilot log file (UAV Toolbox)](https://www.mathworks.com/help/uav/ref/ardupilotreader.html)

