# -*- coding: latin-1 -*-

# to delete the commented_lines in python
# # sed -e '/^ *#/d' file001.py > file001_no_comments.py
#
# to delete the void lines
# # sed '/^$/d'

import os

import re
import sys
sys.path.append("..")
import getopt
import xlsxwriter
import csv
import time


# lasa zao 

from Tools.Tools_PDF import Tools_PDF
from Tools.Tools_Basic import Tools_Basic
from Tools.Tools_System import Tools_System
from Tools.Tools_File import Tools_File
from Tools.Tools_Excel import Tools_Excel
from Tools.Tools_Basic import Tools_Basic
from Tools.Tools_Beautiful_Soup import Tools_Beautiful_Soup
from Test001.All_Tests import Test_to_del
from Test001.All_Tests import To_del001
import sys
import datetime
from datetime import date
import threading
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

from Test999 import coco # Test999 is in the parent_folder 

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
    def materials():
        print('Here are some materials which I used to write this code')
        print('- 1: Effective Python Penetration Testing.pdf _ by Rejah Rehim')
    

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
        # # [{'trends': [{'name': '#KarneGünü', 'url': 'http://twitter.com/search?q=%23KarneG%C3%BCn%C3%BC', 
        # # # 'promoted_content': None, 'query': '%23KarneG%C3%BCn%C3%BC', 'tweet_volume': 12103}, {'name': 
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
    def rcs001(
        url = r'C:/Users/windows010/Documents/RCS/pers_physique/Ramiaka001.html'
    ):
        content_html_to_treat = Tools_Beautiful_Soup.get_content_of_url(
            url = url
        )
        # print("type(content_html_to_treat): ", type(content_html_to_treat))
        # # <class 'bs4.BeautifulSoup'>

        
        

        tbody = content_html_to_treat.find("tbody").find_all("tr")
        headers = []
        value_of_headers = []
        headers_and_value = {}

        for c in tbody:
            # print (c.get_text().split('\n'))
            # ['', ' Immatriculation  ', ': RCS Antananarivo 2016 A 00951', '']
            content_one_line = c.get_text().split('\n')
            content_one_line = [e for e in content_one_line if e not in ('')]

            # print(content_one_line)
            # [' Immatriculation  ', ': RCS Antananarivo 2016 A 00951']

            data = []
            
            col = None
            val = None

            i = 0
            for a in content_one_line:
                
                if i == 0:
                    col = a
                    if col not in headers:
                        headers.append(col)
                    print('col: ', col)
                    i += 1
                    pass
                else:
                    val = a
                    # print(a)
                    value_of_headers.append(val)
                    i = 0
                headers_and_value[col] = val

            print('val: ', val)
            # input()


            

        # print('headers:', headers)
        # # [' Immatriculation  ', ' CivilitÃ© ', ... ]

        # print("value_of_headers: ", value_of_headers)
        # # [': RCS Antananarivo 2016 A 00951', ': Monsieur', ': RAMIAKAJAT

        # print('headers_and_value: ', headers_and_value)

        # print('headers_and_value: ', headers_and_value.pop(r'\t\t\t\t\t\t\t', None))
        # # {' Immatriculation  ': ': RCS Antananarivo 2016 A 00951', ' CivilitÃ© ': ': Monsieur', ' Nom et PrÃ©noms ': ': RAMIAKAJATO Voninahindrainy Jaofera', ' Date de naissance ': ':16/01/1973 ', '\t\t\t\t\t\t\t': ':16/01/1973 ', ' Lieu

        # the previous result contain some key which are sth like a ghost
        del headers_and_value['\t\t\t\t\t\t\t']
        print(headers_and_value)


        with open('result001.csv', 'a') as csv_file:
            fieldnames = headers
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerow(
                headers_and_value
            )

            pass



        # print("len(tbody): ", len(tbody))
        # 10
        # print(tbody)
        # [<tr> <td> <strong>Immatriculation </strong> ... ]
        # print(type(tbody))
        # bs4.element.ResultSet
        

        # tbody = content_html_to_treat.find_all("tbody")

        # print ("tbody: ", tbody)
        # # div:  [<tbody><tr> <td> <strong>Immatriculation ..... </tbody> ]

        # path_html_to_treat = r'C:\Users\windows010\Documents\RCS\pers_physique\Ramiaka001.html'
        # content_html_to_treat = Tools_File.read_file_line_by_line(
            # path_file = path_html_to_treat
        # )
        # d = content_html_to_treat.find_all("div")
        # print ("d: ", d)

        # print ("content_html_to_treat: " + content_html_to_treat)
        # # <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <!-- saved from url=(0064)http://www.rcsmada.mg/index.php?pgdown=consultation&soc=10-43070 --> <html xmlns="http://www.w3.org/1999/xhtml" class="gr__rcsmada_mg"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <title>RNCS-CM MADAGASCAR</title> <link href="./Ramiaka001_files/design3.css" rel="stylesheet" type="text/css"> <meta name="author" content="MTC"> <meta name="copyr
        # # this is going to be the html which contains the data in which we want to extract


        pass
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

    def main_xl(self):
        # Tanjona: Avoaka ny Main_py.xlsx
        # Vakiana ny Main_py.xlsx
        # # Tonga de izai misy zvt ftsn no mnw execution
        # alefa ny execution

        # ny zvt ande hoapdirina ao zao
        # # mapditra zvt ao anaty bdd
        # ##Note omeo ligne ak10 am voloo, depart 01@xl > 00@program
        # ###Mongo omeo ligne ak50, depart 11@xl > 10@program
        # ###Mysql omeo ligne ak50, depart 61@xl > 60@program

        # mnw connection am Mongo
        self.mongo001 = MongoDb()
        self.mongo001.connection()

        self.xl_main_read = "Main_py.xlsx"

        workbook_write = xlsxwriter.Workbook(self.xl_main_read)

        header_format_red = workbook_write.add_format({'bold': True,
                                'align': 'center',
                                'valign': 'vcenter',
                                'fg_color': '#c80815', # 200, 8, 15
                                'border': 1})


        header_format_blue001 = workbook_write.add_format({'bold': True,
                            'align': 'center',
                            'valign': 'vcenter',
                            'fg_color': '#4d8fac', # 77, 143, 172
                            'border': 1})

        header_format_blue002 = workbook_write.add_format({'bold': True,
                            'align': 'center',
                            'valign': 'vcenter',
                            'fg_color': '#a3c7d6', # 163, 199, 214
                            'border': 1})
        header_format_blue002 = workbook_write.add_format({'bold': True,
                            'align': 'center',
                            'valign': 'vcenter',
                            'fg_color': '#a3c7d6', # 163, 199, 214
                            'border': 1})

        sheet_main = workbook_write.add_worksheet('Main')
        cell_format_union = workbook_write.add_format({'align': 'center',
            'valign': 'vcenter',
            'border': 1})
        sheet_main.merge_range('A1:D1', "", 
            cell_format_union)
        sheet_main.merge_range('A2:B2', "", 
            cell_format_union)
                    #    y  x
        sheet_main.write(0, 0, 'Notes', header_format_blue001)
        sheet_main.write(1, 0, 'Mainly KeyWords', header_format_blue002)
        sheet_main.write(1, 2, '#MongoDb')
        sheet_main.write(1, 3, '#MySQL')

        sheet_main.merge_range('A11:D11', "", 
            cell_format_union)
        sheet_main.write(10, 0, '###MongoDb', header_format_blue001)
        sheet_main.write(11, 0, 'Raha ohatra ka hampiditra Fichier anaty MongoDb', header_format_blue002)
        sheet_main.write(13, 0, 'Rah ohatra k hnw Select ao anaty MongoDb', header_format_blue001)

        workbook_write.close()
        os.system(self.xl_main_read)

        test001 = Tools_Excel.read_one_cell_from_xl(
            xl_file = self.xl_main_read
            , sheet_index = 0
            , y = 1 # noho ireo val ireo dia B2 no voavaky
            , x = 1
        )

        # 0 34 38 499 03

        print ('test001: ', test001)

        pass

# def main():
    
#     Our_Tools_py3().main_xl()
    

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
        and (sys.argv[2] == 'rcs_treat_html_code001')
    ): 


        list_url = [
            r'C:/Users/windows010/Documents/RCS/pers_physique/Ramiaka001.html'
            , r'C:/Users/windows010/Documents/RCS/pers_physique/SAM_Ki001.html'
            , r'C:/Users/windows010/Documents/RCS/pers_physique/Hasiniosy.html'
        ]

        with open('result001.csv', 'a') as csv_file:
        for url in list_url:
            Our_Tools_py3.rcs001(
                url = url
            )
        pass

    elif (        
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'read_file_line_by_line')
    ): 
        # path_html_to_treat = r'C:\Users\windows010\Documents\RCS\pers_physique\Ramiaka001.html'
        print(
            Tools_File.read_file_line_by_line()
        )
        pass

    elif (        
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'merge_pdf')
    ): 
        path_pdf = r'C:\Users\windows010\Downloads\Documents\babypips\elementary'
        list_pdf = [
            r'E:\sync_google_drive\babypips\babypips_com_preschool.pdf'
            , r'C:\Users\windows010\Downloads\Documents\babypips\preschool_pics\pic_preschool.pdf'
        ]
        Tools_PDF.merge_pdf(
            merged_pdf = "babypips_com_preschool_with_pics.pdf"
            , list_pdf = list_pdf
        )


    elif (        
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_bonjour_monde')
    ): 
        Test_to_del.bonjour_monde()

    elif (        
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_iota001')
    ): 
        Test_to_del.test_hello_world_iota()
        pass


    elif (        
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_thread_event004')
    ): 
        To_del001.test004()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_thread_semaphore_003')
    ): 
        To_del001.test003()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_thread_barrier002')
    ): 
        To_del001.test002()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_thread_barrier001')
    ): 
        To_del001.test001()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_to_del001')
    ): 
        Test_to_del.to_del001()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_bs007')
    ): 
        Tools_Beautiful_Soup().get_list_lang_of_ted_talk()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_bs006')
    ): 
        bs = Tools_Beautiful_Soup()
        # maka anle id001
        url = 'https://www.ted.com/talks/nina_dolvik_brochmann_and_ellen_stokken_dahl_the_virginity_fraud/transcript'
        # url = 'https://www.ted.com/talks/sofia_jawed_wessel_the_lies_we_tell_pregnant_women/transcript'
        id001 = bs.get_id_of_link_of_ted(url = url)
        # maka anle json_transcript mfandray am id001
        # # fa mbola mila traitena ilay json
        json_to_treat = bs.get_json_of_transcript(id001 = int(id001))
        # traitena ilay json amzai ilay transcript ftsn no azo

        # alaina loo ny key001 ao am json_to_treat
        key001 = json_to_treat.keys()
        # print('key001: ', key001)
        # # dict_keys(['paragraphs'])

        key001 = list(key001)
        key001 = key001[0]
        # print (key001[0])
        # # paragraphs

        # print(json_to_treat[key001])
        # # [{'cues': [{'time': 751, 'text': 'Nina Dølvik Brochman

        for dict_contain_list_of_time_and_transcript in json_to_treat[key001]:
            # print ('do_not_know_yet: ', do_not_know_yet)
            # # {'cues': [{'time': 428446, 'text': 'You can s
            # input()
            # Tools_Basic.long_print()
            list_of_time_and_transcript = dict_contain_list_of_time_and_transcript['cues']
            # print ('list_of_time_and_transcript: ', list_of_time_and_transcript)
            # # [{'time': 273598, 'text': "That's a popula
            # input()
            # Tools_Basic.long_print()
            for time_and_transcript in list_of_time_and_transcript:
                print(time_and_transcript['time'], end = ": ")
                print(time_and_transcript['text'])
                input()
            pass


        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_bs005')
    ): 
        Tools_Beautiful_Soup().get_id_of_link_of_ted()

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_bs004')
    ): 
        Tools_Beautiful_Soup.test_from_book001()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_bs003')
    ): 
        bs = Tools_Beautiful_Soup()
        bs.get_transcript_from_ted()

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_bs002')
    ): 
        
        bs = Tools_Beautiful_Soup()

        # link001 = '/talks/nina_dolvik_brochmann_and_ellen_stokken_dahl_the_virginity_fraud'
        # transcript = '/transcript'
        # link_to_search_transcript = link001 + transcript



        # sys.exit(0)

        folder_content001 = r'E:\DEV\python\ted_transcript'

        for compteur in range(1, 76):
            url_page = "https://www.ted.com/talks?page=" + str(compteur)
            print (compteur)
            links = bs.get_links(url = url_page)
            # print (links)
            main_url = 'https://www.ted.com'
            for link in links:
                # print (folder_content001 + '\\' + link.replace('/', '_'))
                # input()
                container_folder = (folder_content001 + '\\' + link.replace('/', '_'))
                Tools_System.create_folder(container_folder)
                # print (link)
                # # /talks/naoko_ishii_an_economic_case_for_saving_th
                url_transcript = main_url + link + '/transcript'
                
                # print(url_transcript)
                # # https://www.ted.com/talks/david_katz_the_surprising_solution_to_ocean_plastic/transcript
                
                url_w_list_language = bs.get_list_url_talk_w_list_lang(
                    url = main_url + link + '/transcript'
                )
                # print (url_w_list_language)
                # # ['https://www.ted.com/talks/tanya_menon_the_secret_to_great_opportunities_the_person_you_haven_t_met_yet/transcript', '"x-default"', '"en"', '"en"', '"en"']




                id001 = bs.get_id_of_link_of_ted(url = url_w_list_language[0])
                print ('url_w_list_language[1::1]: ', url_w_list_language[1::1])
                # # 
                # input()

                for lang in url_w_list_language[1::1]:
                    if lang == '"x-default"':
                        pass
                    else:
                        file_w_lang = container_folder + '\\' + lang.replace('"', '')

                        print('file_w_lang: ', file_w_lang)
                        # # E:\DEV\python\ted_transcript\_talks_peter_ouko_how_i_earned_a_law_diploma_while_on_death_row\ar
                        # input()



                        json_to_treat = bs.get_json_of_transcript(
                            id001 = int(id001)
                            , language = lang.replace('"', '')
                        )

                        key001 = json_to_treat.keys()
                        key001 = list(key001)
                        key001 = key001[0]
                        # print('key001: ', key001)
                        # print('url_w_list_language[0]: ', url_w_list_language[0])
                        # input()
                        for dict_contain_list_of_time_and_transcript in json_to_treat[key001]:
                            list_of_time_and_transcript = dict_contain_list_of_time_and_transcript['cues']
                            for time_and_transcript in list_of_time_and_transcript:
                                print(
                                    # query01.encode('ISO-8859-1')
                                    time_and_transcript['time'], 
                                    end = ": ", 
                                    file=open(file_w_lang, "a")
                                )
                                try:
                                    print(
                                        time_and_transcript['text'].encode(
                                            'ISO-8859-1'
                                        )
                                        , file=open(file_w_lang, "a")
                                    )
                                except UnicodeEncodeError:
                                    pass

                        # vita ny language01 am lien01
                        time.sleep(20)



            print (compteur)
            Tools_Basic.long_print()
            time.sleep(100000)


        # sys.exit(0)
        
        # l = bs.get_links()
        # print(l)
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_bs001')
    ): 
        bs = Tools_Beautiful_Soup()
        # bs.get_title(("http://www.pythonscraping.com/pages/page1.html"))
        # bs.get_title(("http://www.pythonscraping.com/pages/warandpeace.html"))
        
        bs.get_title()
        print(bs.get_from_tag())

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_action_select004')
    ): 
        MongoDb().action_select_file(
            print_only = 0
            , json_filter = {
                'path_file_origin':{
                    '$regex': '.*tsiakoraka.*'
                }
            }
        )
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_action_select003')
    ): 
        MongoDb().action_select_file(
            print_only = 0
            , json_filter = {
                'file_name_origin': {
                    '$regex': 'Introducing Ethereum and Solidity.*'
                }
            }
        )
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_action_select002')
    ): 
        MongoDb().action_select_file()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_action_select001')
    ): 
        # m = MongoDb()
        # m.connection()
        res = MongoDb().action_select_not_file(
            collection = 'appli'
            , database = 'db002'
            , json_filter = {
                'name_exe': {
                    '$regex': '.*foxit.*'
                }
            }
        )
        for r in res:
            print(r)
        pass
        
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_xlrd002')
    ): 
        val00 = Tools_Excel.read_one_col_of_sheet_xl()
        print('val00: ', val00)
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_xlrd001')
    ): 
        val00 = Tools_Excel.read_one_cell_from_xl()
        print('val00: ', val00)
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_update_mongo001')
    ): 
        MongoDb().action_not_select(
            action = 'update_not_file'
            , collection = 'person'
            , doc_of_file_or__not_file = (
                {"alias":"alias001"},
                {"$set":{"alias":"alias from update"}}
            )
        )
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_system005')
    ): 
        a = Tools_Basic().crawl_into_folder()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_system004')
    ): 
        Tools_System().insert_folder()
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_system003')
    ): 
        # walk_dir = r'E:\Serie'
        walk_dir = r'E:\New folder'
        for root, subdirs, files in os.walk(walk_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                print('(full path: %s)' % (file_path))

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_system002')
    ): 
        s = Tools_System().get_file_from_mongodb()
        pass
    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'set_file_del_sys001')
    ): 
        s = Tools_System().set_file_to_mongodb__del_in_sys(
            path_file = r'G:\doc\cryptocurrency\Introducing Ethereum and Solidity.pdf'
        )
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_appli002')
    ): 
        app = MongoDb().modify_file(
            patt_to_search_in_file_name = 'msg_03'
        )

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_appli001')
    ): 
        app = MongoDb().exe_one_file(
            file_name = 'Newral'
        )
        # print ('app: ', app)
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb009')
    ):
    # C:\Program Files (x86)\Foxit Software\Foxit Reader
        MongoDb().action_not_select(
            action = 'insert_not_file'
            , collection = 'appli'
            , doc_of_file_or__not_file = {
                'path_exe': r'C:\Program Files (x86)\Foxit Software\Foxit Reader\FoxitReader.exe'
                , 'name_exe': 'foxit_reader'
                , 'version': """
Version 8.1.0.1013                
"""
                , 'type_os': 'Windows'
            }
        )
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'search_file_in_mongodb')
    ):
        words_to_search = 'Android Cookbook'
        try: 
            path_file = MongoDb().action_select(
                action = 'find_file'
                , print_only = True
                , doc_of_file_or__not_file = {
                    'path_file_origin': {
                        '$regex': '.*'+ words_to_search +'.*'
                    }
                }
            )
        except gridfs.errors.NoFile:
            print()
            print ('The file('+ words_to_search +') you wanted is missing')
            print()
            return
        pass

    elif (
        (len (sys.argv) == 3) 
        and (sys.argv[1] in ("-T", "--all_test"))
        and (sys.argv[2] == 'test_mongodb011')
    ):
        MongoDb().action_not_select(
            collection = 'file_inserted'
            , action = 'delete_file'
            , doc_of_file_or__not_file = {
                'file_name_origin': 'CentOS-7-x86_64-DVD-1503-01.iso'
            }
        )
        print('file deleted 345HDHDFGH463456DF')

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
        and (sys.argv[2] == 'test_insert_file_mongodb001')
    ):
        MongoDb().action_not_select(
            collection = 'file_inserted'
            , action = 'insert_file'
            , doc_of_file_or__not_file = {
                'path_file_origin': r'G:\CentOS-7-x86_64-DVD-1503-01.iso'
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
        and (sys.argv[2] == 'test_insert_mysql001')
    ):
        our_tools_py3 = Our_Tools_py3()
        our_tools_py3.db_not_select(
            test001 = False
            , query01 = "insert into twitter_app (id_str) values ('coco')"
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

        coco()

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

