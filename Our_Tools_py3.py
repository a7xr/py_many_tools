import os
import re
import sys
import getopt
import threading

from bs4 import BeautifulSoup
import requests

import configparser


from ctypes import windll, Structure, c_short, c_ushort, byref
SHORT = c_short
WORD = c_ushort

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





config = configparser.ConfigParser()
config.read('all_confs.txt')

class Our_Tools_py3(threading.Thread):

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
