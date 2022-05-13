class Router:

    def __init__(self, name, neighbors):
        self.name = name
        self.neighbors = neighbors
        self.INF = 'INF'
        self.distance_table = {
            router: (1, router)
            for router in self.neighbors
        }

    def get_distance(self, key):
        if key in self.distance_table:
            return self.distance_table[key][0]
        return self.INF

    def update_distance_table(self, key, new_value, next_hop):
        if new_value != self.INF and (key not in self.distance_table or new_value + 1 < self.distance_table[key][0]):
            self.distance_table[key] = (new_value + 1, next_hop)
            return True
        return False

    def show_statistics(self):
        print(f'{"[Source IP]":25} {"[Destination IP]":25} {"[Next Hop]":25} {"Metric":25}')
        for dest_router in self.distance_table:
            print(f'{self.name:25} {dest_router:25} {self.distance_table[dest_router][1]:25} '
                  f'{str(self.distance_table[dest_router][0]):25}')
