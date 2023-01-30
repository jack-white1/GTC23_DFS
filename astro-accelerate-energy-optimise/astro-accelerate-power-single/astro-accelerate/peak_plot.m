data_table = readtable('real_data_345s_200shiftplane.dat');
data_xyz = table2array(data_table);
data_table = [];
data_xyz = [data_xyz(:,1) data_xyz(:,4) data_xyz(:,5)];
dotsize = 50;  %adjust as needed
scatter3(data_xyz(:,1), data_xyz(:,2), data_xyz(:,3), dotsize, data_xyz(:,3), 'filled');
colormap turbo
ylim([250 6000]);
%ylim([926.185 926.2]);
%ylim([1389.25 1389.35]);
%ylim([1852 1854]);
%zlim([20 30]);
xlabel('Acceleration');
ylabel('Frequency');
zlabel('Power');