# 模型测试
# 优化问题求解：解决储能系统何时充电和放电以及光伏出力多少，以最小化经济成本，同时满足电力系统的运行约束

import numpy as np
# pip3 install cvxpy 用于构建和求解优化问题
from cvxpy import Variable, Minimize, Problem, sum, multiply, constraints
# pip3 install matplotlib
import matplotlib.pyplot as plt

# 数据加载，全部需要导入
# 储能放电价格 1*31
price_dis = np.array([0.010, 0.700, 1.100, 0.620, 0.840, 0.790, 0.960, 0.590, 0.350, 0.010, 
                      0.010, 0.900, 0.540, 1.000, 1.090, 0.900, 0.590, 0.670, 0.850, 0.660, 
                      0.680, 0.770, 0.660, 1.030, 1.080, 0.710, 1.010, 0.420, 1.120, 1.270, 0.730])
# 储能充电价格 1*31
price_chr = np.array([0.930, 0.700, 0.820, 0.720, 0.760, 0.830, 0.740, 0.750, 0.320, 0.010, 
                      0.010, 0.900, 0.780, 0.720, 0.890, 0.710, 0.770, 0.740, 0.770, 0.740, 
                      0.750, 0.800, 0.740, 0.860, 0.720, 0.790, 0.740, 0.870, 0.740, 0.750, 0.740])
# 光伏出力价格 1*31
price_pv = np.array([0.950, 0.700, 0.850, 0.710, 0.740, 0.870, 0.770, 0.750, 0.400, 0.010, 
                     0.010, 0.910, 0.780, 0.720, 0.960, 0.710, 0.770, 0.740, 0.760, 0.750, 
                     0.760, 0.810, 0.720, 0.940, 0.730, 0.790, 0.750, 0.870, 0.740, 0.750, 0.740])
# 光伏装机容量
P_PV =150
# 充电桩电量 1*31
P_load = np.array([16.0, 15.69, 65.61, 45.7, 57.51, 32.2, 13.38, 62.82, 39.68, 43.0, 
                   45.0, 41.79, 97.64, 20.35, 77.36, 122.89, 104.29, 91.0, 79.4, 57.7, 
                   72.94, 43.58, 113.64, 61.41, 49.33, 13.07, 48.65, 55.74, 48.84, 10.84, 43.21])
# 储能最大放电功率
P_dis_max = 60  # kWh
# 储能最大充电功率
P_chr_max = 60
# 储能容量
S = 120
# 储能初始容量
S_0 = 0.3 * S
# 储能最大出力容量
S_max = 0.9 * S
# 储能最小出力容量
S_min = 0.2 * S
# 储能充电效率
yita = 0.9

# 根据价格数组的形状确定时间大小（天数）
T = price_dis.shape[0]  # 天数
# 变量加载
P_dis = Variable(T)
P_chr = Variable(T)
P_pv = Variable(T)
S_es = Variable(T)
u_chr = Variable(T, boolean=True)
u_dis = Variable(T, boolean=True)

# 约束条件
constraints = []

# 功率平衡约束
for i in range(T):
    constraints.append(P_dis[i] + P_pv[i] - P_chr[i] == P_load[i])

# 光伏约束
constraints += [P_pv >= 0, P_pv <= P_PV]

# 储能约束
constraints += [P_dis >= 0, P_dis <= P_dis_max]
constraints += [P_chr >= 0, P_chr <= P_chr_max]

# 储能状态约束
constraints += [S_es[0] == S_0, S_es[-1] == S_0]
constraints += [S_es >= S_min, S_es <= S_max]
for t in range(1, T):
    constraints.append(S_es[t] - S_es[t-1] + P_dis[t]/yita - P_chr[t]*yita == 0)

# 目标函数
cost_es = sum(0.01 * (price_dis + price_chr))
objective = Minimize(sum(multiply(P_dis, price_dis)) - sum(multiply(P_chr, price_chr)) + sum(multiply(P_pv, price_pv)) - cost_es)

# 求解
problem = Problem(objective, constraints)
problem.solve()

# 电价计算
price = []
for i in range(T):
    dual_val = constraints[i].dual_value
    if dual_val is not None:
        price.append(-dual_val)
    else:
        print(f"Dual variable for constraint {i+1} is not valid.")

# 绘图
P = np.vstack([P_dis.value - P_chr.value, P_pv.value]).T

plt.figure()
print(range(T))
plt.bar(range(T), P[:, 0], label='ES_DIS')
plt.bar(range(T), P[:, 1], bottom=P[:, 0], label='PV')
plt.plot(P_load, label='LOAD')
plt.legend()
plt.savefig('energy_distribution.png')
plt.show()

profit_pv = sum(P_pv.value * price)
profit_es = sum(P_dis.value * price) - sum(P_chr.value * price)
print("profit_pv", profit_pv.value)
print("profit_es", profit_es.value)

# 电价图
plt.figure()
print("price", price)
plt.plot(price)
plt.title('electricity_price')
plt.xlabel('time/h')
plt.ylabel('declaration_electricity_price')
plt.savefig('electricity_price.png')
plt.show()

# 光伏中标结果
plt.figure()
print("PV", P_pv.value)
plt.bar(range(T), P_pv.value)
plt.title('PV_bid_electricity_bid_winning')
plt.xlabel('time/h')
plt.ylabel('power/kwh')
plt.savefig('PV_bid_electricity_bid_winning.png')
plt.show()

# 储能中标结果
plt.figure()
print("energy_storage", P_dis.value - P_chr.value)
plt.bar(range(T), P_dis.value - P_chr.value)
plt.title('energy_storage_electricity_bid_winning')
plt.xlabel('time/h')
plt.ylabel('power/kwh')
plt.savefig('energy_storage_electricity_bid_winning.png')
plt.show()