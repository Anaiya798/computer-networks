
class TestTriple(unittest.TestCase):
    def test_create(self):
        triple1 = Triple.Triple('C', 1.2, 'B')
        self.assertEqual('C', triple1.dest)
        self.assertEqual(1.2, triple1.dist)
        self.assertEqual('B', triple1.first_hop)
        triple2 = Triple.Triple('D', 2.5, 'B')
        self.assertEqual('D', triple2.dest)
        self.assertEqual(2.5, triple2.dist)
        self.assertEqual('B', triple2.first_hop)
        triple3 = Triple.Triple('C', 3.4, 'A')
        self.assertEqual('C', triple3.dest)
        self.assertEqual(3.4, triple3.dist)
        self.assertEqual('A', triple3.first_hop)


if __name__ == "__main__":
    unittest.main()