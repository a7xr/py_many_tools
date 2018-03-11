# going to study testing with python
# to delete the commented_lines in python
# # sed -e '/^ *#/d' file001.py > file001_no_comments.py
#
# to delete the void lines
# # sed '/^$/d'



import unittest
import os
import pprint

from Tools.Tools_Basic import *
from Tools.Print_Color import *
from Tools.Tools_MySQL import *
from Tools.Tools_MongoDb import *
from Tools.Tools_Win32 import *


config = configparser.ConfigParser()
config.read('all_confs.txt')


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
#         self.assertEqual(
#             1, 
#             self.mysql.connect_db(
#                 server01 = config['mysql_localhost_db_s']['ip_host']
#                 , user01 = config['mysql_localhost_db_s']['username']
#                 , password01 = config['mysql_localhost_db_s']['password']
#                 , database01 = config['mysql_localhost_db_s']['database']
#                 , port = config['mysql_localhost_db_s']['port']
#                 , log = False
#             )
#         )

#         # test insertion to the database
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
# 
#end__class__MySQL_Test




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
        self.assertEqual(
            1,
            self.mongodb.action_not_select(
                action = 'insert_file'
                , collection = 'file_inserted'
                , _id = 'file001'
                , doc_of_file_or__not_file = {
                    'path_file_origin': 'g:\\michel.txt'
                    , 'name_to_store_in_db': "m001.txt"
                    , 'type' : 'audio_music'
                    , 'insertion_type': "mongofiles"
                }
            )
        )

        # test delete_file into mongodb
        self.assertEqual(
            1,
            self.mongodb.action_not_select(
                action = 'delete_file'
                , collection = 'file_inserted'
                , _id = 'file001'
                , doc_of_file_or__not_file = {
                    'name_stored_in_db': "m001.txt"
                    , 'insertion_type': "mongofiles"
                    , 'deletion_type': "mongofiles"
                    , 'name_stored_in_db': "m001.txt"
                }
            )
        )


        # test delete_file into mongodb
        # self.assertEqual(
        #     1,
        #     self.mongodb.action_not_select(
        #         action = 'delete_file'
        #         , collection = 'file_inserted'
        #         , _id = 'file001'
        #         , doc_of_file_or__not_file = {
        #             'file_name_origin': 'a.mp3'
        #             , 'type' : 'audio_music'
        #         }
        #     )
        # )


        pass
#end_class__MongoDB_Test
    






if __name__ == "__main__":
    unittest.main()
    # os.system(r"C:\Program Files\MongoDB\Server\3.4\bin\mongod.exe --dbpath G:\mongo_data\test002 --port 5566")

    # a = subprocess.Popen([r'C:\Program Files\MongoDB\Server\3.4\bin\mongod.exe', "--dbpath", r'G:\mongo_data\test001', '--port', '5566'])
    # MongoDb().run_one_server()
    # MongoDb().kill_all_servers()
    # print('killed')