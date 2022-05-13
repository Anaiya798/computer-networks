from network import Network
from random_ips import *


import json

if __name__ == '__main__':
    configs = json.load(open('config.json'))
    routers = generate_ips()
    my_network = build_scheme(configs, routers)
    Network(my_network).rip()
