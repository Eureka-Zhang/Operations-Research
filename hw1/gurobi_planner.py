import gurobipy as gp
from gurobipy import GRB

# 创建模型
model = gp.Model("simple_lp")

# 定义变量（默认下限为0，所以这里要放宽）
x1 = model.addVar(lb=0, name="x1")
x2 = model.addVar(lb=0, name="x2")

# 设置目标函数
model.setObjective(x1 + x2, GRB.MINIMIZE)

# 添加约束
model.addConstr(x1 >= 1, "c1")
model.addConstr(x2 >= 2, "c2")

# 求解
model.optimize()

# 打印解
if model.status == GRB.OPTIMAL:
    print("\n最优目标值:", model.objVal)
    for v in model.getVars():
        print(v.varName, "=", v.x)
1