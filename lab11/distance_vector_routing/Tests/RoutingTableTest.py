import unittest
import RoutingTable


class Test(unittest.TestCase):

    def test_add(self):
        route_table = RoutingTable.RoutingTable('A')
        route_table.add_route('C', 1.2, 'B')
        self.assertEqual(True, route_table.contains('C'))
        route_table.add_route('D', 1.4, 'B')
        self.assertEqual(True, route_table.contains('D'))
        route_table.add_route('E', 1.6, 'C')
        self.assertEqual(True, route_table.contains('E'))
        self.assertEqual(False, route_table.contains('F'))

    def test_edit(self):
        route_table = RoutingTable.RoutingTable('A')
        route_table.add_route('C', 1.2, 'B')
        route_table.add_route('D', 1.4, 'B')
        route_table.add_route('E', 1.6, 'C')
        route_table.edit_route('C', 1.4, 'E')
        self.assertFalse(route_table.get_vector('C').dist == 1.2)
        self.assertEqual(route_table.get_vector('C').dist, 1.4)
        route_table.edit_route('D', 2.3, 'E')
        self.assertFalse(route_table.get_vector('D').dist == 1.4)
        self.assertEqual(route_table.get_vector('D').dist, 2.3)
        route_table.edit_route('E', 1.1, 'D')
        self.assertFalse(route_table.get_vector('E').dist == 1.6)
        self.assertEqual(route_table.get_vector('E').dist, 1.1)

    def testDel(self):
        route_table = RoutingTable.RoutingTable('A')
        route_table.add_route('C', 1.2, 'B')
        route_table.add_route('D', 1.4, 'B')
        route_table.add_route('E', 1.6, 'C')
        self.assertEqual(True, route_table.contains('C'))
        route_table.del_route('C')
        self.assertFalse(route_table.contains('C'))
        route_table.del_route('D')
        self.assertFalse(route_table.contains('D'))
        route_table.del_route('E')
        self.assertFalse(route_table.contains('E'))


if __name__ == "__main__":
    unittest.main()
