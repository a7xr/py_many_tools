
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
                    self.connect_server_localhost = pymongo.MongoClient(server01, port01)
                    self.local_db001 = self.connect_server_localhost.db001
                    print('Connected to db(' + database + ') at server('+ server01 +') _ code6356745473')
                    
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
                if(action == 'find_not_file'):
                    if (collection == 'person'):
                        
                        print('Connection from def(query_select) _ code76543222888')
                        res_query = self.local_db001.person.find(
                            doc
                        )
                        # error below
                        # res_query = self.local_db001.getCollection(collection).find(
                        #     doc
                        # )
                        pass
                    else: # the collection is unknown
                        pass
                elif(
                    (action == 'find_file')
                    and (collection == 'file_inserted')
                ):
                    # list_files_inserted__from_reg_file_name \
                    regex001 = '.*' + patt_to_search_in_file_name + '.*'
                    # res_query__files_info \
                    res_query \
                        = self.local_db001.file_inserted.find({
                            'file_name_origin': {'$regex': 
                                    str(regex001)
                                    , '$options':'i'
                            }
                        })
                    # print('res_query: ', res_query)
                    # # <pymongo.cursor.Cursor object at 0x000002289D165F60>
                    if (res_query.count() == 1):
                        # print('len is 1')
                        
                    else:
                        print ('Not yet managed')
                        print ('res_query.count(): ', res_query.count())
                        sys.exit(0)

                    # print('list_files_inserted__from_reg_file_name: ', list_files_inserted__from_reg_file_name)
                    # print('res_query: ', res_query)
                    # # <pymongo.cursor.Cursor object at 0x0000025B4F415F60>
                    pass
                else: # the action is unknown
                    pass
                pass
            else: # the database is unknown
                pass
        else: # the server is unknown
            pass
        pass

        # if res_query != None: # misy zvt ny resultat anle requete
        #     for doc01 in res_query:
        #         print ("doc01")
        #     pass
        # else:
        #     pass
        # print('type(res_query)0001: ', type(res_query))
        # # <class 'pymongo.cursor.Cursor'>
        for doc01 in res_query:
            res.append(doc01)
        return res

    # this method is going to be Complicated
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
                if (action == 'insert_not_file'):
                    if (collection == 'person'):

                        # print('type(p)001: ', type(p))
                        # # <class 'dict'> 
                        # print ('p001: ', str(p))
                        # # {'alias': 'alias001', 'phone': 'phone001'}
                        self.local_db001.person.insert(doc_of_file_or__not_file)
                        # print('type(p)002: ', type(p))
                        # # <class 'dict'>
                        txt = 'Inserted into: db(' + database + '), collection('+ collection +'), doc('+ str(doc) +')'
                        # print('p003: ', p)
                        # # {'alias': 'alias001', 'phone': 'phone001', '_id': ObjectId('5a6ae9562b29952464011e6b')}
                        print (txt)
                    elif (collection == 'user'):
                        self.local_db001.user.insert(doc_of_file_or__not_file)
                        txt = 'Inserted into: db(' + database + '), collection('+ collection +'), doc('+ str(doc) +')'
                        print (txt)
                        pass
                    else: # tsy fantatra ilay collection izay anovana action
                        print('Unknown Collection which we want to ', action)
                elif(
                    (action == 'insert_file') # var(server, database) are already defined
                    and (collection == 'file_inserted')
                ):
                    fileID = self.fs_loc_db001.put(
                        open(
                            doc_of_file_or__not_file['path_file_origin']
                            , 'rb'
                        )
                    )
                    # print ('fileID: ', fileID)
                    # # 5a6c8cf42b2995113cd81aeb
                    self.local_db001.file_inserted.insert({
                        'path_file_origin': doc_of_file_or__not_file['path_file_origin']
                        , 'uid': fileID
                        , 'file_name_origin': doc_of_file_or__not_file['path_file_origin'].rsplit('\\', 1)[1]
                    })

                    print('File inserted _ 6268846943239003322')
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