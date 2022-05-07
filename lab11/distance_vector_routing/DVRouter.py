import RoutingTable


class DVRouter:
    def __init__(self, name):
        self.name = name
        self.route_table = RoutingTable.RoutingTable(name)
        self.links = {}
        self.add_link(name, 0)

    def export(self):
        return self.route_table

    def update_routes(self, neighbor_tables):
        return_value = False

        for neighbor_table in neighbor_tables:
            if neighbor_table.name in self.links:
                for vector in neighbor_table.vector_list:
                    new_dist = vector.dist + self.route_table.get_vector(neighbor_table.name).dist
                    if self.route_table.contains(vector.dest):
                        if new_dist < self.route_table.get_vector(vector.dest).dist:
                            self.route_table.edit_route(vector.dest, new_dist, neighbor_table.name)
                            return_value = True
                    else:
                        self.route_table.add_route(vector.dest, new_dist, neighbor_table.name)
                        return_value = True
        return return_value

    def add_link(self, router_name, dist):
        self.links[router_name] = dist
        self.route_table.add_route(router_name, dist, router_name)

    def remove_link(self, router_name):
        del self.links[router_name]
        v = self.route_table.get_vector(router_name)
        if v.first_hop == router_name:
            self.route_table.del_route(router_name)

    def print_table(self):
        self.route_table.print_table()
