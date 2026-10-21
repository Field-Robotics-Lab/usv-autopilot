% Read_SITL_Run.m
% Read the newest SITL .BIN log, plot ground speed, and save the run's
% parameters as a .parm file next to the log.
% Needs MATLAB with the UAV Toolbox.

% Settings: change to your Linux user name and distribution name
linuxUser = "<user>";
distro    = "Ubuntu-22.04";

% Windows path to the Linux logs folder
folder = "\\wsl.localhost\" + distro + "\home\" + linuxUser + "\ardupilot\Rover\logs";

% Find the newest log
d = dir(fullfile(folder,"*.BIN"));
[~,k] = max([d.datenum]);

% Open the log
logObj = ardupilotreader(fullfile(folder,d(k).name));

% Table of the message types recorded in the log
logObj.AvailableMessages

% Plot ground speed versus time
gps = readMessages(logObj,"MessageName",{'GPS'});
T = gps.MsgData{1};
plot(T.Properties.RowTimes, T.Spd)
xlabel("Time"); ylabel("Speed (m/s)"); grid on

% Read every parameter in the log; keep the last value of each
% (includes any changes made during the run)
P = readParameters(logObj);
[names,idx] = unique(string(P.Name),"last");
vals = P.Value(idx);

% Save as a .parm file with the same name as the log, e.g. 00000003.parm
[~,base] = fileparts(d(k).name);
parmFile = fullfile(folder,base + ".parm");
writelines(compose("%s,%.7g",names,vals),parmFile);

% Open the .parm file in a new Editor tab
edit(parmFile)
