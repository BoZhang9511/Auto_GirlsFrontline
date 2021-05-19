# from LogInfo import LogInfo
import numpy as np
import pulp as lp


# 设置目标天数为0表示要求用最短时间增加到指定资源/用最长时间减少到指定资源（取决于现有资源和目标资源的大小关系）
# 不为则0表示要求在指定天数内获得最多的资源
# 当目标天数设置为0时，可以将目标资源设置为不大于1的数来表示最大化资源的比例
# 例如，设置目标天数为0，目标四项资源为20w,5w,20w,10w，则会计算如何在最短的时间内将四项资源跑到目标值
# 设置目标天数为20，目标四项资源为0.2,0.05,0.2,0.1，则会计算如何在20天内按照2021公式的资源比例尽可能最大化资源储备
# 设置目标天数为20，目标四项资源为20w,5w,0.2,0.1，则会计算如何在20天内将人力弹药跑到20w和5w，并在期间内按照2:1的比例尽可能最大化口粮和零件的储备

target_day = 6  # 目标天数

cntBuild = 0
combatHours = 0
times = combatHours*60/3.8
res = [
#    现有    目标    每日消耗
    [9,  0.7+2000*cntBuild, 97*4+210*5+900*24/11+(42-500/26)*times],  # 人力
    [9, 0.6+500*cntBuild, 404*4+210*5+900*24/11+(25-586/26)*times],   # 弹药
    [9, 0.1+2000*cntBuild, 404*4+50*5+900*24/11+(10-454/26)*times],  # 口粮
    [9, 0.4+1000*cntBuild, 97*4+100*5+300*24/11-115/26],  # 零件
    [0,   0,      0],    # 人形
    [0,   0,      0],    # 装备
    [0,   0,      0],    # 快建
    [0,   0,      0],    # 快修
    [0,   0,      0],    # 采购
]
auto_restore = [0, 0, 0, 0]  # 人力弹药口粮零件的自回，1为有自回，0没有
level = 100  # 队伍等级
sleeping =  0 # 睡觉时长（分钟）
delay =  4.5 # 平均延迟（分钟）
sep = 9  # 最小检查周期（分钟）
min_len = 10  # 最短后勤时间（分钟）
holy_log = 0  # 是否处于生煎期间，1是生煎，0是普通

LogInfo = [
#      后勤  时间  人力  弹药  口粮  零件  人形  装备  快建  快修  采购
    [' 0-1',   50,    0,  145,  145,    0, 0.00, 0.00, 0.20, 0.50, 0.00],
    [' 0-2',  180,  550,    0,    0,  350, 0.50, 0.00, 0.00, 0.00, 0.00],
    [' 0-3',  720,  900,  900,  900,  250, 0.00, 0.50, 0.00, 0.50, 0.00],
    [' 0-4', 1440,    0, 1200,  800,  750, 0.00, 0.00, 0.00, 0.00, 1.00],
    [' 1-1',   15,   10,   30,   15,    0, 0.00, 0.00, 0.00, 0.00, 0.00],
    [' 1-2',   30,    0,   40,   60,    0, 0.00, 0.00, 0.00, 0.00, 0.00],
    [' 1-3',   60,   30,    0,   30,   10, 0.00, 0.00, 0.00, 0.60, 0.00],
    [' 1-4',  120,  160,  160,    0,    0, 0.20, 0.00, 0.00, 0.00, 0.00],
    [' 2-1',   40,  100,    0,    0,   30, 0.00, 0.00, 0.00, 0.00, 0.00],
    [' 2-2',   90,   60,  200,   80,    0, 0.00, 0.00, 0.00, 0.30, 0.00],
    [' 2-3',  240,   10,   10,   10,  230, 0.00, 0.00, 0.50, 0.50, 0.00],
    [' 2-4',  360,    0,  250,  600,   60, 0.80, 0.00, 0.00, 0.00, 0.00],
    [' 3-1',   20,   50,    0,   75,    0, 0.00, 0.00, 0.00, 0.00, 0.00],
    [' 3-2',   45,    0,  120,   70,   30, 0.00, 0.00, 0.00, 0.00, 0.00],
    [' 3-3',   90,    0,  300,    0,    0, 0.00, 0.00, 0.40, 0.45, 0.00],
    [' 3-4',  300,    0,    0,  300,  300, 0.35, 0.40, 0.00, 0.00, 0.00],
    [' 4-1',   60,    0,  185,  185,    0, 0.00, 0.20, 0.00, 0.00, 0.00],
    [' 4-2',  120,    0,    0,    0,  210, 0.00, 0.00, 0.50, 0.00, 0.00],
    [' 4-3',  360,  800,  550,    0,    0, 0.70, 0.00, 0.00, 0.30, 0.00],
    [' 4-4',  480,  400,  400,  400,  150, 0.00, 0.00, 1.00, 0.00, 0.00],
#      后勤  时间  人力  弹药  口粮  零件  人形  装备  快建  快修  采购
    [' 5-1',   30,    0,    0,  100,   45, 0.00, 0.00, 0.00, 0.00, 0.00],
    [' 5-2',  150,    0,  600,  300,    0, 0.00, 0.00, 0.00, 0.80, 0.00],
    [' 5-3',  240,  800,  400,  400,    0, 0.00, 0.60, 0.00, 0.00, 0.00],
    [' 5-4',  420,  100,    0,    0,  700, 0.40, 0.00, 0.00, 0.00, 0.00],
    [' 6-1',  120,  300,  300,    0,  100, 0.00, 0.00, 0.00, 0.00, 0.00],
    [' 6-2',  180,    0,  200,  550,  100, 0.00, 0.00, 0.30, 0.70, 0.00],
    [' 6-3',  300,    0,    0,  200,  500, 0.00, 0.80, 0.00, 0.00, 0.00],
    [' 6-4',  720,  800,  800,  800,    0, 0.00, 0.00, 0.00, 0.00, 0.70],
    [' 7-1',  150,  650,    0,  650,    0, 0.00, 0.00, 0.00, 0.00, 0.00],
    [' 7-2',  240,    0,  650,    0,  300, 0.70, 0.00, 0.00, 0.20, 0.00],
    [' 7-3',  330,  900,  600,  600,    0, 0.00, 0.50, 0.00, 0.00, 0.00],
    [' 7-4',  480,  250,  250,  250,  600, 0.00, 0.00, 0.90, 0.00, 0.00],
    [' 8-1',   60,  150,  150,  150,    0, 0.00, 0.40, 0.00, 0.00, 0.00],
    [' 8-2',  180,    0,    0,    0,  450, 0.00, 0.00, 0.00, 0.80, 0.00],
    [' 8-3',  360,  400,  800,  800,    0, 0.00, 0.00, 0.50, 0.50, 0.00],
    [' 8-4',  540, 1500,  400,  400,  100, 0.80, 0.00, 0.00, 0.00, 0.00],
    [' 9-1',   30,    0,    0,  100,   50, 0.00, 0.00, 0.00, 0.00, 0.00],
    [' 9-2',   90,  180,    0,  180,  100, 0.00, 0.00, 0.25, 0.00, 0.00],
    [' 9-3',  270,  750,  750,    0,    0, 0.80, 0.00, 0.00, 0.00, 0.00],
    [' 9-4',  420,  500,  900,  900,    0, 0.00, 1.00, 0.00, 0.00, 0.00],
#      后勤  时间  人力  弹药  口粮  零件  人形  装备  快建  快修  采购
    ['10-1',   40,  140,  200,    0,    0, 0.00, 0.00, 0.00, 0.00, 0.00],
    ['10-2',  100,    0,  240,  180,    0, 0.75, 0.00, 0.25, 0.00, 0.00],
    ['10-3',  320,    0,  480,  480,  300, 0.00, 0.00, 0.60, 0.40, 0.00],
    ['10-4',  600,  660,  660,  660,  330, 0.00, 0.80, 0.00, 0.00, 0.00],
    ['11-1',  240,  350, 1050,    0,    0, 0.60, 0.40, 0.00, 0.00, 0.00],
    ['11-2',  240,  360,  540,  540,    0, 1.00, 0.00, 0.00, 0.00, 0.00],
    ['11-3',  480,    0,  750, 1500,  250, 0.00, 0.00, 0.00, 0.80, 0.00],
    ['11-4',  600,    0, 1650,    0,  900, 0.00, 0.00, 1.00, 0.00, 0.00],
    ['12-1',   60,    0,  220,  220,    0, 0.00, 0.60, 0.00, 0.00, 0.00],
    ['12-2',   90,  360,    0,    0,  120, 0.00, 0.00, 0.00, 0.00, 0.00],
    ['12-3',  540,  800, 1200, 1200,    0, 0.00, 0.00, 1.00, 0.00, 0.00],
    ['12-4', 1440, 1800,    0, 1800,    0, 1.00, 0.00, 0.00, 0.00, 0.00],
    ['13-1',  180,    0,    0, 1200,    0, 0.00, 0.00, 1.00, 0.00, 0.00],
    ['13-2',  360,  800,  800,  800,  300, 0.00, 0.00, 0.00, 0.00, 0.00],
    ['13-3', 1440,    0, 4000,    0, 1200, 0.00, 1.00, 0.00, 0.00, 0.00],
    ['13-4',  360,    0,    0,    0, 1000, 1.00, 0.00, 0.00, 0.00, 0.00],
#      后勤  时间  人力  弹药  口粮  零件  人形  装备  快建  快修  采购
]

for i in range(4):
    if auto_restore[i] != 0:
        res[i][2] -= i != 3 and 24 * 60 or 24 * 20


# 计算实际效率
log_info = np.asarray(LogInfo)[:, 1:].astype('float')
nb_logs = log_info.shape[0]
succ = holy_log == 1 and 0.3 + 0.006 * level or 0.15 + 0.0045 * level
log_info[:, 1:5] *= 1 + succ * 0.5
log_info[:, 5:10] *= (1 - succ) + 1 / (log_info[:, 5:10].sum(axis=1)[:, np.newaxis] + 1e-30) * succ
log_info[:, 0][log_info[:, 0] < min_len] = min_len
log_info[:, 0] = np.ceil(log_info[:, 0] / sep) * sep + delay
night_info = np.copy(log_info)
night_info[:, 0][night_info[:, 0] < sleeping + delay] = sleeping + delay

# 建模问题
min_day = 0
max_day = target_day
if target_day > 0:
    target = lp.LpVariable('target', 0)
    problem = lp.LpProblem('Logistics', lp.LpMaximize)
    cond = False
    for r in res:
        if -1 <= r[1] <= 1 and r[1] != 0:
            r[1] = r[1]*target
            cond = True
    if not cond:
        print('你没有设置求解目标啊老铁')
        exit(-1)
    problem += target
else:
    problem_min = False
    if sum([r[0] < r[1] for r in res]) > 0:
        problem = lp.LpProblem('Logistics', lp.LpMinimize)
        max_day = lp.LpVariable('max_day', 0)
        problem += max_day
        problem_min = True
    else:
        problem = lp.LpProblem('Logistics', lp.LpMaximize)
        min_day = lp.LpVariable('min_day', 0)
        max_day = min_day+1
        problem += min_day

day = [lp.LpVariable('day_%d' % i, 0) for i in range(nb_logs)]
night = [lp.LpVariable('night_%d' % i, 0) for i in range(nb_logs)]
res_keys = ['人力', '弹药', '口粮', '零件', '人形', '装备', '快建', '快修', '采购']
total_time = lp.lpDot(day, log_info[:, 0]) + lp.lpDot(night, night_info[:, 0])
total_full_day = total_time/24/60/4
problem += total_full_day <= max_day
problem += total_full_day >= min_day

# 物资获取约束
res_gain, res_need = {}, {}
for i, k in enumerate(res_keys):
    res_gain[k] = lp.lpDot(day, log_info[:, i+1]) + lp.lpDot(night, night_info[:, i+1]) - res[i][2] * total_full_day
    res_need[k] = res[i][1] - res[i][0]
    problem += res_gain[k] >= res_need[k]

# 各项用时约束
for i in range(nb_logs):
    problem += day[i] * log_info[i, 0] <= total_time/4 * (1 - sleeping/24/60)
    problem += night[i] * night_info[i, 0] <= total_time/4 * (sleeping/24/60)
    if sleeping > 0:
        problem += day[i] <= np.floor((24 * 60 - sleeping)/log_info[i, 0]) * total_full_day
        problem += night[i] <= total_full_day

if sleeping > 0:
    problem += lp.lpSum(night) >= total_full_day * 4
solved = problem.solve()
if solved != 1:
    print({-1: '目标定的太大啦，臣妾做不到啊', -2: '资源太多啦，这辈子也用不完啊'}[solved])
    exit(-2)

total = lp.value(total_full_day)
print('天数:%.1f\n' % total)

chosen_list = []
total += 0.001 if total == 0 else 0
for i in range(nb_logs):
    d, n = lp.value(day[i]) / total, lp.value(night[i]) / total
    d = d > 0.01 and d or 0
    n = n > 0.01 and n or 0
    if d > 0 or n > 0:
        # chosen_list.append({'mission': LogInfo[i][0], 'day': d, 'night': n})
        chosen_list.append({'mission': LogInfo[i][0], 'day': d*log_info[i][0]/60, 'night': n*night_info[i][0]/60})

lines = ['关卡', '白天', '晚上']
for i in chosen_list:
    lines[0] += '\t%7s' % i['mission']
    lines[1] += '\t%7s' % (i['day'] > 0 and '%.1f' % i['day'] or '')
    lines[2] += '\t%7s' % (i['night'] > 0 and '%.1f' % i['night'] or '')
for line in lines:
    print(line)
print('')
lines = ['类别', '现有', '获取', '总量']
for i, k in enumerate(res_keys):
    lines[0] += '\t%5s' % k
    lines[1] += '\t%7d' % res[i][0]
    lines[2] += '\t%7d' % (lp.value(res_gain[k])+0.5)
    lines[3] += '\t%7d' % (lp.value(res_gain[k])+res[i][0]+0.5)
for line in lines:
    print(line)

input()
