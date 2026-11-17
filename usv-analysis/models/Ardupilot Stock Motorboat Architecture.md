# Stockboat Physics

ArduPilot's stock motorboat used for SITL and HIl simulations is defined in two files:
[SIM_Sailboat.cpp](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.cpp)
and [SIM_MotorBoat.h](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_MotorBoat.h).
The boat mass is not set in any of those files, it is a fixed constant in [SIM_Sailboat.h](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.h).
The motorboat itself, SIM_MotorBoat.h has no physics of its own. It reuses the sailboat, SIM_Sailboat.cpp physics while 
turning the motor on and removing the sail. 

[SIM_Sailboat.cpp](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.cpp#L43C1-L52) and [SIM_Sailboat.h](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.h) contain various important parameters: 

| Parameter | Value | Comment |
|---|---|---|
| mass | 2 kg | Stock value, not based on a real boat. Replace with the Blackjack's weighed mass. |
| steering_angle_max | 35° | Stock value, not based on a real boat. Replace with the Blackjack's maximum rudder angle, measured on the bench. |
| turning_circle | 1.8 m | Stock value, not based on a real boat. Replaced with the Blackjack's full-rudder turning circle, measured on the water. |
| sail_area | 1.0 | Set to 0 by `SIM_MotorBoat.h`. Not used in the Blackjack model. |
| motor_connected | false | Set to true by `SIM_MotorBoat.h`. Kept in the Blackjack model. |

``` cpp
const float mass = 2.0f;
Sailboat::Sailboat(const char *frame_str) :
    Aircraft(frame_str),
    sail_area(1.0),
    steering_angle_max(35),
    turning_circle(1.8)
{
    motor_connected = (strcmp(frame_str, "sailboat-motor") == 0);
    skid_steering = strstr(frame_str, "skid") != nullptr;
    lock_step_scheduled = true;
}
```
[SIM_MotorBoat.h Lines 26-33]( https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_MotorBoat.h#L26C1-L33) connects the motor and set the Sail area to zero. 
``` cpp
  a MotorBoat simulator. We re-use SailBoat but force motor_connected and sail_area to 0
 */
class MotorBoat : public Sailboat {
public:
    MotorBoat(const char *frame_str) : Sailboat(frame_str) {
        motor_connected = true;
        sail_area = 0.0;
    }
