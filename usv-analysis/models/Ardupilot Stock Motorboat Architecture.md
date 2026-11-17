# Stockboat Physics

ArduPilot's stock motorboat used for SITL and HIL simulations is defined in two files:
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
| turning_circle | 1.8 m | Stock value, not based on a real boat. Replace with the Blackjack's full-rudder turning circle, measured on the water. |
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
[SIM_MotorBoat.h Lines 26-33](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_MotorBoat.h#L26-L33) connects the motor and sets the Sail area to zero. 
``` cpp
  a MotorBoat simulator. We re-use SailBoat but force motor_connected and sail_area to 0
 */
class MotorBoat : public Sailboat {
public:
    MotorBoat(const char *frame_str) : Sailboat(frame_str) {
        motor_connected = true;
        sail_area = 0.0;
    }
```
## Speed Architecture
Speed is calculated by solving Newton's Second Law of Motion:

$$ m\\dot u = T-D $$

where m is the mass of the boat, T is the motor thrust and D is the hull drag. 

The steps below show where each term comes from:

### Step 1. Current Speed

[Lines 252-256](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.cpp#L252-L256)

First the velocity saved at the end of the previous step is converted into the boat's frame (Forward, Sideways, Down). Then only the forward speed is saved.
```cpp
// speed in m/s in body frame
    Vector3f velocity_body = dcm.transposed() * velocity_ef_water;

    // speed along x axis, +ve is forward
    float speed = velocity_body.x;
```
### Step 2. Hull Drag

$$ D= c_D\ u\|u| $$

where  $c_D$ is the stock value drag coefficient, and u is the forward speed previously calculated.

[Lines 267-271](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.cpp#L267C5-L271C6)

Forward speed is now used to calculate drag for 

```cpp
// hull drag
    float hull_drag = sq(speed) * 0.5f;

    if (!is_positive(speed)) {
        hull_drag *= -1.0f;
    }
```

### Step 3. Thrust

$$ T= F_{Tmax}\\delta_T$$

where $F_{T,max}$ is the motor thrust at full throttle and $δ_T$ is the throttle command from -1 to +1.

[Line 273-285](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.cpp#L273-L285)
``` cpp
  // throttle force (for motor sailing)
    // gives throttle force == hull drag at 10m/s
    float throttle_force = 0.0f;
    if (motor_connected) {
        if (skid_steering) {
            const float throttle_left = input.servos[MOTORLEFT_SERVO_CH] ? normalise_servo_input(input.servos[MOTORLEFT_SERVO_CH]) : 0;
            const float throttle_right = input.servos[MOTORRIGHT_SERVO_CH] ? normalise_servo_input(input.servos[MOTORRIGHT_SERVO_CH]) : 0;
            throttle_force = (0.5f*(throttle_left + throttle_right)) * 50.0f;
        } else {
            const float throttle_out = input.servos[THROTTLE_SERVO_CH] ? normalise_servo_input(input.servos[THROTTLE_SERVO_CH]) : 0;
            throttle_force = throttle_out * 50.0f;
        }
    }
``` 

[!Note] The stock model treats reverse the same as forward with maximum reverse thrust as -50N. Real boats are usually weaker in reverse.

### Step 4. Acceleration

$$ m\\dot u = T-D $$

In this step the force is built as a three-part vector (forward, sideways and down). The forward part is thrust plus force forward (0 for a motorboat), minus the drag.

The sideways and down parts are 0 since the stock model has no side or vertical forces.

Centripetal acceleration is then added so the boat moves where it points with no sideslip. it changes only the direction of travel, not the speed.

Finally, acceleration is converted form the boat's frame into north/east using the boat's heading. This points the forward acceleration towards the boat's heading, so the boat speeds up in that direction. 

[Lines 287–300](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.2/libraries/SITL/SIM_Sailboat.cpp#L287C4-L300)  

``` cpp
    // accel in body frame due acceleration from sail and deceleration from hull friction
    accel_body = Vector3f((throttle_force + force_fwd) - hull_drag, 0, 0);
    accel_body /= mass;

    // add in accel due to direction change
    accel_body.y += radians(yaw_rate) * speed;

    // now in earth frame
    Vector3f accel_earth = temp_dcm * accel_body;

```
