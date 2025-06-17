def int_to_binary_cmd_sts(num):
    if num >= 0:
        binary_str = bin(num)[2:].zfill(31)
        binary_str = '0' + binary_str
        reversed_binary_str = binary_str[::-1]
    else:
        num = num + 2147483648
        binary_str = bin(num)[2:].zfill(31)
        binary_str = '1' + binary_str
        reversed_binary_str = binary_str[::-1]

    return reversed_binary_str


def int_to_binary_msk(num):
    num = num*-1-1
    if num >= 0:
        binary_str = bin(num)[2:].zfill(31)
        binary_str = '0' + binary_str
        reversed_binary_str = binary_str[::-1]
    else:
        num = num + 2147483648
        binary_str = bin(num)[2:].zfill(31)
        binary_str = '1' + binary_str
        reversed_binary_str = binary_str[::-1]

    return reversed_binary_str


def int_to_binary_cmd_sts_list(num):
    if num >= 0:
        binary_str = bin(num)[2:].zfill(31)
        binary_str = '0' + binary_str
        reversed_binary_str = binary_str[::-1]
    else:
        num = num + 2147483648
        binary_str = bin(num)[2:].zfill(31)
        binary_str = '1' + binary_str
        reversed_binary_str = binary_str[::-1]

    return list(reversed_binary_str)


def int_to_binary_msk_list(num):
    num = num*-1-1
    if num >= 0:
        binary_str = bin(num)[2:].zfill(31)
        binary_str = '0' + binary_str
        reversed_binary_str = binary_str[::-1]
    else:
        num = num + 2147483648
        binary_str = bin(num)[2:].zfill(31)
        binary_str = '1' + binary_str
        reversed_binary_str = binary_str[::-1]

    return list(reversed_binary_str)


