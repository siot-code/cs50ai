import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
import degrees
import unittest

class TestDegrees(unittest.TestCase):
    def setUp(self):
        # Minimal mock data for testing
        degrees.people = {
            "1": {"name": "Alice", "birth": "1970", "movies": {"10"}},
            "2": {"name": "Bob", "birth": "1980", "movies": {"10"}},
            "3": {"name": "Charlie", "birth": "1990", "movies": {"20"}},
        }
        degrees.movies = {
            "10": {"title": "Test Movie", "year": "2000", "stars": {"1", "2"}},
            "20": {"title": "Other Movie", "year": "2005", "stars": {"3"}}
        }
        degrees.names = {"alice": {"1"}, "bob": {"2"}, "charlie": {"3"}}

    def test_neighbors_for_person(self):
        neighbors = degrees.neighbors_for_person("1")
        self.assertIn(("10", "2"), neighbors)
        self.assertNotIn(("10", "1"), neighbors)

    def test_person_id_for_name(self):
        self.assertEqual(degrees.person_id_for_name("Alice"), "1")
        self.assertEqual(degrees.person_id_for_name("Bob"), "2")
        self.assertIsNone(degrees.person_id_for_name("CharlieX"))

    def test_shortest_path_no_solution(self):
        # No connection between Alice (1) and Charlie (3)
        path = degrees.shortest_path("1", "3")
        self.assertIsNone(path)

    def test_shortest_path_solution_found(self):
        # Alice (1) and Bob (2) are connected via movie 10
        path = degrees.shortest_path("1", "2")
        self.assertEqual(path, [("10", "2")])

if __name__ == "__main__":
    unittest.main()