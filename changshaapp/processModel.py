import numpy as np
# pip3 install cvxpy 用于构建和求解优化问题
from cvxpy import Variable, Minimize, Problem, sum, multiply, constraints
# pip3 install matplotlib
import matplotlib.pyplot as plt

def data_process(price_dis, price_chr, price_pv, P_PV, P_load, P_dis_max, P_chr_max, S, S_0, S_max, S_min, yita):
    """
    params:
    储能放电价格 1*31 price_dis
    储能充电价格 1*31 price_chr
    光伏出力价格 1*31 price_pv
    充电桩电量 1*31 P_load
    光伏装机容量 P_PV
    储能最大放电功率 kWh P_dis_max
    储能最大充电功率 P_chr_max
    储能容量 S
    储能初始容量 S_0 0.3*S
    储能最大出力容量 S_max 0.9*S
    储能最小出力容量 S_min 0.2*S
    储能充电效率 yita
    """

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

    # # 绘图
    # P = np.vstack([P_dis.value - P_chr.value, P_pv.value]).T

    # plt.figure()
    # print(range(T))
    # plt.bar(range(T), P[:, 0], label='ES_DIS')
    # plt.bar(range(T), P[:, 1], bottom=P[:, 0], label='PV')
    # plt.plot(P_load, label='LOAD')
    # plt.legend()
    # plt.savefig('energy_distribution.png')
    # plt.show()

    profit_pv = sum(P_pv.value * price)
    profit_es = sum(P_dis.value * price) - sum(P_chr.value * price)
    # print("profit_pv", profit_pv.value)
    # print("profit_es", profit_es.value)

    # # 电价图
    # plt.figure()
    # print("price", price)
    # plt.plot(price)
    # plt.title('electricity_price')
    # plt.xlabel('time/h')
    # plt.ylabel('declaration_electricity_price')
    # plt.savefig('electricity_price.png')
    # plt.show()

    # # 光伏中标结果
    # plt.figure()
    # print("PV", P_pv.value)
    # plt.bar(range(T), P_pv.value)
    # plt.title('PV_bid_electricity_bid_winning')
    # plt.xlabel('time/h')
    # plt.ylabel('power/kwh')
    # plt.savefig('PV_bid_electricity_bid_winning.png')
    # plt.show()

    # # 储能中标结果
    # plt.figure()
    # print("energy_storage", P_dis.value - P_chr.value)
    # plt.bar(range(T), P_dis.value - P_chr.value)
    # plt.title('energy_storage_electricity_bid_winning')
    # plt.xlabel('time/h')
    # plt.ylabel('power/kwh')
    # plt.savefig('energy_storage_electricity_bid_winning.png')
    # plt.show()

    return P_dis.value, P_chr.value, P_pv.value, price, profit_pv.value, profit_es.value 