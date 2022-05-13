from router import Router
from random import randint


def generate_ips(n=4):
    router_ips = ['...']
    cur_ip = '...'
    for _ in range(n):
        while cur_ip in router_ips:
            cur_ip = str(randint(0, 255)) + '.' + str(randint(0, 255)) + '.' + str(randint(0, 255)) + '.' + str(
                randint(0, 255))
        router_ips.append(cur_ip)
    router_ips.remove('...')
    return router_ips


def build_scheme(configs, routers):
    network_scheme = {router: [] for router in routers}
    for key in configs.keys():
        network_scheme[routers[int(key) - 1]] = [routers[int(i) - 1] for i in configs[key].split(',')]
    my_network = [
        Router(key, network_scheme[key])
        for key in network_scheme.keys()
    ]
    return my_network
