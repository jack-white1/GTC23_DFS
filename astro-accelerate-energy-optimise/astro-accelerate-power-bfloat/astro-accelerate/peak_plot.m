data_table = readtable('real_data_bfloatpeaks.dat');
data_xyz = table2array(data_table);
data_table = [];
data_xyz = [data_xyz(:,1) data_xyz(:,4) data_xyz(:,5)];
dotsize = 50;  %adjust as needed
scatter3(data_xyz(:,1), data_xyz(:,2), data_xyz(:,3), dotsize, data_xyz(:,3), 'filled');
colormap turbo