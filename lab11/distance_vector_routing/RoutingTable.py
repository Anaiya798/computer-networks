import Triple


class RoutingTable(object):
    def __init__(self, name):
        self.vector_list = []
        self.name = name

    def add_route(self, dest, length, first_hop):
        v = Triple.Triple(dest, length, first_hop)
        self.vector_list.append(v)

    def del_route(self, dest):
        try:
            v = self.get_vector(dest)
            self.vector_list.remove(v)
        except Exception:
            raise ValueError(f"Vector {dest} is not in list")

    def edit_route(self, dest, length, first_hop):
        v = self.get_vector(dest)
        v.dist = length
        v.first_hop = first_hop

    def contains(self, dest):
        for vector in self.vector_list:
            if vector.dest == dest:
                return True
        return False

    def get_vector(self, dest):
        for vector in self.vector_list:
            if vector.dest == dest:
                return vector
        return None

    def print_table(self):
        for vector in self.vector_list:
            print(vector.dest + " " + str(vector.dist) + " " + vector.first_hop)
