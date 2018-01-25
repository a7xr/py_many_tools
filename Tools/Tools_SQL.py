import MySQLdb
import logging

import datetime
from datetime import date

import configparser
config = configparser.ConfigParser()
config.read(
    r'E:\DEV\python\py_many_tools\all_confs.txt'
    # '..\\..\\all_confs.txt'
)

class MySQL:
        
    def db_select(
        self
        , query01 = "select * from table001"
        , host = config['mysql_localhost_tw_app001']['ip_host']
        , db = config['mysql_localhost_tw_app001']['database']

    ):
        results = None
        if (
            (host == config['mysql_localhost_tw_app001']['ip_host']) 
            and (db == config['mysql_localhost_tw_app001']['database'])
        ):
            try:
                self.connect_mysql_local_tw_app01
            except AttributeError:
                self.connect_db(
                    server01 = config['mysql_localhost_tw_app001']['ip_host']
                    , user01 = config['mysql_localhost_tw_app001']['username']
                    , password01 = config['mysql_localhost_tw_app001']['password']
                    , database01 = config['mysql_localhost_tw_app001']['database']
                    , port = config['mysql_localhost_tw_app001']['port']
                    , type = "mysql"
                )
            self.cursor_mysql_local_tw_app001.execute(query01)
            results = self.cursor_mysql_local_tw_app001.fetchall()
            # print ("results: ", results)
        return results
        pass
    

    def disconnect_db(
        self
        , log = True
    ):
        try:
            del self.cursor_mysql_local_tw_app001
            del self.connect_mysql_local_tw_app01
            
            if log == True:
                print ()
                txt = str(datetime.datetime.now()) + ": db(" + self.database + ')@' + self.server + ": Disconnected ( " + self.type + " )"
                print (txt)
                print(txt, file = open(self.log_file, "a"))

        except NameError:
            pass
        except Exception:
            pass
        pass

    def __del__(
        self
    ):  # klass Our_Tools_py3
        self.disconnect_db()

    def __init__(self):     # klass Our_Tools_py3(threading.Thread):
        self.log_file = "general_log.txt"
        pass

    def connect_db(self  
            , server01 = config['mysql_localhost_tw_app001']['ip_host']
            , user01 = config['mysql_localhost_tw_app001']['username']
            , password01 = config['mysql_localhost_tw_app001']['password']
            , database01 = config['mysql_localhost_tw_app001']['database']
            , port = config['mysql_localhost_tw_app001']['port']
            , type = "mysql"
            , log = True
    ):
        self.server = server01
        self.user = user01
        self.database = database01
        self.port = port
        self.type = type

        try:
            if((type == "mysql") 
                and (database01 == config['mysql_localhost_tw_app001']['database'])
                and (server01 == config['mysql_localhost_tw_app001']['ip_host'])
            ):
                self.connect_mysql_local_tw_app01 = MySQLdb.Connection(
                    host=server01,
                    user=user01,
                    passwd=password01,
                    port=int(port),
                    db=database01
                )
                self.cursor_mysql_local_tw_app001 = self.connect_mysql_local_tw_app01.cursor()
                txt = str(datetime.datetime.now()) + ": db(" + self.database + ')@' + self.server + ": Connected ( " + self.type + " )"
                # print ("Connection OK with mysql")
                print (txt)
                print ()
                txt = str(datetime.datetime.now()) + ": db(" + database01 + ")@" + server01 + ": Connection OK, ( " + type +" )"

                if log == True:
                    print(txt, file = open(self.log_file, "a"))
        except Exception as mysql_error:
            logging.exception("message")
            pass
        pass

    def db_not_select(self
            , query01 = "insert into table001(id) values (4)"
            , host = config['mysql_localhost_tw_app001']['ip_host']
            , db = config['mysql_localhost_tw_app001']['database']
            , log_query = False
            , auto_commit = False
            , test001 = True
    ):
        if( 
                (host == config['mysql_localhost_tw_app001']['ip_host']) 
                and (db == config['mysql_localhost_tw_app001']['database'])
        ):
            try:
                self.connect_mysql_local_tw_app01
            except AttributeError:
                self.connect_db(
                    server01 = config['mysql_localhost_tw_app001']['ip_host']
                    , user01 = config['mysql_localhost_tw_app001']['username']
                    , password01 = config['mysql_localhost_tw_app001']['password']
                    , database01 = config['mysql_localhost_tw_app001']['database']
                    , port = config['mysql_localhost_tw_app001']['port']
                    , type = "mysql"
                )
            except Exception as mysql_error:
                logging.exception("message")

            if test001 == False:
                self.cursor_mysql_local_tw_app001.execute(query01)
            if auto_commit == True:
                self.connect_mysql_local_tw_app01.commit()

            pass

        pass


