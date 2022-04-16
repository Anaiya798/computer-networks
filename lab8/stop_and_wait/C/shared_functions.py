def read_file(filename, chunk_size):
    try:
        file = open(filename, "rb")
        pkgs = []
        try:
            bytes_read = file.read(chunk_size)
            pkgs.append(bytes_read)
            while bytes_read:
                bytes_read = file.read(chunk_size)
                pkgs.append(bytes_read)
        except Exception:
            print(f'Unknown exception while reading from {filename}')
        finally:
            file.close()
        pkgs.append('END'.encode('utf-8'))
        return pkgs
    except FileNotFoundError:
        print(f'No such file or directory {filename}')


def process_data(data, type='general'):
    content_size = None
    if type == 'ack':
        data = data.split('\n')
        content_size = int(data[2].split(':')[1])
        checksum = int(data[3].split(':')[1])
        raw_data = '\n'.join(data[:3])
    else:
        data = data.split('\n\t\n')
        checksum = int(data[1].split(':')[1])
        raw_data = '\n'.join(data[:1])

    return content_size, checksum, raw_data
