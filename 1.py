import pandas as pd
import random

# 读取CSV文件中的明文和密文对
csv_file_path = '/mnt/data/差分分析明密文_第16组.csv'

# 假设CSV文件包含两列：明文（plaintext）和密文（ciphertext）
df = pd.read_csv(csv_file_path)

# 查看数据结构，确保包含明文和密文对
print(df.head())


# 密钥调度算法（假设已实现）
def key_schedule(key):
    K0 = key[:16]
    K1 = key[16:]
    return [K0, K1, K0, K1, K0, K1]  # 轮密钥交替使用


# XOR操作
def xor_bits(a, b):
    return [i ^ j for i, j in zip(a, b)]


# S盒层操作（简化版）
def sbox_layer(state):
    output = []
    for i in range(0, 16, 4):
        nibble = state[i:i + 4]
        index = int(''.join(map(str, nibble)), 2)
        substituted = format(S_BOX[index], '04b')
        output.extend([int(bit) for bit in substituted])
    return output


# P盒置换操作（简化版）
def pbox_permutation(bits):
    return [bits[i] for i in P_BOX]


# CipherFour加密算法实现（简化版）
def cipherfour_encrypt(plaintext, key):
    round_keys = key_schedule(key)  # 获取轮密钥
    state = plaintext

    # 轮数1-4
    for i in range(4):
        state = xor_bits(state, round_keys[i])  # 异或轮密钥
        state = sbox_layer(state)  # 通过S盒代换
        state = pbox_permutation(state)  # P置换

    # 最后一轮无P盒
    state = xor_bits(state, round_keys[4])  # 最后一轮异或轮密钥
    state = sbox_layer(state)  # 通过S盒代换
    ciphertext = xor_bits(state, round_keys[5])  # 最后一轮异或得到密文

    return ciphertext


# 计算密钥恢复攻击的成功率
def key_recovery_attack(df, key_schedule, num_trials=100):
    correct_key_guesses = 0

    for _ in range(num_trials):
        # 随机选择一对明文进行加密
        plaintext_pair = random.sample(df['plaintext'], 2)
        ciphertext1 = cipherfour_encrypt(plaintext_pair[0], key_schedule)
        ciphertext2 = cipherfour_encrypt(plaintext_pair[1], key_schedule)

        # 对密文对进行差分分析
        guess_key = perform_diff_analysis(ciphertext1, ciphertext2, key_schedule)

        # 检查密钥是否正确
        if check_correct_key(guess_key, ciphertext1, ciphertext2):
            correct_key_guesses += 1

    # 计算成功率
    success_rate = correct_key_guesses / num_trials
    print(f"密钥恢复攻击成功率: {success_rate * 100:.2f}%")
    return success_rate


# 差分分析：假设你已经定义了基于差分特征的攻击方法
def perform_diff_analysis(ciphertext1, ciphertext2, key_schedule):
    # 假设这个函数使用差分分析方法来恢复密钥
    guessed_key = random.choice(key_schedule)  # 随机选择一个密钥作为猜测
    return guessed_key


# 检查密钥是否正确
def check_correct_key(guess_key, ciphertext1, ciphertext2):
    # 通过使用猜测的密钥解密密文对，检查是否正确恢复
    decrypted1 = decrypt(ciphertext1, guess_key)
    decrypted2 = decrypt(ciphertext2, guess_key)

    # 这里的比较可以根据实际情况做修改，例如比较某些特定的状态或输出
    return decrypted1 == decrypted2


# 假设有一个解密函数（根据你的实现选择适当的解密方法）
def decrypt(ciphertext, key):
    # 这里简化了，实际的解密应该调用CipherFour的解密算法
    return ciphertext  # 需要根据CipherFour的具体实现来解密


# 示例：进行密钥恢复攻击的测试
def test_key_recovery_attack():
    key_schedule = [0x00000000, 0x00010000, 0x00020000]  # 密钥调度样例
    # 假设有一些密文对，这里简化
    ciphertexts = {
        0x00000000: 0x10011000,
        0x00000001: 0x11011000,
        0x00010000: 0x12012000,
        0x00010001: 0x13013000
    }

    # 进行密钥恢复攻击
    key_recovery_attack(ciphertexts, key_schedule, num_trials=100)


# 测试密钥恢复攻击
if __name__ == "__main__":
    test_key_recovery_attack()
