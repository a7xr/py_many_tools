
import sys
import pymongo
import gridfs
import bson
from bson.objectid import ObjectId
import re
import os

from .Print_Color import Print_Color

class MongoDb:

    def __del__(self):
        print ('Object MongoDb destroyed')

    def connection(
        self
        , server01 = 'localhost'
        , database = 'db001'
        , port01 = 27017
    ):
        # print ('server: ', server01, ' database: ', database, 'port: ', port01)
        if(server01 == 'localhost'):
            if(database == 'db001'):
                if(port01 == 27017):
                    user_name = 'admin'
                    password = 'admin'
                    server = '127.0.0.1'
                    uri = "mongodb://" + user_name + ":" + password + "@" + server
                    # self.connect_server_localhost = pymongo.MongoClient(server01, port01)
                    self.connect_server_localhost = pymongo.MongoClient(uri)                    
                    print ('Connected from URI('+uri+')')
                    self.local_db001 = self.connect_server_localhost.db001
                    # print('Connected to db(' + database + ') at server('+ server01 +') _ code6356745473')
                    
                    # print (type(self.connect_server_localhost.db001))
                    # # <class 'pymongo.database.Database'>

                    self.fs_loc_db001 = gridfs.GridFS(self.local_db001)
                else: # only the port is NOT ok
                    print('Server OK: ', server01)
                    print('Database OK: ', database)

                    Print_Color.print_red(
                        txt = 'Port is NOT valid: port = ' + str(port01)
                    )
            else:   # the database01 is NOT ok
                Print_Color.print_red(
                    txt = 'Database is NOT valid: port = ' + str(port01)
                )
                pass
        else:
            Print_Color.print_red(
                txt = 'Server is NOT valid: port = ' + str(port01)
            )
            pass

    def action_select(
        self
        , server = 'localhost'
        , database = 'db001'
        , collection = 'person'
        , action = 'find_not_file'
        , port = 27017
        , doc = {
            'alias': 'alias001',
            'phone': 'phone001'
        }
        , patt_to_search_in_file_name = 'eclipse'
        , output_folder_for_file = "e:\\to_del\\"
    ):
        res_query = None
        res = []
        if (server == 'localhost'):
            if(database == 'db001'):
                try:
                    self.connect_server_localhost

                except AttributeError:
                    self.connection(
                        server01 = server
                        , database = database
                        , port01 = 27017
                    )

                list_collection = self.local_db001.collection_names()

                if (collection not in list_collection):
                    print('Collection (' +collection+ ') is NOT in the list_of_collection ')
                    return

                if(action == 'find_not_file'):
                    res_query = self.local_db001.get_collection(collection).find(
                        doc_of_file_or__not_file
                    )
                    for doc01 in res_query:
                        res.append(doc01)
                        return res
                    pass
                elif(
                    (action == 'find_file')
                ):
                    collection = 'file_inserted'
                    # list_files_inserted__from_reg_file_name \
                    regex001 = '.*' + patt_to_search_in_file_name + '.*'
                    # res_query \
                    res_query__files_info \
                        = self.local_db001.get_collection(collection).find({
                            'file_name_origin': {'$regex': 
                                str(regex001)
                                # {str(regex001)}
                                , '$options':'i'
                            }
                        })
                    # print('res_query: ', res_query)
                    # # <pymongo.cursor.Cursor object at 0x000002289D165F60>

                    i = 0
                    for f in res_query__files_info:
                        # print ('type(f): ', type(f))
                        # # <class 'dict'>
                        # print (f['uid'])
                        # # 59f4870fe97cac22f86e00de
                        # print('f (', i, '): ' , f)
                        # # f ( 0 ):  {'_id': ObjectId('5a6d37912b299517cca02ccd'), 'path_file_origin': 'E:\\tsiakoraka\\Ravin taratasy Tsiakoraka.mp4', 'uid': ObjectId('5a6d37902b299517cca02c9c'), 'file_name_origin': 'Ravin taratasy Tsiakoraka.mp4', 'type': 'mp4'}
                        i += 1
                        grid_file = self.fs_loc_db001.get(
                            ObjectId(str(f['uid']))
                        )
                        # print("f['path_file_origin'].rsplit('\\', 1)[1]: ", f['path_file_origin'].rsplit('\\', 1)[1])
                        # # msg_41.txt
                        file_target_name = output_folder_for_file + f['path_file_origin'].rsplit('\\', 1)[1]
                        file_target = open(
                            file_target_name
                            , 'wb'
                        )
                        file_target.write(grid_file.read())
                        file_target.close()

                        print('The output of your file is saved to: ', file_target_name)
                        # print ('dict01: ', dict01)
                        # # <gridfs.grid_file.GridOut object at 0x0000028120D249E8>
                    
                else: # the action is unknown
                    pass
                pass
            else: # the database is unknown
                pass
        else: # the server is unknown
            pass
        pass

    def exe(
        self
        , like_appli_name = 'vlc'
        , file_to_exe = ''
    ):

        pass

    def action_not_select(
        self
        , server = 'localhost'
        , database = 'db001'
        , collection = 'person'
        , action = 'insert_not_file'
        , doc_of_file_or__not_file = {  # be careful when inserting file01, this has to has keys(path_file_origin, uid, file_name_origin)
            # 'path_file_origin': path_file,
            # 'uid': fileID,
            # 'file_name_origin': path_file.rsplit('\\', 1)[1]
            'path_file_origin' : 'e:\\about_eclipse.txt'
        }
        # , path_file = 'e:\about_eclipse.txt'
    ):
        if (server == 'localhost'):
            if (database == 'db001'):
                try:
                    self.connect_server_localhost
                except AttributeError:
                    self.connection(
                        server01 = server
                        , database = database
                        , port01 = 27017
                    )

                list_collection = self.local_db001.collection_names()
                if (collection not in list_collection):
                    print('Collection (' +collection+ ') is NOT in the list_of_collection ')
                    return

                if (action == 'insert_not_file'):   
                    self.local_db001.get_collection(collection).insert(doc_of_file_or__not_file)
                    txt = 'Inserted into: db(' + database + '), collection('+ collection +'), \n- doc('+ str(doc_of_file_or__not_file) +')'
                    print (txt)

                elif (action == 'delete_not_file'):
                    self.local_db001.get_collection(collection).remove(
                        doc_of_file_or__not_file
                        # , safe = True # not working
                    )
                    txt = r'Deleted from: db(' + database + '), collection('+ collection +'), \n- doc('+ str(doc_of_file_or__not_file) +')'
                    print (txt)
                    pass

                elif (action == 'delete_file'):
                    collection = 'file_inserted'
                    # esorn ny info momba anle file01 > file_inserted
                    # esorn ny fichier ao am self.fs_loc_db001
                    self.local_db001.get_collection(collection).remove(
                        doc_of_file_or__not_file
                        # , safe = True # not working
                    )
                    self.fs_loc_db001.delete(
                        
                    )
                    txt = r'Deleted from: db(' + database + '), collection('+ collection +'), \n- doc('+ str(doc_of_file_or__not_file) +')'
                    print (txt)
                
                elif(
                    (action == 'insert_file') # var(server, database) are already defined
                ):
                    # this next line is going to insert the file inside MongoDb
                    fileID = self.fs_loc_db001.put(
                        open(
                            doc_of_file_or__not_file['path_file_origin']
                            , 'rb'
                        )
                    )
                    # this next_line is going to save the information about the file
                    # # which we just inserted into the database
                    # print ('fileID: ', fileID)
                    # # 5a6c8cf42b2995113cd81aeb
                    self.local_db001.get_collection(collection).insert({
                        'path_file_origin': doc_of_file_or__not_file['path_file_origin']
                        , 'uid': fileID
                        , 'file_name_origin': doc_of_file_or__not_file['path_file_origin'].rsplit('\\', 1)[1]
                        , 'type': doc_of_file_or__not_file['type']
                    })

                    print('File inserted: '+ doc_of_file_or__not_file['path_file_origin'] +' _ 6268846943239003322')
                    pass
                else: # tsy mnw insertion, update, ...
                    print('Unknown Action, action(', action,')')
            else: # tsy fantatra ny bdd izai ho_ampiasaina
                print('Unknown Database: database(', database, ')')
        else:   # tsy fantatra ilay server izan hanaovana action
            print ('Unknown Server: server(', server, ')')
            
        # elif (
        #     (server == 'localhost')
        #     and (database == 'db001')
        #     and (collection == 'file_inserted')
        #     and (action == 'insert')
        # ):
        #     self.local_db001.file_inserted.insert(p)

        pass