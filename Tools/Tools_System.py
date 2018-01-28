from .Tools_MongoDb import MongoDb
import os

# hnw anle we izay zvt tafiditra any anaty MongoDb dia 
# # mba tsy tkn ao anaty System01 tsoon
# not sure if I have to do this
class Tools_System:
    def __init__(self):
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

    def set_file_to_mongodb(
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
        os.remove(path_file)
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