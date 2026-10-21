% Check_SITL_Link.m
% Check that MATLAB receives MAVLink messages from a running SITL on UDP 14551.
% Needs MATLAB with the UAV Toolbox, and SITL running with the 14551 output (Step 6a).

% Load the standard MAVLink message definitions
dialect = mavlinkdialect("common.xml");

% Create a MAVLink connection and listen on UDP port 14551
io = mavlinkio(dialect);
connect(io,"UDP","LocalPort",14551);

% Subscribe to HEARTBEAT messages (sent by the autopilot once per second)
sub = mavlinksub(io,"HEARTBEAT");

% Wait for messages to arrive
pause(3)

% Show the most recent HEARTBEAT, or report that none arrived
msg = latestmsgs(sub,1);
if isempty(msg)
    disp("No HEARTBEAT received. Check that SITL is running and 'output' lists 127.0.0.1:14551.")
else
    disp(msg)
    disp("MATLAB is receiving messages from SITL.")
end

% Close the connection
disconnect(io)
