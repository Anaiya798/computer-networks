def calc_checksum(data, base=16):
    k = base // 8
    result = 0
    for i in range(0, len(data), k):
        result = (result + int.from_bytes(data[i:i + k], 'big')) % 2 ** base
    return 2 ** base - 1 - result


def verify_checksum(data, base=16):
    k = base // 8
    result = 0
    for i in range(0, len(data), k):
        result = (result + int.from_bytes(data[i:i + k], 'big')) % 2 ** base
    return result == 2 ** base - 1
