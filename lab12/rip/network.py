class Network:

    def __init__(self, routers):
        self.routers = routers

    def rip(self):
        step = 0
        changed = True
        while changed:
            step += 1
            changed = False
            for source_router in self.routers:
                for dest_router in self.routers:
                    if source_router.name == dest_router.name:
                        continue
                    for next_router in source_router.neighbors:
                        changed |= source_router.update_distance_table(
                            dest_router.name,
                            dest_router.get_distance(next_router),
                            next_router
                        )
                print(f'Simulation step {step} of router {source_router.name}:')
                source_router.show_statistics()
                print()
            for router in self.routers:
                print(f'Final state of router {router.name}:')
                router.show_statistics()
                print()
