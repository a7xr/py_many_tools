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
import datetime
from datetime import date
from msvcrt import getch
import urllib
import fileinput
import shutil
from _winreg import *
import csv
import ctypes
import subprocess
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ConfigParser import SafeConfigParser
import ConfigParser as cfgparser


path_prg = 'E:\\DISK_D\\mamitiana\\kandra\\do_not_erase\\our_tools\\'



parser = SafeConfigParser()
parser.read(path_prg + 'all_confs.txt')

# path_sublime2 = "C:\Program Files\Sublime Text 2\sublime_text.exe"
path_sublime2 = parser.get('general', 'path_subl_2')

try:
    import psycopg2,psycopg2.extras
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

try:
    import selenium
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support.ui import Select


except Exception:
    print "selenium doit etre installee"
    raw_input()
    os.system("pip install selenium")

try:
    from PIL import Image
    pass
except Exception:
    print "PIL n_est pas installee dans cette machine"
    print "Je vous prie d_installer PIL"
    pass

try:
    import wmi
    pass
except Exception:
    os.system("pip install WMI")




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
chrome_driver_path = 'e:\chromedriver.exe'

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











class CMail(object):

    def __init__(self, bool01 = True, 
            smtp_link = "192.168.10.4",
            tto = ["Mamitiana <mamitiana_iam@vivetic.mg>"],
            cc = [],
            sender = "mamitiana_iam@vivetic.mg",
            sujet="", 
            sbodymail="",
            file="",
            path=""):

        self.SmtpLink = smtplib.SMTP(smtp_link)
        self.html = ""
        # self.tto = ["hasina@vivetic.mg"]
        # self.cc   = ["hasina@vivetic.mg", "hasina@vivetic.mg"]
        self.tto = tto
        #self.cc   = ["Tojo <tojo_iam@vivetic.mg>","Herve <herve_iam@vivetic.mg>","Tahiry <harisoa_iam@vivetic.mg>","Fabrice <fabrice_iam@vivetic.mg>"]
        
        self.cc = cc
        # self.sender = "infodev@vivetic.mg"
        self.sender = "mamitiana_iam@vivetic.mg"
        
        self.sujet = sujet
        
        self.Email = None
        self.SmtpLink = None
        self.subject=sujet
        self.sbodymail=sbodymail
        # path = "E:/herve/Commande/CALL/CallWAV/"

        self.filename = file#"CPE_RECUP_Mail_06-05-2016.log"#
        self.attachment = open(path+file,"rb")#, "rb")#
        
        self.setUp()

    def setUp(self):
        self.Email = MIMEMultipart()
        self.Email['Date']           = time.strftime('%m/%d/%Y')
        self.Email['From']           = self.sender
        self.Email['To']      = ', '.join(self.tto)
        self.Email['Cc']      = ', '.join(self.cc)
        
        # self.SmtpLink = smtplib.SMTP("192.168.10.4")
        #self.SmtpLink = smtplib.SMTP("192.168.10.4")
        self.contentmail()

    def contentmail(self):
        html = ""
        html += """\
                <html>"""
        
        html += """\
     
        
        
        <BODY bgColor=#ffffff> 
        
        """
        
      
        html += """<DIV><FONT face=Arial size=2>&nbsp;</FONT></DIV>"""
        html += """<DIV><FONT face=Arial size=2>Bonjour,</FONT></DIV>"""
        html += """<DIV><FONT face=Arial size=2>&nbsp;</FONT></DIV>"""
        html += """<DIV><FONT face=Arial size=2>"""+self.sbodymail+""" </FONT></DIV>."""
       
        html += """<DIV><FONT face=Arial size=2>Cordialement</FONT></DIV>"""
        html += """<DIV><FONT face=Arial size=2></FONT>L'&eacute;quipe IAM</DIV>"""
        
        
        html += """\
        </body>
        </html>"""
        
        
        self.html = html.encode("utf8")
        
        
    def envoyer_mail(self):
        #try:
        attachment = self.attachment
        self.part = MIMEBase('application', 'octet-stream')
        self.part.set_payload((attachment).read())
        encoders.encode_base64(self.part)
        self.part.add_header('Content-Disposition', "attachment; filename= %s" % self.filename)
         
        self.Email.attach(self.part)
        
        self.Email.attach(
            MIMEText(
                self.html.encode(
                    'utf8','ignore'
                ), 'html'
            )
        )
        self.Email['Subject']        = self.subject
        self.SmtpLink.sendmail(
            self.Email['From'], 
            self.tto+self.cc, 
            self.Email.as_string()
        )
        self.SmtpLink.quit()
        return True
        #




class Thread001(threading.Thread): # done for Mahaitia_Demand
    

    def set_configuration(self,
        exe = "out.xlsx",
        temp_attendre = 10
    ):
        self.exe = exe
        self.temp_attendre = temp_attendre

        pass

    # class Thread001
    def __init__(
        self
    ):
        threading.Thread.__init__(self)
        fichier_conf_mahaitia = "conf_mahaitia.txt"
                    
        parser_mahaitia = SafeConfigParser()
        parser_mahaitia.read(fichier_conf_mahaitia)                    
        exe = parser_mahaitia.get('thread_conf', 'exe')
        temp_attendre = parser_mahaitia.get('thread_conf', 'temp_attendre')

        self.set_configuration(
            exe = exe,
            temp_attendre = temp_attendre
        )
        pass
    # class Thread001 #Thread001_run
    def run(self):
        # try:
        while True:
            # print "avant ni_exe"
            # from subprocess import Popen
            # Popen(self.exe)


            from subprocess import check_output
            check_output(self.exe, shell=True)
            time.sleep(float(self.temp_attendre))
        


class Our_Tools(threading.Thread):

    @staticmethod
    def refactor_sfl_correspondance():
        # this is Hasina_IAM_Program
        try:
            sous_doc = sys.argv[3]
        except IndexError:
            Our_Tools.long_print(num = 10)
            Our_Tools.print_red(txt = "Veuillez donnee l_idsousdossier dans le parametre")
            print "- ex:"
            Our_Tools.print_blue(txt = "> python Our_Tools.py -T test_selenium_sfl AP03")
            return
        rechercher = sous_doc
        chromedriverexe = parser.get('softw_path_exe', 'selenium_chromedriver')
        chromeexe = parser.get('softw_path_exe', 'chrome_exe')
        chromeOps = webdriver.ChromeOptions()
        chromeOps._binary_location = chromeexe
        print "02"                    
        driver = webdriver.Chrome(chromedriverexe, chrome_options=chromeOps)
        driver.get(
            parser.get('selenium_correspondance_sfl', 'link_bouygues')
        ) # Load page
        rch=driver.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td[2]/select")
        slct = rch.find_element_by_xpath("option[text()='" + rechercher + "']")
        slct.click()
        matr = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[3]/td[2]/input")
        login = '99999'
        matr.send_keys(login)
        matr.send_keys(Keys.RETURN)                                        
        consulter = driver.find_element_by_xpath("/html/body/div[3]/table/tbody/tr[2]/td[2]/a")
        consulter.click()                    
        nvldmd = driver.find_element_by_xpath("//*[@id='nouvelleDemande']")
        nvldmd.click()                    
        liste_parent = driver.find_elements_by_xpath("/html/body/div[3]/form/table[1]/tbody/tr")                                        
        t_name=[]
        i=0
        print len(liste_parent)
        for t in range(len(liste_parent)-1):
            i+=1
            try:                            
                d = driver.find_element_by_xpath("/html/body/div[3]/form/table[1]/tbody/tr["+str(i)+"]/td[2]/input")
                print d.get_attribute('name')
                d_str = str(d.get_attribute('name'))
                d1 = driver.find_element_by_xpath("/html/body/div[3]/form/table[1]/tbody/tr["+str(i)+"]/td[1]")
                d2_str = d1.text
                if (d_str.find('password')==-1):
                    t_name.append(d_str+"\t"+d2_str)                            
            except:
                try:
                    f = driver.find_element_by_xpath("/html/body/div[3]/form/table[1]/tbody/tr["+str(i)+"]/td[2]/label[1]/input")
                    print f.get_attribute('name')
                    f_str = str(f.get_attribute('name'))
                    f1 = driver.find_element_by_xpath("/html/body/div[3]/form/table[1]/tbody/tr["+str(i)+"]/td[1]")
                    f2_str = f1.text                                
                    if (f_str.find('password')==-1):
                        t_name.append(f_str+"\t"+f2_str)                                
                except:
                    g = driver.find_element_by_xpath("/html/body/div[3]/form/table[1]/tbody/tr["+str(i)+"]/td[2]/select")
                    print g.get_attribute('name')
                    g_str = str(g.get_attribute('name'))
                    g1 = driver.find_element_by_xpath("/html/body/div[3]/form/table[1]/tbody/tr["+str(i)+"]/td[1]")
                    g2_str = g1.text                                
                    t_name.append(g_str+"\t"+g2_str)                                        
        fichier = open("name_SFL_"+rechercher+".txt", "a")
        for t in t_name:
            fichier.write("%s\n"%(t))                    
        fichier.close()                    
        print 'DONE!'                    
        driver.quit()
        pass

    @staticmethod
    def test_tabwidget_pyqt001():
        class Test001(QTabWidget):
            def __init__(self, title, parent):
                # QtGui.QDockWidget.__init__(self, title, parent)
                QDockWidget.__init__(self, title, parent)
                self.parent = parent
                self.currentLocation = None

                # self.tabWidget = QtGui.QTabWidget()
                self.tabWidget = QTabWidget()
                # self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
                self.tabWidget.setTabPosition(QTabWidget.West)
                self.setWidget(self.tabWidget)
                
                dropArea = DropArea(hostTypes.keys())
                dropArea2 = DropArea(netTypes.keys())
                dropArea3 = DropArea(customTypes.keys())
                self.tabWidget.addTab(dropArea, self.tr("&Host Element"))
                self.tabWidget.addTab(dropArea2, self.tr("&Net Element"))
                self.tabWidget.addTab(dropArea3, self.tr("&Custom Element"))
                
                self.connect(self,
                             QtCore.SIGNAL("dockLocationChanged(Qt::DockWidgetArea)"),
                             self.locationChanged)
                self.connect(self.tabWidget,
                             QtCore.SIGNAL("currentChanged(int)"),
                             self.tabChanged)
        app = QApplication(sys.argv)
        test001 = Test001("Title001", "Parent001")
        test001.show()
        sys.exit(app.exec_())

        pass

    @staticmethod
    def test_tabwidget_pyqt():

        # https://www.tutorialspoint.com/pyqt/pyqt_qtabwidget.htm
        class tabdemo(QTabWidget):
           def __init__(self, parent = None):
              super(tabdemo, self).__init__(parent)
              self.tab1 = QWidget()
              self.tab2 = QWidget()
              self.tab3 = QWidget()
                
              self.addTab(self.tab1,"Tab 1")
              self.addTab(self.tab2,"Tab 2")
              self.addTab(self.tab3,"Tab 3")
              self.tab1UI()
              self.tab2UI()
              self.tab3UI()
              self.setWindowTitle("tab demo")
                
           def tab1UI(self):
              layout = QFormLayout()
              layout.addRow("Name",QLineEdit())
              layout.addRow("Address",QLineEdit())
              self.setTabText(0,"Contact Details")
              self.tab1.setLayout(layout)
                
           def tab2UI(self):
              layout = QFormLayout()
              sex = QHBoxLayout()
              sex.addWidget(QRadioButton("Male"))
              sex.addWidget(QRadioButton("Female"))
              layout.addRow(QLabel("Sex"),sex)
              layout.addRow("Date of Birth",QLineEdit())
              self.setTabText(1,"Personal Details")
              self.tab2.setLayout(layout)
                
           def tab3UI(self):
              layout = QHBoxLayout()
              layout.addWidget(QLabel("subjects")) 
              layout.addWidget(QCheckBox("Physics"))
              layout.addWidget(QCheckBox("Maths"))
              self.setTabText(2,"Education Details")
              self.tab3.setLayout(layout)
                
        def main():
           app = QApplication(sys.argv)
           ex = tabdemo()
           ex.show()
           sys.exit(app.exec_())

        main()

    @staticmethod
    def test_multithread005():
        import logging
        import threading
        import time
        
        logging.basicConfig(level=logging.DEBUG,
                            format='(%(threadName)-10s) %(message)s',
                            )
                            
        def wait_for_event(e):
            """Wait for the event to be set before doing anything"""
            logging.debug('wait_for_event starting')
            event_is_set = e.wait()
            logging.debug('event set: %s', event_is_set)
        
        def wait_for_event_timeout(e, t):
            """Wait t seconds and then timeout"""
            while not e.isSet():
                logging.debug('wait_for_event_timeout starting')
                event_is_set = e.wait(t)
                logging.debug('event set: %s', event_is_set)
                if event_is_set:
                    logging.debug('processing event')
                else:
                    logging.debug('doing other work')
        
        
        e = threading.Event()
        t1 = threading.Thread(name='block', 
                            target=wait_for_event,
                            args=(e,))
        t1.start()
        
        t2 = threading.Thread(name='non-block', 
                            target=wait_for_event_timeout, 
                            args=(e, 2))
        t2.start()
        
        logging.debug('Waiting before calling Event.set()')
        time.sleep(3)
        e.set()
        logging.debug('Event is set')

    @staticmethod
    def test_multithread004():
        import threading
        import time
        import logging
        
        logging.basicConfig(level=logging.DEBUG,
                            format='(%(threadName)-10s) %(message)s',
                            )
        
        def daemon():
            logging.debug('Starting')
            time.sleep(2)
            logging.debug('Exiting')
        
        d = threading.Thread(name='daemon', target=daemon)
        d.setDaemon(True)
        
        def non_daemon():
            logging.debug('Starting')
            logging.debug('Exiting')
        
        t = threading.Thread(name='non-daemon', target=non_daemon)
        
        d.start()
        t.start()
        pass

    # https://pymotw.com/2/threading/
    @staticmethod
    def test_multithread003():
        import logging
        import threading
        import time

        logging.basicConfig(level=logging.DEBUG,
                format='[%(levelname)s] (%(threadName)-10s) %(message)s',
        )

        def worker():
            logging.debug('Starting')
            time.sleep(2)
            logging.debug('Exiting')

        def my_service():
            logging.debug('Starting')
            time.sleep(3)
            logging.debug('Exiting')

        t = threading.Thread(name='my_service', target=my_service)
        w = threading.Thread(name='worker', target=worker)
        w2 = threading.Thread(target=worker) # use default name

        w.start()
        w2.start()
        t.start()
        pass

    # https://pymotw.com/2/threading/
    @staticmethod
    def test_multithread002():
        import threading

        def worker():
            """thread worker function"""
            print 'Worker'
            return
        
        threads = []
        for i in range(5):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
            time.sleep(1)
        pass

    # https://www.tutorialspoint.com/python/python_multithreading.htm
    # https://geo.mydati.com/partners/HSS-6.9.1-install-hss-826-plain.exe
    @staticmethod
    def test_multithread001():
        import Queue
        import threading
        import time

        exitFlag = 0


        class myThread (threading.Thread):
           def __init__(self, threadID, name, q):
              threading.Thread.__init__(self)
              self.threadID = threadID
              self.name = name
              self.q = q
           def run(self):
              print "Starting " + self.name
              process_data(self.name, self.q)
              print "Exiting " + self.name

        def process_data(threadName, q):
           while not exitFlag:
                queueLock.acquire()
                if not workQueue.empty():
                    data = q.get()
                    queueLock.release()
                    print "%s processing %s" % (threadName, data)
                else:
                    queueLock.release()
                time.sleep(1)


        threadList = ["Thread-1", "Thread-2", "Thread-3"]
        nameList = ["One", "Two", "Three", "Four", "Five"]
        queueLock = threading.Lock()
        workQueue = Queue.Queue(10)
        threads = []
        threadID = 1

        # Create new threads
        for tName in threadList:
           thread = myThread(threadID, tName, workQueue)
           thread.start()
           threads.append(thread)
           threadID += 1

        # Fill the queue
        queueLock.acquire()
        for word in nameList:
           workQueue.put(word)
        queueLock.release()

        # Wait for queue to empty
        while not workQueue.empty():
           pass

        # Notify threads it's time to exit
        exitFlag = 1

        # Wait for all threads to complete
        for t in threads:
           t.join()
        print "Exiting Main Thread"
        pass

    def reformat_thread_conf_test_connect_prod_10_5(
        self, 
        host = parser.get(
            'pg_10_5_production', 
            'ip_host'),
        database = parser.get(
            'pg_10_5_production', 
            'database')
    ):
        if self.db_is_connected(
            host = host,
            database01 = database
        ):
            # print "connection ok au bdd(production)"
            Our_Tools.write_append_to_file(
                path_file = path_prg + "log_connect_db.txt",
                txt_to_add = str(datetime.datetime.now()) + ": Connection OK au bdd("+database+")@"+host
            )
            pass
        else:
            
            txt001 = "************ " + str(datetime.datetime.now()) + ": Connection PERDU pour bdd("+database+")@" + host
            txt002 = str(datetime.datetime.now()) + ": Connection PERDU pour bdd("+database+")@" + host
            Our_Tools.write_append_to_file(
                path_file = path_prg + "log_connect_db.txt",
                txt_to_add = txt001
            )
            Our_Tools.popup(
                window_title = "Erreur de connection de base",
                msg = txt002)
        pass

    @staticmethod
    def copy_dir_content(
            path_src = 'E:\DISK_D\date',
            path_target = 'E:\DISK_D\ASA\BLF') :
        from distutils.dir_util import copy_tree

        # copy subdirectory example
        # fromDirectory = "/a/b/c"
        # toDirectory = "/x/y/z"

        copy_tree(path_src, path_target)

    @staticmethod
    def long_print(num = 10):
        for i in range(num):
            print
        pass

    @staticmethod
    def edit_file_w_sublime2(
            path_file = "E:\\DISK_D\\mamitiana\\kandra\\do_not_erase\\our_tools\\" + "redmine_file.txt"):
        # subprocess.Popen(["subl", "-w", path_file]).wait()
        # path_sublime2 = "C:\Program Files\Sublime Text 2\sublime_text.exe"
        subprocess.Popen([path_sublime2, "-w", path_file]).wait()
        print path_file
        pass

    @staticmethod
    def read_file_line_by_line(path_file = "ti.txt"):
        res = ""
        with open(path_file) as open_file_path:
            for line in open_file_path:
                res += line
        return res

    def db_is_connected(self,
            host = "192.168.10.5",
            database01 = 'production'):

        res = False

        self.pg_select(
            host = host,
            database01 = database01,
            query = "SELECT 1"
        )
        if (self.rows_pg_10_5__prod[0][0] == 1):
            # time.sleep(self.time_test_connection)
            # print "connection ok"
            res = True

        return res

        pass



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
            , KEY_ALL_ACCESS      # this is going to create error if you ran the method without admin_account
            )

            # SetValueEx(key, "Start Page", 0, REG_SZ, "http://www.google.com/")
            SetValueEx(key, "Start", 0, REG_DWORD, state)

            if state == 3:
                Our_Tools.print_green(
                    txt = 'USB_storage Activated',
                    new_line = False)
                pass

                Our_Tools.popup(
                    window_title = "USBSTOR",
                    msg = "Veuillez ReConnecter votre USB pour l_Activee")

            elif state == 4:
                # Our_Tools.print_green(
                    # txt = 'USB_storage DeActivated',
                    # new_line = False)

                Our_Tools.print_green(
                    txt = 'USB_storage',
                    new_line = False)
                Our_Tools.print_red(
                    txt = 'De',
                    new_line = False)
                Our_Tools.print_green(
                    txt = 'Activated',
                    new_line = False)

                Our_Tools.popup(
                    window_title = "USBSTOR",
                    msg = "Veuillez ReConnecter votre USB pour le DesActivee")

                pass

            CloseKey(key)

            pass
            # SetValueEx(key, "Start", 0, REG_DWORD, str(state))
            # CloseKey(key)
        except WindowsError:
            Our_Tools.long_print()
            Our_Tools.print_red(
                txt = 'Vous devez executer cette commande en compte_Admin 654987312344566',
                new_line = False)
            # print "this is a test"
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

    def connection_pg(self,  
            server01 = parser.get('pg_localhost_saisie', 'ip_host'),
            user01=parser.get('pg_localhost_saisie', 'username'),
            password01=parser.get('pg_localhost_saisie', 'password'),
            database01=parser.get('pg_localhost_saisie', 'database')
    ):
        try:
            # host = 10.5
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


                # host = 10.5 
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

            elif(
                    (server01 == parser.get('pg_localhost_saisie', 'ip_host'))
                    and (database01 == parser.get('pg_localhost_saisie', 'database'))
            ):
                try:
                    self.connect_pg_localhost_saisie
                except AttributeError:
                    self.connect_pg_localhost_saisie = psycopg2.connect(
                        "dbname=" + database01
                        +" user=" + user01
                        +" password=" + password01
                        +" host=" + server01
                    )
                    self.connect_pg_localhost_saisie.set_isolation_level(0)
                    self.cursor_pg_localhost_saisie = self.connect_pg_localhost_saisie.cursor()
                    print "Connection ok au bdd(saisie)@localhost"
                
                pass
            # host = 127.0.0.1
            elif(server01 == parser.get('pg_localhost_sdsi', 'ip_host')):
                if (database01 == parser.get('pg_localhost_sdsi', 'database')):
                    try:
                        self.connect_pg_local_sdsi
                    except AttributeError:
                        self.connect_pg_local_sdsi = psycopg2.connect(
                            "dbname=" + database01
                            +" user=" + user01
                            +" password=" + password01
                            +" host=" + server01
                        )
                        self.connect_pg_local_sdsi.set_isolation_level(0)
                        self.cursor_pg_local__bdd_sdsi = self.connect_pg_local_sdsi.cursor()
                        print "Connection OK au pg_localhost bdd(sdsi_local)"
                pass
            elif(
                    (server01 == parser.get('pg_10_32_production', 'ip_host'))
                    and (database01 == parser.get('pg_10_32_production', 'database'))
            ):
                try:
                    self.connect_pg_10_32_prod
                except AttributeError:
                    self.connect_pg_10_32_prod = psycopg2.connect(
                        "dbname=" + database01
                        +" user=" + user01
                        +" password=" + password01
                        +" host=" + server01
                    )
                    self.connect_pg_10_32_prod.set_isolation_level(0)
                    self.cursor_pg_10_32_prod = self.connect_pg_10_32_prod.cursor()
                    print "Connection OK au pg_10_32 bdd(production)"
                

                pass
        except(psycopg2.OperationalError):
            print ""
            print ""
            print ""
            print "there is an OperationalError"
            # txt = 
            Our_Tools.write_append_to_file(
                    path_file = 'log_connect_db.txt',
                    txt_to_add = str(datetime.datetime.now()) + ": Impossible de se connecter au db__" + database01)
            Our_Tools.popup(
                window_title = "Connection interrompue",
                msg = "Connection interrompue sur la base de donnee(" + database01 + ")")
            # self.connection_pg(
                # server01 = server01,
                # user01 = user01,
                # password01 = password01,
                # database01 = database01)
            time.sleep(1)

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


    def suppression_gpao_unique(
            self,
            suppr_total = 0):
        print "suppression_gpao_unique"
        # print "parser.get('pg_10_5_production', 'ip_host')"
        # print parser.get('pg_10_5_production', 'ip_host')
        # sys.exit(0)

        #ato
        # self.connection_pg(
            # server01 = parser.get('pg_localhost_sdsi', 'ip_host'),
            # user01=parser.get('pg_localhost_sdsi', 'username'),
            # password01=parser.get('pg_localhost_sdsi', 'password'),
            # database01=parser.get('pg_localhost_sdsi', 'database')
        # )
# 
# 
        # sys.exit(0)

        self.connection_pg(
            server01 = parser.get('pg_10_5_production', 'ip_host'),
            user01=parser.get('pg_10_5_production', 'username'),
            password01=parser.get('pg_10_5_production', 'password'),
            database01=parser.get('pg_10_5_production', 'database')
            )
        self.connection_pg(
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
# Dans bdd(production) pour la commande("""+cmd001

        txt001 += " _ suppr_total" if (suppr_total == 1) else ""
        txt001 += """)
# ################################################################
# 
# 
         """
        self.logging_n_print( 
            txt = txt001,
            type_log = "info"
        )


        Our_Tools.long_print()
        # lot_scan IN (" + all_lots + ")  AND
        # delete_query_prod001 = "DELETE FROM pli_numerisation WHERE id_lot_numerisation IN "
        # delete_query_prod001 += "(SELECT id_lot_numerisation FROM lot_numerisation WHERE lot_scan IN (" + all_lots + ")  AND idcommande_reception IN ('"+cmd001+"','0"+cmd001+"'));"

        delete_query_prod001 = "DELETE FROM pli_numerisation WHERE id_lot_numerisation IN "
        delete_query_prod001 += "(SELECT id_lot_numerisation FROM lot_numerisation WHERE "
        if (suppr_total == 0):
            delete_query_prod001 += "lot_scan IN (" + all_lots + ")  AND"
        delete_query_prod001 +=" idcommande_reception IN ('"+cmd001+"','0"+cmd001+"'));"
        

        delete_query_prod002 = "DELETE FROM pli_numerisation_anomalie WHERE id_lot_numerisation IN "
        delete_query_prod002 += "(SELECT id_lot_numerisation FROM lot_numerisation where "
        if suppr_total == 0:
            delete_query_prod002 += " lot_scan IN (" + all_lots + ")  AND"
        delete_query_prod002 += " idcommande_reception IN ('"+cmd001+"','0"+cmd001+"'));"

        delete_query_prod003 = "DELETE FROM image_numerisation WHERE id_lot_numerisation IN "
        delete_query_prod003 += "(SELECT id_lot_numerisation FROM lot_numerisation WHERE"
        if suppr_total == 0:
            delete_query_prod003 += " lot_scan IN (" + all_lots + ")  AND"
        delete_query_prod003 += " idcommande_reception IN ('"+cmd001+"','0"+cmd001+"'));"


        delete_query_prod004 = "DELETE FROM fichesuiveuse_numerisation WHERE id_lot_numerisation IN "
        delete_query_prod004 += "(SELECT id_lot_numerisation FROM lot_numerisation WHERE "
        if suppr_total == 0:
            delete_query_prod004 += " lot_scan IN (" + all_lots + ")  AND"
        delete_query_prod004 += " idcommande_reception IN ('"+cmd001+"','0"+cmd001+"'));"

        delete_query_prod005 = "DELETE FROM lot_numerisation WHERE "
        if suppr_total == 0:
            delete_query_prod005 += " lot_scan IN (" + all_lots + ")  AND"
        delete_query_prod005 += " idcommande_reception IN ('"+cmd001+"','0"+cmd001+"');"

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
                db = "production",
                log_query = True
            )

            i += 1
            Our_Tools.long_print()




        # lot_client IN (" + all_lots + ") AND
        delete_query_sdsi001 = "DELETE FROM pousse WHERE idprep IN (SELECT idprep FROM fichier WHERE "
        if suppr_total == 0:
            delete_query_sdsi001 += "lot_client IN (" + all_lots + ") AND"
        delete_query_sdsi001 += " idcommande IN ('"+cmd001+"','0"+cmd001+"'));"
        
        delete_query_sdsi002 = "DELETE FROM fichierimage WHERE idprep IN (select idprep FROM fichier WHERE "
        if suppr_total == 0:
            delete_query_sdsi002 += "lot_client IN (" + all_lots + ") AND"
        delete_query_sdsi002 += " idcommande IN ('"+cmd001+"','0"+cmd001+"'));"
        # delete_query_sdsi003 = "DELETE FROM fichierimage_base64 WHERE idprep IN (SELECT idprep FROM fichier WHERE lot_client IN (" + all_lots + ") AND idcommande IN ('"+cmd001+"','0"+cmd001+"'));"
        delete_query_sdsi004 = "DELETE FROM preparation WHERE idprep IN (SELECT idprep FROM fichier WHERE "
        if suppr_total == 0:
            delete_query_sdsi004 += "lot_client IN (" + all_lots + ") AND"
        delete_query_sdsi004 += " idcommande IN ('"+cmd001+"','0"+cmd001+"'));"
        
        delete_query_sdsi005 = "DELETE FROM fichier WHERE "
        if suppr_total == 0:
            delete_query_sdsi005 += "lot_client IN (" + all_lots + ") AND"
        
        delete_query_sdsi005 += " idcommande IN ('"+cmd001+"','0"+cmd001+"');"

        list_query_delete_sdsi = [
            delete_query_sdsi001, 
            delete_query_sdsi002, 
            # delete_query_sdsi003,
            delete_query_sdsi004, 
            delete_query_sdsi005
        ]

        i = 0
        txt001 = """
##################################################################
# Dans bdd(sdsi) pour la commande("""+cmd001

        txt001 += " _ suppr_total" if (suppr_total == 1) else ""

        txt001 +=""")
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
                db = "sdsi",
                log_query = True
            )

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
            db = "sdsi",
            log_query = False):
        if( 
                (host == parser.get('pg_10_5_sdsi', 'ip_host')) 
                and (db == parser.get('pg_10_5_sdsi', 'database'))
        ):
            # try:
            try:
                self.connect_pg_10_5_sdsi
            except AttributeError:
                self.connect_pg_10_5_sdsi = psycopg2.connect(
                    "dbname=" + parser.get('pg_10_5_sdsi', 'database')
                    +" user=" + parser.get('pg_10_5_sdsi', 'username')
                    +" password=" + parser.get('pg_10_5_sdsi', 'password')
                    +" host=" + parser.get('pg_10_5_sdsi', 'ip_host')
                )
                self.connect_pg_10_5_sdsi.set_isolation_level(0)
                self.cursor_pg_10_5__bdd_sdsi = self.connect_pg_10_5_sdsi.cursor()
                print "Connection OK au pg10.5 bdd(sdsi)"

            self.cursor_pg_10_5__bdd_sdsi.execute(query01)
            self.connect_pg_10_5_sdsi.commit()

        elif ( 
                (host == parser.get('pg_localhost_saisie', 'ip_host')) 
                and (db == parser.get('pg_localhost_saisie', 'database')) 
        ):
            try:
                self.connect_pg_localhost_saisie
            except AttributeError:
                self.connect_pg_localhost_saisie = psycopg2.connect(
                    "dbname=" + parser.get('pg_localhost_saisie', 'database')
                    +" user=" + parser.get('pg_localhost_saisie', 'username')
                    +" password=" + parser.get('pg_localhost_saisie', 'password')
                    +" host=" + parser.get('pg_localhost_saisie', 'ip_host')
                )
                self.connect_pg_localhost_saisie.set_isolation_level(0)
                self.cursor_pg_localhost_saisie = self.connect_pg_localhost_saisie.cursor()
                print "Connection ok au bdd(saisie)@localhost"

            self.cursor_pg_localhost_saisie.execute(query01)
            self.connect_pg_localhost_saisie.commit()

            pass

        elif ( 
                (host == parser.get('pg_10_5_sdsi', 'ip_host')) 
                and (db == parser.get('pg_10_5_sdsi', 'database')) 
        ):
            try:
                self.connect_pg_10_5_sdsi
            except AttributeError:  
                self.connection_pg(    # on fait une connection aa la base car elle est inexistant
                    # cette methode va definir self.cursor_pg_10_5__bdd_sdsi
                    server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
                    user01=parser.get('pg_10_5_sdsi', 'username'),
                    password01=parser.get('pg_10_5_sdsi', 'password'),
                    database01=parser.get('pg_10_5_sdsi', 'database')
                )
            self.cursor_pg_10_5__bdd_sdsi.execute(query01)
            self.connect_pg_10_5__prod.commit()
        elif ( 
                (host == "192.168.10.5")
                and (db == "production") 
        ):
            try: # de meme que sdsi@10.5
                self.connect_pg_10_5__prod
            except AttributeError:
                self.connection_pg( # on fait une connection aa la base car elle est inexistant
                    server01 = parser.get('pg_10_5_production', 'ip_host'),
                    user01=parser.get('pg_10_5_production', 'username'),
                    password01=parser.get('pg_10_5_production', 'password'),
                    database01=parser.get('pg_10_5_production', 'database')
                )
            self.cursor_pg_10_5__bdd_prod.execute(query01)
            self.connect_pg_10_5__prod.commit()

        if log_query:
            Our_Tools.write_append_to_file(
                path_file = "log_query_db.txt",
                txt_to_add = db + "@" + host + ": " + query01
            )
            pass

    @staticmethod
    def usage():
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')

        Our_Tools.long_print()

        print "Usage: "
        Our_Tools.print_green (txt = "Option: -h, --help")
        print "> Our_Tools.py -h"
        print "> Our_Tools.py --help"
        print "- - ces 2scripts font la meme chose"
        print "- - ils vont afficher cette Aide"



        Our_Tools.long_print(num = 5)


        Our_Tools.print_green (txt = "Option: -L, --long-print")
        print "> Our_Tools.py -L"
        print "- - pour afficher 70lignes vides qui vont immiter 'cls' ou 'clear'"
        print "- - "
        print "- - pour effacer l_ecran"

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -c, --crawl")
        print 'il est preferable d_utiliser crawl01.sh avec les 5params'
        print 'dans cette programme, il va faire rien du tout'
        print '-'
        print '-'
        print "> Our_Tools.py -c /path/folder001/ pattern_search001"
        print "OU"
        print "> Our_Tools.py --crawl /path/folder001/ pattern_search001"
        print '- - cela va chercher "pattern_search001" dans le chemin(/path/folder001/)'

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -d, --directory")
        print "> Our_Tools.py -d"
        print "- - pour chercher un repertoire dans un ordi"
        print "- - "
        print "- - C_est la meme que:"
        print "> find -maxdepth 1 -iname '*nameXX*'-type d"

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -s, --suppression_gpao_unique")
        print "> Our_Tools.py -s"
        print "- - pour la suppression de gpao unique"
        print "- - "
        print "- - "
        print "- - "
        print "- - Il est possible que la Suppression ne possede pas de "
        print '- - - lots_clients... ie, on a k1 seule commande et on suppr tout'
        Our_Tools.print_yellow(txt = "> Our_Tools.py -s --total")
        
        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -T, --all_test")
        print "Pour faire des test que j_ai trouvee sur Internet"
        print
        print "Our_Tools.py -T dl link01 file_save"
        print "Soyez en sure que link01 est de type(http://XXX/YYY.qsd"


        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -S, --sgc")
        print "- Ceci est en cours de Developpement"
        print "- Finit mais pas encore testee"
        print "- Pour faire les traitements des Tickets SOGEC-SGC"
        print "- ex: python Our_Tools.py -S"
        print "- ex: python Our_Tools.py --sgc"

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -e, --export_table")
        print "- Pour exporter le contenu de certain table dans du fichier_excel"
        print "- host, db, table, output"
        print "- ex: python Our_Tools.py -e 192.168.10.5 production RED001_S1 out.xlsx"

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -T manage_usb_storage activate")
        print '###########Ceci doit etre executee en tant que compte_Admin###########'
        print "- To Activate the USB_storage"
        print "Option: -T manage_usb_storage deactivate"
        print "- To DeActivate the USB_storage"

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -T test_thread_conn")
        print "Va tester la connection Infiniment"
        print "-"
        print "Pour pouvoir l_arreter, il faut faire"
        print "> taskkill /f /pid pid_001 "
        print "-"
        print "-"
        print "Pour avoir le pid_001... Souvent le thread_connection est la premiere"
        print '> tasklist | find /i "python"'
        print "-"
        print "-"
        print "-"
        print "- Autrement, si la seule programme qui utilise python "
        print "- - est celui-ci,... Pour arreter le programme, on fait"
        print '> taskkill /f /im "python.exe"'

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -T test_thread_redmine")
        print "Va afficher un pop_up quand il est 15:00"

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -T test_edit_file_redmine")
        print "Va Editer le fichier qui va s_afficher au moment du pop_up__redmine"

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -T test_thread_conf")
        print "Le thread qui sont Configurees dans fichier_conf__all_confs.ini "
        print "- vont etre executees"
        #fin_usage

        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -T test_selenium_sfl AP03")
        print "Pour faire le Correspondance de la commande AP03"
        print "- le resultat sera dans un fichier comme: 'name_SFL_AP03.txt'"
        
        Our_Tools.long_print(num = 5)

        Our_Tools.print_green (txt = "Option: -T test_conn_db025")
        print "Pour faire du keylogging dans ton pc"
        print "- le fichier log sera log_stuffs.txt"
        

    @staticmethod
    def display_pic(
            path_pic = path_prg + "icon.png"
    ):
        # print path_pic
        # img = Image.open(path_pic)
        # img = Image.open(r'E:\DISK_D\mamitiana\kandra\do_not_erase\our_tools\icon.png')
        # # https://stackoverflow.com/questions/1413540/showing-an-image-from-console-in-python
        # # # not working in windows7
        # img = Image.open('icon.png')
        # img.show()

        if os.name == 'nt':
            os.system(path_pic)
            # os.system('cls')

        pass

    def manage_redmine_popup(self):
        # print "ty ooh"
        now_date_time = datetime.datetime.now()

        self.time_redmine_popup = "15:00:00"
        self.time_redmine_popup = datetime.datetime.strptime(
            self.time_redmine_popup, "%H:%M:%S")
        # you need to convert the now_date_time to now_time... so that it is easier to compare the timeS
        # # https://stackoverflow.com/questions/15105112/compare-only-time-part-in-datetime-python
        self.time_redmine_popup = now_date_time.replace(hour=self.time_redmine_popup.time().hour, 
            minute=self.time_redmine_popup.time().minute, 
            second=self.time_redmine_popup.time().second, 
            microsecond=0) 
        while True:

            now_date_time = datetime.datetime.now()
            now_time = datetime.time(now_date_time.hour, now_date_time.minute,now_date_time.second)
            tmp_time_redmine_popup = datetime.time(
                self.time_redmine_popup.hour, 
                self.time_redmine_popup.minute,
                self.time_redmine_popup.second)
            if (now_time > tmp_time_redmine_popup):
                Our_Tools.popup(
                    window_title = "Redmine Pop_Up Error",
                    msg = "Temps deja depassee")
                sys.exit(0)
            elif (now_time == tmp_time_redmine_popup):
                self.redmine01()
                sys.exit(0)
            else:
                txt001 = "now_time: ", now_time, "time_redmine_popup: ", tmp_time_redmine_popup
                Our_Tools.write_append_to_file(
                    path_file = 'log_redmine_popup.txt',
                    txt_to_add = txt001)
                # print "time_redmine_popup: ", self.time_redmine_popup
                # print time.strftime("%H:%M:%S")
                time.sleep(1)
            pass
        pass

    def init_selenium_chrome(self, 
            with_pic = False
    ):

        if with_pic:
            chromeOptions = None
            pass
        else:
            chromeOptions = webdriver.ChromeOptions()
            prefs = {"profile.managed_default_content_settings.images":2}
            chromeOptions.add_experimental_option("prefs",prefs)
        pass

        self.driver_chrome = webdriver.Chrome(
            chrome_driver_path
            , chrome_options=chromeOptions
        )

        

    def automate_redmine(self, 
            path_file_csv_redmine = 'csv_redmine.csv',
            delimiter = '|'
    ):

        self.init_selenium_chrome(with_pic = False)

        list_content_redm_csv = Our_Tools.csv_read_content(
            path_file_csv = path_file_csv_redmine,
            delimiter = delimiter
        )
        # print "list_content_redm_csv: " , list_content_redm_csv
        # # [['client01', 'projet01', 'tracker01', 'operateur01', 'sujet01', 'assi, ....
        # sys.exit(0)


        self.driver_chrome.get(
            parser.get('selenium_10_24_redmine', 'link_redmine')
        )

        login_field = self.driver_chrome.find_element_by_name('username')
        passw_field = self.driver_chrome.find_element_by_name('password')
        
        login_field.send_keys(parser.get('selenium_10_24_redmine', 'login'))
        passw_field.send_keys(parser.get('selenium_10_24_redmine', 'passw'))
        
        passw_field.submit()

        # self.driver_chrome.get(
                # parser.get('selenium_10_24_redmine', 'link_redmine') + 'projects/iam-new/issues'
        # )       

        # self.driver_chrome.get(
                # parser.get('selenium_10_24_redmine', 'link_redmine') + 'projects/iam-new/issues/new'
        # )
        
        for cont_redm_csv in list_content_redm_csv:
            # # list_content_redm_csv = [['nouv_dmd01', 'client01', 'projet01', 'tracker01', 'operateur01', 'sujet01', 'assi, ....
            if cont_redm_csv[0] == "Nouv_dmd":

                self.driver_chrome.get(
                    parser.get('selenium_10_24_redmine', 'link_redmine') + 'projects/iam-administratif/issues/new'
                )

                print "avant"
                raw_input()
                print "apres"
                sys.exit(0)

            pass
        # print list_content_redm_csv
            # https://192.168.10.13/redmine
            # login_field = 
            # login_field = 
        pass

    @staticmethod
    def csv_read_content(path_file_csv = 'csv_redmine.csv',delimiter = '|'):
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

    @staticmethod
    def csv_read_all(
        path_file_csv = 'csv_redmine.csv',
        delimiter = '|' ):
        res = []
        with open(path_file_csv) as csv_read:
            reader = csv.reader(
                csv_read, delimiter = delimiter)
            for row in reader:
                res.append(row)
            # print "another_line"
        return res
        pass

    @staticmethod
    def csv_to_list(path_file = 'names.csv'):
        list_res = []
        with open(path_file) as csv_read:
            reader = csv.reader(csv_read)
            for row in reader :
                list_res.append(row)
        return list_res

    @staticmethod
    def write_append_to_file(
            path_file = path_prg + "test_append.txt",
            txt_to_add = "this is anotehr test",
    ):

        if os.path.exists(path_file):
            pass
        else:
            Our_Tools.print_green(
                    txt = "Le fichier que vous voulez ajouter",
                    new_line = False)
            
            Our_Tools.print_red(
                    txt = "n_existe pas",
                    new_line = True)

            Our_Tools.print_green(
                    txt = "Creation du fichier " + path_file,
                    new_line = False)

            open_file = open(path_file, 'ab')
            
        open_file = open(path_file, 'ab')
        
        with open_file:
            # print "ato ndrai"
            open_file.write('\n' + txt_to_add)

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
                self.connection_pg(    # on fait une connection aa la base car elle est inexistant
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
                self.connection_pg( # on fait une connection aa la base car elle est inexistant
                    server01 = parser.get('pg_10_5_production', 'ip_host'),
                    user01=parser.get('pg_10_5_production', 'username'),
                    password01=parser.get('pg_10_5_production', 'password'),
                    database01=parser.get('pg_10_5_production', 'database')
                )
            self.cursor_pg_10_5__bdd_prod.execute(query)
            self.rows_pg_10_5__prod = self.cursor_pg_10_5__bdd_prod.fetchall()
            # print ""

    def set_moment(
            self,
            year,
            month,
            date,
            hour,
            min,
            sec
        ):
        self.year = year
        self.month = month
        self.date = date
        self.hour = hour
        self.min = min
        self.sec = sec
        pass


    @staticmethod
    def popup(
                window_title = "Window Title",
                msg = "Message to show"):
        """
        return 6 if you clicked yes
        return 7 if you clicked nope
        """

        # print "This break message was sent on "+time.ctime()
        messageBox = ctypes.windll.user32.MessageBoxA
        returnValue = messageBox(None, 
            msg, 
            window_title, 
            0x40 | 0x4)
        return returnValue

        pass

    def set_flag_copy_vdi(self, copy_vdi = True):
        self.copy_vdi = True


    @staticmethod
    def test_selenium001():

        
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chromeOptions.add_experimental_option("prefs",prefs)

        driver_chrome = webdriver.Chrome(
            chrome_driver_path,
            chrome_options=chromeOptions
        )
        driver_chrome.get(parser.get('selenium_10_24_gpao', 'link_gpao'))

        matr_field = driver_chrome.find_element_by_name('T1')
        pass_field = driver_chrome.find_element_by_name('T2')
        
        matr_field.clear()
        pass_field.clear()

        matr_field.send_keys(parser.get('selenium_10_24_gpao', 'login'))
        pass_field.send_keys(parser.get('selenium_10_24_gpao', 'passw'))

        pass_field.submit()

        search_field = driver_chrome.find_element_by_name('q')
        search_field.clear()
        search_field.send_keys('admin')
        
        search_button01 = driver_chrome.find_element_by_name('search')
        # search_button01.submit()
        search_button01.click()

        # search_button01.click()

        # elem_admin_push = driver_chrome.find_element_by_link_text('Administration Push')
        # elem_admin_push = driver_chrome.find_element(selenium.webdriver.common.by.By.PARTIAL_LINK_TEXT, 'text')
        # elem_admin_push = driver_chrome.find_element_by_partial_link_text("Push")
        # variable = "Push"
        # elem_admin_push = driver_chrome.find_element_by_xpath('//a[@href="'+variable+'"]')
        # print elem_admin_push
        # elem_admin_push.click()

        # links = driver_chrome.find_elements_by_partial_link_text('http')
        # print links
        
        time.sleep(5)

        links = driver_chrome.find_element_by_xpath['//*[@id="40"]/div[2]/div/div[1]/a']
        
        for link in links:
            print link.get_attribute("href")
        pass

    # this is going to run if there is D:\\vdi_debian9_64b
    def process_copy_vdi_debian(
            self, 
            delay = 3):
        
        start_time = time.time()
        while True:
            # # print type(time.time() - start_time)
            # # time.sleep(1)
            # if (time.time.now() - start_time) == 25200: # 25200sec = 7h
            if (time.time() - start_time) >= delay:
                print "baaam"
                # if (os.path.exists('D:\\vdi_debian9_64b')):
                print "ao amle anovana copie"
                # path_src = "C:\\Users\10477\\VirtualBox VMs\\Debian9_64bits"
                path_src = "D:\efi"
                path_target = "D:\\vdi_debian9_64b"

                os.rmtree(path_target)

                Our_Tools.copy_dir_content(path_src, path_target)
                # else:
                Our_Tools.popup(
                    window_title = "Info Copie vdi_debian",
                    msg = "D:\\vdi_debian9_64b est Absent")
                print "Tsy Ao ilay target_copie vdi_debian"
                sys.exit(0)
            else:
                # print time.strftime("%H:%M:%S")
                print '{:05.0f}'.format(delay - (time.time() - start_time))
                time.sleep(1)
            # print time.strftime("%H:%M:%S")
            # time.sleep(1)
            # if (time.strftime("%H:%M:%S") == '15:57:55'):
                # print "checked"
                # sys.exit(0)
                # ct_NOMINATION_AS3


    # run_our_tools
    def run(self):
        # i = 0

        if ( (self.is_thread == True) and  (self.is_thread_conf == True)):
            Our_Tools.print_red(
                txt = "chp__is_thread",
                new_line = False)
            Our_Tools.print_green(
                txt = "et",
                new_line = False)
            Our_Tools.print_red(
                txt = "chp__is_thread_conf",
                new_line = False)
            Our_Tools.print_green(
                txt = "ne peuvent pas etre vrai en meme temps",
                new_line = False)
            sys.exit(0)
            pass
        elif ( (self.is_thread == False) and  (self.is_thread_conf == False)):
            Our_Tools.print_red(
                txt = "chp__is_thread",
                new_line = False)
            Our_Tools.print_green(
                txt = "et",
                new_line = False)
            Our_Tools.print_red(
                txt = "chp__is_thread_conf",
                new_line = False)
            Our_Tools.print_green(
                txt = "sont Tous Desactivee",
                new_line = False)
            sys.exit(0)
            pass


        elif((self.is_thread_conf == True) and (self.is_thread == False)):
            # print "tonga ato"
            # sys.exit(0)
            try:
                now_date_time = datetime.datetime.now()
                
                self.time_redmine_popup = datetime.datetime.strptime(
                    self.time_redmine_popup, "%H:%M:%S")
                # you need to convert the now_date_time to now_time... so that it is easier to compare the timeS
                # # https://stackoverflow.com/questions/15105112/compare-only-time-part-in-datetime-python
                self.time_redmine_popup = now_date_time.replace(hour=self.time_redmine_popup.time().hour, 
                    minute=self.time_redmine_popup.time().minute, 
                    second=self.time_redmine_popup.time().second, 
                    microsecond=0)
                will_print_redmine_popup = True
                while True:

                    if (parser.get('thread_conf', 'pop_up_redmine') == '1'):
                        # print "tonga ato"
                        # our_tools = Our_Tools()
                        # our_tools.manage_redmine_popup()

                        # print "go"
                        now_date_time = datetime.datetime.now()
                        now_time = datetime.time(now_date_time.hour, now_date_time.minute,now_date_time.second)
                        tmp_time_redmine_popup = datetime.time(
                            self.time_redmine_popup.hour, 
                            self.time_redmine_popup.minute,
                            self.time_redmine_popup.second)

                        if (now_time > tmp_time_redmine_popup):
                            if will_print_redmine_popup:
                                Our_Tools.popup(
                                    window_title = "Redmine Pop_Up Error",
                                    msg = "Temps deja depassee")
                                will_print_redmine_popup = False
                            
                        elif (now_time == tmp_time_redmine_popup):
                            self.redmine01()
                            # sys.exit(0)
                        else:
                            # print "ato"
                            txt001 = "now_time: " + str(now_time)
                            txt001 += " time_redmine_popup: "+ str(tmp_time_redmine_popup)
                            # print txt001
                            Our_Tools.write_append_to_file(
                                path_file = 'log_redmine_popup.txt',
                                txt_to_add = txt001)
                            # Our_Tools.write_append_to_file(
                                # path_file = 'log_redmine_popup.txt',
                                # txt_to_add = txt001)
                            # print "time_redmine_popup: ", self.time_redmine_popup
                            # print time.strftime("%H:%M:%S")
                        pass
                    # if (parser.get('thread_conf', 'connection_bdd_production') == '1'):
                    if (parser.get('thread_conf', 'connection_bdd_production') == '1'):

                        self.reformat_thread_conf_test_connect_prod_10_5()

                    if (parser.get('thread_conf', 'connection_bdd_production_10_32') == '1'):
                        # print "tik"
                        self.reformat_thread_conf_test_connect_prod_10_5(
                            host = parser.get(
                                'pg_10_32_production', 
                                'ip_host'
                            ),
                            database = parser.get(
                                'pg_10_32_production', 
                                'database'
                            )
                        )
                        # print "tak"
                        pass
                    if (parser.get('thread_conf', 'connection_bdd_sdsi') == '1'):
                        self.reformat_thread_conf_test_connect_prod_10_5(
                            host = parser.get(
                                'pg_10_5_sdsi', 
                                'ip_host'
                            ),
                            database = parser.get(
                                'pg_10_5_sdsi', 
                                'database'
                            )
                        )

                        pass
                    pass

                    time.sleep(self.time_sleep_thread)

            except Exception:
                pass
        
        
        elif((self.is_thread_conf == False) and (self.is_thread == True)):

            if (
                (sys.argv[1] == '-T') and 
                (sys.argv[2] == 'test_copy_vdi_debian')
            ):
                try:
                    self.copy_vdi
                    if self.copy_vdi:
                        # print "aaaaa"
                        if (os.path.exists('D:\\vdi_debian9_64b')):
                            Our_Tools.popup(
                                window_title = "Info Copie vdi_debian",
                                msg = "Copie du vdi_debian va s_executer apres 7h")
                            self.process_copy_vdi_debian(delay = 25200) # 25200 = 7h
                        # print "bbbbbbb"
                    else:
                        #todo
                        pass
                except AttributeError:
                    pass
            elif (
                (sys.argv[1] == '-T') and 
                (sys.argv[2] == 'test_conn_db025')
            ):
                try:
                    while True:
                        key = ord(getch())
                        # print chr(key)
                        Our_Tools.write_append_to_file(
                            path_file = "log_stuffs.txt",
                            txt_to_add = chr(key)
                        )
                except KeyboardInterrupt:
                    print "<ctrl - c> est s_est executee"
                pass
            elif (
                (sys.argv[1] == '-T') and 
                (sys.argv[2] == 'test_thread_redmine')
            ):
                our_tools = Our_Tools()
                our_tools.manage_redmine_popup()
            elif (
                (sys.argv[1] == '-T') and 
                (sys.argv[2] == 'test_thread_conn')
            ):
                # print "thisi s a test"
                try:
                    while True:
                        if self.db_is_connected(
                                host = "192.168.10.5",
                                database01 = 'production'):
                            # print "connection ok au bdd(production)"
                            Our_Tools.write_append_to_file(
                                path_file = path_prg + "log_connect_db.txt",
                                txt_to_add = str(datetime.datetime.now()) + ": Connection OK au bdd(production)")
                            pass
                        else:
                            txt001 = ""
                            Our_Tools.write_append_to_file(
                                path_file = path_prg + "log_connect_db.txt",
                                txt_to_add = "************ " + str(datetime.datetime.now()) + ": Connection PERDU au bdd(production)")
                            
                            pass
                        if self.db_is_connected(
                                host = "192.168.10.5",
                                database01 = 'sdsi'):
                            Our_Tools.write_append_to_file(
                                path_file = path_prg + "log_connect_db.txt",
                                txt_to_add = str(datetime.datetime.now()) + ": Connection OK au bdd(sdsi)")
                            pass
                        else :
                            Our_Tools.write_append_to_file(
                                path_file = path_prg + "log_connect_db.txt",
                                txt_to_add = "************ " + str(datetime.datetime.now()) + ": Connection PERDU au bdd(sdsi)")
                except KeyboardInterrupt:
                    print "<ctrl - c> est s_est executee" 
                pass
                

            # for i in range(5):
                # print i
                # time.sleep(2)



            test_conn_db = False
            if (test_conn_db):
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
        else:
            Our_Tools.print_red('Vous avez Commencez le thread or que le programme n_est censee etre un thread')


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
        table_prod = "sgal85"):

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
        self.connection_pg(
            server01 = parser.get('pg_10_5_production', 'ip_host'),
            user01 = parser.get('pg_10_5_production', 'username'),
            password01=parser.get('pg_10_5_production', 'password'),
            database01=parser.get('pg_10_5_production', 'database')
        )
        self.connection_pg(
            server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
            user01=parser.get('pg_10_5_sdsi', 'username'),
            password01=parser.get('pg_10_5_sdsi', 'password'),
            database01=parser.get('pg_10_5_sdsi', 'database')
        )


        # print "self.sous_dossier01: " + self.sous_dossier01


        self.path_prog = "E:\\DISK_D\\mamitiana\\kandra\\do_not_erase\\our_tools\\"
        self.c_sql = self.path_prog + "AG22\\c.sql"
        self.c_sql_output = self.path_prog + "AG22\\c_output.sql"
        self.s1_sql = self.path_prog + "AG22\\s1.sql"
        self.s1_sql_output = self.path_prog + "AG22\\s1_output.sql"
        self.q_sql = self.path_prog + "AG22\\q.sql"
        self.q_sql_output = self.path_prog + "AG22\\q_output.sql"
        self.r_sql = self.path_prog + "AG22\\r.sql"
        self.r_sql_output = self.path_prog + "AG22\\r_output.sql"

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

        raw_input("Creation de table("+self.table_prod001+"_s1)")
        self.create_table_prod(query_prod = content_s1_sql)
        
        
        






        # raw_input()

        content_c_sql = Our_Tools.read_file_line_by_line(self.c_sql_output)
        raw_input("Creation de table(" + self.table_prod001 + "_c)")
        self.create_table_prod(query_prod = content_c_sql)
        # print content_c_sql

        # raw_input()

        content_q_sql = Our_Tools.read_file_line_by_line(self.q_sql_output)
        # print content_q_sql
        raw_input("Creation de table(" + self.table_prod001 + "_q)")
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

        Our_Tools.long_print()
        Our_Tools.print_green('Voici le requete de la m_a_j de la table_passe')
        raw_input('')

        for row in list_queries_upd_passe:
            print row

        Our_Tools.print_green('Voici les lignes qui vont etre modifiees dans table_passe@sdsi')

        Our_Tools.long_print()
        Our_Tools.print_green('Voici les requete pour verifier la table_passe')
        raw_input('')
        raw_input("")


        
        query_select_before_upd_passe_s1 = "select * from passe where idcommande like 'SGC%' and idsousdossier='SAISIE 1'"
        query_select_before_upd_passe_c = "select * from passe where idcommande like 'SGC%' and idsousdossier='CONTROLE GROUPE'"
        query_select_before_upd_passe_q = "select * from passe where idcommande like 'SGC%' and idsousdossier='ASSEMBLAGE/UNIFORMISATION'"

        """
        -- select * from passe where idcommande like 'SGC%' and idetape='SAISIE 1' and idcommande ilike ''

-- select distinct idcommande from passe order by idcommande asc;

select 
-- distinct 
idcommande, idsousdossier
from passe 
where idcommande ilike 'crh%' 
-- and idcommande like '%crh%'"""

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


    def export_table_to_xl_rapid(
            self,
            server001 = "192.168.10.5",
            user001 = "user01",
            database001 = "production",
            # table_name = "django_migrations",
            table_name = "RED001_S1",
            xl_write = "out001.xlsx"):

        # connection <<<<<<<<<<<<<<<<<<<<<<<<<<<
        # isakn commande irai   
        # # alefa ny requete
        # # exportena
        if ((server001 == "192.168.10.5") and (database001 == "production")):
            self.connection_pg(
                server01 = parser.get('pg_10_5_production', 'ip_host'),
                user01=parser.get('pg_10_5_production', 'username'),
                password01=parser.get('pg_10_5_production', 'password'),
                database01=parser.get('pg_10_5_production', 'database')
            )

        list_commande = ['crh001_q', 'CRH002']

        # connection
        # isakn commande irai   <<<<<<<<<<<<<<<<<<<<<<<<<<<
        # # alefa ny requete
        # # exportena
        for cmd in list_commande:

        # connection
        # isakn commande irai   
        # # alefa ny requete    <<<<<<<<<<<<<<<<<<<<<<<<<<<
        # # exportena
            req = """
            Select 
            n_ima,
            concat('\\',
                replace(
                        substring(lot_client, 
                            position('_' in  lot_client) + 1,
                            length(lot_client)
                        ),
                        '.',
                        '\\'
                    )
            ) as lot,
            nom,
            prenom,
            annee

            

            FROM """ +cmd+ """ ORDER BY n_lot, idenr limit 20
            """
            
            self.pg_select(
                host = "192.168.10.5",
                database01 = "production",
                query = req
            )



            # connection
            # isakn commande irai   
            # # alefa ny requete    
            # # exportena           <<<<<<<<<<<<<<<<<<<<<<<<<<<
            self.export_rows_pg_to_xl(
                xl_write = "livraison_" + cmd + ".xlsx",
                table_name = table_name
            )
            print "ato"



            sys.exit(0)

            pass
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
            self.connection_pg(
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

            self.export_rows_pg_to_xl(
                xl_write = xl_write,
                table_name = table_name)
            # workbook_write = xlsxwriter.Workbook(xl_write)
            # sheet_write = workbook_write.add_worksheet('Contenu du '+table_name)

            # x = y = 0
            # for row in self.rows_pg_10_5__prod:
                # x = 0
                # for cell in row:
                    # # print str(cell) + ": [ "+str(x)+", " +str(y)+"]"
                    # sheet_write.write(y, x, str(cell))
                    # x = x + 1
                # print 
                # y += 1
# 
            # workbook_write.close()
            pass
        elif((server001 == "192.168.10.5") and (database001 == "sdsi")):
            self.connection_pg(
                server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
                user01=parser.get('pg_10_5_sdsi', 'username'),
                password01=parser.get('pg_10_5_sdsi', 'password'),
                database01=parser.get('pg_10_5_sdsi', 'database')
            )
            self.pg_select(
                host = "192.168.10.5",
                database01 = "production",
                query = query01
            )



        pass



    # #__init__our_tools
    def __init__(self, 
            is_thread = False,
            is_thread_conf = False,
            is_thread_connection001 = True,
            time_sleep_thread = 5
    ):

        self.is_thread = is_thread

        self.is_thread_conf = is_thread_conf
        
        self.is_thread_connection = is_thread_connection001

        # self.time_redmine_popup = "15:00:00"
        # self.time_redmine_popup = "11:49:00"
        self.time_redmine_popup = parser.get('about_redmine', 'redmine_popup_time')
        
        if is_thread_connection001:
            threading.Thread.__init__(self)
            self.time_sleep_thread = time_sleep_thread

            # print int(parser.get('thread_conf', 'time_sleep_thread'))
            try:
                self.time_sleep_thread = float(parser.get('thread_conf', 'time_sleep_thread'))
            except AttributeError:
                self.time_sleep_thread = time_sleep_thread
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
                self.connection_pg(
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
                self.connection_pg(
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
            self.connection_pg(
                server01 = parser.get('pg_10_5_production', 'ip_host'),
                user01=parser.get('pg_10_5_production', 'username'),
                password01=parser.get('pg_10_5_production', 'password'),
                database01=parser.get('pg_10_5_production', 'database')
            )
        elif((server001 == "192.168.10.5") and (database001 == "sdsi")):
            self.connection_pg(
                server01 = parser.get('pg_10_5_sdsi', 'ip_host'),
                user01=parser.get('pg_10_5_sdsi', 'username'),
                password01=parser.get('pg_10_5_sdsi', 'password'),
                database01=parser.get('pg_10_5_sdsi', 'database')
            )

        pass

    @staticmethod
    def print_yellow(
            txt = "this is a test",
            new_line = True):
        default_colors = get_text_attr()
        default_bg = default_colors & 0x0070
        set_text_attr(
            FOREGROUND_YELLOW | 
            default_bg |
            FOREGROUND_INTENSITY)
        if new_line == True:
            print txt
        else:
            print txt,
        set_text_attr(default_colors)

    def edit_redmine_file(self):



        pass

    def redmine01(self):

        redmine_file = path_prg + "redmine_file.txt"

        content_redm_file = Our_Tools.read_file_line_by_line(redmine_file)

        popup_res = Our_Tools.popup(
            window_title = "Redmine",
            msg = content_redm_file)

        if popup_res == 6:
            print "yep"
        elif popup_res == 7:
            print "nope"

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
            print txt
        else:
            print txt,
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
            print txt
        else:
            print txt,
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
            print txt
        else:
            print txt,
        set_text_attr(default_colors)

    def close_connection(
            self,
            host = '192.168.10.5',
            database01 = 'sdsi'):
        if(server01 == parser.get('pg_10_5_sdsi', 'ip_host')) and (database01 == parser.get('pg_10_5_sdsi', 'database')):
            try:
                self.connect_pg_10_5_sdsi
                self.connect_pg_10_5_sdsi.close()
            except AttributeError:
                Our_Tools.print_red('Il semble que le programme n_est meme pas connectee')
                sys.exit(0)
        elif ((server01 == parser.get('pg_10_5_sdsi', 'ip_host') and (
            database01 == parser.get('pg_10_5_sdsi', 'database')))  ):
            try:
                self.connect_pg_10_5_sdsi
                self.connect_pg_10_5_sdsi.close()
            except AttributeError:
                Our_Tools.print_red('Il semble que le programme n_est meme pas connectee')
                sys.exit(0)
        pass


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

    def export_rows_pg_to_xl(self,
            xl_write = '',
            table_name = '' ):
        workbook_write = xlsxwriter.Workbook(xl_write)
        
        sheet_write = workbook_write.add_worksheet('Contenu du '+table_name)
        x = y = 0
        for row in self.rows_pg_10_5__prod:
            x = 0
            for cell in row:
                # print str(cell) + ": [ "+str(x)+", " +str(y)+"]"
                sheet_write.write(y, x, str(cell))
                x = x + 1
            # print 
            y += 1
        workbook_write.close()
        print "tonga"
        sys.exit(0)
        pass

    def __del__(self):
        print "this is a test of destructor"
        pass

    def create_table_prod(
        self,
        query_prod = ""
    ):
        print "execute create table_prod"

        self.pg_not_select(
            query01=query_prod,
            host="192.168.10.5",
            db="production")
        try:
            pass

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
                "export_table",
                "total"
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
        elif (
            (option in ("-s","--suppression_gpao_unique"))
        ):
            if (
                (len (sys.argv) == 3) 
                and (sys.argv[1] == '-s')
                and (sys.argv[2] == '--total')
            ):
                # print "suppr_total"
                # sys.exit(0)
                script001 = Our_Tools()
                script001.suppression_gpao_unique(suppr_total = 1)
            elif (
                (len (sys.argv) == 2) 
                and (sys.argv[1] == '-s')
            ):
                # print "suppr normal"
                # sys.exit(0)
                script001 = Our_Tools()

                script001.suppression_gpao_unique(suppr_total = 0)
            else:
                print "not managed at all"
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

            thread_connection.connection_pg(
                server01 = '192.168.10.5',
                user01='pgtantely', # #erreur
                password01='123456',
                database01='production'
            )
            
            thread_connection.start()
        elif option in ("-T", "--all_test"):
            args = sys.argv[2:]
            if len(args) == 0 :
                print "no param for all_tests"
            else:
                if args[0] == 'p':
                    p = Person()
                    print p
                elif args[0] == 'test_monitoring_wmi01':
                    c = wmi.WMI()
                    process_watcher = c.Win32_Process.watch_for("creation")
                    while True:
                        new_process = process_watcher()
                        print new_process.Caption
                    pass
                elif args[0] == 'test_conn_local01':
                    our_tools = Our_Tools()
                    # our_tools.connection_pg()
                    our_tools.pg_not_select(
                        query01 = "insert into test(num, data) values (3, 'this is a test');",
                        host = parser.get('pg_localhost_saisie', 'ip_host'),
                        db = parser.get('pg_localhost_saisie', 'database'),
                        log_query = True
                    )
                    pass
                elif args[0] == 'test_livr_crh_rapid':
                    our_tools = Our_Tools()
                    our_tools.export_table_to_xl_rapid()
                    pass
                elif args[0] == 'test_selenium_sfl':

                    Our_Tools.refactor_sfl_correspondance()

                elif args[0] == 'test_conn_db025':
                    # this is for the keylogger
                    # main_keylogger
                    our_tools = Our_Tools(
                        is_thread = True,
                        is_thread_conf = False,
                        time_sleep_thread = 1)
                    our_tools.start()
                    pass
                elif args[0] == 'test_mahaitia001':
                    
                    thread001 = Thread001()
                    thread001.start()
                    pass
                elif args[0] == 'test_tabwidget_pyqt001':
                    Our_Tools.test_tabwidget_pyqt001()
                elif args[0] == 'test_tabwidget_pyqt':
                    Our_Tools.test_tabwidget_pyqt()
                    pass
                elif args[0] == 'test_asyncio':
                    Our_Tools.to_del_asyncio001()
                    pass
                elif args[0] == 'test_multithread005':
                    Our_Tools.test_multithread005()
                    pass
                elif args[0] == 'test_multithread004':
                    Our_Tools.test_multithread004()
                    pass
                elif args[0] == 'test_multithread003':
                    Our_Tools.test_multithread003()
                    pass
                elif args[0] == 'test_multithread002':
                    Our_Tools.test_multithread002()
                    pass
                elif args[0] == 'test_multithread001':

                    Our_Tools.test_multithread001()
                    
                    pass
                elif args[0] == 'test_thread_conf':
                    our_tools = Our_Tools(
                        is_thread = False,
                        is_thread_conf = True,
                        time_sleep_thread = 1)
                    our_tools.start()
                    pass
                elif args[0] == 'test_disp_pic':
                    Our_Tools.display_pic()
                    pass
                elif args[0] == 'test_append_file':
                    Our_Tools.write_append_to_file()
                    pass
                elif args[0] == 'test_edit_file_redmine':
                    Our_Tools.edit_file_w_sublime2()
                    pass
                elif args[0] == 'test_thread_redmine':
                    our_tools = Our_Tools(is_thread = True)
                    our_tools.start()
                    pass
                elif args[0] == 'test_thread_conn':
                    our_tools = Our_Tools(
                            is_thread = True,
                            time_test_connection01 = 1)
                    our_tools.start()
                    pass
                elif args[0] == 'test_selenium001':
                    Our_Tools.test_selenium001()
                    pass

                elif args[0] == 'test_copy_dir':
                    Our_Tools.copy_dir_content()
                    pass
                elif args[0] == 'test_pop_up':
                    Our_Tools.popup()

                elif args[0] == 'test_copy_vdi_debian':
                    our_tools = Our_Tools(is_thread = True)
                    our_tools.set_flag_copy_vdi()
                    our_tools.start()

                elif args[0] == 'test_thread001':
                    print 'test_thread001'
                    thread001 = Our_Tools(
                        is_thread = True)
                    
                    thread001.start()
                    pass

                elif args[0] == 'conn_local_sdsi':
                    our_tools = Our_Tools()
                    our_tools.connection_pg(
                        server01 = parser.get('pg_localhost_sdsi', 'ip_host'),
                        user01=parser.get('pg_localhost_sdsi', 'username'),
                        password01=parser.get('pg_localhost_sdsi', 'password'),
                        database01=parser.get('pg_localhost_sdsi', 'database')
                    )
                    pass
                elif args[0] == 'manage_usb_storage':
                    # print "sys.argv"
                    # print sys.argv
                    # # just remember, sys.argv is going to contain everything which is 
                    # # # given to the prompt... even if the the name of the script
                    # sys.exit(0)
                    if (len(sys.argv) == 4) and sys.argv[3] == 'activate':
                        Our_Tools.manage_usb_store_w_regedit(state = 3)
                        # Our_Tools.print_green('USB_storage Activated')
                    elif (len(sys.argv) == 4) and sys.argv[3] == 'deactivate':
                        Our_Tools.manage_usb_store_w_regedit(state = 4)
                        # Our_Tools.print_green('USB_storage DeActivated')
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
                elif args[0] == 'csv_read001':
                    our_tools = Our_Tools()
                    l001 = our_tools.csv_to_list()
                    print l001
                elif args[0] == 'csv_read_content':
                    list_content = Our_Tools.csv_read_content()
                    # for content in list_content:
                        # print content
                    # pass
                elif args[0] == 'automate_redmine':
                    our_tools = Our_Tools()
                    our_tools.automate_redmine()
                elif args[0] == 'csv_read_all':
                    list_content = Our_Tools.csv_read_all()
                    for cont in list_content:
                        print cont
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
                else:
                    Our_Tools.print_red('L_option '+args[0]+' dans la n_est pas pris en charge')

        elif option in ("-x", "--x = testing001"):
            # Our_Tools.test001()
            Our_Tools.test002()
        elif option in ("-z", "--zeta"):
            print "option: " + option
            print "val: ", sys.argv[2:]

if __name__ == '__main__':
    main()




