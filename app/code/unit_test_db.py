import unittest
import db


class TestDbMethods(unittest.TestCase):
    def test_connection(self):
        mysql = db.Mysql()
        self.assertIsNotNone(mysql)
        self.assertIsNotNone(mysql.connection)

    def test_exec_sql(self):
        mysql = db.Mysql()
        self.assertTrue(mysql.exec_sql("show databases"))
        self.assertTrue(mysql.exec_sql("show tables"))

    def test_generate_table_exec_sql(self):
        mysql = db.Mysql()
        csv_path = "/dataset/origin.csv"
        mysql.create_table(csv_path, "test_db")
        self.assertTrue(("test_db",) in mysql.exec_sql("show tables"))
        self.assertFalse(mysql.exec_sql("drop table test_db"))

    def test_import_csv(self):
        mysql = db.Mysql()
        csv_path = "/dataset/origin.csv"
        mysql.create_table(csv_path, "test_db")
        mysql.import_csv(csv_path, "test_db")
        self.assertNotEqual(len(mysql.exec_sql("SELECT count(*) from test_db limit 10;")), 0)
        self.assertFalse(mysql.exec_sql("drop table test_db"))

if __name__ == '__main__':
    unittest.main()
