import math
from gurobipy import *
import matplotlib.pyplot as plt

# -------------------------------------------------
# 函数：生成正五边形顶点
# -------------------------------------------------
def regular_pentagon(center, radius, theta0):
    cx, cy = center
    pts = []
    for k in range(5):
        ang = theta0 + 2 * math.pi * k / 5
        pts.append((cx + radius * math.cos(ang),
                    cy + radius * math.sin(ang)))
    return pts

# -------------------------------------------------
# 五边形 A 和 B 参数
# -------------------------------------------------
A_center = (0.0, 0.0)
B_center = (2.0, 2.0)
R = 1.0

theta0_A = 0.0          # A 的一个顶点在 (1, 0)
theta0_B = -math.pi/2   # B 的一个顶点在 (2, 1)

# 生成顶点
A_pts = regular_pentagon(A_center, R, theta0_A)
B_pts = regular_pentagon(B_center, R, theta0_B)

nA = len(A_pts)
nB = len(B_pts)

# -------------------------------------------------
# Gurobi 模型：最短距离（凸组合法）
# -------------------------------------------------
model = Model("MinDistance_Polygons")

alpha = model.addVars(nA, lb=0, name="alpha")
beta  = model.addVars(nB, lb=0, name="beta")

# A 点
xA = model.addVar(name="xA")
yA = model.addVar(name="yA")

# B 点
xB = model.addVar(name="xB")
yB = model.addVar(name="yB")

# α_i 求和 = 1
model.addConstr(sum(alpha[i] for i in range(nA)) == 1)
model.addConstr(xA == sum(alpha[i] * A_pts[i][0] for i in range(nA)))
model.addConstr(yA == sum(alpha[i] * A_pts[i][1] for i in range(nA)))

# β_j 求和 = 1
model.addConstr(sum(beta[j] for j in range(nB)) == 1)
model.addConstr(xB == sum(beta[j] * B_pts[j][0] for j in range(nB)))
model.addConstr(yB == sum(beta[j] * B_pts[j][1] for j in range(nB)))

# 目标函数：最小化距离平方
model.setObjective((xA - xB)**2 + (yA - yB)**2, GRB.MINIMIZE)

# 求解
model.optimize()

# -------------------------------------------------
# 输出结果
# -------------------------------------------------
print("\n==== 结果 ====")
print(f"最短距离平方 = {model.objVal}")
print(f"最短距离 = {model.objVal**0.5:.6f}")
print(f"A 上最近点 = ({xA.X:.6f}, {yA.X:.6f})")
print(f"B 上最近点 = ({xB.X:.6f}, {yB.X:.6f})")

print("\nA 的凸组合系数 α：")
for i in range(nA):
    print(f"  α[{i}] = {alpha[i].X:.6f}")

print("\nB 的凸组合系数 β：")
for j in range(nB):
    print(f"  β[{j}] = {beta[j].X:.6f}")