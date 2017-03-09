# -*- coding: utf-8 -*-
import csv
import pymysql

''' Usage

mysql = Mysql()
mysql.create_table(csv_path, db_name)
mysql.import_csv(csv_path, db_name)

'''


class Mysql:
    def __init__(self):
        self.connection = pymysql.connect(host="db", user="root", passwd="", db="eps", local_infile=True)

    def __del__(self):
        self.connection.close()

    def exec_sql(self, sql):
        '''
        Execute the sql
        :param sql:
        :return: the result if any
        '''
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            self.connection.commit()
            return cursor.fetchall()

    def __generate_table_structure_from_csv(self, path):
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

    def create_table(self, path, db_name):
        '''
        Create database table from the csv file in path
        :param path:
        :param db_name:
        :return:
        '''
        structure = self.__generate_table_structure_from_csv(path)
        sql_create_table = """drop table if exists `{0}`;
              create table `{0}` ({1});""".format(db_name, structure)
        self.exec_sql(sql_create_table)


    def import_csv(self, path, db_name):
        '''
        Import the csv file in path to the database db_name
        :param path:
        :param db_name:
        :return:
        '''
        sql = "load data local infile '{0}' into table {1} columns terminated by ','"\
        "LINES TERMINATED BY '\n' IGNORE 1 LINES;".format(path, db_name)
        self.exec_sql(sql)
