from checksum import calc_checksum, verify_checksum


def test_base_16_good():
    data = b'Asta la vista, baby!'
    result = calc_checksum(data)
    data_with_sum = result.to_bytes(2, byteorder='big') + data
    assert verify_checksum(data_with_sum)


def test_base_32_good():
    data = b'Goodbye, America!'
    result = calc_checksum(data, 32)
    data_with_sum = result.to_bytes(4, byteorder='big') + data
    assert verify_checksum(data_with_sum, 32)


def test_base_16_bad():
    data = b'Sorry, I am lady'
    result = calc_checksum(data)
    data_with_sum = result.to_bytes(2, byteorder='big') + data + b'1'
    assert not verify_checksum(data_with_sum)


if __name__ == '__main__':
    test_base_16_good()
    test_base_32_good()
    test_base_16_bad()
