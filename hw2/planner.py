import gurobipy as gp
from gurobipy import GRB

# 创建模型
model = gp.Model("Problem2")

# 定义变量（x1 ~ x7, 均为非负）
x = [model.addVar(lb=0, name=f"x{i}") for i in range(1, 8)]

# 设置目标函数：max (3/4)x4 - 20x5 + (1/2)x6 - 6x7
model.setObjective((3/4)*x[3] - 20*x[4] + 0.5*x[5] - 6*x[6], GRB.MAXIMIZE)

# 添加约束
# 1) x1 + 1/4 x4 - 8x5 - x6 + 9x7 = 0
model.addConstr(x[0] + 0.25*x[3] - 8*x[4] - x[5] + 9*x[6] == 0, name="eq1")

# 2) x2 + 1/2 x4 - 12x5 - 1/2 x6 + 3x7 = 0
model.addConstr(x[1] + 0.5*x[3] - 12*x[4] - 0.5*x[5] + 3*x[6] == 0, name="eq2")

model.addConstr(x[2] + x[5] <= 0, name="conflict") 

# 3) x3 + x6 = 1
model.addConstr(x[2] + x[5] == 1, name="eq3")

# 启用 Bland 规则防止退化循环（可选）
try:
    model.Params.Bland = 1
except Exception:
    pass

# 优化
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    print("\n✅ 最优目标值: ", model.objVal)
    print("✅ 最优解：")
    for v in model.getVars():
        print(f"  {v.varName} = {v.x:.4f}")
else:
    model.computeIIS()
    model.write("infeasible.ilp")
    for c in model.getConstrs():
        if c.IISConstr:
            print(f"冲突约束: {c.ConstrName}")
    print(f"⚠️ 模型未找到最优解，状态码: {model.status}")
