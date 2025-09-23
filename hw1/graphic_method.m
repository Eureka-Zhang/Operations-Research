% lp_plot_vertices.m
% 图解法：绘制线性规划的可行域，标注顶点，并找最优解
% 模型：
% max z = x1 + 2*x2
% s.t.   2x1 + 5x2 >= 12
%        x1 + 2x2 <= 8
%        0 <= x1 <= 4
%        0 <= x2 <= 3

clear; clc; close all;

% 约束直线（写成 a*x1 + b*x2 = c 的形式）
lines = {
    [2 5], 12;   % 2x1+5x2=12
    [1 2], 8;    % x1+2x2=8
    [1 0], 0;    % x1=0
    [1 0], 4;    % x1=4
    [0 1], 0;    % x2=0
    [0 1], 3     % x2=3
};

m = size(lines,1);

% --- 计算所有直线交点 ---
pts = [];
for i = 1:m-1
    a1 = lines{i,1}; c1 = lines{i,2};
    for j = i+1:m
        a2 = lines{j,1}; c2 = lines{j,2};
        A = [a1; a2];
        b = [c1; c2];
        if abs(det(A)) > 1e-9
            x = A\b;
            pts = [pts; x'];
        end
    end
end

% 去掉重复点
tol = 1e-8;
pts = unique(round(pts/tol)*tol,'rows');

% --- 筛选可行点 ---
feasible = [];
for k = 1:size(pts,1)
    x1 = pts(k,1); x2 = pts(k,2);
    if (2*x1 + 5*x2 >= 12-1e-9) && ...
       (x1 + 2*x2 <= 8+1e-9) && ...
       (x1 >= -1e-9) && (x1 <= 4+1e-9) && ...
       (x2 >= -1e-9) && (x2 <= 3+1e-9)
        feasible = [feasible; x1 x2];
    end
end

% --- 绘图 ---
figure('Color','w'); hold on; box on;
xlabel('x_1'); ylabel('x_2');
title('线性规划可行域与顶点');

x1v = linspace(-0.5,4.5,400);

% 约束直线
h1=plot(x1v,(12-2*x1v)/5,'b','LineWidth',1.5);     % 2x1+5x2=12
h2=plot(x1v,(8-x1v)/2,'r','LineWidth',1.5);        % x1+2x2=8
h3=plot([0 0],[0 3],'k--'); 
plot([4 4],[0 3],'k--'); % x1=0,4
h4=plot([0 4],[0 0],'k--'); 
plot([0 4],[3 3],'k--'); % x2=0,3

% 可行域（凸包填充）
if size(feasible,1) >= 3
    kch = convhull(feasible(:,1),feasible(:,2));
    h5=fill(feasible(kch,1), feasible(kch,2), [0.8 0.9 1],'FaceAlpha',0.5,'EdgeColor','b');
end

% 标出顶点并标注坐标
h6=plot(feasible(:,1),feasible(:,2),'ko','MarkerFaceColor','k','MarkerSize',6);
for i = 1:size(feasible,1)
    text(feasible(i,1)+0.05, feasible(i,2)+0.05, ...
        sprintf('(%.2f, %.2f)', feasible(i,1), feasible(i,2)));
end

% --- 找最优解 ---
z = feasible(:,1) + 2*feasible(:,2);
[~,idx] = max(z);
opt_pt = feasible(idx,:);
h7=plot(opt_pt(1), opt_pt(2), 'rp','MarkerFaceColor','r','MarkerSize',14);
text(opt_pt(1)+0.1,opt_pt(2)-0.1, ...
    sprintf('最优解 (%.2f, %.2f), z=%.2f',opt_pt(1),opt_pt(2),z(idx)), ...
    'Color','r','FontWeight','bold');

axis([0 4 0 3]);
legend([h1,h2,h3,h4,h5,h6,h7],{'2x1+5x2=12','x1+2x2=8','x1=0~4','x2=0~3','可行域','顶点','最优解'}, ...
    'Location','northeastoutside');
