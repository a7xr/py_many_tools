# going to study testing with python
# to delete the commented_lines in python
# # sed -e '/^ *#/d' file001.py > file001_no_comments.py
#
# to delete the void lines
# # sed '/^$/d'

import unittest



from Tools.Print_Color import *
from Tools.Tools_MySQL import *
from Tools.Tools_MongoDb import *


config = configparser.ConfigParser()
config.read('all_confs.txt')



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



class MongoDB_Test(unittest.TestCase):

    # MongoDB_Test
    def setUp(self):
        self.mongodb_server = config["mongo_l"]["ip_host"]
        self.mongodb_database = config["mongo_l"]["database"]
        self.mongodb_port = config["mongo_l"]["port"]

        self.mongodb = MongoDb()
        
        pass

    # MongoDB_Test
    def tearDown(self):

        input("Going to delete all documents in collection(person)")
        self.mongodb.local_db001.get_collection('person')\
            .delete_many(
                {
                    '_id': {
                        '$gt': 0
                    }
                }
            )

        pass

    def test_all_test_mongodb(self):
        # do not know how to set the file_test.py into a folder yet

        # testing the connection
        self.assertEqual(
            1
            , self.mongodb.connection()
        )

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
        self.assertEqual(
            self.mongodb.action_select_not_file(
                collection = 'person'
                , print_only = True

                , json_filter = {
                    'name': 'name001'
                }
            )
            , self.mongodb.results_select_mongo
        )

        pass

    






if __name__ == "__main__":
    unittest.main()