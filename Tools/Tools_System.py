from .Tools_MongoDb import MongoDb
from .Tools_Basic import Tools_Basic
import os

# hnw anle we izay zvt tafiditra any anaty MongoDb dia 
# # mba tsy tkn ao anaty System01 tsoon
# not sure if I have to do this
class Tools_System:
    def __init__(self):
        pass

    @staticmethod
    def run_file(
        file_to_run = "../file001.py"
    ):
        # there are multiple ways to run a python_script
        # # at this time, this is going to use "os.system(...) Only"
        if (os.path.exists(file_to_run)):
            os.system(
                file_to_run
            )
        else:
            input(file_to_run + " is Missing")
        # input(str(file_to_run) + " has run")
        pass

    @staticmethod
    def create_file(
        path_system = "E:\DEV\python\ted_transcript\file001.txt"
    ):
        
        pass

    @staticmethod
    def create_folder(
        path_system = "E:\DEV\python\ted_transcript"
    ):
        if not os.path.exists(path_system):
            os.makedirs(path_system)
        pass

    # TODO going to insert a whole folder into mongodb
    def insert_folder(
        self
        , walk_dir = 'E:\\New folder\\New folder\\'
    ):
        # I can use Tools_Basic.crawl_into_folder
        # # but it is going to run to many loops
        for root, subdirs, files in os.walk(walk_dir):
            for filename in files:
                path_file = os.path.join(root, filename)
                # print("path_file.rsplit('.', 1)[1]: ", path_file.rsplit('.', 1)[1])
                # # mp3
                self.mongodb.action_not_select(
                    action = 'insert_file'
                    , collection = 'file_inserted'
                    , doc_of_file_or__not_file = {
                        'path_file_origin': path_file
                        , 'type': path_file.rsplit('.', 1)[1]
                    }
                )
                print('(full path: %s)' % (path_file))
        pass

    def connect_to_db(
        self
        , server01 = 'localhost'
        , database = 'db001'
        , port01 = 27017
    ):
        self.mongodb = MongoDb()
        self.mongodb.connection(
            server01 = 'localhost'
            , database = 'db001'
            , port01 = 27017
        )
        pass

    def __init__(self):
        self.connect_to_db()
        pass

    def set_file_to_mongodb__del_in_sys(
        self
        , path_file = r'e:\disk_part.txt'
        , type001 = 'text'
    ):
        # apdirina any anaty mongodb ny path_file
        # supprimena anaty System01 ny path_file

        self.mongodb.action_not_select(
            action = 'insert_file'
            , collection = 'file_inserted'
            , doc_of_file_or__not_file = {
                'path_file_origin': path_file
                , 'type': type001
            }
        )
        try:
            os.remove(path_file)
        except PermissionError as err:
            print()
            print ('The file('+ str(path_file) +') which you wanted to insert then delete into System is in use by another Program')
            return
        print(path_file, ' has been removed')
        pass

    def get_file_from_mongodb(
        self
        , patt_file_to_search = 'disk_part'
        , output_folder_for_file = r'e:\\'
    ):
        self.mongodb.action_select(
            action = 'find_file'
            , doc_of_file_or__not_file = {
                'file_name_origin' : {
                    '$regex': '.*'+ patt_file_to_search +'.*'
                }
            }
            , output_folder_for_file = output_folder_for_file
        )
        print('File containing('+ patt_file_to_search +') have been extracted _ 345DFGHQF3456QZERT')
        pass