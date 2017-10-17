clear; clc; close all;

du = 0.5;
th = 0.02;

[FileName,PathName] = uigetfile('*.wav',...
    'Read the wave from audio file (.wav)');
FileName = strcat(PathName, FileName);
[x,fs] = audioread(FileName);
s= x(:,1);

N = length(s);
time_duration = du;
time_length = time_duration*fs;
num_times = floor (N/time_length);
y=zeros(N,1);
count = 0;
number = 0;
for i = 1:num_times
    time=s((i-1)*time_length+1:time_length*i);
    max_value=max(time);
    if (max_value > th)
        count = count + 1;
        y((count-1)*time_length + 1:time_length*count) = time;
    else
        number = number + 1;
    end
end;
y(N-number*time_length:end) = [];

[pathstr,name,ext] = fileparts(FileName);
FileName = strcat(pathstr, '\', name, '[-r]', ext);
audiowrite(FileName,y,fs);
msgbox('Successfully Saved','');
