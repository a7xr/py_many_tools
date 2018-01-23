import os
import MySQLdb
import re
import sys
import getopt
import csv
import logging
import sys
import datetime
from datetime import date
import threading
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


import pprint
import threading
import tweepy

import pandas as pd

from bs4 import BeautifulSoup
import requests

import configparser



import twitter
from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

import json

from ctypes import windll, Structure, c_short, c_ushort, byref
SHORT = c_short
WORD = c_ushort


config = configparser.ConfigParser()
config.read('all_confs.txt')


ckey = config['twitter001']['CONSUMER_KEY']
csecret = config['twitter001']['CONSUMER_SECRET']
atoken = config['twitter001']['ACCESS_TOKEN']
asecret = config['twitter001']['ACCESS_TOKEN_SECRET']

# tweets_data_path = 'twitter_data.txt'
# write_file_twitter_data = open(tweets_data_path, "w")



#Inherit stream listener to get the twitter data
class Twitter_Listener(StreamListener):

    def __init__(
        self
        , file_twitter_data = 'twitter_data.txt'
        , words_to_search = ["iPhone 7","Note 5"]
    ):
        self.write_file_twitter_data = open(file_twitter_data, "w")
        self.words_to_search = words_to_search
        self.i = 0
        pass

    def collect_data_twitter(self):
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)

        twitterStream = Stream(auth, Twitter_Listener())
        twitterStream.filter(
            track = self.words_to_search
        )
        # print (type(twitterStream) + '2345676543444444', file = open('twitter_data.txt', 'a'))
        sys.exit(0)
        # twitterStream.retweet(async=True)

        # print (type(twitterStream))
        # sys.exit(0)

        self.write_file_twitter_data.close()

        pass

    def on_status(self, status):
        print('ato')
        print(status.text)
        # print ("status.retweeted_status: ", status.retweeted_status)
        # if status.retweeted_status:
            # print ("status.retweeted_status: ", status.retweeted_status)
        # else:
# 
#             return

    def on_data(self, data):
        # print (data)
            #Store twitter data in a text file  
        # print (type(data))
        # # <class 'str'>
        # sys.exit(0)
        print(self.i)
        self.i += 1
        if '"retweeted":false' in data:
            print ("retweeted:false")
        elif '"retweeted":true' in data:
            print ("retweeted:true")

        # self.write_file_twitter_data.write(data)

        #You can also access data this way
        #all_data = json.loads(data)
        #tweet = all_data["text"]
        #lang = all_data["lang"]
        #username = all_data["user"]["screen_name"]
        #print "username:%s, tweet:%s, language:%s" %(username, tweet, lang)

        return True

    def on_error(self, status):
        print ("Error:", status)


class Part_I_Twitt_App():
    # ty tkn mjery we efa misy v ilay table_word_to_search_in_twitter
    # # rah efa misy table_word_to_search_in_twitter
    # # # suppr table_word_to_search_in_twitter
    # # # mnw creation table__twitter_word_search
    # # # insertion am table__twitter_word_search
    # # # 
    # # rah mbola tsis:
    # # # mnw creation table__twitter_word_search
    # # # insertion am table__twitter_word_search
    #
    # ty tkn tsis thread
    def __init__(self):     # klass Part_I_Twitt_App
        
        self.log_twitter_app = 'log_twitter_app.txt'

        self.our_tools_py3 = Our_Tools_py3()
        # self.our_tools_py3.connect_db()

        self.server = config['mysql_localhost_tw_app001']['ip_host']
        self.user = config['mysql_localhost_tw_app001']['username']
        self.password = config['mysql_localhost_tw_app001']['password']
        self.database = config['mysql_localhost_tw_app001']['database']
        self.port = config['mysql_localhost_tw_app001']['port']
        self.type = "mysql"

        self.our_tools_py3.connect_db(
            server01 = self.server
            , user01 = self.user
            , password01 = self.password
            , database01 = self.database
            , port = self.port
            , type = self.type
            , log = False   
        )
        txt = str(datetime.datetime.now()) + ": db(" + self.database + '@' + self.server + ": Connection OK ( " + self.type + " )"
        print(txt, file = open(self.log_twitter_app, "a"))
        pass

    def refactor_create_insert_table_word_search_query(
        self
        , create_table_word_search_query = ""
    ):

            self.our_tools_py3.db_not_select(
                test001 = False
                , query01 = create_table_word_search_query
                , auto_commit = True
            )
            print ('table created')



            twitter_to_search = Our_Tools_py3.csv_read_all(
                path_file_csv = 'twitter_data001.csv'
                , delimiter = ','
            )
            print ("twitter_to_search", twitter_to_search)
            # # [['python'], ['java'], ['android'], ['cisco'], ['nuvus']]

            for line in twitter_to_search:
                for val in line:
                    insert_query = 'INSERT INTO twitter_word_search (word_search) VALUES ("'+ str(val) +'")'
                    # print ('insert_query: ', insert_query)
                    self.our_tools_py3.db_not_select(
                        query01 = insert_query
                        , auto_commit = True
                        , test001 = False
                    )
                    pass
            pass
    def __del__(self):      # klass Part_I_Twitt_App
        self.our_tools_py3.disconnect_db(log = False)
        pass

    def run(self):  # klass Part_I_Twitt_App... This does NOT extend from Threading

        # print (config['mysql_localhost_tw_app001']['ip_host'])
        # print (config['mysql_localhost_tw_app001']['database'])
        # sys.exit(0)
        # foo = "True" if test else "False" 
        is_table_twitter_app = 0 if (
            len(
                self.our_tools_py3.db_select(
                            # query01 = 'SELECT * from table001 limit 1'
                            query01 = "SHOW TABLES LIKE 'twitter_word_search'"
                            , host = config['mysql_localhost_tw_app001']['ip_host']
                            , db = config['mysql_localhost_tw_app001']['database']
                )
            ) == 0 
        ) else 1
        #   print ("res001: ", res001)

        create_table_word_search_query = """
                create table twitter_word_search(
                    word_search varchar(75)
                )
        """

        create_table_twitter_app_query = """
                create table twitter_app(
                    created_at DATETIME,
                    id_str varchar(200) DEFAULT NULL,
                    text text,
                    `user.name` varchar(200) DEFAULT NULL,
                    `user.followers_count` int(5),
                    coordinates varchar(200) DEFAULT NULL,
                    reply_count int(5),
                    retweet_count int(5),
                    `entities.hashtags` varchar(200) DEFAULT NULL
                )
        """

        # print ('is_table_twitter_app: ', is_table_twitter_app)
        # # 1
        if is_table_twitter_app == 1:       # # rah efa misy table_word_to_search_in_twitter

            print('table(twitter_word_search) exists already')
            # sys.exit(0)
            self.our_tools_py3.db_not_select(
                test001 = False
                , query01 = "drop table twitter_word_search"
                , auto_commit = True
            )
            print ('table dropped')



            self.refactor_create_insert_table_word_search_query(
                create_table_word_search_query = create_table_word_search_query
                # , 
            )

            # self.our_tools_py3.db_not_select(
                # test001 = False
                # , query01 = create_table_word_search_query
                # , auto_commit = True
            # )
            # print ('table created')
# 
# 
# 
            # twitter_to_search = Our_Tools_py3.csv_read_all(
                # path_file_csv = 'twitter_data001.csv'
                # , delimiter = ','
            # )
            # print ("twitter_to_search", twitter_to_search)
            # [['python'], ['java'], ['android'], ['cisco'], ['nuvus']]
# 
            # for line in twitter_to_search:
                # for val in line:
                    # insert_query = 'INSERT INTO twitter_word_search (word_search) VALUES ("'+ str(val) +'")'
                    # print ('insert_query: ', insert_query)
                    # self.our_tools_py3.db_not_select(
                        # query01 = insert_query
                        # , auto_commit = True
                        # , test001 = False
                    # )
                    # pass
            # pass
            print ('after insertion098787765')
        else:       # mbola tsy ao ny table__twitter_app
            # mbola tsy ao ny table__twitter_app d mnw insertion
            # # alaina dol loon ny avy any am csv
            # # isakn iray avy any am csv dia apdirn
            # print ('ato amle 0')

            

            self.our_tools_py3.db_not_select(
                test001 = False
                , query01 = create_table_word_search_query
                , auto_commit = True
            )
            print ('table created')



            twitter_to_search = Our_Tools_py3.csv_read_all(
                path_file_csv = 'twitter_data001.csv'
                , delimiter = ','
            )
            # print ("twitter_to_search", twitter_to_search)
            # # [['python'], ['java'], ['android'], ['cisco'], ['nuvus']]
            for line in twitter_to_search:
                for val in line:
                    insert_query = 'INSERT INTO twitter_word_search (word_search) VALUES ("'+ str(val) +'")'
                    self.our_tools_py3.db_not_select(
                        query01 = insert_query
                        , auto_commit = True
                        , test001 = False
                    )
            print ('after insertion33246357')

        pass

    @staticmethod
    def csv_read_all(
        path_file_csv = 'file001.csv',
        delimiter = '|' 
    ):
        res = []
        with open(path_file_csv) as csv_read:
            reader = csv.reader(
                csv_read, delimiter = delimiter)
            for row in reader:
                res.append(row)
            # print "another_line"
        return res


    @staticmethod
    def csv_read_content(path_file_csv = 'file001.csv',delimiter = '|'):
        # print "coco"
        # print res
        res = []
        list01 = Our_Tools.csv_read_all(
            path_file_csv = path_file_csv,
            delimiter = delimiter)[1:]
        for elem in list01:
            res.append(elem)
        return res
        # for elem in list01:
            # print elem    



    

class Part_II_Twitt_App(threading.Thread):
    def __init__(self): # klass Part_II_Twitt_App
        self.log_twitter_app = 'log_twitter_app.txt'
        self.our_tools_py3 = Our_Tools_py3()

        self.server = config['mysql_localhost_tw_app001']['ip_host']
        self.user = config['mysql_localhost_tw_app001']['username']
        self.password = config['mysql_localhost_tw_app001']['password']
        self.database = config['mysql_localhost_tw_app001']['database']
        self.port = config['mysql_localhost_tw_app001']['port']
        self.type = "mysql"

        # mnw connection isakn partie satria independant izy ireo
        self.our_tools_py3.connect_db(
            server01 = self.server
            , user01 = self.user
            , password01 = self.password
            , database01 = self.database
            , port = self.port
            , type = self.type
            , log = False   
        )

        pass

    def run(self):  # klass Part_II_Twitt_App
        # # mamaky anle zvt avy anaty table__twitter_word_search
        # # jerena isakn avy any am content(table__twitter_word_search)
        # # # mtady anzai tsy_retweet
        # # # izay tsy_retweet dia sauvena : created_at id_str text user.name user.followers_count coordinates reply_count retweet_count entities.hashtags

        words_to_search = self.our_tools_py3.db_select(
                    # query01 = 'SELECT * from table001 limit 1'
                    query01 = "select word_search from twitter_word_search"
                    , host = config['mysql_localhost_tw_app001']['ip_host']
                    , db = config['mysql_localhost_tw_app001']['database']
        )

        # print ('words_to_search: ', words_to_search)
        # # (('python',), ('java',), ('android',)

        list_to_search = []
        for line in words_to_search:
            list_to_search.append(line[0])
            pass
        # print ('list_to_search: ', list_to_search)
        # # ['python', 'java', 'android',



        # sys.exit(0)

        l = Twitter_Listener(
            words_to_search = list_to_search
        )
        l.collect_data_twitter()
        pass
    pass

class Part_III_Twitt_App(threading.Thread):
    def __init__(self): # klass Part_III_Twitt_App
        pass

    def run(self): # klass Part_III_Twitt_App
        pass

    pass

class Part_IV_Twitt_App(threading.Thread):
    def __init__(self): # klass Part_IV_Twitt_App
        pass

    def run(self):      # klass Part_IV_Twitt_App
        pass

    pass

class COORD(Structure):
  """struct in wincon.h."""
  # https://www.burgaud.com/bring-colors-to-the-windows-console-with-python/
  _fields_ = [
    ("X", SHORT),
    ("Y", SHORT)]

class SMALL_RECT(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("Left", SHORT),
    ("Top", SHORT),
    ("Right", SHORT),
    ("Bottom", SHORT)]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("dwSize", COORD),
    ("dwCursorPosition", COORD),
    ("wAttributes", WORD),
    ("srWindow", SMALL_RECT),
    ("dwMaximumWindowSize", COORD)]

# winbase.h
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# wincon.h
FOREGROUND_BLACK     = 0x0000
FOREGROUND_BLUE      = 0x0001
FOREGROUND_GREEN     = 0x0002
FOREGROUND_CYAN      = 0x0003
FOREGROUND_RED       = 0x0004
FOREGROUND_MAGENTA   = 0x0005
FOREGROUND_YELLOW    = 0x0006
FOREGROUND_GREY      = 0x0007
FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

BACKGROUND_BLACK     = 0x0000
BACKGROUND_BLUE      = 0x0010
BACKGROUND_GREEN     = 0x0020
BACKGROUND_CYAN      = 0x0030
BACKGROUND_RED       = 0x0040
BACKGROUND_MAGENTA   = 0x0050
BACKGROUND_YELLOW    = 0x0060
BACKGROUND_GREY      = 0x0070
BACKGROUND_INTENSITY = 0x0080 # background color is intensified.

stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo


def get_text_attr():
    """Returns the character attributes (colors) of the console screen
    buffer."""
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
    return csbi.wAttributes


def set_text_attr(color):
  """Sets the character attributes (colors) of the console screen
  buffer. Color is a combination of foreground and background color,
  foreground and background intensity."""
  SetConsoleTextAttribute(stdout_handle, color)





class Our_Tools_py3(threading.Thread):

    def disconnect_db(
        self
        , log = True
    ):
        try:
            del self.cursor_mysql_local_tw_app001
            del self.connect_mysql_local_tw_app01
            
            if log == True:
                txt = str(datetime.datetime.now()) + ": db(" + self.database + ')@' + self.server + ": Disconnected ( " + self.type + " )"
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
                print ("Connection OK with mysql")
                
                txt = str(datetime.datetime.now()) + ": db(" + database01 + ")@" + server01 + ": Connection OK, ( " + type +" )"
                
                if log == True:
                    print(txt, file = open(self.log_file, "a"))
        except Exception as mysql_error:
            logging.exception("message")
            pass
        pass

    @staticmethod
    def write_append_to_file(
            path_file = "test_append.txt",
            txt_to_add = "this is anotehr test",
    ):

        print(txt_to_add, file = open(path_file, "a"))
        
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

    @staticmethod
    def csv_read_content(
        path_file_csv = 'file001.csv',
        delimiter = '|'
    ):
        # print "coco"
        # print res
        res = []
        list01 = Our_Tools_py3.csv_read_all(
            path_file_csv = path_file_csv,
            delimiter = delimiter)[1:]
        for elem in list01:
            res.append(elem)
        return res
        # for elem in list01:
            # print elem


    @staticmethod
    def csv_read_all(
        path_file_csv = 'file001.csv',
        delimiter = '|' 
    ):
        res = []
        with open(path_file_csv) as csv_read:
            reader = csv.reader(
                csv_read, delimiter = delimiter)
            for row in reader:
                res.append(row)
            # print "another_line"
        return res

    @staticmethod
    def read_csv_from_pandas(
        csv_file = r'file001.csv'
        , delimiter = ','
    ):
        csv_content = pd.read_csv(
            csv_file
            , sep = delimiter
        )
        return csv_content
        # #                                                   review sentiment
        # # 0      One of the other reviewers has mentioned that ...  positive
        # # 1      A wonderful little production. <br /><br />The...  positive

    def twitter_retweet001(self):
        # https://stackoverflow.com/questions/38872195/tweepy-exclude-retweets

        # Consumer keys and access tokens, used for OAuth
        consumer_key = config['twitter001']['CONSUMER_KEY']
        consumer_secret = config['twitter001']['CONSUMER_SECRET']
        access_token = config['twitter001']['ACCESS_TOKEN']
        access_token_secret = config['twitter001']['ACCESS_TOKEN_SECRET']

        # OAuth process, using the keys and tokens
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)


        api = tweepy.API(auth)
        # Open/Create a file to append data
        csvFile = open('file001.csv', 'a')
        #Use csv Writer
        csvWriter = csv.writer(csvFile)


        ids = set()
        i = 0
        rate_limit = 5 # afaik, this should NOT go beyond 2335
        # # you have to wait 

        search = "java"

        result_tweet_search = tweepy.Cursor(
            api.search
            , q = search
            , include_entities = True
        ).items()

        # https://stackoverflow.com/questions/21308762/avoid-twitter-api-limitation-with-tweepy?rq=1
        while True:
            try:
                tweet = result_tweet_search.next()
                # Insert into db
            except tweepy.TweepError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break

        # for tweet in tweepy.Cursor(api.search, 
        #                     q="docker", 
        #                     Since="2016-08-09", 
        #                     #until="2014-02-15", 
        #                     lang="en").items(rate_limit):
        #     print (tweet)
            # there will be a rate_limit = 2335
            
            # if not tweet.retweeted:
            #     print (tweet.retweeted)
            #     print (i)
            #     i += 1
       
    def twitter_auth001(self):
        CONSUMER_KEY = config['twitter001']['CONSUMER_KEY']
        CONSUMER_SECRET = config['twitter001']['CONSUMER_SECRET']
        OAUTH_TOKEN = config['twitter001']['access_token']
        OAUTH_TOKEN_SECRET = config['twitter001']['access_token_secret']

        self.auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
        self.twitter_api = twitter.Twitter(auth=self.auth)

        # print (twitter_api)
        # # <twitter.api.Twitter object at 0x0000027CDC91BEF0>

        WORLD_WOE_ID = 1
        US_WOE_ID = 23424977

        world_trends = self.twitter_api.trends.place(_id=WORLD_WOE_ID)
        us_trends = self.twitter_api.trends.place(_id=US_WOE_ID)
        
        # print (world_trends)
        # # [{'trends': [{'name': '#KarneGünü', 'url': 'http://twitter.com/search?q=%23KarneG%C3%BCn%C3%BC', 'promoted_content': None, 'query': '%23KarneG%C3%BCn%C3%BC', 'tweet_volume': 12103}, {'name': 
        print (us_trends)
        # # [
        # # # {'trends': [
        # # # # {
        # # # # # 'name': '#ReleaseTheMemo', 
        # # # # # 'url': 'http://twitter.com/search?q=%23ReleaseTheMemo', 
        # # # # # 'promoted_content': None, 
        # # # # # 'query': '%23ReleaseTheMemo', 
        # # # # # 'tweet_volume': 888816
        # # # # }, {'name': '#FridayFeeling', 'url': 'http://twit
        pass

    @staticmethod
    def test_twitter_trending_topics():
        t = twitter.Twitter(domain='api.twitter.com', api_version='1')

        print (json.dumps(t.trends(), indent=1))

        pass

    @staticmethod
    def oauth_login(app_name='',
        consumer_key='',
        consumer_secret='',
        token_file='out/twitter.oauth'
    ):
        try:
            (access_token, access_token_secret) = read_token_file(token_file)
        except IOError as e:
            (access_token, access_token_secret) = oauth_dance(
                app_name, consumer_key, consumer_secret)
            if not os.path.isdir('out'):
                os.mkdir('out')
            write_token_file(token_file, access_token, access_token_secret)
            print ("OAuth Success. Token file stored to: ", token_file)

        print ('Authentication OK')




        # # otrn we mtad anze resaka important ao am FB ao
        # # tsy nety ito
        # t = twitter.Twitter(domain='api.twitter.com', api_version='1')
# 
        # print (json.dumps(t.trends(), indent=1))



        # Q = ' '.join(sys.argv[1])
        Q = 'python java'
        MAX_PAGES = 15
        RESULTS_PER_PAGE = 100
        twitter_search = twitter.Twitter(domain="search.twitter.com")

        print (twitter_search)

        search_results = []
        for page in range(1,MAX_PAGES+1):
            search_results += twitter_search.search(q=Q, rpp=RESULTS_PER_PAGE, page=page)['results']
        print (json.dumps(search_results, indent=1))

        # return twitter.Twitter(
            # domain='api.twitter.com', api_version='1',
            # auth=twitter.oauth.OAuth(access_token, access_token_secret,
                # consumer_key, consumer_secret
            # )
        # )

    @staticmethod
    def import_twitter_api():
        import os
        import sys
        import twitter
        from twitter.oauth import write_token_file, read_token_file
        from twitter.oauth_dance import oauth_dance
        print ('Imported Twitter_api')
        pass

    @staticmethod
    def get_some_part_of_page(
        url = config["urls"]["test002"]
    ):
        content = Our_Tools_py3.get_content_of_url()
        a_s = content.find_all("div")

        print (a_s)

        # for a in a_s:
        #     print (a)
        pass
        pass

    @staticmethod
    def get_links_of_url(
        url = config["urls"]["test002"]
    ):
        url__content_of_page = Our_Tools_py3.get_content_of_url(url)
        res = []
        for link in url__content_of_page.find_all('a'):
            res.append(link.get('href'))
            pass
        return res
        pass

    @staticmethod
    def get_content_of_url(
        url = config["urls"]["test002"]
    ):
        url_request  = requests.get("http://" +url)
        url_content_of_page = BeautifulSoup(url_request.text)
        return url_content_of_page
        pass

    @staticmethod
    def print_green(
            txt = "this is a test",
            new_line = True):
        default_colors = get_text_attr()
        default_bg = default_colors & 0x0070
        set_text_attr(
            FOREGROUND_GREEN | 
            default_bg |
            FOREGROUND_INTENSITY)
        if new_line == True:
            print( txt)
        else:
            print( txt, end = "")
        set_text_attr(default_colors)

    @staticmethod
    def print_blue(txt = "this is a test",
            new_line = True):
        default_colors = get_text_attr()
        default_bg = default_colors & 0x0070
        set_text_attr(
            FOREGROUND_BLUE | 
            default_bg |
            FOREGROUND_INTENSITY)
        if new_line == True:
            print (txt)
        else:
            print (txt, end = "")
        set_text_attr(default_colors)


    @staticmethod
    def print_red(
            txt = "this is a test",
            new_line = True
    ):
        default_colors = get_text_attr()
        default_bg = default_colors & 0x0070
        set_text_attr(
            FOREGROUND_RED | 
            default_bg |
            FOREGROUND_INTENSITY)
        if new_line == True:
            print (txt)
        else:
            print (txt, end = "")
        set_text_attr(default_colors)

    @staticmethod
    def usage():
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')


        print ("Usage: ")
        Our_Tools_py3.print_green (txt = "Option: -h, --help")
        print ("> Our_Tools.py -h")
        print ("> Our_Tools.py --help")
        print ("- - mtov n zvt atwnreo")
        print ("- - hamoaka ny 'help' ireo")
    pass



def main():
    try:
        #opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:", ["help","listen","execute","target","port","command","upload"])
        opts, args = getopt.gnu_getopt(sys.argv[1:],
            "T",
            [
                "all_test"
            ]
        )
    except getopt.GetoptError as err:
        print (str(err))
        Our_Tools_py3.usage() 

    if len (sys.argv) == 1:
        Our_Tools_py3.usage()
        sys.exit(0)
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_freelance003')
    ):
        part_2 = Part_II_Twitt_App()
        part_2.run()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_freelance002')
    ):
        l = Twitter_Listener()
        l.run()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_freelance001')
    ):
        part_I_twitt_app = Part_I_Twitt_App()
        part_I_twitt_app.run()
        pass

    elif (
        (len (sys.argv) == 3)
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mysql002')
    ):
        our_tools_py3 = Our_Tools_py3()
        res_query = our_tools_py3.db_select()
        for line in res_query:
            print (line)
            # for val in line:
            #     print (val)
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mysql001')
    ):
        our_tools_py3 = Our_Tools_py3()
        our_tools_py3.db_not_select(
            test001 = False
            , query01 = "alter table table001 add column pname text"
            , auto_commit = True
        )
        print ('tonga ato')
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_connection_mysql01')
    ):
        our_tools_py3 = Our_Tools_py3()
        our_tools_py3.connect_db()

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_read_csv001')
    ):
        csv_content = Our_Tools_py3.csv_read_all(
            delimiter = ','
        )
        print(csv_content)
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_pandas001')
    ):
        csv_content = Our_Tools_py3.read_csv_from_pandas()
        # print (type(csv_content))
        # # <class 'pandas.core.frame.DataFrame'>
        
        # print (csv_content)

        for row in csv_content:
            print (row)
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'twitter_retweet001')
    ):
        our_tools_py3 = Our_Tools_py3()
        our_tools_py3.twitter_retweet001()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_twitter_api002')
    ):
        our_tools_py3 = Our_Tools_py3()
        our_tools_py3.twitter_auth001()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_twitter_api001')
    ):
        # Our_Tools_py3.import_twitter_api()

        APP_NAME = config['twitter001']['APP_NAME']
        CONSUMER_KEY = config['twitter001']['CONSUMER_KEY']
        CONSUMER_SECRET = config['twitter001']['CONSUMER_SECRET']
        Our_Tools_py3.oauth_login(
            APP_NAME, CONSUMER_KEY, CONSUMER_SECRET
        )

        # Our_Tools_py3.test_twitter_trending_topics()

        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_beautiful_soup004')
    ):
        content = Our_Tools_py3.get_content_of_url()
        a_s = content.find_all("div", "cls-content")
        for a in a_s:
            print (a)
        pass
        # content.
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_beautiful_soup003')
    ):
        content = Our_Tools_py3.get_content_of_url()
        print (content)
        

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_beautiful_soup002')
    ):
        links = Our_Tools_py3.get_links_of_url()
        print (links)
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_beautiful_soup001')
    ):
        url = config["urls"]["test002"]
        url_request  = requests.get("http://" +url)
        url_content_of_page = BeautifulSoup(url_request.text)
        for link in url_content_of_page.find_all('a'):
            print(link.get('href'))
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_config_parser001')
    ):
        # # do not understand, if this is uncommented, then the 
        # # # -T test_beautiful_soup001... will NOT work
        # config = configparser.ConfigParser()
        # config.read('all_confs.txt')
        # print(config["urls"]["test001"])

        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test001')
    ):
        print ("this is a super test")
        pass


if __name__ == '__main__':
    main()
