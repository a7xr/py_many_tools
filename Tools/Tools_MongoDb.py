
# to delete the commented_lines in python
# # sed -e '/^ *#/d' file001.py > file001_no_comments.py
#
# to delete the void lines
# # sed '/^$/d'
import sys
sys.path.append("..")

import pymongo
import gridfs
import bson
from bson.objectid import ObjectId
import re
import os
import subprocess
import time

from .Tools_Basic import *

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

    def repair_server(self):
        # mongod.exe --repair --dbpath g:\mongo_data\test002
        Tools_Basic.long_print()
        time.sleep(4)
        input('Going to repair the server_stockage')
        subprocess.Popen([
            confs_at_tools['mongo_l']['path_mongod']
            , '--repair'
            , '--dbpath'
            , confs_at_tools['mongo_l']['db_path_mongo']
        ]).wait()
        return 1
        pass

    def run_one_server(self):
        # vakiana dol loo ny zvt ilaina: 
        # # chemin_.exe, chemin_storage
        # mandefa anle serveur
        subprocess.Popen([
            confs_at_tools['mongo_l']['path_exe']
            
            , "--dbpath", confs_at_tools['mongo_l']['db_path_mongo']
            , '--port', confs_at_tools['mongo_l']['port_mongo']
        ])#\
        #.wait()
        return 1
        pass

    def kill_all_servers(self):
        # subprocess.Popen([
        #     'taskkill /f /im "mongod.exe"'
        #     # , '/f'
        #     # , '/im'
        #     # , '"mongod.exe"'
        # ])
        os.system('taskkill /f /im "mongod.exe"')
        return 1
        pass

    def stop_server(self):

        pass

    def __del__(self):
        print ('Object MongoDb destroyed')

    def connection(
        self
        , conf_file = 'default_conf_file'
        , server01 = 'localhost'
        , database = 'db001'
        , port01 = 27017
    ):
        # print ('server: ', server01, ' database: ', database, 'port: ', port01)
        if(server01 == 'localhost'):
            if(database == 'db001'):
                if(port01 == 27017):
                    # TODO, don_t know when Testing, this is going to 
                    if (conf_file == 'default_conf_file'):
                        user_name = confs_at_tools['mongo_l']['username']
                        password = confs_at_tools['mongo_l']['password']
                        server = confs_at_tools['mongo_l']['ip_host']
                    else:
                        conf_from_param = configparser.ConfigParser()
                        conf_from_param.read(conf_file)

                        user_name = confs_at_tools['mongo_l']['username']
                        password = confs_at_tools['mongo_l']['password']
                        server = confs_at_tools['mongo_l']['ip_host']

                    uri = "mongodb://" + user_name + ":" + password + "@" + server
                    # self.connect_server_localhost = pymongo.MongoClient(server01, port01)
                    print("uri124124: ", uri)
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
                    return 1
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
        # supprimena ny any anaty inserted_files sy ny fs_loc_db001
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
            , collection = 'inserted_files'
            , doc_of_file_or__not_file = {
                'path_file_origin': path_file
                , 'type': 'text'
            }
        )
        print ('File updated inside the database 234545869SDFGDFG')

        # uid_file = self.action_select(
        #     collection = 'inserted_files'
        #     , action = 'find_not_file'
        #     , doc_of_file_or__not_file = {
        #         'file_name_origin': path_file.rsplit('\\', 1)[1]
        #     }
        # )[0]['uid']

        # print ('uid_file: ', uid_file)
        # # 59f48596e97cac03cc5e1d23


        pass

    def action_select_file(
        self
        , server = 'localhost'
        , database = 'db001'
        , port = 27017

        , collection = 'inserted_files'
        , print_only = 1 # 1 means, we are going to print ONLY
                        # 0 means, we are going to download ONLY
                        # 2 means, we are going to print AND download

        , json_filter = {
            'file_name_origin': {
                '$regex': '.*msg.*'
            }
        }

        , output_folder_for_file = "e:\\to_del\\"
    ):
        if (server == 'localhost'):
            if(database == 'db001'):
                try:
                    self.connect_server_localhost

                except AttributeError:
                    self.connection(
                        server01 = server
                        , database = database
                        , port01 = port
                    )
                try:
                    list_collection = self.local_db001.collection_names()
                except pymongo.errors.OperationFailure:
                    print('Authentication@Connection to database Error _ 72621184')

                if (collection not in list_collection):
                    print('Collection (' +collection+ ') is NOT in the list_of_collection ')
                    return

                # connection is set
                # we are in (server == 'localhost', database == 'db001')
                collection = 'inserted_files'
                # results = self.local_db001\
                #     .get_collection(collection).find(json_filter)
                res_query__files_info \
                        = self.local_db001.get_collection(collection).find(json_filter
                        )
                res = []
                i = 0
                for about_file in res_query__files_info:
                    # print(result)
                    # res.append(result)

                    # should find a better solution, this one is going to let the computer make a lot of branch
                    if print_only == 0: # we are going to Download ONLY
                        # print (about_file['uid'])
                        # sys.exit(0)
                        try: 
                            grid_file = self.fs_loc_db001.get(
                                ObjectId(str(about_file['uid']))
                            )
                        except gridfs.errors.NoFile as err: # the information is in collection('inserted_files'), but that file is missing in MongoDb
                            print (about_file['uid'])
                            Print_Color.print_blue (txt = 'Looks like the information of the file is in collection(inserted_files)')
                            Print_Color.print_blue (txt = '- but the file is missing in MongoDb:server('+ server +'), database('+ database +')')
                            self.local_db001.get_collection('inserted_files').remove({'uid': about_file['uid']})
                            print()
                            print('uid: ', str(about_file['uid']), ' has been')
                            Print_Color.print_red(txt = '- deleted')
                            sys.exit(0)
                        file_target_name = output_folder_for_file + about_file['path_file_origin'].rsplit('\\', 1)[1]
                        res.append(file_target_name)
                        file_target = open(
                            file_target_name
                            , 'wb'
                        )
                        file_target.write(grid_file.read())
                        file_target.close()
                        print('Your file is saved to: ', file_target_name)
                        pass
                    elif print_only == 1: # we are going to print ONLY
                        try:
                            print()
                            print('uid: ', about_file['uid'])
                            print('file_name_origin: ', about_file['file_name_origin'])
                            print('path_file_origin: ', about_file['path_file_origin'])
                            print('type: ', about_file['type'])
                            pass
                        except KeyError:
                            pass
                    elif print_only == 2: # we are going to print AND download
                        pass

                return res
                pass
            else: # the database which is selected is missing
                print('The database('+ database +') which you wanted is ')
                Print_Color.print_red(txt = '- missing')
                sys.exit(0)
        else:
            print('The server('+ server +') which you wanted is ')
            Print_Color.print_red(txt = '- missing')
            sys.exit(0)
        pass
        # end of def action_select_file()




    def select_data(
        self
        , collection = "person"
        , json001 = {
            'first_name' : "first_name001"
            , 'last_name' : "last_name001"
        }
    ):
        # tadidio fa ito dia mameno zvt any am self.listOfDict__results_select_mongodb loo
        self.listOfDict__results_select_mongodb = []
        for row in self.local_db001.get_collection(collection).find(json001):
            self.listOfDict__results_select_mongodb.append(row)
        return 1
        pass

    # this is going to select file or NOT file
    # the parameter_json_filter is very important
    def action_select_not_file(
        self
        , server = 'localhost'
        , database = 'db001'
        , port = 27017

        , collection = 'inserted_files'
        , print_only = True

        , json_filter = {
            'file_name_origin': {
                '$regex': '.*msg.*'
            }
        }
    ):
        if (server == 'localhost'):
            if(database == 'db001'):
                try:
                    self.connect_server_localhost

                except AttributeError:
                    self.connection(
                        server01 = server
                        , database = database
                        , port01 = port
                    )
                try:
                    list_collection = self.local_db001.collection_names()
                except pymongo.errors.OperationFailure:
                    print('Authentication@Connection to database Error _ 72621184')

                if (collection not in list_collection):
                    print('Collection (' +collection+ ') is NOT in the list_of_collection ')
                    return

                # connection is set
                # we are in (server == 'localhost', database == 'db001')
                results = self.local_db001\
                    .get_collection(collection).find(json_filter)

                res = []
                for result in results:
                    # print(result)
                    res.append(result)
                self.listOfDict__results_select_mongodb = res
                print("self.listOfDict__results_select_mongodb63224679: ", self.listOfDict__results_select_mongodb)
                return 1
                pass
            else: # the database which is selected is missing
                print('The database('+ database +') which you wanted is ')
                Print_Color.print_red(txt = '- missing')
                sys.exit(0)
        else:
            print('The server('+ server +') which you wanted is ')
            Print_Color.print_red(txt = '- missing')
            sys.exit(0)

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
                        
                        # print('type(res_query): ', type(res_query))
                        # # <class 'pymongo.cursor.Cursor'>

                        # print('res_query.count(): ', res_query.count())
                        # # 1
                        i = 0
                        for doc01 in res_query:
                            res.append(doc01)
                            print('doc01: ', doc01, ' _ ', i)
                            i += 1
                    else:
                        res_query = self.local_db001.get_collection(collection).find(
                            doc_of_file_or__not_file
                            , projection
                        )
                    if (limit_number != 10000000000000):
                        pass

                    # print ('doc_of_file_or__not_file 9484: ', doc_of_file_or__not_file)

                    i = 0
                    # for doc01 in res_query:
                    #     res.append(doc01)
                    #     print('doc01: ', doc01, ' _ ', i)
                    #     i += 1

                    return res

                    pass
                elif(
                    (action == 'find_file')
                ):
                    collection = 'inserted_files'
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

    def insert_file(
        self
        , path_file = 'g:\\michel.txt'
        , name_to_store_in_register = 'm001.txt'
    ):
        fileID = self.fs_loc_db001.put(
            open(
                path_file
                , 'rb'
            )
        )

        collection = "inserted_file"
        self.local_db001.get_collection(collection).insert({
            'path_file_origin': path_file
            , 'uid': fileID
            , 'file_name_origin': name_to_store_in_register
            , 'type': "text"
        })
        return 1
        pass


    def get_file(
        self
        , name_stored_in_register = "m001.txt"
    ):
        collection = "inserted_file"
        self.store_dldd_file = 'g:\\to_del'

        self.local_db001.get_collection(collection).find({

        })
        try: 
            self.action_select_not_file(
                collection = 'inserted_file'
                , print_only = True

                , json_filter = {
                    'file_name_origin': 'm001.txt'
                }
            )
            self.select_data(
                collection = 'inserted_file'
                , json001 = {

                }
            )
            grid_file = self.fs_loc_db001.get(
                ObjectId(self.listOfDict__results_select_mongodb[0]['uid'])
            )
            file_target = self.store_dldd_file + '\\' + json_filter['file_name_origin']
            file_target = open(
                file_target_name
                , 'wb'
            )
            file_target.write(grid_file.read())
            file_target.close()
        except gridfs.errors.NoFile as err: # the information is in collection('inserted_files'), but that file is missing in MongoDb
            print ("MAYBE the file which you wanted is missing in the GridFS, but it exists inside the register")

        pass

    def delete_file(
        self
        , name_stored_in_register = 'm001.txt'
    ):
        # alaina ilay uid_file_to_delete
        # supprimena 
        collection = "inserted_file"

        try:
            self.action_select_not_file(
                collection = 'inserted_file'
                , print_only = True

                , json_filter = {
                    'file_name_origin': 'm001.txt'
                }
            )
            uid_file_to_delete = self.listOfDict__results_select_mongodb[0]['uid']
            # print("uid_file_to_delete03948569: ", uid_file_to_delete)
            # input()
            self.fs_loc_db001.delete(
                {
                    '_id': ObjectId(uid_file_to_delete)
                }
            )
            # input('Before deleting a line in collection(inserted_files)')
            self.local_db001.get_collection(collection).remove({
                'uid': ObjectId(uid_file_to_delete)
            })

            return 1
            pass
        except IndexError:
            print('MAYBE the file which you wanted to delete do NOT exist Anymore')
            pass

        pass

    def insert_data(
        self
        , collection = ''
        , list_json001 = {

        }
    ):
        # jerena loo we ao v ilay collection hanaovana insertion
        # rah ao:
        # # manao insertion
        # rah tsy ao:
        # # affichena we ilay collection hanaovana insertion tsy ao... ar mvoka






        # jerena loo we ao v ilay collection hanaovana insertion
        # rah ao:
        if ( collection in self.local_db001.collection_names() ):
            # # manao insertion
            self.local_db001.get_collection(collection).insert_many(list_json001)
            return 1
            pass
        # rah tsy ao:
        else:
            # # affichena we ilay collection hanaovana insertion tsy ao... ar mvoka
            Print_Color.print_red(
                txt = "The collection( "+ collection +" ) which you wanted to insert something is missing"
            )
            return 0
            pass

        pass

    def action_not_select(
        self
        , server = 'localhost'
        , database = 'db001'
        , collection = 'person'
        , action = 'insert_not_file'
        , _id = 1 # normally, this is going to be done by 
        , doc_of_file_or__not_file = {  # be careful when inserting file01, this has to has keys(path_file_origin, uid, file_name_origin)
            # 'path_file_origin': path_file,
            # 'uid': fileID,
            # 'file_name_origin': path_file.rsplit('\\', 1)[1]
            'path_file_origin' : 'g:\\michel.txt'
            , 'name_to_store_in_db': "m001.txt"
            , 'type': "text"
        }
        # , path_file = 'e:\about_eclipse.txt'
    ):
        # print("tonga ato")
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
                    print ("list_collection: ", list_collection)
                except pymongo.errors.OperationFailure:
                    print('Authentication@Connection to database Error _ 463575584')
                    sys.exit(0)
                if (collection not in list_collection):
                    print('Collection (' +collection+ ') is NOT in the list_of_collection ')
                    return 0

                if (action == 'insert_not_file'):   
                    doc_of_file_or__not_file['_id'] = _id
                    self.local_db001.get_collection(collection)\
                        .insert(doc_of_file_or__not_file)
                    txt = 'Inserted into: db(' + database + '), collection('+ collection +'), \n- doc('+ str(doc_of_file_or__not_file) +')'
                    print (txt)
                    return 1

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

                # elif (action == 'delete_file'): # mbola tsy vita
                #     # print ('ato QDSFSDF564567')   
                #     collection = 'inserted_files'
                #     # alaina ny info momba ilay fichier ho supprimena > file_id
                #     # supprimena ny self.local_db001.get_collection
                #     # supprimena ny self.fs_loc_db001
                #     file_id = '00'
                #     try:
                #         file_id = self.action_select(
                #             collection = 'inserted_files'
                #             , action = 'find_not_file'
                #             , doc_of_file_or__not_file = doc_of_file_or__not_file
                #         )[0]['uid']
                #     except IndexError:
                #         print('looks like the file which you wanted is not in collection(inserted_files) anymore _ 232657568134')

                #     # print('file_id: ', file_id)
                #     # # 5a6d3fcf2b29952158f66485

                #     self.local_db001.get_collection(collection).remove(
                #         doc_of_file_or__not_file
                #         # , safe = True # not working
                #     )
                #     # print ('tafa ato')
                #     # file_id = self.local_db001.get_collection(collection).find(doc_of_file_or__not_file)
                #     self.fs_loc_db001.delete(
                #         {
                #             '_id': ObjectId(file_id)
                #         }
                #     )
                #     print('file_deleted 242345SSDF')

                elif(
                    (action == 'insert_file') # var(server, database) are already defined
                    and (
                        ('insertion_type' in doc_of_file_or__not_file.keys()) and 
                        ('python' == doc_of_file_or__not_file['insertion_type']) 
                    )
                ):
                    return 1
                    fileID = self.fs_loc_db001.put(
                        open(
                            doc_of_file_or__not_file['path_file_origin']
                            , 'rb'
                        )
                    )

                    collection = 'inserted_files'

                    self.mongodb.action_select_not_file(
                        collection = collection
                        , print_only = True

                        , json_filter = {
                            'path_file_origin': doc_of_file_or__not_file['path_file_origin']
                            , 'type': doc_of_file_or__not_file['type']
                            , 'name_to_store_in_db': doc_of_file_or__not_file['name_to_store_in_db']
                        }
                    )

                    # self.local_db001.get_collection(collection).insert({
                    #     'path_file_origin': doc_of_file_or__not_file['path_file_origin']
                    #     , 'uid': fileID
                    #     , 'file_name_origin': doc_of_file_or__not_file['path_file_origin'].rsplit('\\', 1)[1]
                    #     # , 'type': doc_of_file_or__not_file['type']
                    # })

                    pass
                    
                elif(
                    (action == 'insert_file') # var(server, database) are already defined
                    and (
                        ('insertion_type' in doc_of_file_or__not_file.keys()) and 
                        ('mongofiles' == doc_of_file_or__not_file['insertion_type']) 
                    )
                ):
                    #todo... this is going to be used to insert file with mongofiles
                    # mongofiles.exe put -l g:\michel.txt m.txt
                    # mongofiles.exe list
                    # mongofiles.exe delete m.txt

                    # subprocess.Popen([
                    #     confs_at_tools['mongo_l']['path_mongofiles']
                    # ])
                    return 1
                    if( 
                        'name_to_store_in_db' in doc_of_file_or__not_file.keys() 
                    ):
                        name_to_store_in_db = doc_of_file_or__not_file['name_to_store_in_db']
                        subprocess.Popen([
                            confs_at_tools['mongo_l']['path_mongofiles']
                            , 'put'
                            , "-l"
                            , doc_of_file_or__not_file['path_file_origin']
                            ,  name_to_store_in_db
                            # , 'coco.txt'
                        ])


                        return 1
                        pass
                    else:
                        subprocess.Popen([
                            confs_at_tools['mongo_l']['path_mongofiles']
                            , 'put'
                            , doc_of_file_or__not_file['path_file_origin']
                        ])
                        return 1
                        pass

                    

                    pass
                
                elif (
                    (action == 'delete_file')
                    # and (
                    #     ('deletion_type' not in doc_of_file_or__not_file.keys())
                    # )
                ):
                    # by default, this is going to delete the file with mongofiles

                    # mongofiles delete m001.txt
                    subprocess.Popen([
                        confs_at_tools['mongo_l']['path_mongofiles']
                        , "delete"
                        , doc_of_file_or__not_file['name_stored_in_db']
                    ])
                    return 1
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
        #     and (collection == 'inserted_files')
        #     and (action == 'insert')
        # ):
        #     self.local_db001.inserted_files.insert(p)

        pass
