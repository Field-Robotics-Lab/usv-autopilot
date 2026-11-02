% Read_SITL_Run.m
% Plot ground speed from the newest SITL .BIN log and save the run's
% parameters as a .parm file next to the log. Needs the UAV Toolbox.

% Settings: change to your Linux user name and distribution name
linuxUser = "<user>";
distro    = "Ubuntu-22.04";

folder = "\\wsl.localhost\" + distro + "\home\" + linuxUser + "\ardupilot\Rover\logs";
d = dir(fullfile(folder,"*.BIN"));
[~,k] = max([d.datenum]);                              % newest log
logObj = ardupilotreader(fullfile(folder,d(k).name));

gps = readMessages(logObj,"MessageName",{'GPS'});
T = gps.MsgData{1};
plot(T.Properties.RowTimes, T.Spd)                     % speed vs time
xlabel("Time"); ylabel("Speed (m/s)"); grid on

P = readParameters(logObj);                            % parameters from the log
[names,idx] = unique(string(P.Name),"last");
[~,base] = fileparts(d(k).name);
parmFile = fullfile(folder,base + ".parm");
writelines(compose("%s,%.7g",names,P.Value(idx)),parmFile);
edit(parmFile)                                         % open it in a new tab
