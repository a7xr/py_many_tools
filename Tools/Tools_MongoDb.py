
import sys
import pymongo
import gridfs
import bson
from bson.objectid import ObjectId
import re
import os
import subprocess

from Freelance.Twitter001 import Twitter_Code

import configparser

confs_at_tools = configparser.ConfigParser()

# confs_at_tools.read(
#     r'E:\DEV\python\py_many_tools\Tools\confs_at__tools.txt')

# misy zvt tsy azoko ito
# # nga tsy tokony ho any am mis anle fichier mnw import ny misy anle confs_at_tools
confs_at_tools.read('all_confs.txt')

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
                    user_name = confs_at_tools['mongo_l']['username']
                    password = confs_at_tools['mongo_l']['password']
                    server = confs_at_tools['mongo_l']['ip_host']
                    uri = "mongodb://" + user_name + ":" + password + "@" + server
                    # self.connect_server_localhost = pymongo.MongoClient(server01, port01)

                    # tsy mamoka erreur ito rah diso ny credentials
                    # # any am insert sy find iz no mnw erreur rah diso ny credentials
                    self.connect_server_localhost = pymongo.MongoClient(uri)                    
                    print ('Connected from URI('+uri+')')
                    print()
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

    def exe_one_file(
        self
        , appli_name = 'vlc'
        , file_name = 'Newral'
    ):
        # alaina loo le URI misy anle appli01
        # alaina ilay URI misy anle file01

        # tsy apiasaina ito code eto ambany eto ty rah windows no apiasaina
        # mapiasa ternaire
        path_appli = self.action_select(
            collection = 'appli'
            , action = 'find_not_file'
            , doc_of_file_or__not_file = {
                'name_exe': appli_name
            }
        )[0]['path_exe'] if (
            len(
                self.action_select(
                    collection = 'appli'
                    , action = 'find_not_file'
                    , doc_of_file_or__not_file = {
                        'name_exe': appli_name
                    }
                )
            ) == 1
        ) else 'Path_appli unknown or there are many'
        # print('path_appli: ', path_appli)
        # # C:\Program Files\VideoLAN\VLC\vlc.exe
        
        if path_appli == 'Path_appli unknown or there are many':
            print (path_appli + ' _ 3676445759432111')
            return
            pass



        

        path_file = self.action_select(
            action = 'find_file'
            , doc_of_file_or__not_file = {
                'file_name_origin':{
                    '$regex': '.*'+ file_name +'.*'
                }
            }
        )
        # print ('path_file 2467888: ', path_file)
        # sys.exit(0)
        if(len(path_file)!=1):
            print ('Path_file unknown or there are many 47899333')
            Print_Color.print_red(
                txt = 'Going to run(' + str(path_file[0]) + ') ONLY'
            )
            # return

        # # ti akrai ty natao ho an'i windows irery
        subprocess.check_output(
            str(path_file[0])
            , shell = True
        )

        # print('path_appli: ', path_appli)
        # print ('path_file: ', str(path_file[0]))

        # subprocess.Popen(
        #     [
        #         path_appli
        #         , path_file
        #     ]
        # )

        os.remove(str(path_file[0]))
        print()
        print(path_file[0] + ' has been run, then deleted',)
        pass

    def get_path_appli(
        self
        , appli_name = 'sublime_text'
    ):
        path_appli = self.action_select(
            collection = 'appli'
            , action = 'find_not_file'
            , doc_of_file_or__not_file = {
                'name_exe': appli_name
            }
        )[0]['path_exe'] if (
            len(
                self.action_select(
                    collection = 'appli'
                    , action = 'find_not_file'
                    , doc_of_file_or__not_file = {
                        'name_exe': appli_name
                    }
                )
            ) == 1
        ) else 'Path_appli unknown or there are many _ 356893211156777'
        # print('path_appli: ', path_appli)
        # # C:\Program Files\VideoLAN\VLC\vlc.exe
        
        if path_appli == 'Path_appli unknown or there are many':
            print (path_appli + ' _ 356893211156777')
            return path_appli
            pass

        return str(path_appli)
        pass
    # ny fichier mety modifiena atreto dia
    # # .txt IRERY
    def modify_file(
        self
        , patt_to_search_in_file_name = 'eclipse'
        , name_exe = 'sublime_text'
    ):
        # 
        # any anaty bdd ny fichier ary alefa anaty to_del > path_file
        # vakina am sublime ilay path_file
        # # aza adino ny mnw sauvegarde aa
        # supprimena ny any anaty file_inserted sy ny fs_loc_db001
        # mnw insertion anle path_file
        try: 
            path_file = self.action_select(
                action = 'find_file'
                , print_only = False
                , doc_of_file_or__not_file = {
                    'path_file_origin': {
                        '$regex': '.*'+ patt_to_search_in_file_name +'.*'
                    }
                }
            )
            # print('path_fileAZFQSDF3452345: ', path_file)
            # # # ['e:\\to_del\\msg_03.txt', 'e:\\to_del\\msg_03.txt']
            # sys.exit(0)
            if (len(path_file) > 1):
                print('There are many files which you wanted to ', end = '')
                Print_Color.print_red(txt = 'modify')
                print()
                print('Which one of them do you want to modify')
                i = 0
                for file001 in path_file:
                    print(str(i) + ': ' + file001)
                    i += 1
                i = input(': ')
                path_file = path_file[int(i)]
            if (len(path_file) == 1):
                path_file = path_file[0]
            # sys.exit(0)
        except gridfs.errors.NoFile:
            print()
            print ('The file('+ patt_to_search_in_file_name +') you wanted is missing')
            print()
            return
        # path_file = str(path_file[0]) if (len(path_file) == 1) else 'File missing or you selected to many files'

        # print('path_file: ', path_file)
        # sys.exit(0)
        
        print('path_extension: ' + str(path_file.rsplit('.', 1)[1]))
        # txt


        file_extension = path_file.rsplit('.', 1)[1]
        if ( file_extension == 'txt'):
            path_appli = self.get_path_appli(
                appli_name = 'sublime_text'
            )

            subprocess.Popen(
                [
                    path_appli
                    , '-w'
                    , path_file
                ]
            ).wait()
        elif ( file_extension == 'pdf'):
            path_appli = self.get_path_appli(
                appli_name = 'foxit_reader'
            )
            subprocess.Popen(
                [
                    path_appli
                    , path_file
                ]
            )

        # print ('path_appli A34RT45SF2E: ', path_appli)
        # # C:\Program Files (x86)\Sublime Text 3\sublime_text.exe
        # print ('path_file 3YQGDF7657541241S: ', path_file)
        # # e:\to_del\msg_02.txt


        self.action_not_select(
            action = 'delete_file'
            , doc_of_file_or__not_file = {
                'file_name_origin': patt_to_search_in_file_name
            }
        )

        self.action_not_select(
            action = 'insert_file'
            , collection = 'file_inserted'
            , doc_of_file_or__not_file = {
                'path_file_origin': path_file
                , 'type': 'text'
            }
        )
        print ('File updated inside the database 234545869SDFGDFG')

        # uid_file = self.action_select(
        #     collection = 'file_inserted'
        #     , action = 'find_not_file'
        #     , doc_of_file_or__not_file = {
        #         'file_name_origin': path_file.rsplit('\\', 1)[1]
        #     }
        # )[0]['uid']

        # print ('uid_file: ', uid_file)
        # # 59f48596e97cac03cc5e1d23


        pass

    # this is going to select file or NOT file
    # the parameter_json_filter is very important
    def action_select_not_file(
        self
        , server = 'localhost'
        , database = 'db001'
        , port = 27017

        , collection = 'file_inserted'
        , action = 'find_not_file'
        , print_only = True

        , json_filter = {
            'file_name_origin': {
                '$regex': '.*msg.*'
            }
        }
    ):
        results = self.local_db001\
            .get_collection(collection).find(json_filter)

        res = []
        for result in results:
            # print(result)
            res.append(result)
        return res
        pass

    
    def action_select(
        self
        , server = 'localhost'
        , database = 'db001'
        , port = 27017

        , collection = 'person'
        , action = 'find_not_file'
        , print_only = True

        , doc_of_file_or__not_file = {
            'alias': 'alias001',
            'phone': 'phone001'
        }
        , projection = {}
        , limit_number = 10000000000000 # otrn mila anle mnw append_dict ito izay vao miainga
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
                try:
                    list_collection = self.local_db001.collection_names()
                except pymongo.errors.OperationFailure:
                    print('Authentication@Connection to database Error _ 72621184')

                if (collection not in list_collection):
                    print('Collection (' +collection+ ') is NOT in the list_of_collection ')
                    return

                if(action == 'find_not_file'):
                    # don_t know yet how to append a dictionary
                    if (len(projection) == 0):
                        res_query = self.local_db001.get_collection(collection).find(
                            doc_of_file_or__not_file
                            # , projection
                        )
                    else:
                        res_query = self.local_db001.get_collection(collection).find(
                            doc_of_file_or__not_file
                            , projection
                        )
                    if (limit_number != 10000000000000):
                        pass
                    # print ('res_query 820303933: ', res_query)

                    # print ('doc_of_file_or__not_file 9484: ', doc_of_file_or__not_file)

                    for doc01 in res_query:
                        res.append(doc01)

                    return res

                    pass
                elif(
                    (action == 'find_file')
                ):
                    collection = 'file_inserted'
                    # list_files_inserted__from_reg_file_name \
                    

                    res_query__files_info \
                        = self.local_db001.get_collection(collection).find(doc_of_file_or__not_file
                        )
                    # print('res_query: ', res_query)
                    # # <pymongo.cursor.Cursor object at 0x000002289D165F60>

                    i = 0
                    res = []
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

                        res.append(file_target_name)
                        if (print_only == True):
                            print(file_target_name)
                            pass
                        else:
                            file_target = open(
                                file_target_name
                                , 'wb'
                            )
                            file_target.write(grid_file.read())
                            file_target.close()
                            print('The output of your file is saved to: ', file_target_name)

                        # print ('dict01: ', dict01)
                        # # <gridfs.grid_file.GridOut object at 0x0000028120D249E8>
                    return res
                    
                else: # the action is unknown
                    pass
                pass
            else: # the database is unknown
                pass
        else: # the server is unknown
            pass
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

                try:
                    list_collection = self.local_db001.collection_names()
                except pymongo.errors.OperationFailure:
                    print('Authentication@Connection to database Error _ 463575584')
                    sys.exit(0)
                if (collection not in list_collection):
                    print('Collection (' +collection+ ') is NOT in the list_of_collection ')
                    return

                if (action == 'insert_not_file'):   
                    self.local_db001.get_collection(collection).insert(doc_of_file_or__not_file)
                    txt = 'Inserted into: db(' + database + '), collection('+ collection +'), \n- doc('+ str(doc_of_file_or__not_file) +')'
                    print (txt)

                elif (action == 'update_not_file'):
                    self.local_db001.get_collection(collection).update(doc_of_file_or__not_file)
                    print('updated: ', doc_of_file_or__not_file)
                    pass

                elif (action == 'delete_not_file'):
                    self.local_db001.get_collection(collection).remove(
                        doc_of_file_or__not_file
                        # , safe = True # not working
                    )
                    txt = r'Deleted from: db(' + database + '), collection('+ collection +'), \n- doc('+ str(doc_of_file_or__not_file) +')'
                    print (txt)
                    pass

                elif (action == 'delete_file'): # mbola tsy vita
                    # print ('ato QDSFSDF564567')
                    collection = 'file_inserted'
                    # alaina ny info momba ilay fichier ho supprimena > file_id
                    # supprimena ny self.local_db001.get_collection
                    # supprimena ny self.fs_loc_db001
                    file_id = '00'
                    try:
                        file_id = self.action_select(
                            collection = 'file_inserted'
                            , action = 'find_not_file'
                            , doc_of_file_or__not_file = doc_of_file_or__not_file
                        )[0]['uid']
                    except IndexError:
                        print('looks like the file which you wanted is not in collection(file_inserted) anymore _ 232657568134')

                    # print('file_id: ', file_id)
                    # # 5a6d3fcf2b29952158f66485

                    self.local_db001.get_collection(collection).remove(
                        doc_of_file_or__not_file
                        # , safe = True # not working
                    )
                    # print ('tafa ato')
                    # file_id = self.local_db001.get_collection(collection).find(doc_of_file_or__not_file)
                    self.fs_loc_db001.delete(
                        file_id
                    )
                    print('file_deleted 242345SSDF')
                    
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