% 1. 导入 Excel 数据
filename = '苏州市2.xlsx';  % 需要确保路径正确
data = readtable(filename);

% 2. 提取数据
stations = data.name;  % 站点名称
lines = data.line;     % 线路名称
numbers = data.number; % 序号
lon = data.lon;        % 经度
lat = data.lat;        % 纬度

% 3. 检查并处理重复站点
[unique_stations, ~, idx] = unique(stations);
% 获取与唯一站点相对应的经度和纬度
unique_lon = accumarray(idx, lon, [], @(x) {unique(x)});
unique_lat = accumarray(idx, lat, [], @(x) {unique(x)});

% 确保每个唯一站点的经度和纬度是一维数组
unique_lon = cell2mat(unique_lon);
unique_lat = cell2mat(unique_lat);

% 4. 创建图的节点和边
G = graph(); % 创建一个空图
G = addnode(G, unique_stations); % 添加唯一节点

% 5. 添加线路边
for i = 1:height(data)-1
    if strcmp(data.line{i}, data.line{i+1}) % 同一条线路
        G = addedge(G, stations{i}, stations{i+1});
    end
end

% 6. 绘制拓扑图
figure;
p = plot(G, 'Layout', 'layered'); % 使用分层布局
title('苏州地铁拓扑图');

% 7. 创建与唯一站点相对应的序号
station_numbers = zeros(length(unique_stations), 1); % 初始化序号数组
for i = 1:length(unique_stations)
    station_numbers(i) = data.number(find(strcmp(data.name, unique_stations{i}), 1)); % 获取对应的序号
end

% 8. 显示站点序号
labelnode(p, 1:length(unique_stations), string(station_numbers)); % 用序号代替站点名

% 9. 设置节点位置
p.XData = unique_lon; % 设置唯一节点的 X 坐标
p.YData = unique_lat; % 设置唯一节点的 Y 坐标

% 10. 优化图形
p.NodeColor = 'r'; % 设置节点颜色
p.EdgeColor = 'k'; % 设置边颜色

% 3. 检查并处理重复站点
[unique_stations, ~, idx] = unique(stations);
unique_lon = accumarray(idx, lon, [], @(x) {unique(x)});
unique_lat = accumarray(idx, lat, [], @(x) {unique(x)});
unique_lon = cell2mat(unique_lon);
unique_lat = cell2mat(unique_lat);

% 4. 计算两点之间的地理距离（使用哈弗辛公式）
R = 6371;  % 地球半径（单位：千米）
adj_matrix = zeros(length(unique_stations), length(unique_stations));

haversine = @(lat1, lon1, lat2, lon2) R * 2 * asin(sqrt(sin((lat2 - lat1) / 2).^2 + cos(lat1) .* cos(lat2) .* sin((lon2 - lon1) / 2).^2));

% 计算邻接矩阵的值
for i = 1:length(unique_stations)
    for j = i+1:length(unique_stations)
        % 计算站点 i 和站点 j 之间的距离
        dist = haversine(deg2rad(unique_lat(i)), deg2rad(unique_lon(i)), deg2rad(unique_lat(j)), deg2rad(unique_lon(j)));
        
        % 假设只有同一线路的站点之间才有连接
        if strcmp(lines{i}, lines{j})
            adj_matrix(i, j) = dist;  % 赋值为距离
            adj_matrix(j, i) = dist;  % 对称赋值
        end
    end
end

% 5. 使用 graph 类
G = graph(adj_matrix, unique_stations);

% 6. 计算接近中心性
n = length(unique_stations);  % 节点数量
closeness_centrality = zeros(n, 1);

for i = 1:n
    % 使用 distances 函数计算站点 i 到其他所有站点的最短路径
    dist = distances(G, i);  % 返回从站点 i 到其他所有站点的最短路径长度
    
    % 过滤掉无连接的站点（无法到达的站点将给定一个很大的数值）
    dist(dist == Inf) = max(dist(dist ~= Inf)) + 1;  % 把无法到达的距离设为最大距离+1
    
    % 计算接近中心性
    closeness_centrality(i) = (n - 1) / sum(dist);
end

% 7. 输出接近中心性结果
closeness_centrality_table = table(unique_stations, closeness_centrality, 'VariableNames', {'Station', 'ClosenessCentrality'});

% 保存为 Excel 文件
output_file = '接近中心性.xlsx';
writetable(closeness_centrality_table, output_file);

disp('接近中心性已保存到 Excel 文件。');
