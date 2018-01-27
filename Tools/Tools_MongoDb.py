
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

    def connect(
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
                    print('Connected to db(' + database + ') at server('+ server01 +')')
                    
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

    def action_not_select(
        self
        , server = 'localhost'
        , database = 'db001'
        , collection = 'person'
        , action = 'insert'
        , p = {
            'alias': 'alias001',
            'phone': 'phone001'
        }
    ):
        if (
            (server == 'localhost')
            and (database == 'db001')
            and (collection == 'person')
            and (action == 'insert')
            and (file_to_insert ==   'E:\\about eclipse.txt')
        ):
            # print('type(p)001: ', type(p))
            # # <class 'dict'>
            # print ('p001: ', str(p))
            # # {'alias': 'alias001', 'phone': 'phone001'}
            self.local_db001.person.insert(p)
            # print('type(p)002: ', type(p))
            # # <class 'dict'>
            txt = 'Inserted into: db(' + database + '), collection('+ collection +'), doc('+ str(p) +')'
            # print('p003: ', p)
            # # {'alias': 'alias001', 'phone': 'phone001', '_id': ObjectId('5a6ae9562b29952464011e6b')}

            print (txt)
            
        elif (
            (server == 'localhost')
            and (database == 'db001')
            and (collection == 'file_inserted')
            and (action == 'insert')
        ):
            self.local_db001.file_inserted.insert(p)

        pass