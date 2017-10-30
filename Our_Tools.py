# -*- coding: latin-1 -*-
# probleme sur les accents et les special_char
# # https://www.python.org/dev/peps/pep-0263/

# default value of HKEY_CURRENT_USE\Software\Microsoft\Internet Explorer\Main\Start Page
# # http://go.microsoft.com/fwlink/?LinkId=69157

# def importation_installation():

import os
import re
import sys
import getopt
import logging
import threading
import time
from msvcrt import getch
import urllib
import fileinput
import shutil
from _winreg import *
import csv

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('all_confs.ini')

try:
    import psycopg2
except Exception:
    print "psycopg2 doit etre installee"
    raw_input()
    os.system("pip install psycopg2")
try:
    import xlwt
except Exception:
    print "xlwt doit etre installee"
    raw_input()
    os.system("pip install xlwt")
try:
    import xlrd
except Exception:
    print "xlrd doit etre installee"
    raw_input()
    os.system("pip install xlrd")
try:
    import xlsxwriter
except Exception:
    print "xlsxwriter doit etre installee"
    raw_input()
    os.system("pip install xlsxwriter")

print "Toute les packets utils au bon fonctionnement du programme sont installees"

# importation_installation()

reload(sys)
sys.setdefaultencoding("cp1252")


# based on: 
# # 
# # 
# # when crawling for file or for folder
# # # https://stackoverflow.com/questions/2212643/python-recursive-folder-read
# # #
# # # when checking for the depth of the crawl
# # # # https://stackoverflow.com/questions/42720627/python-os-walk-to-certain-level

"""
Colors text in console mode application (win32).
Uses ctypes and Win32 methods SetConsoleTextAttribute and
GetConsoleScreenBufferInfo.

$Id: color_console.py 534 2009-05-10 04:00:59Z andre $
"""

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















class Person:
    def __init__(self):
        print "this is a test"












class Our_Tools(threading.Thread):


    @staticmethod
    def long_print(num = 10):
        for i in range(num):
            print
        pass

    @staticmethod
    def read_file_line_by_line(path_file = "ti.txt"):
        res = ""
        with open(path_file) as open_file_path:
            for line in open_file_path:
                res += line
        return res



    @staticmethod
    def replacer_factory(spelling_dict):
        def replacer(match):
            word = match.group()
            return spelling_dict.get(word, word)
        return replacer

    @staticmethod
    def replace_in_file(
            path_file_input = "ti.txt",
            path_file_output = "ta.txt",
            replacements = {
                "coco": 'toto',
                "tic": """tac
                this is going to be a very long txt
                hereis not yet the end
                looks like this is the end
                finally, the end"""
            }):
        with open(path_file_input) as infile, open(path_file_output, 'w') as outfile:
            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)
        pass

    @staticmethod
    def manage_usb_store_w_regedit(state = 3):
        # state = 3 > activated
        # state = 4 > deactivated

        # this has to be run as an administrator_account
        keyVal = r'SYSTEM\CurrentControlSet\services\USBSTOR'

        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\services\\USBSTOR', 
            0
            , KEY_ALL_ACCESS      # this is going to create error... have to #dig more
            )

            # print "key"
            # print key
#             
            # result = QueryValueEx(key, "Start")
# 
            # print "result"
            # print result

            # SetValueEx(key, "Start Page", 0, REG_SZ, "http://www.google.com/")
            SetValueEx(key, "Start", 0, REG_DWORD, state)

            CloseKey(key)

            pass
            # SetValueEx(key, "Start", 0, REG_DWORD, str(state))
            # CloseKey(key)
        except WindowsError:
            Our_Tools.long_print()
            Our_Tools.print_red('Vous devez executer cette commande en compte_Admin 654987312344566')
            pass
        except Exception:
            Our_Tools.long_print()
            Our_Tools.print_red ("there is error 9876568965654654")
            sys.exit(0)
            key = CreateKey(HKEY_CURRENT_USER, keyVal)
        
        # print "done 6549316876"

        pass

    @staticmethod
    def ame_to_bre(text = "this is a test",
        changmt = {
            'tire':'tyre', 
            'color':'colour', 
            'utilize':'utilise',
            'foo': 'bar'
            }):
        pattern = r'\b\w+\b'  # this pattern matches whole words only

        replacer = Our_Tools.replacer_factory(changmt)
        return re.sub(pattern, replacer, text)

    def connect_pg(self, 
            server01 = '127.0.0.1',
            user01='postgres',
            password01='123456',
            database01='saisie'):
        try:

            if(server01 == parser.get('pg_10_5_sdsi', 'ip_host')):
                if (database01 == parser.get('pg_10_5_sdsi', 'database')):
                    try:
                        self.connect_pg_10_5_sdsi
                    except AttributeError:
                        self.connect_pg_10_5_sdsi = psycopg2.connect(
                            "dbname=" + database01
                            +" user=" + user01
                            +" password=" + password01
                            +" host=" + server01
                        )
                        self.connect_pg_10_5_sdsi.set_isolation_level(0)
                        self.cursor_pg_10_5__bdd_sdsi = self.connect_pg_10_5_sdsi.cursor()
                        print "Connection OK au pg10.5 bdd(sdsi)"
    
                elif (database01 == parser.get('pg_10_5_production', 'database')):
                    self.connect_pg_10_5__prod = psycopg2.connect(
                        "dbname=" + database01
                        +" user=" + user01
                        +" password=" + password01
                        +" host=" + server01
                    )
                    self.connect_pg_10_5__prod.set_isolation_level(0)
                    self.cursor_pg_10_5__bdd_prod = self.connect_pg_10_5__prod.cursor()
                    print "Connection OK au pg "+server01+" bdd("+database01+")"
        except(psycopg2.OperationalError):
            print ""
            print ""
            print ""
            print "there is an OperationalError"

    def logging_n_print(self, 
            bool01 = True,
            type_log = "info", # OU warning OU debug
            txt = "text",
            log_only = True):

        if(type_log == "warning"):
            logging.warning(txt)
            if log_only == False:
                print txt
            

        elif (type_log == "info"):
            logging.info(txt)
            if log_only == False:
                print txt

        elif ((type_log == "debug") & (log_only == False)):
            logging.debug(txt)
            if log_only == False:
                print txt

        elif ((type_log == "debug") & (log_only == True)):
            logging.debug(txt)
            if log_only == False:
                print txt


    @staticmethod
    def get_xls_tab_name(
        path_file_xls = 'AG22\\AG08_DescripteurSaisie.xls'
        ):
        pointSheetObj = []
        xl_read = xlrd.open_workbook(path_file_xls)
        pointSheets = xl_read.sheet_names()

        # print pointSheets
        return pointSheets

        # otrn tsy ilaina ireo ambany ireo aah
        # sys.exit(0)

        # for i in pointSheets:
            # pointSheetObj.append(
                # tuple(
                    # (xl_read.sheet_by_name(i),i)))
# 
        # res = []
# 
        # for obj, sh_n in pointSheetObj:
            # res.append(sh_n)
# 
        # return res

    @staticmethod
    def test001():
        try:
            while True:
                print "test"
                time.sleep(1)
        except KeyboardInterrupt:
            print "interrompue"
        pass


    def suppression_gpao_unique(self):
        print "suppression_gpao_unique"
        # print "parser.get('pg_10_5_production', 'ip_host')"
        # print parser.get('pg_10_5_production', 'ip_host')
        # sys.exit(0)
        self.connect_pg(
            server01 = parser.get('pg_10_5_production', 'ip_host'),
            user01=parser.get('pg_10_5_production', 'username'),
            password01=parser.get('pg_10_5_production', 'password'),
            database01=parser.get('pg_10_5_production', 'database')
            )
        self.connect_pg(
            server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
            user01=parser.get('pg_10_5_sdsi', 'username'),
            password01=parser.get('pg_10_5_sdsi', 'password'),
            database01=parser.get('pg_10_5_sdsi', 'database')
            )

        self.fichier_xlsx = "file01.xlsx"


        # # workbook_write = xlwt.Workbook()
        # if (os.path.exists(self.fichier_xlsx)):
        workbook_write = xlsxwriter.Workbook(self.fichier_xlsx)
        # workbook_write = xlwt.open_workbook_write(self.fichier_xlsx)
        # # sheet_write = workbook_write.add_sheet('suppression_gpao_unique')
        
        header_format_red = workbook_write.add_format({'bold': True,
                            'align': 'center',
                            'valign': 'vcenter',
                            'fg_color': '#c80815',
                            'border': 1})


        header_format_blue = workbook_write.add_format({'bold': True,
                            'align': 'center',
                            'valign': 'vcenter',
                            'fg_color': '#4d8fac',
                            'border': 1})

                                   


        sheet_suppr_gpao_uniq = workbook_write.add_worksheet('Suppression GPAO Unique')
        cell_format_union = workbook_write.add_format({'align': 'center',
            'valign': 'vcenter',
            'border': 1})
        sheet_suppr_gpao_uniq.merge_range('A1:B1', "", 
            cell_format_union)
        #                           y  x
        sheet_suppr_gpao_uniq.write(0, 0, 'Veuillez entrer les valeurs correspondants au dessous des cases colorees', header_format_red)
        sheet_suppr_gpao_uniq.write(3, 0, 'Commande', header_format_blue)
        sheet_suppr_gpao_uniq.write(3, 1, 'Lots', header_format_blue)
        
        
        
        sheet_suppr_gpao_uniq.set_column('A:A', 20)
        sheet_suppr_gpao_uniq.set_column('B:B', 75)


        # sheet_write.workbook_write.sheet_by_index(0)

        #                 y  x  " eto le txt soratana"
        # sheet_write.write(0, 0, "Ce ligne contient l_Utilisation de ce programme")
        # sheet_write.write(1, 0, "")

        # workbook_write.save(self.fichier_xlsx)
        workbook_write.close()
        os.system(self.fichier_xlsx)
        


        # vita soratra ny "commande" sy ny "lot" rhf tonga eto

        workbook_read = xlrd.open_workbook(self.fichier_xlsx)
        sheet_read = workbook_read.sheet_by_index(0)
        try:

        # time.sleep(10)
                                        #  y  x
            cmd001 = sheet_read.cell_value(4, 0)
        except IndexError:
            print
            Our_Tools.print_green("Vous avez entree vide pour la cellule(Commande)")
            self.logging_n_print( 
                txt = "Commande vide dans l'Excel\n\n",
                type_log = "info"
            )
            sys.exit(0)

        # print "cmd001: " + cmd001
        # # LOX098
        # sys.exit(0)

        # datas = [sheet_read.cell_value(1, col) for col in range(sheet_read.ncols)]
        #                               y   x                   
        datas = [sheet_read.cell_value(row, 1) for row in range(4, sheet_read.nrows)]
        # print datas
        # # [u'BE_20170923_02_P_R', u'BE_20170923_03_P_R', u'BE_20, ....
        
        # print "len(datas): " + str(len(datas))
        # print datas

        if (len(datas) == 1) and (len(datas[0]) == 0):  # possible we vide ny lot apdirn fa 
            print "tsisy nininn ao am lot_s aah"
            sys.exit(0)

        all_lots = ""
        for lot01 in datas:
            if isinstance(lot01, float):
                all_lots += "'" + '{:.0f}'.format(lot01) + "', "
            elif (isinstance(lot01, unicode) or isinstance(lot01, str) ):
                all_lots += "'" + str(lot01) + "', "

            # # 'BE_20170923_02_P_R','BE_20170923_03_P_R', ...
            # # no tanjona


        # all_lots = "','".join(datas)
        # all_lots = "'" + all_lots + "'"
        all_lots = all_lots[:-2]

        print all_lots
        # sys.exit(0)
        # print all_lots
        # # 'BE_20170923_02_P_R','BE_20170923_03_P_R', ...

        # sys.exit(0)

        # compteur = 0
        # all_lots = ""
        # for data in range(0, sheet_read.nrows):
# 
            # val001 = sheet_read.row_values(data, 0, 1)[0]
#                 
            # if compteur == 0:
                # cmd001 = str(val001)
            # elif compteur == 1:
                # pass
            # else:
                # all_lots += "'" + str(val001) + "',"
# 
            # #print "val001[ " + str(compteur) + "]: " + str(val001)
# 
            # compteur += 1
# 
        # print str(val001)
#         
# 
        # all_lots = all_lots[:-1]

        # print "cmd001: " + cmd001
        
        # print "all_lots: " + all_lots
        # txt001 = "aa"
        txt001 = """
# ################################################################
# Dans bdd(production) pour la commande("""+cmd001+""")
# ################################################################
# 
# 
         """
        self.logging_n_print( 
            txt = txt001,
            type_log = "info"
        )


        Our_Tools.long_print()







        delete_query_prod001 = "DELETE FROM pli_numerisation WHERE id_lot_numerisation IN "
        delete_query_prod001 += "(SELECT id_lot_numerisation FROM lot_numerisation WHERE lot_scan IN (" + all_lots + ")  AND idcommande_reception IN ('"+cmd001+"','0"+cmd001+"'));"

        delete_query_prod002 = "DELETE FROM pli_numerisation_anomalie WHERE id_lot_numerisation IN "
        delete_query_prod002 += "(SELECT id_lot_numerisation FROM lot_numerisation where lot_scan IN ("+ all_lots +")  AND idcommande_reception IN ('"+cmd001+"','0"+cmd001+"'));"

        delete_query_prod003 = "DELETE FROM image_numerisation WHERE id_lot_numerisation IN "
        delete_query_prod003 += "(SELECT id_lot_numerisation FROM lot_numerisation WHERE lot_scan IN (" + all_lots + ")  and idcommande_reception IN ('"+cmd001+"','0"+cmd001+"'));"

        delete_query_prod004 = "DELETE FROM fichesuiveuse_numerisation WHERE id_lot_numerisation IN "
        delete_query_prod004 += "(SELECT id_lot_numerisation FROM lot_numerisation WHERE lot_scan IN (" + all_lots + ")  and idcommande_reception IN ('"+cmd001+"','0"+cmd001+"'));"

        delete_query_prod005 = "DELETE FROM lot_numerisation WHERE lot_scan IN (" + all_lots + ")  AND idcommande_reception IN ('"+cmd001+"','0"+cmd001+"');"

        list_query_delete_prod = [
            delete_query_prod001, 
            delete_query_prod002, 
            delete_query_prod003,
            delete_query_prod004, 
            delete_query_prod005
        ]

        i = 0
        for query_prod in list_query_delete_prod:
            # print "delete_query_prod00"+ str(i) +": " + query_prod
            self.logging_n_print( 
                txt = query_prod + "\n", 
                type_log = "info"
            )

            #eto
            self.pg_not_select(
                query01 = query_prod,
                host = "192.168.10.5",
                db = "production")

            i += 1
            Our_Tools.long_print()





        delete_query_sdsi001 = "DELETE FROM pousse WHERE idprep IN (SELECT idprep FROM fichier WHERE lot_client IN (" + all_lots + ") AND idcommande IN ('"+cmd001+"','0"+cmd001+"'));"
        delete_query_sdsi002 = "DELETE FROM fichierimage WHERE idprep IN (select idprep FROM fichier WHERE lot_client IN (" + all_lots + ") AND idcommande IN ('"+cmd001+"','0"+cmd001+"'));"
        delete_query_sdsi003 = "DELETE FROM fichierimage_base64 WHERE idprep IN (SELECT idprep FROM fichier WHERE lot_client IN (" + all_lots + ") AND idcommande IN ('"+cmd001+"','0"+cmd001+"'));"
        delete_query_sdsi004 = "DELETE FROM preparation WHERE idprep IN (SELECT idprep FROM fichier WHERE lot_client IN (" + all_lots + ") AND idcommande IN ('"+cmd001+"','0"+cmd001+"'));"
        delete_query_sdsi005 = "DELETE FROM fichier WHERE lot_client IN (" + all_lots + ") AND idcommande IN ('"+cmd001+"','0"+cmd001+"');"

        list_query_delete_sdsi = [
            delete_query_sdsi001, 
            delete_query_sdsi002, 
            delete_query_sdsi003,
            delete_query_sdsi004, 
            delete_query_sdsi005
        ]

        i = 0
        txt001 = """
##################################################################
# Dans bdd(sdsi) pour la commande("""+cmd001+""")
##################################################################
# 
# 

         """
        self.logging_n_print( 
            txt = txt001 ,
            type_log = "info")
        for query_sdsi in list_query_delete_sdsi:
            # print "delete_query_sdsi00"+ str(i) +": " + query_sdsi
            self.logging_n_print( 
                txt = query_sdsi + "\n", 
                type_log = "info"
            )

            #eto
            self.pg_not_select(
                query01 = query_sdsi,
                host = "192.168.10.5",
                db = "sdsi")

            i += 1
            Our_Tools.long_print()



        long_void = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        self.logging_n_print( 
            txt = long_void,
            type_log = "info")

        print long_void
        print "Fin"
        sys.exit(0) 



    def pg_not_select(self, 
            query01 = "",            
            host = "127.0.0.1",
            db = "sdsi"):
        if( host == "127.0.0.1"):
            self.cursor_pg_local.execute(query01)
            self.connect_pg_local.commit()
        elif ( (host == "192.168.10.5") and (db == "sdsi") ):
            try:
                self.connect_pg_10_5_sdsi
            except AttributeError:  
                self.connect_pg(    # on fait une connection aa la base car elle est inexistant
                    # cette methode va definir self.cursor_pg_10_5__bdd_sdsi
                    server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
                    user01=parser.get('pg_10_5_sdsi', 'username'),
                    password01=parser.get('pg_10_5_sdsi', 'password'),
                    database01=parser.get('pg_10_5_sdsi', 'database')
                )
            self.cursor_pg_10_5__bdd_sdsi.execute(query01)
            self.connect_pg_10_5__prod.commit()
        elif ( (host == "192.168.10.5")
               and (db == "production") ):
            try: # de meme que sdsi@10.5
                self.connect_pg_10_5__prod
            except AttributeError:
                self.connect_pg( # on fait une connection aa la base car elle est inexistant
                    server01 = parser.get('pg_10_5_production', 'ip_host'),
                    user01=parser.get('pg_10_5_production', 'username'),
                    password01=parser.get('pg_10_5_production', 'password'),
                    database01=parser.get('pg_10_5_production', 'database')
                )
            self.cursor_pg_10_5__bdd_prod.execute(query01)
            self.connect_pg_10_5__prod.commit()

    @staticmethod
    def usage():
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')

        Our_Tools.long_print()

        print "Usage: "
        print "Option: -h, --help"
        print "> Our_Tools.py -h"
        print "> Our_Tools.py --help"
        print "- - ces 2scripts font la meme chose"
        print "- - ils vont afficher cette Aide"


        Our_Tools.long_print(num = 5)


        print "Option: -L, --long-print"
        print "> Our_Tools.py -L"
        print "- - pour afficher 70lignes vides qui vont immiter 'cls' ou 'clear'"
        print "- - "
        print "- - pour effacer l_ecran"

        Our_Tools.long_print(num = 5)

        print "Option: -c, --crawl"
        print 'il est preferable d_utiliser crawl01.sh avec les 5params'
        print 'dans cette programme, il va faire rien du tout'
        print '-'
        print '-'
        print "> Our_Tools.py -c /path/folder001/ pattern_search001"
        print "OU"
        print "> Our_Tools.py --crawl /path/folder001/ pattern_search001"
        print '- - cela va chercher "pattern_search001" dans le chemin(/path/folder001/)'

        Our_Tools.long_print(num = 5)

        print "Option: -d, --directory"
        print "> Our_Tools.py -d"
        print "- - pour chercher un repertoire dans un ordi"
        print "- - "
        print "- - C_est la meme que:"
        print "> find -maxdepth 1 -iname '*nameXX*'-type d"

        Our_Tools.long_print(num = 5)

        print "Option: -s, --suppression_gpao_unique"
        print "> Our_Tools.py -s"
        print "- - pour la suppression de gpao unique"
        print "- - "
        

        Our_Tools.long_print(num = 5)

        print "Option: -T, --all_tests"
        print "Pour faire des test que j_ai trouvee sur Internet"
        print
        print "Our_Tools.py -T dl link01 file_save"
        print "Soyez en sure que link01 est de type(http://XXX/YYY.qsd"


        Our_Tools.long_print(num = 5)

        print "Option: -S, --sgc"
        print "- Ceci est en cours de Developpement"
        print "- Finit mais pas encore testee"
        print "- Pour faire les traitements des Tickets SOGEC-SGC"
        print "- ex: python Our_Tools.py -S"
        print "- ex: python Our_Tools.py --sgc"

        Our_Tools.long_print(num = 5)

        print "Option: -e, --export_table"
        print "- Pour exporter le contenu de certain table dans du fichier_excel"
        print "- host, db, table, output"
        print "- ex: python Our_Tools.py -e 192.168.10.5 production RED001_S1 out.xlsx"

        Our_Tools.long_print(num = 5)

        print "Option: -T manage_usb_storage activate"
        print '###########Ceci doit etre executee en tant que compte_Admin###########'
        print "- To Activate the USB_storage"
        print "Option: -T manage_usb_storage deactivate"
        print "- To DeActivate the USB_storage"

        Our_Tools.long_print(num = 5)


    @staticmethod
    def csv_test003():

        
        f = open('names.csv', 'ab')

        with f:
            
            fnames = ['first_name', 'last_name']
            writer = csv.DictWriter(f, fieldnames=fnames)    
        
            writer.writeheader()
            writer.writerow({'first_name' : 'John', 'last_name': 'Smith'})
            writer.writerow({'first_name' : 'Robert', 'last_name': 'Brown'})
            writer.writerow({'first_name' : 'Julia', 'last_name': 'Griffin'})

        pass

    @staticmethod
    def csv_test002():
        csv.register_dialect("hashes", delimiter="#")

        f = open('items3.csv', 'ab')
        
        with f:
        
            writer = csv.writer(f, dialect="hashes")
            writer.writerow(("pens", 4)) 
            writer.writerow(("plates", 2))
            writer.writerow(("bottles", 4))
            writer.writerow(("cups", 1))
        pass

    @staticmethod
    def csv_test001():
        # print "methode csv_test001"
        # print "https://docs.python.org/2/library/csv.html"
        # print "https://pythonspot.com/en/files-spreadsheets-csv/"

        with open('persons.csv', 'ab') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Name', 'Profession'])
            filewriter.writerow(['Derek', 'Software Developer'])
            filewriter.writerow(['Steve', 'Software Developer'])
            filewriter.writerow(['Paul', 'Manager'])

    def pg_select(self, 
            host = "192.168.10.5",
            database01 = "sdsi",
            query = "select * from execute"):
        if ((host == "192.168.10.5") and (database01 == "sdsi")):
            # on va d_abord tester SI il y a connection
            # # si pas de connection aa sdsi@10.5... alors on fait une connection
            try:
                self.connect_pg_10_5_sdsi
            except AttributeError:  
                self.connect_pg(    # on fait une connection aa la base car elle est inexistant
                    server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
                    user01=parser.get('pg_10_5_sdsi', 'username'),
                    password01=parser.get('pg_10_5_sdsi', 'password'),
                    database01=parser.get('pg_10_5_sdsi', 'database')
                )
            self.cursor_pg_10_5__bdd_sdsi.execute(query)
            self.rows_pg_10_5__sdsi = self.cursor_pg_10_5__bdd_sdsi.fetchall()
        elif ((host == "192.168.10.5") and (database01 == "production")):
            try: # de meme que sdsi@10.5
                self.connect_pg_10_5__prod
            except AttributeError:
                self.connect_pg( # on fait une connection aa la base car elle est inexistant
                    server01 = parser.get('pg_10_5_production', 'ip_host'),
                    user01=parser.get('pg_10_5_production', 'username'),
                    password01=parser.get('pg_10_5_production', 'password'),
                    database01=parser.get('pg_10_5_production', 'database')
                )
            self.cursor_pg_10_5__bdd_prod.execute(query)
            self.rows_pg_10_5__prod = self.cursor_pg_10_5__bdd_prod.fetchall()
            print ""



    # in the class_Our_Tools
    def run(self):
        # i = 0
        try:
            while True:
                # if (i < 5):
                    # print str(i) + " - this is a thread of class_our_tools\n",
                    # time.sleep(self.time_test_connection)
                    # i += 1
                # else:
                    # break
                key = ord(getch())  # https://stackoverflow.com/questions/12175964/python-method-for-reading-keypress
                print key
                if key == 3:
                    raise KeyboardInterrupt() # https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
                elif key == 117:    # pressed__u
                    self.pg_select(
                        host = "192.168.10.5",
                        database01 = "production",
                        query = "SELECT 1"
                    )
                    if (self.rows_pg_10_5__prod[0][0] == 1):
                        time.sleep(self.time_test_connection)
                        print "connection ok"
                        pass
                    else:
                        print "connection interrompue aa la bdd(production)"
                
                    
        except KeyboardInterrupt:
            print "<ctrl - c> est s_est executee"

                    #tapaka#tampoka #connection#killed


    def execute_list_queries_not_select(
            self,
            list_queries = ['', ''],
            host01 = "192.168.10.5",
            db01 = "sdsi"):
        for query01 in list_queries:
            print "pass_65464987987"
            # self.pg_not_select(
                # query01 = query01,
                # host = host01,
                # db = db01)
        pass


    def sgc001(self,
        table_prod = "sgal75"):

        self.table_prod001 = table_prod

        try:
            table_from_prompt = sys.argv[2]
            # print "misy aa"
            self.table_prod001 = table_from_prompt
        except IndexError as index_error:
            # print "tsisy"
            pass
        # sys.exit(0)

        self.long_print()
        print "table_prod: " + self.table_prod001


        txt01 = 'Etes-vous sure que table_prod = ' + self.table_prod001 + ' [y/n]'
        confirm_table_prod = raw_input(txt01)

        if confirm_table_prod == 'y':
            pass
        else:
            sys.exit(0)
            pass



        self.sous_dossier01 = self.table_prod001[-4:].upper()
        # # AL75
        
        # connection to dbb
        self.connect_pg(
            server01 = parser.get('pg_10_5_production', 'ip_host'),
            user01=parser.get('pg_10_5_production', 'username'),
            password01=parser.get('pg_10_5_production', 'password'),
            database01=parser.get('pg_10_5_production', 'database')
        )
        self.connect_pg(
            server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
            user01=parser.get('pg_10_5_sdsi', 'username'),
            password01=parser.get('pg_10_5_sdsi', 'password'),
            database01=parser.get('pg_10_5_sdsi', 'database')
        )





        # print "self.sous_dossier01: " + self.sous_dossier01


        self.c_sql = "AG22\\c.sql"
        self.c_sql_output = "AG22\\c_output.sql"
        self.s1_sql = "AG22\\s1.sql"
        self.s1_sql_output = "AG22\\s1_output.sql"
        self.q_sql = "AG22\\q.sql"
        self.q_sql_output = "AG22\\q_output.sql"
        self.r_sql = "AG22\\r.sql"
        self.r_sql_output = "AG22\\r_output.sql"

        self.subm_js = "AG22\\submit_form_sfl159.js"

        # apache@10.13
        # 

        # print "sgc"
        self.xlsx_descripteur = r"AG22\AG08_DescripteurSaisie.xls"
        self.xlsx_dsd = r"AG22\AG08_importation Sgc.xls"
        # fichier dsd = fichier_importation
        self.ctrl_standard = r"AG22\CONTROLE_STANDARD.sql"




        workbook_read_dsd = xlrd.open_workbook(self.xlsx_dsd)

        sheet_read_dsd = workbook_read_dsd.sheet_by_index(0)
        #                                          y   x
        fields_at_s1 = [sheet_read_dsd.cell_value(row, 0) for row in range(1, sheet_read_dsd.nrows)]

        chg_fields_s1 = ' character varying(254), \n'.join(fields_at_s1)
        chg_fields_s1 += ' character varying(254),\n'

        # print chg_fields_s1
        # # date_cachet_poste character varying(254),
        # # civilite character varying(254),
        # # nom character varying(254),
        # # prenom character varying(254),
        # # cp character varying(254),
        # # ...
        
        chg_fields_c = chg_fields_s1

        chg_fields_q = chg_fields_s1.replace('numvoie character varying(254),', '')
        chg_fields_q = chg_fields_q.replace('chaine1 character varying(254),', '')
        chg_fields_q = chg_fields_q.replace('numvoie1 character varying(254),', '')
        chg_fields_q = chg_fields_q.replace('chaine2 character varying(254),', '')
        chg_fields_q = chg_fields_q.replace('numvoie2 character varying(254),', '')
        chg_fields_q = chg_fields_q.replace('chaine3 character varying(254),', '')
        chg_fields_q = chg_fields_q.replace('numvoie3 character varying(254),', '')

        # print chg_fields_q
        # mtov am "chg_fields_s1" fa nesorina ny
        # # (numvoie chaine1 numvoie1 chaine2 numvoie2 chaine3 numvoie3)

        chg_fields_r = chg_fields_q

        self.replace_in_file(
            path_file_input = self.s1_sql,
            path_file_output = self.s1_sql_output,
            replacements = {
                "____table_prod____": self.table_prod001,
                "-- miova654321654": chg_fields_s1
            })

        self.replace_in_file(
            path_file_input = self.c_sql,
            path_file_output = self.c_sql_output,
            replacements = {
                "____table_prod____": self.table_prod001,
                "-- miova654321654": chg_fields_c
            })

        self.replace_in_file(
            path_file_input = self.q_sql,
            path_file_output = self.q_sql_output,
            replacements = {
                "____table_prod____": self.table_prod001,
                "-- miova654321654": chg_fields_q
            })

        self.replace_in_file(
            path_file_input = self.r_sql,
            path_file_output = self.r_sql_output,
            replacements = {
                "____table_prod____": self.table_prod001,
                "-- miova654321654": chg_fields_r
            })

        content_s1_sql = Our_Tools.read_file_line_by_line(self.s1_sql_output)
        # print content_s1_sql
        # sys.exit(0)


        query_create_table = "create table ecoute_ip (a int)"
        # try:
            # self.pg_not_select(
                    # query01 = content_s1_sql,
                    # host = "192.168.10.5",
                    # db = "production")
# 
        # except psycopg2.ProgrammingError:
            # print "programming error"
# 
            # txt001 = "On dirait que la table("+self.table_prod001+"_s1) existe deja dans la bdd(production)"
            # Our_Tools.print_red(
                # txt = txt001
            # )
            # pass

        self.create_table_prod(query_prod = content_s1_sql)
        
        
        






        # raw_input()

        content_c_sql = Our_Tools.read_file_line_by_line(self.c_sql_output)
        self.create_table_prod(query_prod = content_c_sql)
        # print content_c_sql

        # raw_input()

        content_q_sql = Our_Tools.read_file_line_by_line(self.q_sql_output)
        # print content_q_sql
        self.create_table_prod(query_prod = content_q_sql)
        
        txt001 = "Les tables "+self.table_prod001+"_s1, "+self.table_prod001+"_s1, "+self.table_prod001+"_s1"
        txt001 += " sont creees"

        Our_Tools.print_green(txt001)

        # sys.exit(0)
        




        query_update_passe_s1 = "update passe set tableprod='"+self.table_prod001+"_s1' where idcommande like 'SGC%' and idsousdossier='"+self.sous_dossier01+"' and idetape='SAISIE 1';"
        query_update_passe_c = "update passe set tableprod='"+self.table_prod001+"_c' where idcommande like 'SGC%' and idsousdossier='"+self.sous_dossier01+"' and idetape='CONTROLE GROUPE';"
        query_update_passe_q = "update passe set tableprod='"+self.table_prod001+"_q' where idcommande like 'SGC%' and idsousdossier='"+self.sous_dossier01+"' and idetape='ASSEMBLAGE/UNIFORMISATION';"

        list_queries_upd_passe = [
            query_update_passe_s1,
            query_update_passe_c,
            query_update_passe_q
        ]

        self.execute_list_queries_not_select(list_queries_upd_passe)

        # sys.exit(0)

        self.long_print()
        print "query_update_passe_s1 @ sdsi: \n" + query_update_passe_s1
        print 
        print "query_update_passe_c @ sdsi: \n" + query_update_passe_c
        print 
        print "query_update_passe_q @ sdsi: \n" + query_update_passe_q

        self.long_print()

        query_prendre_viv_prest_id_sous_doss = "SELECT vivetic_prestation_id, sous_dossier_id "
        query_prendre_viv_prest_id_sous_doss += " FROM vivetic_prestation "
        query_prendre_viv_prest_id_sous_doss += "WHERE code_prestation = 'SGC'"
        query_prendre_viv_prest_id_sous_doss += " AND nom_prestation like '"+self.sous_dossier01+"'"
        print "query_prendre_viv_prest_id_sous_doss  @ production: "  
        print query_prendre_viv_prest_id_sous_doss 



        #ato002
        # vivetic_prestation_id01 = 1593
        self.pg_select(
            query = query_prendre_viv_prest_id_sous_doss,
            host = "192.168.10.5",
            database01 = "production"
            )
        try:
            vivetic_prestation_id01 = self.rows_pg_10_5__prod[0][0]
        except IndexError:
            self.long_print()
            Our_Tools.print_red ("N_a pas pu prendre vivetic_prestation_id ET sous_dossier_id")
            print
            print "On dirait que l'etape Importation n'est pas encore finit"
            print
            Our_Tools.print_green (query_prendre_viv_prest_id_sous_doss)
            sys.exit(0)
            pass
        sous_dossier_id01 = self.rows_pg_10_5__prod[0][1]

        print "vivetic_prestation_id01"
        print vivetic_prestation_id01

        print "sous_dossier_id01"
        print sous_dossier_id01
        # sous_dossier_id01 = 299

        self.long_print()

        query_upd_input_mask = "UPDATE vivetic_champs SET input_mask = '99/99/9999' WHERE vivetic_type_id = 30 "
        query_upd_input_mask += "AND description ILIKE 'date%' AND vivetic_prestation_id = " + str(vivetic_prestation_id01)

        print "query_upd_input_mask @ production"
        print query_upd_input_mask


        # self.pg_not_select(
            # query01 = "",            
            # host = "127.0.0.1",
            # db = "sdsi"
        # )

        # sys.exit(0)
        self.long_print()
        # print "query_upd_input_mask: "
        # print query_upd_input_mask
        # # UPDATE vivetic_champs SET input_mask = '99/99/9999' WHERE vivetic_type = 30 AND description ILIKE 'date%' AND vivetic_prestation_id = 1593

        #ato002
        print "manao copy anle js... FA mbola TSY renomee... sady mbola en local"
        # shutil.copy(self.subm_js, self.subm_js + '__')

        subm_js_file_cp = self.subm_js.rsplit('\\', 1)[0] 
        subm_js_file_cp += '\\'
        subm_js_file_cp += self.subm_js.rsplit('\\', 1)[1][:-6] 
        subm_js_file_cp += str(sous_dossier_id01)
        subm_js_file_cp += self.subm_js.rsplit('\\', 1)[1][-3:] 

        print "subm_js_file_cp: " 
        print subm_js_file_cp
        #ato002$
        print "renomena ilay js_vaovao... mbola en local aa"
        # os.rename(self.subm_js + '__', subm_js_file_cp)

        path_cp_js_saisie = '/var/www/localhost/htdocs/test/version2/saisie/'
        path_cp_js_saisie += 'js/submit_script'

        path_cp_js_controle = '/var/www/localhost/htdocs/test/version2/online_controle/'
        path_cp_js_controle += 'js/submit_script'
        
        path_cp_js_rejet = '/var/www/localhost/htdocs/test/version2/online_rejet/'
        path_cp_js_rejet += 'js/submit_script'
        
        print "asina anle js_saisie"
        print path_cp_js_saisie
        print "mnw copie anle js_saisie"
        # shutil.copy(subm_js_file_cp, path_cp_js_saisie)


        print
        print

        print "asina anle js_controle"
        print path_cp_js_controle
        print "mnw copie anle js_controle"
        # shutil.copy(subm_js_file_cp, path_cp_js_controle)

        print
        print

        print "asina anle js_rejet"
        print path_cp_js_rejet
        print "mnw copie anle js_rejet"
        # shutil.copy(subm_js_file_cp, path_cp_js_rejet)

        # for obj, sh_n in Our_Tools.get_xls_tab_name():
            # print sh_n

        print "vita dol ny copie js mankan am serveur"



        self.long_print(num = 10)
        print "ande hnw anle code_barre RAH ohatra ka misy"

        all_tabs_xl_descript = Our_Tools.get_xls_tab_name(
                path_file_xls = self.xlsx_descripteur
            )

        # 'code'
        print 'all_tabs_xl_descript'
        print all_tabs_xl_descript

        tab_code_barre_num = 0
        present_tab_code_barre = False

        # ande hitady we misy code_barre v ilay descripteur.xlsx
        # raw_input('Ande hnw resaka codebarre')
        for tab01 in all_tabs_xl_descript:
            if (re.search('code', tab01, re.IGNORECASE)) and (re.search('barre', tab01, re.IGNORECASE)):
                present_tab_code_barre = True
                num_tab_code_barre = tab_code_barre_num
            else:
                pass
            tab_code_barre_num += 1


        if present_tab_code_barre:
            print "misy tab code barre"

            print "num_tab_code_barre"
            print num_tab_code_barre
            # sys.exit(0)

            workbook_read = xlrd.open_workbook(self.xlsx_descripteur)
            sheet_read = workbook_read.sheet_by_index(num_tab_code_barre)
            # print "sheet_read.cell_value(9, 0)"
            # print sheet_read.cell_value(9, 0)
            # # 8806088725918

            query_maka_plus_grand_id_code_barre = "SELECT sgc_codebarre_id FROM sgc_codebarre "
            query_maka_plus_grand_id_code_barre += "WHERE sgc_codebarre_id = "
            query_maka_plus_grand_id_code_barre += "(SELECT MAX(sgc_codebarre_id) FROM sgc_codebarre)"

            self.pg_select(
                query = query_maka_plus_grand_id_code_barre,
                host = "192.168.10.5",
                database01 = "production"
            )

            sgc_max_codebarre_id = self.rows_pg_10_5__prod[0][0]

            # print "sgc_max_codebarre_id"
            # print sgc_max_codebarre_id
            # # 7464
            # sys.exit(0)

            print "sheet_read.nrows"
            print sheet_read.nrows
            list_code_barre = [sheet_read.cell_value(row, 0) for row in range(0, sheet_read.nrows)]

            # print "datas_code_barre"
            # print datas_code_barre
            # # [8806086428293.0, 8806088775883.0, 8806088952, ...

            

            query_insert_codebarre = 'INSERT INTO sgc_codebarre VALUES '

            # print "list_code_barre"
            # print list_code_barre
            # sys.exit(0)
            for code_barre in list_code_barre:
                # print "type (code_barre)"
                # print type(code_barre)
                # print type('{:.0f}'.format(code_barre))
                # # str
                # print "type(sgc_max_codebarre_id)"
                # print type(sgc_max_codebarre_id)
                # sys.exit(0)
                sgc_max_codebarre_id = sgc_max_codebarre_id + 1
                if isinstance(code_barre, float):
                    query_insert_codebarre +="("+str(sgc_max_codebarre_id)+", '"+'{:.0f}'.format(code_barre)+"', 'AL75'),"
                elif isinstance(code_barre, unicode):
                    query_insert_codebarre +="("+str(sgc_max_codebarre_id)+", '"+str(code_barre)+"', 'AL75'),"
            print "query_insert_codebarre @ production"
            print query_insert_codebarre

            query_insert_codebarre = query_insert_codebarre[:-1]
            # # INSERT INTO sgc_codebarre VALUES (7465, '8806086428293', 'AL75'),(746

            # #ato002
            # self.pg_not_select(
                # query01 = query_insert_codebarre,
                # host = "192.168.10.5",
                # db = "sdsi")

            sys.exit(0)

            print 
            pass
        else:
            print "tsis tab code barre"
            pass

    def export_table_to_xl(
            self,
            server001 = "192.168.10.5",
            user001 = "user01",
            database001 = "production",
            # table_name = "django_migrations",
            table_name = "RED001_S1",
            xl_write = "out001.xlsx"):

        
        # print "len(sys.argv)"
        # print len(sys.argv)
        # print "sys.argv[2]"
        # print sys.argv[1]
        

        if len(sys.argv) == 6:

            server001 = sys.argv[2]
            database001 = sys.argv[3]
            table_name = sys.argv[4]
            xl_write = sys.argv[5]

            if table_name.islower():
                query01 = "select * from "+table_name
            elif table_name.isupper():
                query01 = 'select * from "'+table_name+'"'
            else:
                txt001 = 'Le Nom du table n_est pas connue si Majuscule ou Minuscule \n'
                txt001 += str(table_name)
                Our_Tools.print_green(txt = txt001)
                sys.exit(0)

            print "query01"
            print query01
            # sys.exit(0)

            pass

        if ((server001 == "192.168.10.5") and (database001 == "production")):
            self.connect_pg(
                server01 = parser.get('pg_10_5_production', 'ip_host'),
                user01=parser.get('pg_10_5_production', 'username'),
                password01=parser.get('pg_10_5_production', 'password'),
                database01=parser.get('pg_10_5_production', 'database')
            )
            self.pg_select(
                host = "192.168.10.5",
                database01 = "production",
                query = query01
            )

            workbook_write = xlsxwriter.Workbook(xl_write)
            sheet_write = workbook_write.add_worksheet('Contenu du '+table_name)

            x = y = 0
            for row in self.rows_pg_10_5__prod:
                x = 0
                for cell in row:
                    # print str(cell) + ": [ "+str(x)+", " +str(y)+"]"
                    sheet_write.write(y, x, str(cell))
                    x = x + 1
                print 
                y += 1

            workbook_write.close()
            pass
        elif((server001 == "192.168.10.5") and (database001 == "sdsi")):
            self.connect_pg(
                server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
                user01=parser.get('pg_10_5_sdsi', 'username'),
                password01=parser.get('pg_10_5_sdsi', 'password'),
                database01=parser.get('pg_10_5_sdsi', 'database')
            )






        pass

    # this is the constructor of class(Our_Tools)
    def __init__(self, 
            is_thread_connection001 = True,
            time_test_connection01 = 5):


        
        self.is_thread_connection = is_thread_connection001
        
        if is_thread_connection001:
            threading.Thread.__init__(self)
            self.time_test_connection = time_test_connection01
        else:
            print "not a thread"
            pass

        self.log_file__suppr_gpao_unique = ".\log_file__suppr_gpao_unique.log"
        
        logging.basicConfig(
            filename=self.log_file__suppr_gpao_unique,
            level=logging.DEBUG,
            format='%(asctime)s : %(levelname)s : %(message)s'
        )

        pass

    @staticmethod
    def long_print(num = 5):
        for a in range(num):
            print 


    def search_a_dir001(self, 
            walk_dir = "",
            depth = 0,
            pattern_search = "do_not_erase"):
        # OK
        # print "searching for a directory"

        print "this is the same as:"
        print "> find -maxdepth 1 -iname '*nameXX*'-type d"
        
        sys.exit(0)

        walk_dir = sys.argv[2]
        # pattern_search = sys.argv[3]
        # extensions = ('txt', 'sh', 'php', 'js', 'py')

        for root, subdirs, files in os.walk(walk_dir):
            if root[len(walk_dir):].count(os.sep) <= depth :
            # the test above is
            # # going to check for some var_depth from the var__walk_dir only
                for subdir in subdirs:
                    # print "subdir: " + os.path.join(root, subdir)
                    # # do_not_erase\xlsxwriter
                    if (pattern_search in os.path.join(root, subdir)):
                        print os.path.join(root, subdir)
        pass

    def check_table_exists(
            self,
            host = '192.168.10.5',
            db = 'sdsi'):

        if ((host == '192.168.10.5') and (db == 'sdsi')):
            if self.is_already_connected_to_db(
                    host = '192.168.10.5',
                    db = 'sdsi'):
                print "already connected to sdsi 3216494231676"
                
            else:
                # print "not yet connected 6546546897"
                self.connect_pg(
                    server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
                    user01=parser.get('pg_10_5_sdsi', 'username'),
                    password01=parser.get('pg_10_5_sdsi', 'password'),
                    database01=parser.get('pg_10_5_sdsi', 'database')
                )
                # print "connection ok 987647619764"
            pass
        elif ((host == '192.168.10.5') and (db == 'production')):
            if self.is_already_connected_to_db(
                    host = '192.168.10.5',
                    db = 'production'):
                print "already connected to production 25014821389546213879"
                
            else:
                # print "not yet connected 6546546897"
                self.connect_pg(
                    server01 = parser.get('pg_10_5_production', 'ip_host'),
                    user01=parser.get('pg_10_5_production', 'username'),
                    password01=parser.get('pg_10_5_production', 'password'),
                    database01=parser.get('pg_10_5_production', 'database')
                )
                # print "connection ok 987647619764"
            

    def is_already_connected_to_db(
            self,
            host=  '192.168.10.5',
            db = 'sdsi'):
        res = True
        if ( (host == '192.168.10.5') and (db == 'sdsi') ):
            try:
                self.connect_pg_10_5_sdsi
                pass
            except NameError:
                res = False
                pass
            except AttributeError:
                # print "missing"
                res = False
                pass
            pass
        return res
        pass

    def copy_table(self,
            host_src = "192.168.10.5",
            dbb_src = "production",
            table_src = "sfl087_l",
            host_target = "192.168.10.5",
            dbb_target = "sdsi",
            table_target = "sfl087_l"):

        if ((dbb_src == dbb_target) and (table_src == table_target)):
            print "not yet managed 654898761364"
            pass
        else:

            list_tuple_src = self.get_column_name_w_descr_to_listTuple(
                server01 = host_src,
                database01 = dbb_src,
                table_name = table_src)
            print "list_tuple_src"
            # print list_tuple_src

            query_copy_table = 'CREATE TABLE '

            if table_target.isupper():
                query_copy_table += '"'+table_target+'" ('
            else:
                query_copy_table += table_target + ' ('


            cols_def = ""
            for row in list_tuple_src:
                if (row[0].isupper()):
                    cols_def += '"'+row[0]+'" '
                elif (row[0].islower()):
                    cols_def += row[0]+' '

                cols_def += str(row[1]) + ' ' + str(row[2]) + ', \n'

                # print row

            cols_def = cols_def[:-3]

            cols_def += ')'

            query_copy_table

            print cols_def

            # ('n_enr', 'character varying', 50, 'YES')
            # ('n_ima', 'character varying', 50, 'YES')
            # ...
            # ...
            # sys.exit(0)



            # verifieo we ao v ilay table_target
            # # rah tsy ao d mnw create_table__table_target
            # # rah ao d mamoka erreur

    def get_column_name_w_descr_to_listTuple(
            self,
            server01 = "192.168.10.5",
            database01 = "production",
            table_name = "AAC001_C"):
        # if ((server001 == "192.168.10.5") and (database001 == "production")):
        self.conn_pg_prod_OR_sdsi(
            server001 = server01,
            database001 = database01)
        if ((server01 == "192.168.10.5") and (database01 == "production")):
            # https://www.postgresql.org/docs/9.1/static/infoschema-columns.html
            query001 = "SELECT column_name, data_type, character_maximum_length, is_nullable FROM information_schema.columns WHERE table_name = '"+table_name+"'"
            self.pg_select(
                host = server01,
                database01 = "production",
                query = query001
            )
            
            res = []
            for row in self.rows_pg_10_5__prod:
                res.append(row)

        elif ((server01 == "192.168.10.5") and (database01 == "sdsi")):
            query001 = "SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = '"+table_name+"'"
            self.pg_select(
                host = server01,
                database01 = "sdsi",
                query = query001
            )
            
            res = []
            for row in self.rows_pg_10_5__prod:
                res.append(row)


            # res = []
            # for row in self.rows_pg_10_5__prod:
                # for cell in row:
                    # res.append(cell)
        return res

        pass

    def get_column_name_to_list(
            self,
            server01 = "192.168.10.5",
            database01 = "production",
            table_name = "AAC001_C"):
        # if ((server001 == "192.168.10.5") and (database001 == "production")):
        self.conn_pg_prod_OR_sdsi(
            server001 = server01,
            database001 = database01)
        if ((server01 == "192.168.10.5") and (database01 == "production")):
            query001 = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name='"+table_name+"'"
            self.pg_select(
                host = server01,
                database01 = "production",
                query = query001
                )
            # self.cursor_pg_10_5__bdd_prod.execute(query001)

            res = []
            for row in self.rows_pg_10_5__prod:
                for cell in row:
                    res.append(cell)
        return res

        pass


    def conn_pg_prod_OR_sdsi(self,
            server001 = "192.168.10.5",
            database001 = "production"):

        if ((server001 == "192.168.10.5") and (database001 == "production")):
            self.connect_pg(
                server01 = parser.get('pg_10_5_production', 'ip_host'),
                user01=parser.get('pg_10_5_production', 'username'),
                password01=parser.get('pg_10_5_production', 'password'),
                database01=parser.get('pg_10_5_production', 'database')
            )
        elif((server001 == "192.168.10.5") and (database001 == "sdsi")):
            self.connect_pg(
                server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
                user01=parser.get('pg_10_5_sdsi', 'username'),
                password01=parser.get('pg_10_5_sdsi', 'password'),
                database01=parser.get('pg_10_5_sdsi', 'database')
            )

        pass


    @staticmethod
    def print_green(txt = "this is a test"):
        default_colors = get_text_attr()
        default_bg = default_colors & 0x0070
        set_text_attr(
            FOREGROUND_GREEN | 
            default_bg |
            FOREGROUND_INTENSITY)
        print txt
        set_text_attr(default_colors)

    @staticmethod
    def print_blue(txt = "this is a test"):
        default_colors = get_text_attr()
        default_bg = default_colors & 0x0070
        set_text_attr(
            FOREGROUND_BLUE | 
            default_bg |
            FOREGROUND_INTENSITY)
        print txt
        set_text_attr(default_colors)


    @staticmethod
    def print_red(txt = "this is a test"):
        default_colors = get_text_attr()
        default_bg = default_colors & 0x0070
        set_text_attr(
            FOREGROUND_RED | 
            default_bg |
            FOREGROUND_INTENSITY)
        print txt
        set_text_attr(default_colors)


    @staticmethod
    def replace_accent(
        walk_dir = "",
        extensions = ()
        ):
        print "removed this project"
        sys.exit(0)

        default_colors = get_text_attr()
        default_bg = default_colors & 0x0070
        set_text_attr(
            FOREGROUND_BLUE | 
            default_bg |
            FOREGROUND_INTENSITY)
        print "replace_accent"
        set_text_attr(default_colors)


        # sys.exit(0)
        if len(extensions) == 0:
            extensions = ('txt', 'xls', 'xlsx', 'docx', 'doc')

        char_to_replace = ['é', 'è', 'à']

        walk_dir = sys.argv[2]

        for root, subdirs, files in os.walk(walk_dir):
            for filename in files:
                for ch in char_to_replace:
                    if ch in filename:
                        print "ao"
                    else:
                        print "missing"
                file_path = os.path.join(root, filename)
                print "file_path: " + file_path

        pass

    def create_table_prod(
        self,
        query_prod = ""
    ):
        try:
            print "execute create table_prod"
            
            # self.pg_not_select(
                    # query01 = query_prod,
                    # host = "192.168.10.5",
                    # db = "production")

        except psycopg2.ProgrammingError:
            print "programming error"

            txt001 = "On dirait que la table("+self.table_prod001+"_s1) existe deja dans la bdd(production)"

            Our_Tools.print_red(
                txt = txt001
            )

            txt002 = "Je vous prie de le verifier"
            Our_Tools.print_green(
                txt = txt002
            )
            sys.exit(0)
            pass
        pass


    def crawl__search_for_file001(self, 
            walk_dir = "",
            pattern_search = "",
            extensions = ()):
        # print "tonga ato"

        if len(extensions) == 0:
            extensions = ('txt', 'sh', 'php', 'js', 'py')

        walk_dir = sys.argv[2]
        pattern_search = sys.argv[3]
        print "walk_dir: " + walk_dir
        print "pattern_search: " + pattern_search

        sys.exit(0)

        for root, subdirs, files in os.walk(walk_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                print('(full path: %s)' % (file_path))
                # # .\bash_script\crawl01.sh
                

                # print "file_path.rsplit('.', 1)[1]: " +\
                    # file_path.rsplit('.', 1)[1]
                # # sh
                # # txt
                # # py
                # # ... 
                print file_path

                if file_path.rsplit('.', 1)[1] in extensions:
                    
                    wrote_file_path = False
                    with open(file_path) as open_file_path:
                        for line_number, line in enumerate(open_file_path, 1):
                            # print pattern_search
                            if ((pattern_search in line) and (wrote_file_path == False)):
                                Our_Tools.long_print(num = 10)
                                print "file_path: " + file_path
                                # print str(line_number) +": "+ line
                                wrote_file_path = True
                            if ((pattern_search in line) and (wrote_file_path == True)) :
                                print str(line_number) +": "+ line



def main():
    try:
        #opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:", ["help","listen","execute","target","port","command","upload"])
        opts, args = getopt.gnu_getopt(sys.argv[1:],
            "hcLdsrtTxSz:e", 
            [
                "help", 
                "crawl", 
                "long-print",
                "directory",
                "suppression_gpao_unique",
                "replace_accent",
                "thread_test",
                "all_tests"
                "x = testing001",
                "sgc",
                "export_table"
            ])
    except getopt.GetoptError as err:
        print str(err)
        Our_Tools.usage()


    # print "sys.arg: " + str(len (sys.argv))
    # # si le nombre de parametre donnee au script est vide
    # # ceci va retourner 1
    if len (sys.argv) == 1:
        Our_Tools.usage()
        sys.exit(0)


    for option,val in opts:
        if option in ("-h","--help"):
            Our_Tools.usage()
        elif option in ("-c","--crawl"):
            script001 = Our_Tools()
            script001.crawl__search_for_file001()
        elif option in ("-L", "--long-print"):
            args = sys.argv[2:]
            if len(args) == 0:
                Our_Tools.long_print(num = 70)
            else:
                print "to manage"
        elif option in ("-d","--directory"):
            script001 = Our_Tools()
            script001.search_a_dir001()
        elif option in ("-s","--suppression_gpao_unique"):
            script001 = Our_Tools()
            # at this time, only meth(suppression_gpao_unique)
            # # is going to connect the db(production, sdsi)
            # # is going to create a new excel_file
            script001.suppression_gpao_unique()
        elif option in ("-r","--replace_accent"):
            Our_Tools.replace_accent()
        elif option in ("-e", "--export_table"):
            our_Tools001 = Our_Tools()
            our_Tools001.export_table_to_xl()
        elif option in ("-S", "--sgc"):
            our_Tools001 = Our_Tools()
            our_Tools001.sgc001()
            pass
        elif option in ("-t", "--thread_test"):
            # thread_conn_pg = Connection_pg()
            # thread_conn_pg.start()
            thread_connection = Our_Tools(
                is_thread_connection001 = True,
                time_test_connection01 = .0001
            )

            thread_connection.connect_pg(
                server01 = '192.168.10.5',
                user01='pgtantely', # #erreur
                password01='123456',
                database01='production'
            )
            # thread_connection.pg_select(
                # host = "192.168.10.5",
                # database01 = "production",
                # query = "select idenr, \"MATRICULE\" from \"ARL001_S1\" where idenr = 5")
            # print thread_connection.rows_pg_10_5__prod[0][0]

            thread_connection.start()
        elif option in ("-T", "--all_test"):
            args = sys.argv[2:]
            if len(args) == 0 :
                print "no param for all_tests"
            else:
                if args[0] == 'p':
                    p = Person()
                elif args[0] == 'manage_usb_storage':
                    # print "sys.argv"
                    # print sys.argv
                    # # just remember, sys.argv is going to contain everything which is 
                    # # # given to the prompt... even if the the name of the script
                    # sys.exit(0)
                    if (len(sys.argv) == 4) and sys.argv[3] == 'activate':
                        Our_Tools.manage_usb_store_w_regedit(state = 3)
                        Our_Tools.print_green('USB_storage Activated')
                    elif (len(sys.argv) == 4) and sys.argv[3] == 'deactivate':
                        Our_Tools.manage_usb_store_w_regedit(state = 4)
                        Our_Tools.print_green('USB_storage DeActivated')
                    else:
                        Our_Tools.usage()
                    pass
                elif args[0] == 'change_regedit003':
                    keyVal = r'Software\Microsoft\Internet Explorer\Main'
                    try:
                        key = OpenKey(HKEY_CURRENT_USER, r'Software\Microsoft\Internet Explorer\Main', 
                            0, KEY_ALL_ACCESS)
                        SetValueEx(key, "Start Page", 0, REG_SZ, "http://www.google.com/")
                        CloseKey(key)
                    except:
                        Our_Tools.print_red('Error qsdmfklqsdjmfkl  azemrjazemlrj  654654564')
                        key = CreateKey(HKEY_CURRENT_USER, keyVal)
                    
                        pass
                elif args[0] == 'change_regedit001':
                    # https://www.blog.pythonlibrary.org/2010/03/20/pythons-_winreg-editing-the-windows-registry/


                    keyVal = r'Software\Microsoft\Internet Explorer\Main'
                    # keyVal = r'SYSTEM\CurrentControlSet\Services\USBSTOR'
                    try:
                        # key = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
                        # key = OpenKey(HKEY_LOCAL_MACHINE, keyVal, 0, KEY_ALL_ACCESS)
                        key = OpenKey(HKEY_LOCAL_MACHINE, r'Software\Microsoft\Internet Explorer\Main', 
                            0, KEY_ALL_ACCESS)
                        # SetValueEx(key, "Start Page", 0, REG_SZ, "http://google.com")
                        # CloseKey(key)
                    except:
                        Our_Tools.print_red("Error 6543216aaeer3qsdf564654")
                        key = CreateKey(HKEY_CURRENT_USER, keyVal)
                    
                    print "done 6549316876"

                    pass
                    # https://stackoverflow.com/questions/23015222/checking-if-registry-key-exists-with-python
                elif args[0] == 'read_regedit001':
                    # https://www.experts-exchange.com/questions/26622655/Python-code-examples-on-how-to-read-Windows-Registry.html
                    # # the code in it has to be changed a bit

                    # key_to_read = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
                    key_to_read = r'SYSTEM\CurrentControlSet\Services\USBSTOR'
                    
                    try:
                        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                        k = OpenKey(reg, key_to_read)

                        result = QueryValueEx(k, "Start")
                        print k
                        print "result"
                        print result
                    
                        # do things with the key here ...
                    
                    except Exception:
                        print "Exception in reading the regedit"
                    pass
                elif args[0] == 'singleton':
                    our_Tools001 = Our_Tools()
                    our_Tools001.pg_select(
                        host = "192.168.10.5",
                        database01 = "sdsi",
                        query = "select * from etape"
                    )
                    for row in our_Tools001.rows_pg_10_5__sdsi:
                        print row
                    pass
                elif args[0] == 'csv_write003':
                    Our_Tools.csv_test003()
                elif args[0] == 'csv_write002':
                    Our_Tools.csv_test002()
                elif args[0] == 'csv_write001':
                    Our_Tools.csv_test001()
                    # print 'csv'
                    pass
                elif args[0] == 'chk_table':
                    our_Tools001 = Our_Tools()
                    our_Tools001.check_table_exists()
                    pass
                elif args[0] == 'cp_table':
                    our_Tools001 = Our_Tools()
                    print our_Tools001.copy_table()
                    pass
                elif args[0] == 'get_col':
                    our_Tools001 = Our_Tools()
                    print our_Tools001.get_column_name_to_list()
                    pass
                elif args[0] == 'get_col_w_descr':
                    our_Tools001 = Our_Tools()
                    l_t = our_Tools001.get_column_name_w_descr_to_listTuple()

                    for tuple01 in l_t:
                        print tuple01

                    pass
                elif args[0] == 'color':
                    Our_Tools.print_blue("coco")
                    Our_Tools.print_red("coco red")

                elif args[0] == 'coco':
                    # print "coco"
                    # ame_to_bre_spellings = {'tire':'tyre', 'color':'colour', 'utilize':'utilise'}
                    text = 'foo color, entire, utilize'
                    print (Our_Tools.ame_to_bre(text = text))
                    pass
                elif args[0] == 'read_line':
                    print Our_Tools.read_file_line_by_line()
                elif args[0] == 'repl_file01':
                    Our_Tools.replace_in_file()
                elif args[0] == '23':
                    from test_py.test001 import FetchUrls
                    print "ao"
                elif args[0] == 'dl':
                    print "len(args): " + str(len(args))
                    print args
                    # # ['dl', "'http:..., file_out.pdf]
                    # sys.exit(0)
                    if len(args) == 3:
                        link01 = args[1]
                        file_save = args[2]

                        print "link01: " + link01
                        print "file_save: " + file_save
                        urllib.urlretrieve(link01, file_save)
                    else:
                        print "not yet managed 0214564"

        elif option in ("-x", "--x = testing001"):
            # Our_Tools.test001()
            Our_Tools.test002()
        elif option in ("-z", "--zeta"):
            print "option: " + option
            print "val: ", sys.argv[2:]

if __name__ == '__main__':
    main()