import netifaces


def ips_and_masks():  # вывод ip-адресов и масок по всем доступным интерфейсам
    for interface in netifaces.interfaces():
        try:
            print('===')
            print(f'Interface: {interface}')
            print(f"IP Address: {netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']}")
            print(f"Mask: {netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']}")
        except:
            pass


if __name__ == '__main__':
    ips_and_masks()
