import unittest
import DVRouter


class Test(unittest.TestCase):

    def test_add_link(self):
        router_1 = DVRouter.DVRouter('B')
        router_1.add_link('C', 1.2)
        router_1.add_link('A', 2.3)
        self.assertTrue('C' in router_1.links)
        self.assertTrue(router_1.route_table.contains('C'))
        self.assertTrue('A' in router_1.links)
        self.assertTrue(router_1.route_table.contains('A'))

    def test_remove_link(self):
        router_1 = DVRouter.DVRouter('B')
        router_1.add_link('C', 1.2)
        router_1.add_link('A', 2.3)
        self.assertTrue('C' in router_1.links)
        self.assertTrue(router_1.route_table.contains('C'))
        self.assertTrue('A' in router_1.links)
        self.assertTrue(router_1.route_table.contains('A'))
        router_1.remove_link('C')
        self.assertFalse('C' in router_1.links)
        self.assertFalse(router_1.route_table.contains('C'))
        router_1.remove_link('A')
        self.assertFalse('A' in router_1.links)
        self.assertFalse(router_1.route_table.contains('A'))

    def test_export(self):
        router_1 = DVRouter.DVRouter('B')
        router_1.add_link('C', 1.2)
        router_1.add_link('A', 2.3)
        router_2 = DVRouter.DVRouter('C')
        router_2.add_link('B', 1.6)
        router_2.add_link('A', 2.5)
        router_3 = DVRouter.DVRouter('D')
        router_3.add_link('C', 1.6)
        table = router_1.export()
        self.assertEqual(table, router_1.route_table)
        table1 = router_2.export()
        self.assertEqual(table1, router_2.route_table)
        table2 = router_3.export()
        self.assertEqual(table2, router_3.route_table)

    def test_update(self):
        router_1 = DVRouter.DVRouter('A')
        router_1.add_link('B', 1.5)
        router_1.add_link('C', 1.2)
        router_2 = DVRouter.DVRouter('B')
        router_2.add_link('C', 1.0)
        router_2.add_link('A', 1.5)
        router_2.add_link('D', 1.3)
        router_3 = DVRouter.DVRouter('C')
        router_3.add_link('A', 1.2)
        router_3.add_link('B', 1.0)
        router_4 = DVRouter.DVRouter('D')
        router_4.add_link('B', 1.3)
        router_1.update_routes([router_2.export(), router_3.export()])
        self.assertTrue(router_1.route_table.contains('D'))
        self.assertTrue(router_1.route_table.get_vector('D').dist == 2.8)
        self.assertTrue(router_1.route_table.get_vector('D').first_hop == 'B')
        self.assertTrue(router_1.route_table.get_vector('B').dist == 1.5)
        self.assertTrue(router_1.route_table.get_vector('C').dist == 1.2)
        self.assertTrue(router_1.route_table.get_vector('A').dist == 0)
        router_2.update_routes([router_1.export(), router_3.export()])
        self.assertTrue(router_2.route_table.get_vector('D').dist == 1.3)
        self.assertTrue(router_2.route_table.get_vector('A').dist == 1.5)
        self.assertTrue(router_2.route_table.get_vector('B').dist == 0)
        self.assertTrue(router_2.route_table.get_vector('C').dist == 1.0)


if __name__ == "__main__":
    unittest.main()
