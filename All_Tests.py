# going to study testing with python
# to delete the commented_lines in python
# # sed -e '/^ *#/d' file001.py > file001_no_comments.py
#
# to delete the void lines
# # sed '/^$/d'



import unittest
import os
import pprint
import sys
sys.path.append("..")

from Tools.Tools_Basic import *
from Tools.Print_Color import *
from Tools.Tools_MySQL import *
from Tools.Tools_MongoDb import *
from Tools.Tools_Win32 import *
from Tools.Tools_SQLite import *


config = configparser.ConfigParser()
config.read('all_confs.txt')


# class SQLite_Test(unittest.TestCase):

#     def setUp(self):
#         self.sqlite = Tools_SQLite()
#         self.sqlite.connect_db(
#             file_db = config['sqlite']['file_sqlite']
#         )
#         pass

#     def tearDown(self):
#         self.sqlite.action_not_select(
#             query = "delete from table001"
#         )
#         print('deleted all content of table(table001)')

#         self.sqlite.disconnect_db()

#         pass

#     def test_all_sqlite_test(self):
#         # going to test for the connection
#         self.assertIsNotNone(
#             self.sqlite.connection
#         )

#         # going to test the insertion into the database
#         self.assertEqual(
#             1,
#             self.sqlite.action_not_select(
#                 query = 'insert into table001 (txt) values ("test")'
#             )
#         )

#         # test select into the database
#         # # you should take the result of your query inside "self.sqlite.cursor_sqlite"
#         self.assertEqual(
#             1,
#             self.sqlite.action_select(
#                 query = 'select * from table001'
#             )
#         )

#         print(self.sqlite.res_query_select)
#         self.assertEqual(
#             [('test', )],   # you have to understand 
#                             # # when you are going to select a row from sqlite3, it have to be similar that that result
#             self.sqlite.res_query_select
#         )


#         # test update
#         self.assertEqual(
#             1,
#             self.sqlite.action_not_select(
#                 query = 'update table001 set txt = "testing the update"'
#             )
#         )

#         # NOT A TEST, 
#         self.sqlite.action_not_select(
#             query = 'insert into table001(txt) values ("val001"), ("val002"), ("val003"), ("val004"), ("val005"), ("val006"), ("val007"), ("val008"), ("val009");'
#         )
#         self.assertEqual(
#             1,
#             self.sqlite.action_not_select(
#                 query = 'delete from table001 where txt like "val006"'
#             )
#         )
#         self.sqlite.action_select(
#             query = 'select * from table001'
#         )


#         # for a in self.sqlite.res_query_select:
#         #     print(a)

#         self.assertNotIn(
#             ('val006', )
#             , self.sqlite.res_query_select
#         )

#         self.assertIn(
#             ('val005', )
#             , self.sqlite.res_query_select
#         )

        # self.assertEqual()

        # going to test the insertion into the database
        # self.assertEqual(
        #     1,
        #     self.sqlite.action_select(
        #         query = 'select * from table001 where '
        #     )
        # )


#end_class__SQLite_Test


# class Win32_Test(unittest.TestCase):

#     def test_win32(self):
#         self.assertEqual(
#             'windows010'
#             , Tools_Win32().get_username()
#         )

#     pass

#end_class__Win32_Test


# class Print_Color_Test(unittest.TestCase):

#     # Print_Color_Test
#     def setUp(self):
        
#         pass

#     # Print_Color_Test
#     def tearDown(self):        
#         pass


#     def test_print_green(self):

#         self.assertEqual(
#             1, Print_Color.print_blue()
#         )

#         pass

#end_class__Print_Color_Test



# class MySQL_Test(unittest.TestCase):

#     # MySQL_Test
#     def setUp(self):
#         self.server_mysql = config['mysql_localhost_db_s']['ip_host']
#         self.user = config['mysql_localhost_db_s']['username']
#         self.password_mysql = config['mysql_localhost_db_s']['password']
#         self.database_mysql = config['mysql_localhost_db_s']['database']
#         self.port_mysql = 3306

#         self.mysql = MySQL()

#         self.mysql.connect_db(
#             server01 = self.server_mysql
#             , user01 = self.user
#             , password01 = self.password_mysql
#             , database01 = self.database_mysql
#             , port = self.port_mysql
#             , log = False
#         )

#         pass

#     # MySQL_Test
#     def tearDown(self):

#         self.mysql.db_not_select(
#             query01 = "delete from torm where id < 2222222"
#             , host = self.server_mysql
#             , db = self.database_mysql
#             , log_query = False
#             , auto_commit = True
#             , test001 = False
#         )
#         pass

#     # 
#     def test_mysql_test(self):
#         # test connection to the database
#         # self.assertEqual(
#         #     1, 
#         #     self.mysql.connect_db(
#         #         server01 = config['mysql_localhost_db_s']['ip_host']
#         #         , user01 = config['mysql_localhost_db_s']['username']
#         #         , password01 = config['mysql_localhost_db_s']['password']
#         #         , database01 = config['mysql_localhost_db_s']['database']
#         #         , port = config['mysql_localhost_db_s']['port']
#         #         , log = False
#         #     )
#         # )

#         # # test insertion to the database
#         self.assertEqual(
#             1,
#             self.mysql.db_not_select(
#                 query01 = "insert into torm (txt) values ('55')"
#                 , host = self.server_mysql
#                 , db = self.database_mysql
#                 , log_query = False
#                 , auto_commit = True
#                 , test001 = False
#             )
#         )

#         # test select from the database
#         self.assertEqual(
#             1
#             , self.mysql.db_select(
#                 query01 = "select * from torm"
#                 , host = self.server_mysql
#                 , db = self.database_mysql
#             )
#         )

#         # another testing from the database
#         self.assertEqual(
#             self.mysql.results_select_query[0][1]
#             , ('55')
#         )

#         pass

# end__class__MySQL_Test




class MongoDB_Test(unittest.TestCase):


    # # otrn tsis ilaivan anreto aa
    # def test_run_server(self):
    #     self.assertEqual(
    #         1,
    #         self.mongodb.run_one_server()
    #     )

    # def test_kill_all_servers(self):
    #     self.assertEqual(
    #         1,
    #         self.mongodb.kill_all_servers()
    #     )

    # MongoDB_Test
    def setUp(self):

        self.mongodb_server = config["mongo_l"]["ip_host"]
        self.mongodb_database = config["mongo_l"]["database"]
        self.mongodb_port = config["mongo_l"]["port"]

        self.mongodb = MongoDb()
        self.mongodb.run_one_server()
        self.mongodb.connection()
        Tools_Basic.long_print()
        pass

    # MongoDB_Test
    def tearDown(self):
        Tools_Basic.long_print()
        input("Going to delete all documents in collection(person)")
        self.mongodb.local_db001.get_collection('person')\
            .delete_many(
                {
                    '_id': {
                        '$gt': 0
                    }
                }
            )
        self.mongodb.kill_all_servers()
        pass

    def test_all_test_mongodb(self):
        # do not know how to set the file_test.py into a folder yet




        # # repairing the server when you deleted some files into the database
        # # # so that the files you deleted are not in the register anymore
        # self.assertEqual(
        #     1,
        #     self.mongodb.repair_server()
        # )

        # testing the connection
        # # should be commented, otherwise, ther is a second_connection
        # self.assertEqual(
        #     1
        #     , self.mongodb.connection()
        # )

        # test insert_not_file into the database
        # # all the documents which are going to be inserted in collection(person) will be deleted by tearDown
        self.assertEqual(
            1
            , self.mongodb.action_not_select(
                server = 'localhost'
                , database = 'db001'
                , collection = 'person'
                , action = 'insert_not_file'
                , _id = 1
                , doc_of_file_or__not_file = {  # be careful when inserting file01, this has to has keys(path_file_origin, uid, file_name_origin)
                    'name': 'name001'
                }
            )
        )

        # test select_not_file
        # # this is going to be done in 2steps
        # # # we are going to set the query and the result is going to be set into "self.mongodb.results_select_mongodb
        # # # we take the result of the query inside "self.mongodb.results_select_mongodb"
        self.assertEqual(
            self.mongodb.action_select_not_file(
                collection = 'person'
                , print_only = True

                , json_filter = {
                    'name': 'name001'
                }
            )
            , 1
            # , self.mongodb.results_select_mongodb     # <<<<<<<<<<<<<<< after doing a select_not_file in mongo,
                                                    # # you should grab the result in self.mongodb.results_select_mongodb
        )
        self.assertEqual(
            [{'_id': 1, 'name': 'name001'}]
            , self.mongodb.results_select_mongodb
        )

        # test insert_file into mongodb
        # self.assertEqual(
        #     1,
        #     self.mongodb.action_not_select(
        #         action = 'insert_file'
        #         , collection = 'inserted_files'
        #         , doc_of_file_or__not_file = {
        #             'path_file_origin': 'g:\\michel.txt'
        #             , 'name_to_store_in_db': "m001.txt"
        #             , 'insertion_type': 'python'
        #         }
        #     )
        # )
        #
        #
        # aleo averina amboarina mitsn n mnw insertion fichier







        # inserting file inside mongo
        self.assertEqual(
            1,
            self.mongodb.insert_file(
                path_file = 'g:\\michel.txt'
                , name_to_store_in_register = 'm001.txt'
            )
        )

        # deleting file inside the mongodb
        self.assertEqual(
            1,
            self.mongodb.delete_file()
        )

        # downloading file from mongo
        self.mongodb.get_file()
        self.assertTrue(
            os.path.exists(
                self.mongodb.store_dldd_file + "m001.txt"
            )
        )









        pass
# end_class__MongoDB_Test
    






if __name__ == "__main__":
    unittest.main()