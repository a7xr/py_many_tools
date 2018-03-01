# going to study testing with python

import unittest



from Tools.Print_Color import *
from Tools.Tools_MySQL import *


config = configparser.ConfigParser()
config.read('all_confs.txt')


class Print_Color_Test(unittest.TestCase):

    def setUp(self):
        
        pass
    
    def test_print_green(self):

        self.assertEqual(
            1, Print_Color.print_blue()
        )

        pass





class MySQL_Test(unittest.TestCase):
    
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
    
    def tearDown(self):

        last_inserted = self.mysql.db_not_select(
            query01 = "insert into torm (txt) values ('55')"
            , host = self.server
            , db = self.database
            , log_query = False
            , auto_commit = True
            , test001 = False
        )

        last_inserted_torm = self.mysql.db_select(
            query01 = "select id from torm where id = last_insert_id()"
            , host = self.server
            , db = self.database
        )

        print ('last_inserted_torm: ', last_inserted_torm)
        pass

    def test_db_select(self):
        self.assertEqual(
            1, 
            self.mysql.db_select(
                query01 = "select * from torm"
                , host = config['mysql_localhost_db_s']['ip_host']
                , db = config['mysql_localhost_db_s']['database']
            )
        )
        pass

    def test_connect_db(self):
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
        pass

    def test_insert_db(self):
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
        pass

if __name__ == "__main__":
    unittest.main()