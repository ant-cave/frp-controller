import random

def generate_valid_id_number(gender=None):
    """生成符合逻辑的随机身份证号（18位）
    :param gender: None=随机, 'M'=男, 'F'=女
    :return: 身份证号字符串
    """
    # 1. 行政区划代码（前6位，确保长度正确）
    province_codes = [
        '11', '12', '13', '14', '15',  # 华北
        '21', '22', '23',               # 东北
        '31', '32', '33', '34', '35', '36', '37',  # 华东
        '41', '42', '43', '44', '45', '46',  # 中南
        '50', '51', '52', '53', '54',       # 西南
        '61', '62', '63', '65'              # 西北
    ]
    # 确保生成完整的6位区县代码
    region_code = random.choice(province_codes) + f"{random.randint(1000, 9999):04d}"[:4]
    region_code = region_code[:6]  # 确保正好6位

    # 2. 出生日期（1950-2023年，避免未来日期）
    year = random.randint(1950, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # 简单处理避免闰年问题
    birth_date = f"{year:04d}{month:02d}{day:02d}"

    # 3. 顺序码（第15-17位）
    seq_code = random.randint(1, 999)
    if gender == 'M':
        seq_code = seq_code if seq_code % 2 == 1 else seq_code + 1  # 确保奇数
    elif gender == 'F':
        seq_code = seq_code if seq_code % 2 == 0 else seq_code + 1  # 确保偶数
    seq_code = min(999, max(1, seq_code))  # 确保在1-999范围内
    seq_code = f"{seq_code:03d}"

    # 4. 拼接前17位并计算校验码
    id_17 = f"{region_code}{birth_date}{seq_code}"
    assert len(id_17) == 17, f"前17位长度错误: {len(id_17)}"  # 调试检查

    def get_check_digit(id_17):
        """计算校验码"""
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_map = '10X98765432'
        total = sum(int(id_17[i]) * weights[i] for i in range(17))
        return check_map[total % 11]

    check_code = get_check_digit(id_17)
    return id_17 + check_code

# 测试
for _ in range(5):
    print("随机生成:", generate_valid_id_number())
print("男性:", generate_valid_id_number(gender='M'))
print("女性:", generate_valid_id_number(gender='F'))