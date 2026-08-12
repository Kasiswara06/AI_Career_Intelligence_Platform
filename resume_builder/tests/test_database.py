import unittest
from database.connection import get_connection

class TestDatabase(unittest.TestCase):
    def test_db_connection(self):
        conn, engine = get_connection()
        self.assertIsNotNone(conn)
        self.assertIn(engine, ["sqlite", "mysql"])

if __name__ == "__main__":
    unittest.main()
