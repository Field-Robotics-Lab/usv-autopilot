# Stock Motorboat Source Code

ArduPilot's stock motorboat (`sim_vehicle.py -f motorboat`) is defined in three files, pinned to release Rover-4.7.2.

| File | Description |
|---|---|
| [SIM_Sailboat.cpp](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.cpp) | Runs the boat physics. Reads the rudder and throttle, computes thrust, hull drag, and yaw rate, and integrates speed, heading, and position. No transfer functions, it calculates parameters by solving motion equations |
| [SIM_Sailboat.h](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.h) | Lists the boat's settings and variables: mass, rudder limit, turning circle, and the stored velocity that the physics updates. |
| [SIM_MotorBoat.h](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_MotorBoat.h) | Creates the motorboat by reusing the sailboat model, turning the motor on and removing the sail area. Contains no physics of its own. |
