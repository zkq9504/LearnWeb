import string
from random import choice


def generate_random(random_length, str_type):
    """
    随机字符串生成函数
    :param random_length: 字符串长度
    :param str_type: 字符串类型（0：纯数字，1：数字+字符，2：数字+字符+特俗字符）
    :return:随机字符串
    """
    if str_type == 0:
        random_seed = string.digits
    elif str_type == 1:
        random_seed = string.digits + string.ascii_letters
    elif str_type == 2:
        random_seed = string.digits + string.ascii_letters + string.punctuation
    random_str = []
    while (len(random_str)) < random_length:
        random_str.append(choice(random_seed))
    return ''.join(random_str)


if __name__ == "__main__":
    print(generate_random(4, 0))
