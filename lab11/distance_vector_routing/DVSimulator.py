import DVRouter


class DVSimulator:
    def __init__(self, file):
        self.routers = []
        self.split = False
        self.file = open(file, 'r')
        for line in self.file:
            info = line.split()
            if self.contain_router(info[0]) == False:
                new_router = DVRouter.DVRouter(info[0])
                self.routers.append(new_router)
            if self.contain_router(info[1]) == False:
                new_router = DVRouter.DVRouter(info[1])
                self.routers.append(new_router)
            for router in self.routers:
                if router.name == info[0]:
                    router.add_link(info[1], float(info[2]))
                elif router.name == info[1]:
                    router.add_link(info[0], float(info[2]))

    def run_simulation(self):
        run_again = True
        iteration = 1
        while run_again:
            print("Iteration " + str(iteration))
            iteration += 1
            run_again = False
            router_tables = self.collect_tables()
            self.print_routers()
            for router in self.routers:
                if router.update_routes(router_tables) == True:
                    run_again = True
            print('====\n\n')

    def collect_tables(self):
        router_tables = []
        for router in self.routers:
            router_tables.append(router.export())
        return router_tables

    def contain_router(self, name):
        for router in self.routers:
            if router.name == name:
                return True
        return False

    def get_router(self, name):
        for router in self.routers:
            if router.name == name:
                return router
        return None

    def dist(self, x, y):
        router = self.get_router(x)
        if router.export().contains(y):
            return float(router.export().get_vector(y).dist)
        else:
            return float('inf')

    def print_routers(self):
        for router in self.routers:
            print("Router: " + router.name)
            router.print_table()


if __name__ == '__main__':
    simulator = DVSimulator("network.txt")
    simulator.run_simulation()
