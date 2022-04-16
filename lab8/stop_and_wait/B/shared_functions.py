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