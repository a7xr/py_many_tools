import os

import re
import sys
import getopt
import csv

from Tools.Tools_Basic import Tools_Basic

import sys
import datetime
from datetime import date
import threading
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

from Tools.Tools_Pics import Tools_Pics
from Tools.Tools_MatPlotLib import MatPlotLib
from Tools.Tools_Selenium import Tools_Selenium
from Tools.Print_Color import Print_Color
from Tools.Tools_MySQL import MySQL
from Tools.Tools_MongoDb import MongoDb

from Freelance.Twitter001 import Twitter_Code
from Machine_Learning.Machine_Learning import *

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


class Our_Tools_py3(threading.Thread):

    @staticmethod
    def write_append_to_file(
            path_file = "test_append.txt",
            txt_to_add = "this is anotehr test",
    ):

        print(txt_to_add, file = open(path_file, "a"))

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
    def usage():
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')


        print ("Usage: ")
        Our_Tools_py3.print_green (txt = "Option: -h, --help")
        print ("> Our_Tools_py3.py -h")
        print ("> Our_Tools_py3.py --help")
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
        and (sys.argv[2] == 'test_appli001')
    ): 
        app = MongoDb().exe_one_file(
            file_name = 'eclipse'
        )
        # print ('app: ', app)
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb009')
    ):
        MongoDb().action_not_select(
            action = 'insert_not_file'
            , collection = 'appli'
            , doc_of_file_or__not_file = {
                'path_exe': r'C:\Windows\SysWOW64\mspaint.exe'
                , 'name_exe': 'mspaint'
                , 'version': """
Version 1709 (OS Build 16299.192)
"""
                , 'type_os': 'Windows'
            }
        )
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb008')
    ):
        res_query = MongoDb().action_select(
            # collection = 'file_inserted'
            action = 'find_file'
            , patt_to_search_in_file_name = 'Newral'
        )
        # for val in res_query:
        #     print('val: ', val )
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb011')
    ):
        MongoDb().action_not_select(
            collection = 'person'
            , action = 'delete_file'
            , doc_of_file_or__not_file = {
                'file_name_origin': 'Gothic Storm - Newral takeover.mp3'
            }
        )

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb010')
    ):
        MongoDb().action_not_select(
            collection = 'person'
            , action = 'delete_not_file'
            , doc_of_file_or__not_file = {
                'file_name_origin': r"Gothic Storm - Newral takeover.mp3"
            }
        )

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb007')
    ):
        MongoDb().action_not_select(
            collection = 'file_inserted'
            , action = 'insert_file'
            , doc_of_file_or__not_file = {
                'path_file_origin': r'E:\New folder\extracted\FOR HONOR\Gothic Storm - Newral takeover.mp3'
                , 'type': 'mp3'
            }
            , 
        )
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb006')
    ):
        MongoDb().action_not_select(
            collection = 'user'
            , action = 'insert_not_file'
            , doc_of_file_or__not_file = {
                'user_name': 'super potatoe'
            }
        )
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb_select003')
    ):
        # this is the same as:
        # # where alias like '%t%'
        res_query = MongoDb().action_select(
            collection = 'person'
            , action = 'find_not_file'
            # don_t know, why this one doesn_t work
            , doc_of_file_or__not_file = {
                'alias':{
                    '$regex': '.*t.*'
                }
            }
            , projection = {
                'alias': 1
                , 'phone': 1
                , '_id': 0
            }
        )
        print ('res_query: ', res_query)
        print ('res_query.count(): ', len(res_query))
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb_select002') # tsy mande
    ):
        # this is the same as:
        # # where alias like '%t%'
        res_query = MongoDb().action_select(
            collection = 'person'
            , action = 'find_not_file'
            # don_t know, why this one doesn_t work
            , doc_of_file_or__not_file = {
                {}
            }
        )
        print ('res_query: ', res_query)
        print ('res_query.count(): ', len(res_query))
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb_select001')
    ):
        # this is the same as:
        # # where alias like '%t%'
        res_query = MongoDb().action_select(
            collection = 'person'
            , action = 'find_not_file'
            # , doc_of_file_or__not_file = {
            #     'alias': 'a'
            # }
            , doc_of_file_or__not_file = {
                'alias':{
                    '$regex': '.*t.*'
                }
            }
        )
        print ('res_query: ', res_query)
        print ('res_query.count(): ', len(res_query))
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb004')
    ):
        m = MongoDb()
        m.connection()
        res = m.action_select(
            collection = 'person'
            , doc = {
                'alias': 'Mamitiana'
            }
        )
        
        for val in res:
            print('val: ', val)

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb003')
    ):
        m = MongoDb()
        m.connection()
        m.action_not_select(
            collection = 'user'
            , doc = {
                'user_name': 'user02'
            }
        )

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb002')
    ):
        m = MongoDb()
        m.connection()
        m.action_not_select()

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb001')
    ):
        MongoDb().connection()

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_face_detect003')
    ):
        Tools_Pics.face_detect_from_webcam()

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_face_detect002')
    ):
        Tools_Pics.face_detect002()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_camshift001')
    ):
        Tools_Pics.camshift001()
        pass


    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_face_detect')
    ):
        Tools_Pics.face_detect_from_pic()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_meanshift001')
    ):
        Tools_Pics.meanshift001()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_capture_cam002')
    ):
        Tools_Pics.capture_camera002()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_read_video001')
    ):
        Tools_Pics.play_video_from_file()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_camera001')
    ):
        Tools_Pics.capture_camera001()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_pics002')
    ):
        Tools_Pics.show_image002()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_pics001')
    ):
        Tools_Pics.show_image001()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot021')
    ):
        MatPlotLib.test019()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot020')
    ):
        MatPlotLib.test018()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot019')
    ):
        MatPlotLib.test017()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot018')
    ):
        MatPlotLib.test016()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot017')
    ):
        MatPlotLib.test015()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot016')
    ):
        MatPlotLib.test014()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot015')
    ):
        MatPlotLib.test013()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot014')
    ):
        MatPlotLib.test012()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot013')
    ):
        MatPlotLib.test011()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot012')
    ):
        MatPlotLib.test010()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot011')
    ):
        MatPlotLib.test009()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot010')
    ):
        MatPlotLib.test008()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot009')
    ):
        MatPlotLib.test007()
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot008')
    ):
        MatPlotLib.test006()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot007')
    ):
        MatPlotLib.test005()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot006')
    ):
        MatPlotLib().draw_bar_from_list(vert_or_horiz = 'horiz')
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot005')
    ):
        MatPlotLib.test004()
        
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot004')
    ):
        MatPlotLib.test003()
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot003')
    ):
        MatPlotLib.test002()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot002')
    ):
        matPlotLib = MatPlotLib()
        matPlotLib.draw_plot()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_matplot001')
    ):
        MatPlotLib.test001()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_selenium001')
    ):
        tools_selenium = Tools_Selenium()
        tools_selenium.init_selenium_chrome()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mysql101')
    ):
        mysql = MySQL()

        res_query = mysql.db_select()
        for line in res_query:
            print (line)
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_print_color001')
    ):
        Print_Color.print_green(
            txt = 'this is a test'
        )
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_machine001')
    ):
        Machine_Learning.machine_learning()
        pass
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
