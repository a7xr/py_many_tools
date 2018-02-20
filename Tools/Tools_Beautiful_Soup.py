
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from .Tools_Basic import Tools_Basic
import re
import json
import time

class Tools_Beautiful_Soup:

    def get_id_of_link_of_ted(
        self
        , url = 'https://www.ted.com/talks/nina_dolvik_brochmann_and_ellen_stokken_dahl_the_virginity_fraud/transcript'
    ):
        self.html = urlopen(url)
        self.bsObj = BeautifulSoup(self.html)

        tag_to_search = 'meta'
        about_the_field = {"property": "al:ios:url"}

        meta_contains__id_transcript = self.bsObj.findAll(tag_to_search, about_the_field)

        # print(type(meta_contains__id_transcript))
        # # <class 'bs4.element.ResultSet'>

        # print (meta_contains__id_transcript)
        # # [<meta content="ted://talks/9126?source=facebook" property="al:ios:url"/>]

        # print (meta_contains__id_transcript[0]['content'])
        # # <meta content="ted://talks/9126?source=facebook" property="al:ios:url"/>

        # print (meta_contains__id_transcript[0]['content'])
        # # ted://talks/9126?source=facebook

        contain_id_transcript = meta_contains__id_transcript[0]['content']

        part_2_contain_id_transcript = contain_id_transcript.rsplit('/', 1)[1]
        # print ("part_2_contain_id_transcript: ", part_2_contain_id_transcript)
        # # 9126?source=facebook
        id001 = part_2_contain_id_transcript.rsplit('?', 1)[0]
        # print('id001: ', id001)
        # # 9126
        return id001


    def treat_json_to_get_transcript(
        self
        , json_to_treat = ''
    ):

        pass

    def get_json_of_transcript(
        self
        , id001 = 9126
        , language = 'en'
    ):
        url_contains_json = 'https://www.ted.com/talks/' + str(id001) + '/transcript.json?language=' + str(language)

        # print('url_contains_json: ', url_contains_json)
        # input()
        self.html = urlopen(url_contains_json)
        self.bsObj = BeautifulSoup(self.html)
        # print(self.bsObj)
        # # <html><body><p>{"paragraphs":[{"cues":[{"time":751,"text":"Nin....

        # print (type(self.bsObj))
        # # <class 'bs4.BeautifulSoup'>

        # print (self.bsObj.string)
        # # {"paragraphs":[{"cues":[{"time":751,"text":"Nina Dølvik Brochmann:\nWe

        # print (self.bsObj.get_text())
        # # {"paragraphs":[{"cues":[{"time":751,"text":"Nina Dølvik Brochmann:\nWe

        json_to_treat = self.bsObj.get_text()

        json_to_treat = json.loads(json_to_treat)

        # print(json_to_treat.get("paragraphs"))
        # # [{'cues': [{'time': 751, 'text': 'Ni....

        # print(json_to_treat.keys())
        # # dict_keys(['paragraphs'])

        # print(json_to_treat['paragraphs'][0])
        # # {'cues': [{'time': 751, 'text': 'Nina Dølvik Brochmann:\nWe grew up b

        # print(json_to_treat['paragraphs'][0].keys())
        # # dict_keys(['cues'])

        # print (json_to_treat['paragraphs'][0]['cues'])
        # # [{'time': 751, 'text': 'Nina Dølv...

        # print (json_to_treat['paragraphs'][0]['cues'][0])
        # # {'time': 751, 'text': 'Nina Dølvik Brochmann:\nWe grew up believing'}

        # print (json_to_treat['paragraphs'][0]['cues'][0]['time'])
        # # 751

        # print (json_to_treat['paragraphs'][0]['cues'][0]['time'])
        # json_to_treat = dict
        # json_to_treat['paragraphs'] = list
        # json_to_treat['paragraphs'][0] = dict
        # json_to_treat['paragraphs'][0]['cues'] = list
        # json_to_treat['paragraphs'][0]['cues'][0] = dict
        # json_to_treat['paragraphs'][0]['cues'][0]['time'] = value_string
        return json_to_treat



        pass


    # this is going to return list of language of one_talk
    def get_list_url_talk_w_list_lang(
        self
        , url = 'https://www.ted.com/talks/sofia_jawed_wessel_the_lies_we_tell_pregnant_women/transcript'
    ):
        """
        Got this from material_1_p124
        """
        try:
            self.html = urlopen(url)
        except urllib.error.HTTPError:
            time.sleep(60)
            pass
        self.bsObj = BeautifulSoup(self.html)
        
        tag_to_search = 'link'
        about_the_field = {"rel": "alternate"}

        list_to_grab_lang = self.bsObj.findAll(tag_to_search, about_the_field)

        # print ('list_to_grab_lang: ', list_to_grab_lang)
        # [<link href="https://www.ted.com', ....

        # print(type(list_to_grab_lang[0]))
        # # <class 'bs4.element.Tag'>

        # print ('list_to_grab_lang[0]', list_to_grab_lang[0])
        # # <link href="https://www.ted.com/talks/sofia_jawed_wessel_the_lies_we_tell_pregnant_women" hreflang="x-default" rel="alternate"/>
        res = []
        res.append(url)
        for where_to_grab_lang in list_to_grab_lang:
            try:
                part2 = str(where_to_grab_lang).rsplit('hreflang=', 1)[1]
            except IndexError:
                pass
            # print ('part2:', part2)
            # #  "x-default" rel="alternate"/>
            list_to_grab_lang001 = part2.split()
            # print ('list_to_grab_lang001: ', list_to_grab_lang001)
            # print ('lang: ', list_to_grab_lang001[0])
            # # "pt-br"
            # print (list_to_grab_lang001[0])
            # input_w_url_talk()
            res.append(list_to_grab_lang001[0])

        return res

    @staticmethod
    def test_from_book001():
        from urllib.request import urlopen
        from bs4 import BeautifulSoup
        import re
        # url = "http://www.pythonscraping.com/pages/page3.html"
        url = "https://www.ted.com/talks/nina_dolvik_brochmann_and_ellen_stokken_dahl_the_virginity_fraud/transcript"
        html = urlopen(url)
        # print (html)
        # # <http.client.HTTPResponse object at 0x000001A7E851D9E8>
        bsObj = BeautifulSoup(html)
        print (bsObj)
        # input()



        # images = bsObj.findAll("img", {"src":re.compile("\.\.\/img\/gifts/img.*\.jpg")})
        # for image in images:
        #     print(image["src"])
        # pass

    def get_transcript_from_ted(
        self
        , url = "https://www.ted.com/talks/nina_dolvik_brochmann_and_ellen_stokken_dahl_the_virginity_fraud/transcript"
    ):
        self.html = urlopen(url)
        self.bsObj = BeautifulSoup(self.html)

        # contents = self.bsObj.findAll("img", 
        contents = self.bsObj.findAll("a"
            # , {
            #     "src" : re.compile("\.\.\/img\/gifts/img.*\.jpg")
            # }
        )
        for content in contents:
            print (content.string)
            # print(image["src"])

    def get_title(self
        , url = "https://www.ted.com/talks"
    ):
        try:
            self.html = urlopen(url)
        except HTTPError as e:
            return None
        try:
            self.bs_obj = BeautifulSoup(self.html.read())
            title = self.bs_obj.body.h1
        except AttributeError as e:
            return None
        return title

    def get_from_tag(
        self
        , tag_to_search = "img"
        , about_the_field = {"class":" thumb__image"}
    ):
        self.name_list = self.bs_obj.findAll(tag_to_search, about_the_field)
        return self.name_list
        pass

    def get_links(self
        # url = "http://en.wikipedia.org/wiki/Kevin_Bacon"
        , url = "https://www.ted.com/talks?page=1"
        , tag = "a"
        , field = 'href'
    ):

        self.html = urlopen(url)
        self.bsObj = BeautifulSoup(self.html)
        res = []
        for link in self.bsObj.findAll(tag):    # alaina ny ao anatinle <a>
            if 'href' in link.attrs: # maka ireo lien
                if (
                    (
                        ('/talks/' in link.attrs[field])
                    )
                ): # ireo lien misy /talks ihany no stoomn
                    # print (link.attrs)
                    # print (link)
                    res.append(link.attrs[field])
                    # print ()
                # print(link.attrs['href'])
        res = set(res)
        return res
        pass