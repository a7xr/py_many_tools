# going to study testing with python
# to delete the commented_lines in python
# # sed -e '/^ *#/d' file001.py > file001_no_comments.py
#
# to delete the void lines
# # sed '/^$/d'

import unittest



from Tools.Print_Color import *
from Tools.Tools_MySQL import *


config = configparser.ConfigParser()
config.read('all_confs.txt')


class MongoDB_Test(unittest.TestCase):

    # MongoDB_Test
    def setUp(self):
        
        pass

    # MongoDB_Test
    def tearDown(self):
        pass

    def test_all_test_mongodb(unittest.TestCase):



        pass

    

class Print_Color_Test(unittest.TestCase):

    # Print_Color_Test
    def setUp(self):
        
        pass

    # Print_Color_Test
    def tearDown(self):        
        pass


    def test_print_green(self):

        self.assertEqual(
            1, Print_Color.print_blue()
        )

        pass





class MySQL_Test(unittest.TestCase):

    # MySQL_Test
    def setUp(self):
        self.server = config['mysql_localhost_db_s']['ip_host']
        self.user = config['mysql_localhost_db_s']['username']
        self.password = config['mysql_localhost_db_s']['password']
        self.database = config['mysql_localhost_db_s']['database']
        self.port = 3306
        
        self.mysql = MySQL()

        self.mysql.connect_db(
            server01 = self.server
            , user01 = self.user
            , password01 = self.password
            , database01 = self.database
            , port = self.port
            , log = False
        )

        pass

    # MySQL_Test
    def tearDown(self):

        self.mysql.db_not_select(
            query01 = "delete from torm where id < 2222222"
            , host = self.server
            , db = self.database
            , log_query = False
            , auto_commit = True
            , test001 = False
        )
        pass

    # 
    def test_mysql_test(self):
        # test connection to the database
        self.assertEqual(
            1, 
            self.mysql.connect_db(
                server01 = config['mysql_localhost_db_s']['ip_host']
                , user01 = config['mysql_localhost_db_s']['username']
                , password01 = config['mysql_localhost_db_s']['password']
                , database01 = config['mysql_localhost_db_s']['database']
                , port = config['mysql_localhost_db_s']['port']
                , log = False
            )
        )

        # test insertion to the database
        self.assertEqual(
            1,
            self.mysql.db_not_select(
                query01 = "insert into torm (txt) values ('55')"
                , host = self.server
                , db = self.database
                , log_query = False
                , auto_commit = True
                , test001 = False
            )
        )

        # test select from the database
        self.assertEqual(
            1
            , self.mysql.db_select(
                query01 = "select * from torm"
                , host = self.server
                , db = self.database
            )
        )

        # another testing from the database
        self.assertEqual(
            self.mysql.results_select_query[0][1]
            , ('55')
        )

        pass

if __name__ == "__main__":
    unittest.main()