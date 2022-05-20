import scapy.all as scapy
import socket

HOME_IP = '10.0.0.100'
HOME_MAC = 'ac-7d-eb-a7-7d-3e'
HOME_HOST_NAME = socket.gethostbyaddr(HOME_IP)[0]
MASK = [255, 255, 255, 0]


def get_network_ip():
    client_ip = [int(octet) for octet in HOME_IP.split('.')]
    network_ip = ''
    for i in range(len(client_ip)):
        network_ip += str(client_ip[i] & MASK[i]) + '.'
    return network_ip[:-1]


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answer_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []

    for i in answer_list:
        clients_dict = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        clients_list.append(clients_dict)

    return clients_list


def print_result(results_list):
    print("IP Address" + "\t" * 2 + "MAC Address" + "\t" * 4 + "Host name")
    print('Home:')
    print(HOME_IP + "\t\t" + HOME_MAC + "\t\t" + HOME_HOST_NAME)

    print('Local network:')
    for host in results_list:
        ip = host["ip"]
        if ip == HOME_IP:
            continue
        mac_address = host["mac"]
        try:
            host_name = socket.gethostbyaddr(ip)[0]
        except Exception:
            host_name = '-'
        print(ip + "\t" * 2 + mac_address + "\t" * 2 + host_name)


if __name__ == '__main__':
    network_ip = get_network_ip()
    scan_result = scan(network_ip + '/24')
    print_result(scan_result)
