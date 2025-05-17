import numpy as np

# 定义S盒 (此为示例，具体S盒请根据题目提供的S盒进行修改)
S_box = [
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2
]

# 生成差分分布表 (DDT)
def generate_ddt(S_box):
    size = len(S_box)
    ddt = np.zeros((size, size), dtype=int)

    for input_diff in range(size):
        for output_diff in range(size):
            count = 0
            # 遍历所有可能的输入对
            for x in range(size):
                y = x ^ input_diff
                if S_box[x] ^ S_box[y] == output_diff:
                    count += 1
            ddt[input_diff][output_diff] = count
    return ddt

# 获取并打印S盒的差分分布表
ddt = generate_ddt(S_box)
print("S盒的差分分布表（DDT）：\n", ddt)

# 选择最优差分路线
def find_best_differential_route(ddt):
    best_route = []
    best_probability = 0

    for input_diff in range(len(ddt)):
        output_diff_probabilities = ddt[input_diff] / np.sum(ddt[input_diff])
        best_output_diff = np.argmax(output_diff_probabilities)
        best_route.append((input_diff, best_output_diff, output_diff_probabilities[best_output_diff]))

    return best_route

# 找到最优差分路线
best_route = find_best_differential_route(ddt)
print("最优差分路线：\n", best_route)

# 计算路径的概率
def calculate_probability(ddt, path):
    probability = 1
    for delta_in, delta_out, _ in path:  # 修改这里，解包时忽略第三个元素（概率）
        probability *= ddt[delta_in][delta_out] / sum(ddt[delta_in])
    return probability

# 找到更多的差分路径
def find_additional_paths(ddt, best_route):
    additional_paths = []
    # 假设我们从最优路径延伸，找出满足条件的其他差分路径
    # 这里可以根据实际需求扩展路径，假设我们寻找一个深度为3的路径
    for i in range(len(best_route)):
        path = [best_route[i]]  # 起始路径为最优差分路径
        # 在此基础上找到其他符合条件的差分路径
        for _ in range(2):  # 假设继续向下扩展2步，构造新的路径
            last_input_diff, last_output_diff, _ = path[-1]
            next_best_output_diff = np.argmax(ddt[last_input_diff])
            path.append((last_input_diff, next_best_output_diff, ddt[last_input_diff][next_best_output_diff] / np.sum(ddt[last_input_diff])))
        additional_paths.append(path)
    return additional_paths

# 找到更多的差分路径
additional_paths = find_additional_paths(ddt, best_route)

# 计算所有差分路径的总概率
total_probability = 0
# 计算最优路径的概率
total_probability += calculate_probability(ddt, best_route)
# 计算其他路径的概率
for path in additional_paths:
    total_probability += calculate_probability(ddt, path)

print(f"所有差分路径的总概率：{total_probability}")
