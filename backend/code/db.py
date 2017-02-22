# -*- coding: utf-8 -*-
import csv
import pymysql

class MYSQL:
    def __init__(self):
        self.connection = pymysql.connect(host="localhost", user="root", passwd="", db="eps")

    def __del__(self):
        self.connection.close()

    def exec_sql(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            self.connection.commit()
            return cursor.fetchall()

    def generate_table_structure_from_csv(self, path):
        '''
        Generate db table structure from a csv file
        Output should be like :
        `Death Date` TEXT,`Death Time` TEXT,`Manner of Death` TEXT
        By default, all columes are TEXT
        :return:
        '''
        with open(path, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            first_line = spamreader.next()
        if not first_line:
            return

        sql = ""
        for col in first_line:
            sql += "`" + col[1:-1] + "` TEXT,"
        sql = sql[:-1]
        return sql

    def create_tables(self, path):
        structure = self.generate_table_structure_from_csv(path)
        sql_db1 = """drop table if exists `{0}`;
              create table `{0}` ({1});
              """.format("db1", structure)
        self.exec_sql(sql_db1)

        sql_db2 = """drop table if exists `{0}`;
              create table `{0}` ({1});
              """.format("db2", structure)
        self.exec_sql(sql_db2)

    def import_csv(self, path):
        sql = "load data local infile '{0}' into table {1} columns terminated by ','"\
        "LINES TERMINATED BY '\n' IGNORE 1 LINES;".format(path, "db1")
        self.exec_sql(sql)

