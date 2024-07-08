# 使用python读取data/SCED求解结果.xlsx文件，内部包含多个子表
import pandas as pd

# 指定文件路径
file_path = 'data/SCED求解结果.xlsx'

# 读取Excel文件
xlsx = pd.ExcelFile(file_path)

# 存储各个子表的数据
dataframes = {}

# 遍历所有工作表
for sheet_name in xlsx.sheet_names:
    # 读取每个工作表
    df = xlsx.parse(sheet_name, header=None)
    # 由于没有表头，使用默认的列名0, 1, 2, ...
    df.columns = range(df.shape[1])
    # 将当前工作表的数据存储在字典中，键为工作表名
    dataframes[sheet_name] = df

# print(dataframes['支路各时段潮流功率'][:5])

'''
1.出清结果——电能量中标结果
使用文件中“ 各火电机组电能量市场中标结果 ”（选取10*24维度，横向时间尺度应该是96，取前24）
和“ 各储能电能量市场中标结果 ”（选取4*24维度，横向时间尺度应该是96，取前24）两个工作表数据，
在横向尺度也就是24小时进行堆叠，比如说第一个小时也就是A栏数据，将火电机组的10个和储能的4个堆到一起，
但不是相加，因为还要给图注（不过写图注的时候这个储能称呼要改成“充电站”哦）
'''
# 各火电机组电能量市场中标结果
power_market_results = dataframes['各火电机组电能量市场中标'].iloc[:10, :24] 
# 各储能电能量市场中标结果
charge_station_results = dataframes['各储能电站电能量市场中标'].iloc[:4, :24] 
# 在横向尺度上堆叠
combined_power_results = pd.concat([power_market_results, charge_station_results], axis=0)
# 由于堆叠操作，charge_station_results的索引会被改变，需要重新设置索引
combined_power_results.reset_index(drop=True, inplace=True)
# 堆叠后的数据
print(combined_power_results)
'''
2.出清结果——调频市场中标结果
使用文件中“各火电机组调频市场中标结果”和“各储能调频市场中标结果”，数据使用方法和前面一样
这个放到“电能量中标结果”的右边，也就是“当日出清价格”这个模块的位置
'''
# 各火电机组调频市场中标结果
power_FM_results = dataframes['各火电机组调频市场中标'].iloc[:10, :24] 
# 各储能调频市场中标结果
charge_FM_results = dataframes['各储能电站调频市场中标'].iloc[:4, :24] 
# 在横向尺度上堆叠
combined_FM_results = pd.concat([power_FM_results, charge_FM_results], axis=0)
# 由于堆叠操作，charge_station_results的索引会被改变，需要重新设置索引
combined_FM_results.reset_index(drop=True, inplace=True)
# 堆叠后的数据
print(combined_FM_results)
'''
3.出清结果——当日出清价格
暂时把“当日出清价格”这个模块替换到“各分区中标量统计对比”，也就是页面最下面
使用的数据为“节点电价”，选取第一行的前24列数据（1*24维度）以及“调频容量电价”数据的前24列
绘制成24h下的两条曲线，直接画两个图
第一个图用“节点电价”，放在“电能量中标结果”下面，图的名称为“电能量市场出清电价”
第一个图用“调频容量电价”，放在“调频市场中标结果”下面，图的名称为“调频市场出清电价”
'''
# OK
# OK

'''
4.结果评价——交易汇总
使用“收益汇总”工作表数据，里面有火电机组10个数据和储能电站4个数据，就当成10个火电站和4个充电站用户，
标号1-14，然后后面给出他们的收益就行
'''
# OK

'''
5.结果评价——电能量和调频收益
使用“市场收入”，‘火电支出’，‘储能支出’和‘市场盈余’四个工作数据表
计算公式为“市场收入”-‘火电支出’-‘储能支出’=‘市场盈余’
这个模块中的左边“柱状图”为取‘火电支出’和‘储能支出’两个工作表前24列数据绘制
模块右边的“饼图”为取这四个工作表的前24列分部进行求和，得到4个总量来绘制
'''
# OK
# OK
