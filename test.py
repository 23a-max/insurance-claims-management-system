
import os
import sqlite3
import tempfile
import unittest

import database


class TestInsuranceDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_db = database.DATABASE_NAME
        database.DATABASE_NAME = os.path.join(
            self.temp_dir.name, "test.db"
        )
        database.create_tables()

    def tearDown(self):
        database.DATABASE_NAME = self.original_db
        self.temp_dir.cleanup()

    def test_claim_table_exists(self):
        with database.get_connection() as connection:
            result = connection.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type = 'table' AND name = 'claims'
                """
            ).fetchone()

        self.assertIsNotNone(result)

    def test_claim_registration(self):
        with database.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO claims
                (customer_name, policy_number, claim_amount, description)
                VALUES (?, ?, ?, ?)
                """,
                ("Test Customer", "POL1001", 5000, "Vehicle damage"),
            )

            claim = connection.execute(
                "SELECT * FROM claims WHERE policy_number = ?",
                ("POL1001",),
            ).fetchone()

        self.assertIsNotNone(claim)
        self.assertEqual(claim["customer_name"], "Test Customer")
        self.assertEqual(claim["status"], "Submitted")

    def test_negative_claim_amount_is_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            with database.get_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO claims
                    (customer_name, policy_number, claim_amount, description)
                    VALUES (?, ?, ?, ?)
                    """,
                    ("Test Customer", "POL1002", -100, "Invalid claim"),
                )


if __name__ == "__main__":
    unittest.main()
