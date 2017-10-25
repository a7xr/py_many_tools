#!/usr/bin/env python
# -*- coding: cp1252  -*-

# Nom : CLASS D'OBJET MENUS
# Descr: Création d'un intérface graphique menu standard
# Domaine : Commande BDD
# Auteur : Jaona IOS
# Date : 27-12-2010
#Date de mis à jour : 23-02-2011          par : Jaona IOS
#--------------------------------------------------------
import os,stat,re
import psycopg2
import psycopg2.extras
from shutil import *
from string import *

import datetime
from datetime import datetime

#import stdnum

import re
#import testiban as verifIban

import wx
import sys
reload(sys)
sys.setdefaultencoding('cp1252')



#print stdnum.fr.#siren.is_valid('dsd3323232323')
#----------------------------------------------------------------------------------------------------------------------------------------------------
class Fonction:
    """Classe d'objet comportant les bibliotheques des fonction."""
    def __init__(self):
        """ Methode constructeur """
        pass
    
       

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def isnumerique(self,chaine):
        """Fonction de test qui renvoie True si une chaine est entierement numerique"""
        i=0
        result = True
        while (i<len(chaine)):
            if chaine[i] not in "0123456789":
                result = False
                return result
            i= i+1
        return result

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def ismatValide(self,chaine):
        """ Fonction de test si une matricule est valide nombre à 4 chiffres """
        if(self.isnumerique(chaine)==True and len(chaine)==4):
            return True
        else:
            return False

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def iscomValide(self,chaine):
        """ Fonction de test si une identité commande est de la forme 3lettre-3chiffres """
        i=0
        j=3
        res = True
        AaZ = 'AZERTYUIOPQSDFGHJKLMWXCVBN'
        if(len(chaine)!=6):
            return False
        while(i<3):
            if(chaine[i] not in AaZ):
                return False
            i=i+1

        while(j<6):
            if(chaine[j] not in '0123456789'):
                return False
            j=j+1

        return res





    def magicquotes(self,chaine):
        old = "'"
        new = "\\'"
        chaine = chaine.replace(old, new)
        return chaine


    #------------------------------------------------------------------------------------------------------------------------------------------------
    def checkVal(self,tzNameChamp,tzName,conteneur=None):
        i=0
        RES  = True
        while(i<len(tzNameChamp)):
            if(tzNameChamp[i].get()==""):
                if(len(tzNameChamp)==len(tzName)):
                    self.errorDlg("Champ requis!","Le champs :"+tzName[i]+" est obligatoire !")
                    if(conteneur!=None):
                        conteneur.yview('moveto',float(i)*0.08,1.0)
                    tzNameChamp[i].focus_force()
                    return False
                else:
                    self.errorDlg("Champ requis!","Un champ réquis  est vide !")
                    tzNameChamp[i].focus_force()
                    RES = False
                    return False
            else:
                pass
            i=i+1
        return RES

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def delAll(self,tzWid):
        if(len(tzWid)>0):
            i=0
            while(i<len(tzWid)):
                tzWid[i].delete(0,END)
                i=i+1

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def delEntry(self,widget):
        widget.delete(0,END)

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def formates(self,iNombre):
        """ Formater un chiffre en format de 3 chiffre """
        if(str(iNombre) in '0123456789'):
            if(iNombre<10):
                zFormt = '00'+str(iNombre)
                return zFormt
            elif(iNombre<100):
                zFormt = '0'+ str(iNombre)
                return zFormt
            else:
                return iNombre
        else:
            return iNombre

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def isNumpos(self,Chaine,baccepterzero=False):
        """Fonction de test et renvoie une valeur True si toutes les caracteres dans une chaine Chaine sont tous des nombres positives, renvoie False si non.  """
        res = False
        chiffre = "123456789"
        if baccepterzero==True:
            chiffre=chiffre+"0"
        i=0
        sCh  = str(Chaine)
        while(i<len(sCh)):
            if(sCh[i] in chiffre):
                res = True
            i=i+1
        return res


    #------------------------------------------------------------------------------------------------------------------------------------------------
    def is0a9(self,Chaine):
        """ Cette fonction renvoie True si les carateres dans Chaine sont tous des nombres 0 à 9, revoie False si non. """
        res = True
        AaZ = "0123456789"
        i=0
        while(i<len(Chaine)):
            if(Chaine[i] not in AaZ):
                res = False
                break
            i=i+1
        return res

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def GetMarqueCount(self,chaine,separateur):
        """Compte les caracteres separateur presents dans chaine, ajoute un separateur fictif en fin de chaine, renvoie les nombre des separateurs incrementé de 1. """
        i = chaine.count(separateur)
        if(i>0):
            resultat = i+1
        else:
            resultat = 1
        return resultat

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def GetMarqueString(self,index,chaine,separateur):
        """Cette fonction subdivise la chaine en fonction des nombres de separateur , renvoie la subdivision numéro index. """
        nCount = self.GetMarqueCount(chaine,separateur)
        res = ""
        if(nCount==1):
            res = chaine
        else:
            i=1
            debut = 0
            while(i<=nCount):
                position1 = debut
                position2 = chaine.find(separateur,position1+1)

                if(position2==-1):
                    sCh = chaine[position1:len(chaine)]
                else:
                    sCh = chaine[position1:position2]

                if(i==index):
                    res = sCh
                i=i+1
                step = len(separateur)
                debut = position2+step
        return res

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def isDansUnique(self,sVal,sCount,sSep=";"):
        """ Renvoie True si la chaine sVal est une sous ensembe de la chaine sCount separée par le separateur sSep, False si non """
        IsDansUnique = False
        nCount = self.GetMarqueCount(sCount,sSep)

        if(nCount>1):
            i=1
            while(i<=nCount):
                sCh = self.GetMarqueString(i, sCount, sSep)

                if(sCh==sVal):
                    IsDansUnique=True
                i=i+1

        else:
            if(sCount == sVal ):
                IsDansUnique = True
        return IsDansUnique

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def isDansMultiple_old(self,sVal,sCount,sSep,step=1):
        """ Pas encore terminé """
        iTest = sVal.find(sSep)
        if(iTest==-1):
            sCh = ""
            NbLoop = math.floor(len(sVal)/step)
            i=0
            offset = step
            while(i<NbLoop):
                if(i<NbLoop-1):
                    sCh = sCh + sVal[i:offset]+';'
                else:
                    sCh = sCh + sVal[i:offset]
                i=i+1

            sVal = sCh
        return NbLoop

    def isDansMultiple(self,sVal,sLim,sSep=';'):
        """ Pas encore terminé """
        isdansMultiple = False
        tLim = sLim.split(sSep)
        if sVal in tLim:
            isdansMultiple = True

        return isdansMultiple


    def isEmailValide(self,semail):
        valiny = True
        if semail.islower()==False:
            return False
        #email_re = re.compile(r"(^[-_0-9A-Z]+(\.[-_0-9A-Z]+)*)$", re.IGNORECASE)
        email_re = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)
        semail = "%s"%(semail)
        return bool(email_re.search(semail))



    def isBicValide(self,sbic):
        #email_re = re.compile(r"(^[-_0-9A-Z]+(\.[-_0-9A-Z]+)*)$", re.IGNORECASE)
        bic_re = re.compile(r"^([a-zA-Z]){4}([a-zA-Z]){2}([0-9a-zA-Z]){2}([0-9a-zA-Z]{3})?$")
        sbic = "%s"%(sbic)
        return bool(bic_re.search(sbic))

    def checkIban(self,sIban):
        return verifIban.is_valid(sIban)




    def replaceAll(self,text, char_map):
        """Replace the char_map in text"""
        for k, v in char_map.iteritems():
            text = text.replace(k, v)
        return text

    def is_valid_iban(self,iban):
        """Test the International Bank Account Number"""
        IBAN_CHAR_MAP = {"A":"10", "B":"11", "C":"12", "D":"13", "E":"14", "F":"15",
                         "G":"16", "H":"17", "I":"18", "J":"19", "K":"20", "L":"21",
                         "M":"22", "N":"23", "O":"24", "P":"25", "Q":"26", "R":"27",
                         "S":"28", "T":"29", "U":"30", "V":"31", "W":"32", "X":"33",
                         "Y":"34", "Z":"35"}

        sIban = u"%s"%(iban)
        resulttest = True
        for c in sIban:
            if (ord(c) >=48 and ord(c)<=57 ) or (ord(c) >=65 and ord(c)<=90 ) or (ord(c) >=97 and ord(c)<=122 ):
                pass
            else:
                resulttest = False
                return resulttest
                break

        if sIban.isupper()==False:
            return False
        iban = iban.replace('-', '').replace(' ', '')
        iban = self.replaceAll(iban[4:]+iban[0:4], IBAN_CHAR_MAP)
        res = int(iban) % 97
        return res == 1

    def checkSiret(self,sSiren):
        sSiren = str(sSiren)
        if len(sSiren)!=14:
            return False
        tpair = []
        timpair = []
        for c in range(14,0,-1):
            if sSiren[c-1] not in "0123456789":
                return False
            if c%2==0:
                timpair.append(sSiren[c-1])
            else:
                tpair.append(str(int(sSiren[c-1])*2))

        spair  = 0
        for c in tpair:
            for s in c:
                spair+=int(s)

        simpair = 0
        for c in timpair:
            simpair+=int(c)*1

        resultat = spair+ simpair
        return resultat%10==0

    def checkSiren(self,sSiren):
        sSiren = str(sSiren)
        if len(sSiren)!=9:
            return False
        tpair = []
        timpair = []
        for c in range(9,0,-1):
            if sSiren[c-1] not in "0123456789":
                return False
            if c%2==0:
                tpair.append(str(int(sSiren[c-1])*2))
            else:
                timpair.append(sSiren[c-1])

        spair  = 0
        for c in tpair:
            for s in c:
                spair+=int(s)

        simpair = 0
        for c in timpair:
            simpair+=int(c)*1

        resultat = spair+ simpair
        return resultat%10==0




    def isEmailValide000(self,semail):
        email_re = re.compile(r"(^[-_0-9A-Z]+(\.[-_0-9A-Z]+)*)$", re.IGNORECASE)
        semail = "%s"%(semail)
        return bool(email_re.search(semail))

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def isMailCorrect(self,sMail):
        """ Cette fonction permet de verifier si une chaine sMail a un bon format d'email, la fonction retourne False si c pas un bon format et True si oui."""
        Test = True
        strapres = ""
        strAvant = ""
        strDomaine = ""
        AaZ = 'azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN'
        Autres = '0123456789-_.'
        posarondbase = sMail.find('@')
        strApresavecDom = sMail[posarondbase+1:len(sMail)]
        if(posarondbase==-1):
            Test = False
            return Test
        else:
            strAvant = sMail[0:posarondbase]
            strApresavecDom = sMail[posarondbase:len(sMail)]

            posPoint = strApresavecDom.find('.')
            if(posPoint==-1):
                Test = False
                return Test
            else:
                strapres = strApresavecDom[1:posPoint]
                strDomaine = strApresavecDom[posPoint+1:len(strApresavecDom)]
            if(strAvant==""):
                Test = False
                return Test
            else:

                if(len(strAvant)>60):
                    Test = False
                    return Test
                else:
                    i=0
                    while(i<len(strAvant)):
                        if(strAvant[i] not in AaZ and strAvant[i] not in Autres ):
                            Test = False
                            return Test
                        i=i+1

            #strapres
            if(strapres == ""):
                Test = False
                return Test
            else:
                if(len(strapres)>50):
                    Test = False
                    return Test
                else:
                    i=0
                    while(i<len(strapres)):
                        if(strapres[i] not in AaZ and strapres[i] not in Autres):
                            Test = False
                            return Test
                        i=i+1

        #strdomaine

            if(strDomaine==""):
                Test = False
#desactivation car le domaine comme .mg .net introuvable alors toujours faux sinon
#            else:
#                connexion       =  psycopg2.connect("dbname=Adresse user=op1 password=aa host=192.168.10.5")
#
#                strDomaine      = strApresavecDom[1:len(strApresavecDom)].lower()
#
#                curseur         = connexion.cursor()
#                curseur.execute("SELECT * FROM \"EMAIL_DOMAINE\" WHERE \"DOMAINE\" ='"+strDomaine+"'")
#                verif           = curseur.fetchone()
#                if(verif==None):
#                    Test=False

        return Test


    #------------------------------------------------------------------------------------------------------------------------------------------------

    def isAnneebissec(self,annee):
        pas = """L'année n'est pas bissextile."""
        oui = """L'année est bissextile."""
        #print "type entry(%s):%s"%(annee,type(annee))
        try:
            annee=int(annee)
        except:
            pass

        bresult = False
        if annee%4==0 :
        	if annee%100==0 :
        		if annee%400==0 :
        			bresult = True
        	else :
        		bresult = True
        return bresult


    #todo test datesogec
    def isDateSogec(self,sDate,sType,sLimitAnnee = ["2013","2014","2015","2016","2017"]):
        """ Fonction de verification si la chaine sDate a un bon format date selon les specification sType : D1-D2-D3-D4-D5-D6 """
        #print 'test date',sDate,' dddddd'
        #sLimitAnnee = []
        j=0
        m=0
        a=0
        Test = True
        


        if(sType=='D2'):#----JJ/MM/AAAA
            if(sDate=="" or sDate.isspace()== True or len(sDate)!=10):
                Test = False;return Test
            else:
                if sDate.count("/")!=2:
                    return False
                if sDate.rfind("/")!=5:
                    return False

                j = sDate[0:2]
                m = sDate[3:5]
                a = sDate[6:10]
                if len(a)!=4:
                    return False

                if len(sLimitAnnee)>0:
                    if str(a) not in sLimitAnnee:
                        return False
        


        if(self.isNumpos(j) and self.isNumpos(m) and self.isNumpos(a,baccepterzero=True)):
            Test = True
        else:
            Test = False
            return Test

        if(int(m)<1 or int(m)>12 or int(j)<1 or int(j)>31 or int(a)<0 ):
            Test = False
            return Test
        else:
            if(m in ['04','06','09','11']):
                if(int(j)>30):
                    Test = False
                    return Test

            elif(m=='02'):
                if self.isAnneebissec(a):
                    if(int(j)>29):
                        Test = False
                        return Test
                else:
                    if(int(j)>28):
                        Test = False
                        return Test
        if Test==True:
            sdate_sogec=sDate[6:]+"-"+sDate[3:5] +"-" +sDate[0:2]
            #print sdate_sogec
#            dateb = datetime.now()           
#            datedujour = dateb.strftime('%Y/%m/%d')
            sdsi      = psycopg2.connect("dbname=sdsi user=prep1 password=pp1p  host=192.168.10.5") #sdsi
            sdsi.set_isolation_level(0)
            cursdsi   = sdsi.cursor(cursor_factory=psycopg2.extras.DictCursor);            
            sql = "select now()::date::text as datedujour"
            cursdsi.execute(sql)
            datedujour = cursdsi.fetchone()
            datedujour = datedujour['datedujour']
            #print datedujour       

            if (sdate_sogec > datedujour):
                Test = False
                return Test
            
              
        return Test
    
    def isDateCorrect(self,sDate,sType,sLimitAnnee = ["2013","2014"]):
            """ Fonction de verification si la chaine sDate a un bon format date selon les specification sType : D1-D2-D3-D4-D5-D6 """
            #print 'test date',sDate,' dddddd'
            #sLimitAnnee = []
            j=0
            m=0
            a=0
            Test = True
            if(sType!='D1' and sType!='D2' and sType!='D3' and sType!='D4' and sType!='D5' and sType!='D6'):
                Test = False;return Test
            else:
                if(sType=='D1'):#----JJ/MM/AA
                    if(sDate=="" or sDate.isspace()== True or len(sDate)!=8):
                        Test = False;return Test
                    else:
                        if sDate.count("/")!=2:
                            return False
                        j = sDate[0:2]
                        m = sDate[3:5]
                        a = sDate[6:8]
    
    
                elif(sType=='D2'):#----JJ/MM/AAAA
                    if(sDate=="" or sDate.isspace()== True or len(sDate)!=10):
                        Test = False;return Test
                    else:
                        if sDate.count("/")!=2:
                            return False
                        if sDate.rfind("/")!=5:
                            return False
    
                        j = sDate[0:2]
                        m = sDate[3:5]
                        a = sDate[6:10]
                        if len(a)!=4:
                            return False
    
                        if len(sLimitAnnee)>0:
                            if str(a) not in sLimitAnnee:
                                return False
                elif(sType=='D3'):#----AAAA-MM-JJ
                    if(sDate=="" or sDate.isspace()== True or len(sDate)!=10):
                        Test = False;return Test
                    else:
                        if sDate.count("-")!=2:
                            return False
                        if sDate.find("-")!=4:
                            return False
    
                        j = sDate[8:10]
                        m = sDate[5:7]
                        a = sDate[0:4]
                        if len(sLimitAnnee)>0:
                            if str(a) not in sLimitAnnee:
                                return False
    
                elif(sType=='D4'):#-----AAAAMMJJ
                    if(sDate=="" or sDate.isspace()== True or len(sDate)!=8):
                        Test = False
                        return Test
                    else:
                        j = sDate[6:8]
                        m = sDate[4:6]
                        a = sDate[0:4]
                        if len(sLimitAnnee)>0:
                            if str(a) not in sLimitAnnee:
                                return False
    
    
                elif(sType=='D5'):#-----JJMMAA
                    if(sDate=="" or sDate.isspace()== True or len(sDate)!=6):
                        Test = False
                        return Test
                    else:
                        j = sDate[0:2]
                        m = sDate[2:4]
                        a = sDate[4:6]
                elif(sType=='D6'):#----JJMMAAAA
                    if(sDate=="" or sDate.isspace()== True or len(sDate)!=8):
                        Test = False
                        return Test
                    else:
                        j = sDate[0:2]
                        m = sDate[2:4]
                        a = sDate[4:8]
                        if len(sLimitAnnee)>0:
                            if str(a) not in sLimitAnnee:
                                return False
    
                elif(sType=='D7'):#----JJ/MM/AAAA ou 00/MM/AAAA OU 00/00/AAAA ou 00/00/0000
                    if(sDate=="" or sDate.isspace()== True or len(sDate)!=10):
                        Test = False
                        return Test
                    else:
                        j = sDate[0:2]
                        m = sDate[3:5]
                        a = sDate[6:10]
                        if len(sLimitAnnee)>0:
                            if str(a) not in sLimitAnnee:
                                return False
    
    
                if(self.isNumpos(j) and self.isNumpos(m) and self.isNumpos(a,baccepterzero=True)):
                    Test = True
                else:
                    Test = False
                    return Test
    
            if(int(m)<1 or int(m)>12 or int(j)<1 or int(j)>31 or int(a)<0 ):
                Test = False
                return Test
            else:
                if(m in ['04','06','09','11']):
                    if(int(j)>30):
                        Test = False
                        return Test
    
                elif(m=='02'):
                    if self.isAnneebissec(a):
                        if(int(j)>29):
                            Test = False
                            return Test
                    else:
                        if(int(j)>28):
                            Test = False
                            return Test
            return Test
    

    def setdate(self,sDate,sTypeCible):
        """ Fonction de verification si la chaine sDate a un bon format date selon les specification sType : D1-D2-D3-D4-D5-D6 """
        #print 'test date',sDate,' dddddd'
        j=0
        m=0
        a=0
        Test = True
        if(sTypeCible!='D1' and sTypeCible!='D2' and sTypeCible!='D3' and sTypeCible!='D4' and sTypeCible!='D5' and sTypeCible!='D6'):
            Test = False;return sDate
        else:
            if(sTypeCible=='D1'):#----JJ/MM/AA
                if(sDate=="" or sDate.isspace()== True or len(sDate)!=8):
                    Test = False;return sDate
                else:
                    j = sDate[0:2]
                    m = sDate[2:4]
                    a = sDate[6:]
                    return j+'/'+m+'/'+a

            elif(sTypeCible=='D2'):#----JJ/MM/AAAA
                if(sDate=="" or sDate.isspace()== True or len(sDate)!=8):
                    Test = False;return sDate
                else:
                    j = sDate[0:2]
                    m = sDate[2:4]
                    a = sDate[4:]
                    return j+'/'+m+'/'+a

            elif(sTypeCible=='D3'):#----AAAA-MM-JJ
                if(sDate=="" or sDate.isspace()== True or len(sDate)!=8):
                    Test = False;return sDate
                else:
                    j = sDate[0:2]
                    m = sDate[2:4]
                    a = sDate[4:]
                    return a+'-'+m+'-'+j

            elif(sTypeCible=='D4'):#-----AAAAMMJJ
                if(sDate=="" or sDate.isspace()== True or len(sDate)!=8):
                    Test = False;return sDate
                else:
                    j = sDate[0:2]
                    m = sDate[2:4]
                    a = sDate[4:]
                    return str(a)+str(m)+str(j)


            elif(sTypeCible=='D5'):#-----JJMMAA
                if(sDate=="" or sDate.isspace()== True or len(sDate)!=8):
                    Test = False;return sDate
                else:
                    j = sDate[0:2]
                    m = sDate[2:4]
                    a = sDate[6:]
                    return str(j)+str(m)+str(a)

            else:
                return sDate


    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsEspacePresent(self,chaine):
        """ Cette fonction renvoie une valeur True si une espace est presente dans chaine, false si non."""
        i=0
        res = False
        while(i<len(chaine)):
            if(chaine[i]==" "):
                res = True
                break
            i=i+1
        return res


    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsAccentPresent(self,chaine):
        """ Fonction de vérification si un caractere accentué est present dans chaine, retourne True si OUI et False si NON"""
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"
        res = False
        i=0
        while(i<len(chaine)):
            if(chaine[i] in ListeAccents):
                res = True
                break
            i=i+1
        return res

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsMajus(self,chaine):
        """Retourne True si touts les caracteres dans chaine sont majuscules """
        for i in chaine:
#            print i
            if str(i).upper()  in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if i.isupper()==False:
                    return False
        return True

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsMinus(self,chaine):
        """Retourne True si touts les caracteres dans chaine sont minuscules """
        for i in chaine:
            if str(i).upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if i.islower()==False:
                    return False
        return True


    #------------------------------------------------------------------------------------------------------------------------------------------------
    def GetIllOut(self,chaine,signe='<?>'):
        """Enleve les caracteres signe dans chaine """
        nCount = self.GetMarqueCount(chaine,signe)
        if(nCount>1):
            GetIllOut = ""
            i=0
            while(i<=nCount):
                GetIllOut = GetIllOut + " " + self.GetMarqueString(i, chaine, signe)
                i=i+1
        else:
            GetIllOut = chaine

        return GetIllOut

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsMontant(self,chaine,sep=','):
        """ Verifier si chaine est un montant composé par des chiffre , avec ou sans virgule sep, et seulement 2 chiffres apres virgule. """
        res = True
        i=0
        while(i<len(chaine)):
            if(chaine[i] not in '0123456789'+sep):
                res = False
                return res
            i=i+1
        nombVirgule = chaine.count(sep)
        if(nombVirgule!=1):
            res = False
            return res
        else:
            posVirgule = chaine.find(sep)
            if(posVirgule!=-1):
                sChApres   = chaine[posVirgule+1:len(chaine)]
                if(len(sChApres)!=2):
                    res = False
                    return res
        return res

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def RemplacerXParY(self,chaine,old,new,nombre=0):
        """Remplace l'occurence old par new dans chaine, Si nombre est vide ou zero, toutes les occurences seront remplacées, si non les occurences nombre premiers seront remplacées"""
        if(nombre!=0 and str(nombre) in ('123456789')):
            sCh = chaine.replace(old,new,nombre)
        else:
            sCh = chaine.replace(old,new)
        return sCh

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsDieseEtoilePresent(self,chaine):
        """ Cette fonction renvoie une valeur True si il y  a un caractere * ou # dans chaine, False si non. """
        i=0
        res = False
        while(i<len(chaine)):
            if(chaine[i] in ('*#')):
                res = True
                return res
            i=i+1
        return res

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def GetCodePays(self,pays):
        """ Fonction qui renvoie le code du pays pays"""
        connexion       =  psycopg2.connect("dbname=postgres user=postgres password=123456")
        data = BDD.selectfirst(connexion,"SELECT CODE FROM pays WHERE PAYS='"+pays+"'")
        if(data!=None):
            return data[0]
        else:
            return "Vide"

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def Compare(self,table1='standard',table2='standard2'):
        connexion       =  psycopg2.connect("dbname=postgres user=postgres password=123456")
        """ Verification si les contenues des deux tables table1 et table2 sont identiques """
        tzChamps = BDD.getChamps(table1)
        res     = True
        tsta    = BDD.selectfirst(connexion,"SELECT * FROM " + table1)
        tsta2   = BDD.selectfirst(connexion,"SELECT * FROM " + table2)

        if(len(tsta)!=len(tsta2)):
            res = False
            return res
        else:
            nmbCol = len(tsta)
            i=0
            erreur = 0
            zChampErr = ""
            while(i<nmbCol):
                if(tsta[i]!=tsta2[i]):
                    erreur = erreur+1
                    if(zChampErr==""):
                        zChampErr = tzChamps[i][0]
                    else:
                        zChampErr = zChampErr + ','+ tzChamps[i][0]

                    res = False
                    req = "INSERT INTO  \"CHAMPS_FAUTES\"  VALUES('"+tsta[0]+"','"+tsta[1]+"','"+tzChamps[i][0]+"')"
                    #print req
                    BDD.insertion(connexion,req)
                    #return res
                i=i+1
        if(res==False):
            pass
        return res

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def replaceX(self,chaine):
        """ Enleve les accents dans chaine ."""
        sCh = chaine.replace("°", "")
        sCh = sCh.replace("'", "")
        sCh = sCh.replace(";", "")

        sCh = sCh.replace("É", "E")
        sCh = sCh.replace("Ê", "E")
        sCh = sCh.replace("È", "E")
        sCh = sCh.replace("Ë", "E")

        sCh = sCh.replace("À", "A")
        sCh = sCh.replace("Â", "A")
        sCh = sCh.replace("Ä", "A")

        sCh = sCh.replace("Ù", "U")
        sCh = sCh.replace("Û", "U")
        sCh = sCh.replace("Ü", "U")

        sCh = sCh.replace("Î", "I")
        sCh = sCh.replace("Ï", "I")

        sCh = sCh.replace("Ö", "O")
        sCh = sCh.replace("Ô", "O")
        return sCh

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def MajIni(self,chaine):
        newChaine = chaine
        Ini = chaine[0:1]
        if(Ini.isupper()==False):
            newChaine = Ini.upper()+chaine[1:len(chaine)]
        return newChaine

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsCodePaysIn (self,sCode,table='PAYS1'):
        connexion       =  psycopg2.connect("dbname=postgres user=postgres password=123456")
        """ Fonction qui renvoie true si  le code sCode est verifié """
        REQ = "SELECT * FROM \"" +table+ "\" WHERE \"CODE\"='"+sCode+"'"

        data = BDD.selectfirst(connexion,REQ)
        if(data!=None):
            return True
        else:
            return False

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsPaysIn(self,sPays,table='PAYS1'):
        connexion       =  psycopg2.connect("dbname=postgres user=postgres password=123456")
        """ Fonction qui renvoie true si le pays sPays est verifié"""
        REQ = "SELECT * FROM \"" +table+ "\" WHERE \"PAYS\"='"+sPays+"'"

        data = BDD.selectfirst(connexion,REQ)
        if(data!=None):
            return True
        else:
            return False

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsCodeMagIn(self,sCode,table='tb_magasin'):
        connexion       =  psycopg2.connect("dbname=postgres user=postgres password=123456")
        REQ = "SELECT * FROM \"" +table+ "\" WHERE \"CODE_MAGASIN\"='"+sCode+"'"

        data = BDD.selectfirst(connexion,REQ)
        if(data!=None):
            return True
        else:
            return False

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def TexteEntreDeuxBalises(self,textComm,balise1,balise2):
        posBal1 = textComm.find(balise1)
        posBal2 = textComm.find(balise2)
        if(posBal1!=-1 and posBal2!=-1):
            deb = posBal1+len(balise1)
            fin = posBal2
            texte = textComm[deb:fin]
        else:
            texte = textComm
        return texte

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def exitChamps_D1(self,name1,name2):
        global xretour
        if(xretour==True):
            xretour = False
            name2.focus_force()

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def exitChamps_D2(self,name1,name2):
        global xretour
        if(name1.get()!=name2.get()):
            name1.delete(0,END)
            name2.delete(0,END)
            xretour = True
            name1.focus_force()

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def TDS(self,X1, X2):
        """ Cette fonction compare deux chaine de caractere et renvoie True si les deux chaines sont identiques et False si non """
        res = False
        if((X1.isspace()==True and X2.isspace()==True) or (X1=="" and X2=="")):
            res = True
        else:
            if(X1!=X2):
                res = False
            else:
                res = True
        return res

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def NettoyagePonctPresent(self,chaine):
        """ Cette fonction enleve les accents dans une chaine"""
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"
        ReplaceListeAccents = "EEEEAAAUUUIIOOCeeeeaaauuuiiooc"
        k=0
        chainenew=""
        while(k<len(chaine)):
            j=0
            while(j<len(ListeAccents)):
                if(ListeAccents[j]==chaine[k]):
                    chaine  = chaine.replace(chaine[k],ReplaceListeAccents[j])
                j=j+1
            k=k+1
        return chaine.replace("  "," ")


    #------------------------------------------------------------------------------------------------------------------------------------------------
    def MajContO(self,sTrt,objConnexion):
        requette = "UPDATE CONTROLE SET ETAT = 'O' WHERE TRAITEMENT = '" + sTrt + "' "
        curseur = objConnexion.cursor()
        curseur.execute(requette)
        connexion.commit()
        return True

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def MajContN(self,objConnexion):
        requette = "UPDATE CONTROLE SET ETAT = 'N'"
        curseur = objConnexion.cursor()
        curseur.execute(requette)
        connexion.commit()
        return True


    #------------------------------------------------------------------------------------------------------------------------------------------------
    def Is0a9ponctA(self,chaine,ponctA,ponctNA,bEspA='0'):
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"
        listeAaZ = "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn"
        chiffre = "0123456789"
        Is_0a9PonctA = True
        i=0
        while(i<len(chaine)):
            if(bEspA=='0'):
                if chaine[i]==" ":
                    return False

            else:
                if((ponctA=="" and ponctNA=="") or (ponctA.isspace()==True and ponctNA.isspace()==True)):
                    if(chaine[i] in ListeAccents or chaine[i] in listeAaZ or chaine[i] not in chiffre or chaine[i]=='\t' or chaine[i]=='\n'):
                        Is_0a9PonctA= False
                        return Is_0a9PonctA
                if(ponctA!="" and ponctNA==""):
                    if(chaine[i]  not in ponctA and  chaine[i] not in chiffre ):
                        return False
                if(ponctA=="" and ponctNA!=""):
                    if((chaine[i]  in ponctNA and chaine[i] not in chiffre)  or (chaine[i]=='\t' or chaine[i]=='\n')):
                        return False
                if(ponctA!="" and ponctNA!=""):
                    if((chaine[i] not in ponctA and chaine[i] in ponctNA and chaine[i] not in chiffre)  or (chaine[i]=='\t' or chaine[i]=='\n')):
                        return False

            i=i+1

        return Is_0a9PonctA

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def Is_0a9_Esp(self,chaine):
        chiffre = "0123456789 "
        i=0
        is_0a9_Esp = True
        while(i<len(chaine)):
            if(chaine[i] not in chiffre):
                return False
            i=i+1
        return is_0a9_Esp

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def Is_0a9_Present(self,chaine):
        chiffre = "0123456789"
        i=0
        result = False
        while(i<len(chaine)):
            if(chaine[i] in chiffre):
                result = True
                return result
            i=i+1
        return result

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsPonctPresent(self,chaine,bill=False):
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç "
        listeAaZ = "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn "
        chiffre = "0123456789"
        isPonctPresent = False
#        if(bill==True):
#            sCh = self.GetIllOut(chaine)
#        else:
        sCh = chaine
        i=0
        while(i<len(sCh)):
            if(sCh[i] not in ListeAccents and sCh[i] not in listeAaZ and sCh[i] not in chiffre ):
                isPonctPresent = True
                break
            i=i+1
        return isPonctPresent

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsPonctInListeAuto(self,chaine,sListeAuto,Bill=False):
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç "
        listeAaZ = "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn "
        chiffre = "0123456789"

#        if(Bill==True):
#            sCh = self.GetIllOut(sChaine)
#        else:
        sCh = chaine

        IsPonctInListeAuto = True
        i=0
        while(i<len(sCh)):
            if(sCh[i] not in ListeAccents and sCh[i] not in listeAaZ and sCh[i] not in chiffre and sCh[i] not in sListeAuto):
                IsPonctInListeAuto = False
                break
            i=i+1
        return IsPonctInListeAuto

    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsPonctInListeNonAuto(self,sChaine,sListenonAuto,Bill=False):
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç "
        listeAaZ = "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn "
        chiffre = "0123456789"

#        if(Bill==True):
#            sCh = self.GetIllOut(sChaine)
#        else:

        sCh = chaine

        IsPonctInListeNonAuto = False
        i=0
        while(i<len(sCh)):
            if(sCh[i] not in ListeAccents and sCh[i] not in listeAaZ and sCh[i] not in chiffre and sCh[i]  in sListenonAuto):
                IsPonctInListeNonAuto = True
                break
            i=i+1
        return IsPonctInListeNonAuto


    def GetLengthLim(self,sCont,sSep=';'):
            nCount = self.GetMarqueCount(sCont,sSep)
            if(nCount>1):
                sCh = self.GetMarqueString(1, sCont, sSep)
                GetLengthLim = len(sCh)
            else:
                GetLengthLim = len(sCont)
            return GetLengthLim


    def netoyageReq(self,chaine):
        # chaine = chaine.replace("'","\'")
        i=0
        while(i<len(chaine)):

            ch = chaine
            if(ch[i]=="'"):
                pass
            i=i+1
        return chaine.replace("a","q")


    def readfile(self,file,methode="r+"):
        if(os.access(file,os.F_OK)==True):
            fileOpen = open(file, methode)
            return fileOpen.read()
        else:
           # fileOpen = open(file,"wb+")
            return ""

    def writinFile(file,str,methode="wb+"):
        if(os.access(file,os.F_OK)==True):
            oldCont = readfile(file)
            newCont = oldCont + '\n'+str
            FileOpen = open(file,methode)
            FileOpen.write(newCont)

        else:
            FileOpen = open(file,methode)
            FileOpen.write(str)


    def netoyer(self,string):
        I=0
        newStr = ""
        while(I<len(string)):
            if(string[I]!=""):
                if(newStr==""):
                    newStr = string[I]
                else:
                    newStr = newStr + string[I]
            I=I+1
        return newStr



    #--------FILTRE DES SAISIES QUESTIONS  -----------#
    def filtreQuest(self,e):
        val = e.widget.get()
        sValide = '123'
        tzSpecKey   = ['Left','Up','Down','Delete','Right','End','BackSpace','F9','F10']
        if(val==""):
            if(e.char not in sValide and e.keysym not in tzSpecKey):
                e.widget.mainloop()
        else:
            tzSpecKey.append('Tab')
            if(e.keysym not in tzSpecKey):
                e.widget.mainloop()

    #----------METHODE DE SAISIE DE '1' SEULEMENT DANS UNE ZONE DE SAISIE -----#
    def uniques(self,e):
        val = e.widget.get()
        tzSpecKey   = ['Left','Up','Down','Delete','Right','End','BackSpace','Tab','F9','F10']
        if(e.char !='1' and e.keysym not in tzSpecKey):
            e.widget.mainloop()

    def getfiltreDomaineMail(self,string):
        domaine = ''
        n = string.rfind('.')
        if(n!=-1):
            domaine = string[n+1:len(string)]
        return domaine

    def controle_batch(self,sTab ,bMsg,Bill,conn=None,lot=''):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("SET CLIENT_ENCODING='WIN1252'")
        cur.execute("SELECT * FROM \"CONTROLE_STANDARD\" ")
        trs_Cont =  cur.fetchall()
        cur.execute("SELECT * FROM \""+str(sTab)+"\"")
        trs_Data =  cur.fetchall()

        bControle = False
        if(len(trs_Cont)==0):
            self.errorDlg('Infos','La table de contrôle standard est vide.\nAucun contrôle à faire.')
            return False

        countI=0
        while(countI<len(trs_Cont)):
            rs_Cont = trs_Cont[countI]

            sChp        = "%s"%(self.nz(rs_Cont["NOM_CHAMP"]))
            bVideA      = "%s"%(self.nz(rs_Cont["VIDE_AUTORISE"]))
            bEspA       = "%s"%(self.nz(rs_Cont["ESPACE_AUTORISE"]))
            bAccentA    = "%s"%(self.nz(rs_Cont["ACCENT_AUTORISE"]))
            bPonctA     = "%s"%(self.nz(rs_Cont["PONCT_AUTORISE"]))
            bLongL      = "%s"%(self.nz(rs_Cont["LONGUEUR_LIMITE"]))
            bSep        = "%s"%(self.nz(rs_Cont["SEPARE"]))
            bCasse      = "%s"%(self.nz(rs_Cont["TEST_CASSE"]))
            sLong       = "%s"%(self.nz(rs_Cont["LONGUEUR"]))
            sTypeLong   = "%s"%(self.nz(rs_Cont["TYPE_LONGUEUR_LIMITE"]))
            sSep        = "%s"%(self.nz(rs_Cont["SEPARATEUR"]))
            sLim        = "%s"%(self.nz(rs_Cont["LIMITE"]))
            sCasse      = "%s"%(self.nz(rs_Cont["CASSE"]))
            sTypeCtrl   = "%s"%(self.nz(rs_Cont["TYPE_CONTROLE"]))
            sDefaultVal = "%s"%(self.nz(rs_Cont["PAR_DEFAUT"]))

            #print "sLim:",sLim

            sPonctA     = "%s"%(self.nz(rs_Cont["P_AUTORISEES"]))
            sPonctNonA  = "%s"%(self.nz(rs_Cont["P_NON AUTORISEES"]))

            #Ireo zay mampiasa an'ilay LONGUEUR_LIMITE
            if(sTypeCtrl in ["4","9","6"]):
                if((bLongL=="1") and (sLong == "" or sTypeLong == "")):
                #'Misy diso ny paramétrage
                    self.errorDlg("Erreur","ERREUR PARAMETRAGE.Longueur  ou type longeur  non spécifié pour le champ %s (type 4,9,6) "%(sChp))
                    return False

            #Ireo zay mampiasa ny SEPARATEUR
            if(sTypeCtrl == "8"):
                if(bSep=="1" and sSep == ""):
                    #Then 'Misy diso ny paramétrage
                    self.errorDlg("Erreur","ERREUR PARAMETRAGE.Séprateur non spécifié pour le champ %s (type 8) "%(sChp))
                    return False

            #'Test des 2 valeurs limites
            if(sTypeCtrl== "5"):
                if (sLim == ""):
                    self.errorDlg("Erreur","ERREUR PARAMETRAGE.Valeur limite non spécifié pour le champ %s (type5) "%(sChp))
                    return False
                nPos = sLim.find(">")
                if(nPos == 0):
                    self.errorDlg("Erreur","ERREUR PARAMETRAGE.Valeur limite INCORRECT pour le champ %s ('>' au debut)  "%(sChp))
                    return False
                else:
                    nVal1 = len(sLim[0:nPos - 1])
                    nVal2 = len(sLim[nPos + 1])
                    if nVal2 == 0 :
                        self.errorDlg("Erreur","ERREUR PARAMETRAGE.Valeur limite INCORRECT pour le champ %s ('>' en fin du mot) "%(sChp))
                        return False

                    if(nVal2 < nVal1) :
                        self.errorDlg("Erreur", "ERREUR PARAMETRAGE.Valeur limite INCORRECT pour le champ %s (valeur 2 sup à la valeur 1) "%s(sChp))
                        return False

            #'Ho an'ny ALPHANUMERIQUE : raha toa ka tsy testé ny LONGUEUR
            #'no sady accent autorisé no sady ponct autorisé no sady vide autorisé,esp autorisé
            #'donc TOUT EST AUTORISE -> de tsy misy antony ametrahana azy ao
            if(sTypeCtrl == "9"):
                if(bCasse=="1" and sCasse == ""):
                    self.errorDlg("Erreur", "ERREUR PARAMETRAGE. CASSE non spécifié pour le champ %s(type 9) "%(sChp)+ ".")
                    return False

            #'VITA ZAY NY TEST REHETRA MOMBA NY PARAMETRAGE N'INY CHAMP INY
            #'Tetezo @ zay ny données

            countJ=0
            while(countJ<len(trs_Data)):
                rs_Data = trs_Data[countJ]
                nlot = rs_Data["n_lot"]
                sEnr = rs_Data["n_enr"]
                self.nlot = rs_Data["n_lot"]
                #'Avadika Vide aloha zay null mba hanamora zavatra
                sval        = "%s"%(self.nz(rs_Data[sChp]))
                sval = sval.strip()
                #'Tenir compte des illisibles ?

                if(Bill==True):
                    if(sval.find("<?>") !=-1):
                        countJ=countJ+1
                        continue

                #'Vide autorise ve aloha ?
                if(bVideA!="1"  and sval == ""):
                    sMsg = "Vide non autorisé " +str(sLong)
                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                    #'Erreur sahady : tsy mandray vide ny aty ô ! ... goto erreur
                    #'GoTo Erreur

                if sval != "" :
                    #'Tsy manao zavatra raha tsy misy zavatra atao mazava ho azy
                    #'Valeur par défaut ve aloha misy zavatra ?
                    #'Satria raha misy ka mitovy amin'iny le valeur ho tester-na
                    #'de VRAI foana n'inona n'inona mitranga eo
                    if(sDefaultVal != ""):
                        if sval == sDefaultVal:
                            countJ=countJ+1
                            continue
                    if(sTypeCtrl=='1'):
                        #"EMAIL"
                        if(self.isEmailValide(sval)==False):
                            sMsg = "E-Mail incorrect."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='2'):
                        #"DATE 1 (JJ/MM/AA)"
                        if(self.isDateCorrect(sval, "D1")==False):
                            sMsg = "Date Incorrect. Format ""JJ/MM/AA""."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)
                    if(sTypeCtrl=='3'):
                        #"DATE 2 (JJ/MM/AAAA)"
                        if(self.isDateCorrect(sval, "D2")==False):
                            sMsg = "Date Incorrect. Format ""JJ/MM/AAAA""."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='4'):
                        if(bEspA=="0"):
                            #'ESP NON AUTORISE
                            if sval.find(" ")!=-1:
                                sMsg = "Espace non autorisé pour ce champ."
                                self.writeError(sEnr,sChp,sMsg,conn,nlot)

                            if(bPonctA=="0"):
                                #'NOM COCHE NY PONCTUATION
                                if(self.is0a9(sval)==False):
                                    sMsg = "Valeur NON Numérique."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                if(self.Is0a9ponctA(sval, sPonctA, sPonctNonA, bEspA)==False):
                                    sMsg = "Valeur NON Numérique/Ponct non autorisé."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        else:
                            #'ESP AUTORISE
                            if(bPonctA=="0"):
                                #''NOM COCHE NY PONCTUATION
                                if(self.Is_0a9_Esp(sval)==False):
                                    sMsg = "Valeur NON Numérique."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)

                            else:
                                if(self.Is0a9ponctA(sval, sPonctA, sPonctNonA, bEspA)==False):
                                    sMsg = "Valeur NON Numérique/Ponct non autorisée."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        #'Longueur ve limité ?
                        if(bLongL=="1"):
                            if sTypeLong == "STRICT" :
                                if len(sval) != int(sLong) :
                                    sMsg = "Longueur incorrecte. Strictement égal à %s (type ctrl 4, long strict) "%(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)

                            else:
                                #LARGE
                                if len(sval) > int(sLong) :
                                    sMsg = "Données trop longues. Ne doit pas dépasser " +str( sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='5'):
                        #'NUMERIQUE LIMITE ENTRE 2 VAL
                        if((int(sval) >= nVal1 and int(sval) <= nVal2)==False):
                            sMsg = "Valeur en dehors de la plage(Entre " +str(nVal1)+ " et "+str(nVal2 )+ ")."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='6'):
                        if(self.Is_0a9_Present(sval)==True):
                            sMsg = "CHIFFRE NON autorisé dans ce champ."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        if sLim != "" :
                            if(self.isDansUnique(sval, sLim)==True):
                                sMsg = "Valeur NON accepté.Règle : " +str(sLim) + "."
                                self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        if (bEspA=="0" and sval.find(" ")!=-1):
                            sMsg = "ESPACE NON autorisé dans ce champ."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        if(bAccentA=="0"  and self.IsAccentPresent(sval)==True):
                            sMsg = "Accent NON autorisé dans ce champ."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        #'Non coché ny Ponctuations autorisées, zany hoe
                        #'interdit daholo ny pontuations rehetra
                        if bPonctA=="0":
                            if(self.IsPonctPresent(sval, Bill)==True):
                                sMsg = "Ponctuation NON autorisée dans ce champ."
                                self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        else:
                            #'"Autorisées" no notanisainy sa ny "NON Autorisées"
                            if sPonctA != "":
                                #'"Autorisées"
                                if(self.IsPonctInListeAuto(sval, sPonctA, Bill)==False):
                                    sMsg = "Les ponctuations PERMISES sont "+ sPonctA +""
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                if sPonctNonA != "":
                                    #'NON "Autorisées"
                                    if(self.IsPonctInListeNonAuto(sval, sPonctNonA, Bill)==True):
                                        sMsg = "Les ponctuations NON PERMISES sont " +str(sPonctNonA)+ ""
                                        self.writeError(sEnr,sChp,sMsg,conn,nlot)
                                else:
                                    pass
                                    #'SADY TSY "Autorisées" NO TSY NON "Autorisées"
                                    #'Autorisé daholo izany
                                    #'TSY MANAO N'INON 'INONA

                        if bCasse=="1":
                            if sCasse == "MAJ" :
                                if(self.IsMajus(sval)==False):
                                    sMsg = "Données non MAJUSCULE."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                if(self.IsMinus(sval)==False):
                                    sMsg = "Données non MINUSCULE."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        #'Longueur ve limité ?
                        if bLongL=="1":
                            if sTypeLong == "STRICT" :
                                if len(sval) != int(sLong) :
                                    sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                # 'LARGE
                                if(len(sval) >int(sLong)):
                                    #Then
                                    sMsg = "Données trop longues. Ne doit pas dépasser " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='7'):
                        if(self.isDansUnique(sval, sLim)==False):
                            sMsg = "Valeur NON accepté.Règle : " +str(sLim) +"."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='8'):
                        #'LIMITE/MULTIPLE
                        if sSep =="":
                            sSep = ";"
                        if(self.isDansMultiple(sval, sLim, sSep)==False):
                            sMsg = "Valeur NON accepté.Règle : " + str(sLim) + ". Ou un code se répète plus d'une fois."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        else:

                            #'Edit-er na fa sao de tsy valeur trié no tao
                            #'Oh: 13254 no tao
                            #'marina nefa ohatra io fa mila trier na hoe 12345
                            cur.execute("UPDATE \""+sTab+"\" SET \""+sChp+"\"='"+sval+"' where \"n_enr\"='"+sEnr+"'")

                    if(sTypeCtrl=='9'):
                        if(bEspA=="0" and self.IsEspacePresent(sval)==True):
                            sMsg = "ESPACE NON autorisé dans ce champ."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)
#                        print sval
                        if(bAccentA=="0" and self.IsAccentPresent(sval)==True):
                            sMsg = "Accent NON autorisé dans ce champ."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        #'Non coché ny Ponctuations autorisées, zany hoe
                        #'interdit daholo ny pontuations rehetra
                        if bPonctA=="0":
                            if(self.IsPonctPresent(sval, Bill)==True):
                                sMsg = "Ponctuation NON autorisée dans ce champ."
                                self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        else:
                            #'"Autorisées" no notanisainy sa ny "NON Autorisées"
                            if sPonctA != "":
                                #'"Autorisées"
                                if(self.IsPonctInListeAuto(sval, sPonctA, Bill)==False):
                                    sMsg = "Les ponctuations PERMISES sont  " +str( sPonctA)+""
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                if sPonctNonA != "" :
                                    #'NON "Autorisées"
                                    if self.IsPonctInListeNonAuto(sval, sPonctNonA, Bill)==True:
                                        sMsg = "Les ponctuations NON PERMISES sont  " +str(sPonctNonA) +" "
                                        self.writeError(sEnr,sChp,sMsg,conn,nlot)
                                else:
                                    pass
                                    #'SADY TSY "Autorisées" NO TSY NON "Autorisées"
                                    #'Autorisé daholo izany
                                    #'TSY MANAO N'INON 'INONA

                        if bCasse=="1":
                            if sCasse =="MAJ" :
                                if self.IsMajus(sval)==False:
                                    sMsg = "Données non MAJUSCULE."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:

                                if(self.IsMinus(sval)==False):
                                    sMsg = "Données non MINUSCULE."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        #'Longueur ve limité ?
                        if bLongL=="1":
                            if sTypeLong == "STRICT" :
                                if len(sval) != int(sLong) :
                                    sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)

                            else:
                                # 'LARGE
                                if len(sval) > int(sLong):
                                    sMsg = "Données trop longues. Ne doit pas dépasser " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)



                    if(sTypeCtrl=='10'):
                        #date americaine
                        if(self.isDateCorrect(sval, "D3")==False):
                            sMsg = "Date Incorrect. Format ""AAAA-MM-JJ""."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='11'):
                        if self.isDateCorrect(sval, "D4")==False:
                            sMsg = "Date Incorrect. Format ""AAAA-MM-JJ""."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='12'):
                        if self.isDateCorrect(sval, "D5")==False:
                            sMsg = "Date Incorrect. Format ""JJMMAA""."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='13'):
                        if bEspA=="0":
                            #'ESP NON AUTORISE
                            if bPonctA=="0":
                                #'NOM COCHE NY PONCTUATION
                                if self.is0a9(sval)==False:
                                    sMsg = "Valeur NON Numérique."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                if self.Is0a9ponctA(sval, sPonctA, sPonctNonA, bEspA)==False:
                                    sMsg = "Valeur NON Numérique/Ponct non autorisé."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        else:
                            #'ESP AUTORISE
                            if bPonctA=="0":
                                #''NOM COCHE NY PONCTUATION
                                if self.Is_0a9_Esp(sval)==False:
                                    sMsg = "Valeur NON Numérique."
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                                else:
                                    if self.Is0a9ponctA(sval, sPonctA, sPonctNonA, bEspA)==False:
                                        sMsg = "Valeur NON Numérique/Ponct non autorisée."
                                        self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        if(sval[0]!= "0"):
                            sMsg = "valeur numérique non commencé par 0."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)


                        if bLongL =="1":
                            if sTypeLong == "STRICT" :
                                if len(sval) != int(sLong) :
                                    sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                # 'LARGE
                                if len(sval) > int(sLong):
                                    sMsg = "Données trop longues. Ne doit pas dépasser "+str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)


                    if(sTypeCtrl=='14'):
                        #jjmmaaaa
                        if(self.isDateCorrect(sval, "D6")==False):
                            sMsg = "Date Incorrect. Format ""JJMMAAAA""."
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)


                    if(sTypeCtrl=='15'):
                        if(sval!=None and sval != ""):
                            sMsg = "Ce champ doit être vide. "
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)


                    if(sTypeCtrl=='16'):
                        if self.IsMontant(sval,'.')==False:
                            sMsg = "Ce champ n'est pas de format montant avec 2 chiffres après virgule. "
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        if bLongL=="1":
                            if sTypeLong == "STRICT" :
                                if len(sval) != int(sLong):
                                    sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                # 'LARGE
                                if len(sval) > int(sLong):
                                    sMsg = "Données trop longues. Ne doit pas dépasser " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='17'):
                        #Téléphone mobile
                        if bEspA =="0":
                            if sval.find(" ")!=-1:
                                sMsg = "Espace non autorisée pour ce champ (type: %s). "%(sTypeCtrl)
                                self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        if self.is0a9(sval.replace(" ",""))==False:
                            sMsg = "Valeur non numerique pour ce champ (type: %s). "%(sTypeCtrl)
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        if bLongL=="1":
                            if sTypeLong == "STRICT" :
                                if len(sval) != int(sLong):
                                    sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                # 'LARGE
                                if len(sval) > int(sLong):
                                    sMsg = "Données trop longues. Ne doit pas dépasser " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        if sLim!="":
                            tlimite = sLim.split(";")
                            sMesComm = ""
                            for c in tlimite:
                                sMesComm+="%s ou "%(c)
                            sMesComm=sMesComm.strip("ou ")
                            if sval[0:2] not in tlimite:
                                sMsg = "Cette valeur doit commencer par %s "%(sMesComm)
                                self.writeError(sEnr,sChp,sMsg,conn,nlot)



                    if(sTypeCtrl=='18'):
                        #Téléphone fixe
                        if bEspA =="0":
                            if sval.find(" ")!=-1:
                                sMsg = "Espace non autorisée pour ce champ (type: %s). "%(sTypeCtrl)
                                self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        if self.is0a9(sval.replace(" ",""))==False:
                            sMsg = "Valeur non numerique pour ce champ (type: %s). "%(sTypeCtrl)
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        if bLongL=="1":
                            if sTypeLong == "STRICT" :
                                if len(sval) != int(sLong):
                                    sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            else:
                                # 'LARGE
                                if len(sval) > int(sLong):
                                    sMsg = "Données trop longues. Ne doit pas dépasser " +str(sLong)
                                    self.writeError(sEnr,sChp,sMsg,conn,nlot)
                        if sLim!="":
                            tlimite = sLim.split(";")
                            sMesComm = ""
                            for c in tlimite:
                                sMesComm+="%s ou "%(c)
                            sMesComm=sMesComm.strip("ou ")
                            if sval[0:2] in tlimite:
                                sMsg = "Cette valeur ne doit pas commencer par %s "%(sMesComm)
                                self.writeError(sEnr,sChp,sMsg,conn,nlot)


                    if(sTypeCtrl=='19'):
                        if self.is_valid_iban(sval)==False:
                            sMsg = "Valeur IBAN non valide"
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        #IBAN
                    if(sTypeCtrl=='20'):
                        #BIC
                        if self.isBicValide(sval)==False:
                            sMsg = "Valeur BIC non valide"
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)
                    if(sTypeCtrl=='21'):
                        #BIC
                        if self.checkSiren(sval)==False:
                            sMsg = "Valeur SIREN non valide"
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                    if(sTypeCtrl=='22'):
                        #BIC
                        if self.checkSiret(sval)==False:
                            sMsg = "Valeur SIRET non valide"
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)
                            
                    #todo ajout datesogec
                    if(sTypeCtrl=='30'):
                        if self.isDateSogec(sval,'D2')==False:
                            sMsg = "Valeur date non valide"
                            self.writeError(sEnr,sChp,sMsg,conn,nlot)

                        pass

                countJ=countJ+1
            countI=countI+1


    def nz(self,valeur_o,valeur_pardefaut=''):
        if valeur_o=='' or valeur_o==None:
            return valeur_pardefaut
        else:
            return valeur_o

    def controle(self,schp,svaleur,bMsg,Bill,conn=None):

        sval = svaleur
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SET CLIENT_ENCODING='WIN1252'")
        cur.execute("SELECT * FROM \"CONTROLE_STANDARD\" WHERE \"NOM_CHAMP\"='" +schp+"'")
        trs_Cont =  cur.fetchone()



        if trs_Cont==None:
            self.errorDlg('Infos','La table de contrôle standard est vide.\nAucun contrôle à faire.')
            return False

        rs_Cont     = trs_Cont
        bVideA      = "%s"%(self.nz(trs_Cont["VIDE_AUTORISE"]))
        bEspA       = "%s"%(self.nz(trs_Cont["ESPACE_AUTORISE"]))
        bAccentA    = "%s"%(self.nz(trs_Cont["ACCENT_AUTORISE"]))
        bPonctA     = "%s"%(self.nz(trs_Cont["LONGUEUR_LIMITE"]))
        bLongL      = "%s"%(self.nz(trs_Cont["ESPACE_AUTORISE"]))
        bSep        = "%s"%(self.nz(trs_Cont["SEPARE"]))
        bCasse      = "%s"%(self.nz(trs_Cont["TEST_CASSE"]))

        sLong       = "%s"%(self.nz(trs_Cont["LONGUEUR"]))
        sTypeLong   = "%s"%(self.nz(trs_Cont["TYPE_LONGUEUR_LIMITE"]))

        sSep        = "%s"%(self.nz(trs_Cont["SEPARATEUR"]))
        sLim        = "%s"%(self.nz(trs_Cont["LIMITE"]))
        sCasse      = "%s"%(self.nz(trs_Cont["CASSE"]))
        sPonctA     = "%s"%(self.nz(trs_Cont["P_AUTORISEES"]))
        sPonctNonA  = "%s"%(self.nz(trs_Cont["P_NON AUTORISEES"]))
        sTypeLong   = "%s"%(self.nz(trs_Cont["TYPE_LONGUEUR_LIMITE"]))
        sTypeCtrl   = "%s"%(self.nz(trs_Cont["TYPE_CONTROLE"]))

        sval = "%s"%(self.nz(sval))
        #Ireo zay mampiasa an'ilay LONGUEUR_LIMITE / #'Misy diso ny paramétrage
        if sTypeCtrl in ["4","6","9"]:
            if((bLongL=="1") and (sLong == "" or sTypeLong == "")):
                self.errorDlg("Erreur","ERREUR PARAMETRAGE.Longueur non spécifié pour le champ " +str(schp))
                return False


        #Ireo zay mampiasa ny SEPARATEUR
        if sTypeCtrl in ["8"]:
            if(bSep=="1" and sSep == ""):
                #Then 'Misy diso ny paramétrage
                self.errorDlg("Erreur","ERREUR PARAMETRAGE.Séprateur non spécifié pour le champ " +str(schp))
                return False

        #'Test des 2 valeurs limites
        if sTypeCtrl in ["5"]:
            if (sLim == ""):
                self.errorDlg("Erreur","ERREUR PARAMETRAGE.Valeur limite spécifié pour le champ "  +str(schp))
                return False
            nPos = sLim.find(">")
            if(nPos == 0):
                self.errorDlg("Erreur","ERREUR PARAMETRAGE.Valeur limite INCORRECT pour le champ " +str(schp))
                return False
            else:
                nVal1 = int(str(sLim)[0:nPos].strip())
                nVal2 = int(str(sLim)[nPos:].strip())
                if nVal2 == 0 :
                    self.errorDlg("Erreur","ERREUR PARAMETRAGE.Valeur limite INCORRECT pour le champ " +str(schp))
                    return False

                if(nVal2 < nVal1) :
                    self.errorDlg("Erreur", "ERREUR PARAMETRAGE.Valeur limite INCORRECT pour le champ " +str(schp))
                    return False

        if sTypeCtrl in ["9"]:
            if(bVideA=="1"  and bLongL!="1" and bAccentA=="1" and bPonctA=="1" and bEspA=="1"):
                self.errorDlg("Erreur","ERREUR PARAMETRAGE. Aucun contrôle pour le champ " +str(schp)+ ".\nVeuillez le supprimer de là.")
                return False
            if(bCasse=="1" and sCasse == ""):
                self.errorDlg("Erreur", "ERREUR PARAMETRAGE. CASSE non spécifié pour le champ " +str(schp)+ ".")
                return False

        #'VITA ZAY NY TEST REHETRA MOMBA NY PARAMETRAGE N'INY CHAMP INY
        #'Tetezo @ zay ny données

         #'Tenir compte des illisibles ?

        if(Bill==True):
           if(sval.find("<?>")!=-1):
                return True
        sMsg=""

        if bVideA=='0' and sval=="":
            self.errorDlg("Erreur", "Vide non autorisée pour le champ " +str(schp)+ ".")
            return False

        if sval != "" :
            sval=sval.encode('cp1252')
            if(sTypeCtrl=='1'):
                posarbs = sval.find("@")
                if posarbs==0 or posarbs==-1:
                    self.errorDlg("Erreur","Email incorrect (position @)")
                    return False
                mailAvant = sval[0:posarbs]
                mailApres = sval[posarbs+1:]

                if self.isEmailValide(mailAvant)==False:
                    self.errorDlg("Erreur","Email incorrect (syntaxe email)")
                    return False

                if self.isEmailValide(mailApres)==False:
                    self.errorDlg("Erreur","Email incorrect (syntaxe domaine)")
                    return False

            if(sTypeCtrl=='2'):
                #"DATE 1 (JJ/MM/AA)"
                if(self.isDateCorrect(sval, "D1")==False):
                    sMsg = "Date Incorrect. Format ""JJ/MM/AA""."

            if(sTypeCtrl=='3'):
                #"DATE 2 (JJ/MM/AAAA)"
                if(self.isDateCorrect(sval, "D2")==False):
                    sMsg = "Date Incorrect. Format ""JJ/MM/AAAA""."


            if(sTypeCtrl=='4'):
                if(bEspA=='0'):
                    if(bPonctA=='0'):
                        if(self.is0a9(sval)==False):
                            sMsg = "Valeur NON Numérique."
                    else:
                        if(self.Is0a9ponctA(sval, sPonctA, sPonctNonA, bEspA)):
                            sMsg = "Valeur NON Numérique/Ponct non autorisé."


                else:
                    #'ESP AUTORISE
                    if(bPonctA=='0'):
                        #''NOM COCHE NY PONCTUATION
                        if(self.Is_0a9_Esp(sval)==False):
                            sMsg = "Valeur NON Numérique."
                    else:
                        if(self.Is0a9ponctA(sval, sPonctA, sPonctNonA, bEspA)==False):
                            sMsg = "Valeur NON Numérique/Ponct non autorisée."


                #'Longueur ve limité ?
                if(bLongL=='1'):
                    if sTypeLong == "STRICT" :
                        if len(sval) != int(sLong) :
                            sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)


                    else:
                        #LARGE
                        if len(sval) > int(sLong) :
                            sMsg = "Données trop longues. Ne doit pas dépasser " +str( sLong)


            if(sTypeCtrl=='5'):
                    #'NUMERIQUE LIMITE ENTRE 2 VAL
                if((int(sval) >= nVal1 and int(sval) <= nVal2)==False):
                    sMsg = "Valeur en dehors de la plage(Entre " +str(nVal1)+ " et "+str(nVal2 )+ ")."


            if(sTypeCtrl=='6'):

                if(self.Is_0a9_Present(sval)==True):
                    sMsg = "CHIFFRE NON autorisé dans ce champ."

                if sLim != "" :
                    if(self.isDansUnique(sval, sLim)==True):
                        sMsg = "Valeur NON accepté.Règle : " +str(sLim) + "."

                if (bEspA=='0' and self.IsEspacePresent(sval)==True):
                    sMsg = "ESPACE NON autorisé dans ce champ."

                if(bAccentA=='0'  and self.IsAccentPresent(sval)==True):
                    sMsg = "Accent NON autorisé dans ce champ."

                #'Non coché ny Ponctuations autorisées, zany hoe
                #'interdit daholo ny pontuations rehetra
                if bPonctA=='0':
                    if(self.IsPonctPresent(sval, Bill)==True):
                        sMsg = "Ponctuation NON autorisée dans ce champ."

                else:
                    #'"Autorisées" no notanisainy sa ny "NON Autorisées"
                    if sPonctA != "":
                        #'"Autorisées"
                        if(self.IsPonctInListeAuto(sval, sPonctA, Bill)==False):
                            sMsg = "Les ponctuations PERMISES sont "+ sPonctA +""

                    else:
                        if sPonctNonA != "":
                            #'NON "Autorisées"
                            if(self.IsPonctInListeNonAuto(sval, sPonctNonA, Bill)==True):
                                sMsg = "Les ponctuations NON PERMISES sont " +str(sPonctNonA)+ ""

                        else:
                            pass
                            #'SADY TSY "Autorisées" NO TSY NON "Autorisées"
                            #'Autorisé daholo izany
                            #'TSY MANAO N'INON 'INONA

                if bCasse=="1":
                    if sCasse == "MAJ" :
                        if(self.IsMajus(sval)==False):
                            sMsg = "Données non MAJUSCULE."

                    else:
                        if(self.IsMinus(sval)==False):
                            sMsg = "Données non MINUSCULE."

                #'Longueur ve limité ?
                if bLongL=="1":
                    if sTypeLong == "STRICT" :
                        if len(sval) != int(sLong) :
                            sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)

                    else:
                        # 'LARGE
                        if(len(sval) >int(sLong)):
                            #Then
                            sMsg = "Données trop longues. Ne doit pas dépasser " +str(sLong)


            if(sTypeCtrl=='7'):
                if(self.isDansUnique(sval, sLim)==False):
                    sMsg = "Valeur NON accepté.Règle : " +str(sLim) +"."


            if(sTypeCtrl=='8'):
                #'LIMITE/MULTIPLE
                svar = self.GetLengthLim(sLim)
                if sSep =="":
                    sSep = ";"

                if(self.isDansMultiple(sval, sLim, sSep)==False):
                    sMsg = "Valeur NON accepté.Règle : " + str(sLim) + ". Ou un code se répète plus d'une fois."


                else:
                    pass
                    #'Edit-er na fa sao de tsy valeur trié no tao
                    #'Oh: 13254 no tao
                    #'marina nefa ohatra io fa mila trier na hoe 12345
                    #cur.execute("UPDATE \""+sTab+"\" SET \""+schp+"\"='"+sval+"' where \"N_ENR\"='"+sEnr+"'")

            if(sTypeCtrl=='9'):
                if(bEspA=="0" and self.IsEspacePresent(sval)==True):
                    sMsg = "ESPACE NON autorisé dans ce champ."

                if(bAccentA=="0" and self.IsAccentPresent(sval)==True):
                    sMsg = "Accent NON autorisé dans ce champ."

                #'Non coché ny Ponctuations autorisées, zany hoe
                #'interdit daholo ny pontuations rehetra
                if bPonctA=="0":
                    if(self.IsPonctPresent(sval, Bill)==True):
                        sMsg = "Ponctuation NON autorisée dans ce champ."

                else:
                    #'"Autorisées" no notanisainy sa ny "NON Autorisées"
                    if sPonctA != "":
                        #'"Autorisées"
                        if(self.IsPonctInListeAuto(sval, sPonctA, Bill)==False):
                            sMsg = "Les ponctuations PERMISES sont  " +str( sPonctA)+""

                    else:
                        if sPonctNonA != "" :
                            #'NON "Autorisées"
                            if self.IsPonctInListeNonAuto(sval, sPonctNonA, Bill)==True:
                                sMsg = "Les ponctuations NON PERMISES sont  " +str(sPonctNonA) +" "

                        else:
                            pass
                            #'SADY TSY "Autorisées" NO TSY NON "Autorisées"
                            #'Autorisé daholo izany
                            #'TSY MANAO N'INON 'INONA

                if bCasse=="1":
                    if sCasse =="MAJ" :
                        if self.IsMajus(sval)==False:
                            sMsg = "Données non MAJUSCULE."

                    else:

                        if(self.IsMinus(sval)==False):
                            sMsg = "Données non MINUSCULE."


                #'Longueur ve limité ?
                if bLongL=="1":
                    if sTypeLong == "STRICT" :
                        if len(sval) != int(sLong) :
                            sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)


                    else:
                        # 'LARGE
                        if len(sval) > int(sLong):
                            sMsg = "Données trop longues. Ne doit pas dépasser " +str(sLong)




            if(sTypeCtrl=='10'):
                #date americaine
                if(self.isDateCorrect(sval, "D3")==False):
                    sMsg = "Date Incorrect. Format ""AAAA-MM-JJ""."


            if(sTypeCtrl=='11'):
                if self.isDateCorrect(sval, "D4")==False:
                    sMsg = "Date Incorrect. Format ""AAAA-MM-JJ""."


            if(sTypeCtrl=='12'):
                if self.isDateCorrect(sval, "D5")==False:
                    sMsg = "Date Incorrect. Format ""JJMMAA""."


            if(sTypeCtrl=='13'):
                if bEspA=="0":
                    #'ESP NON AUTORISE
                    if bPonctA==False:
                        #'NOM COCHE NY PONCTUATION
                        if self.is0a9(sval)==False:
                            sMsg = "Valeur NON Numérique."

                    else:
                        if self.Is0a9ponctA(sval, sPonctA, sPonctNonA, bEspA)==False:
                            sMsg = "Valeur NON Numérique/Ponct non autorisé."

                else:
                    #'ESP AUTORISE
                    if bPonctA=="0":
                        #''NOM COCHE NY PONCTUATION
                        if self.Is_0a9_Esp(sval)==False:
                            sMsg = "Valeur NON Numérique."

                        else:
                            if self.Is0a9ponctA(sval, sPonctA, sPonctNonA, bEspA)==False:
                                sMsg = "Valeur NON Numérique/Ponct non autorisée."


                if(sval[0]!= "0"):
                    sMsg = "valeur numérique non commencé par 0."

                if bLongL =="1":
                    if sTypeLong == "STRICT" :
                        if len(sval) != int(sLong) :
                            sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)

                    else:
                        # 'LARGE
                        if len(sval) > int(sLong):
                            sMsg = "Données trop longues. Ne doit pas dépasser "+str(sLong)

            if(sTypeCtrl=='14'):
                #jjmmaaaa
                if(self.isDateCorrect(sval, "D6")==False):
                    sMsg = "Date Incorrect. Format ""JJMMAAAA""."

            if(sTypeCtrl=='15'):
                if(sval!=None and sval != ""):
                    sMsg = "Ce champ doit être vide. "



            if(sTypeCtrl=='16'):
                if self.IsMontant(sval)==False:
                    sMsg = "Ce champ n'est pas de format montant avec 2 chiffres après virgule. "

                if bLongL=="1":
                    if sTypeLong == "STRICT" :
                        if len(sval) != int(sLong):
                            sMsg = "Longueur incorrecte. Strictement égal à " +str(sLong)

                    else:
                        # 'LARGE
                        if len(sval) > int(sLong):
                            sMsg = "Données trop longues. Ne doit pas dépasser " +str(sLong)
            if(sTypeCtrl=='17'):#tel fixe
                if(sval!=None and sval != ""):
                    if(self.is0a9(sval)==False):
                        sMsg = "Valeur NON Numérique."

                    if len(sval)!=10:
                        sMsg = "Champ tel fixe Longuer incorrect (=10). "
                    if str(sval)[0:2] not in ["01","02","03","04","05"]:
                        sMsg = "Champ tel fixe doit commencer par  01,02,03,04,05. "

            if(sTypeCtrl=='18'):#tel MOBILE
                if(sval!=None and sval != ""):
                    if(self.is0a9(sval)==False):
                        sMsg = "Valeur NON Numérique."

                    if len(sval)!=10:
                        sMsg = "Champ tel mobile Longuer incorrect (=10). "
                    if str(sval)[0:2] not in ["06","07"]:
                        sMsg = "Champ tel mobile doit commencer par  06,07. "
            if sMsg !="":
                self.errorDlg("Erreur",sMsg)
                return False
            else:
                return True
        else:
            return True



    def errorDlg(self,title,message):
        msg = wx.MessageDialog ( None, message, caption=title,style=wx.ICON_ERROR|wx.OK , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg

    def InfoDlg(self,title,message):
        msg = wx.MessageDialog ( None, message, caption=title,style=wx.ICON_INFORMATION|wx.OK , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg

    def writeError(self,nenr , Chp, msg,conn,nlot):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #print "SELECT * FROM erreur WHERE n_enr='"+nenr+"' and n_lot='"+str(nlot)+"'"
        cur.execute("SELECT * FROM erreur WHERE n_enr='"+nenr+"' and n_lot='"+str(nlot)+"'")
        t = cur.fetchone()
        #print Chp
        if(t==None):
            #print "INSERT INTO erreur(n_enr,champ,error) VALUES('"+str(nenr)+"','"+str(Chp)+"','"+str(self.cleanAcc(msg))+"')"
            cur.execute("INSERT INTO erreur(n_enr,n_lot,champ,error) VALUES('"+str(nenr)+"','"+str(nlot)+"','"+str(Chp).replace("'","''")+"','"+str(self.cleanAcc(msg)).replace("'","''")+"')")
        else:
            if(t['champ'].find(Chp)==-1):
                newChamp = t['champ']+'-'+ Chp
                newError = t['error']+'-'+ msg
                cur.execute("UPDATE erreur SET champ='"+newChamp.replace("'","''")+"',error='"+str(self.cleanAcc(newError)).replace("'","''")+"'  where n_enr='"+str(nenr)+"' and n_lot='"+str(nlot)+"'")
            else:
                newError = t['error']+'/'+ msg
                cur.execute("UPDATE erreur SET error='"+str(self.cleanAcc(newError))+"'  where n_enr='"+str(nenr)+"' and n_lot='"+str(nlot)+"'")

    def IsMontant_(self,szChaine):

        IsMontant = True
        nbv = 0
        i=0
        while(i <len(szChaine)):
            if szChaine[i] =="," :
                positionv = i
                nbv = nbv + 1
                if nbv == 2 :
                    IsMontant = False
                    return False

            else:
                if szChaine[i] =="." :
                    IsMontant = False
                    return False
                if int(szChaine[i]) < 0 or int(szChaine[i]) > 9 :
                    IsMontant = False
                    return False
            i=i+1


        return IsMontant



    def cleanAcc(self,chaine):
        if self.isnumerique(chaine)==True:
            chaine = str(chaine)
        if self.IsAccentPresent((chaine))==True:
            chaine = self.NettoyagePonctPresent(chaine)
        return chaine

    def IsAccentPresent(self,chaine):
        """ Fonction de vérification si un caractere accentué est present dans chaine, retourne True si OUI et False si NON"""

        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"

        res = False

        i=0
        while(i<len(chaine)):
            if(chaine[i] in ListeAccents):
                res = True
            i=i+1
        return res


    def NettoyagePonctPresent(self,chaine):
        """ Cette fonction enleve les accents dans une chaine"""
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"
        ReplaceListeAccents = "EEEEAAAUUUIIOOCeeeeaaauuuiiooc"
        k=0
        chainenew=""
        while(k<len(chaine)):
            j=0
            while(j<len(ListeAccents)):
                if(ListeAccents[j]==chaine[k]):
                    chaine  = chaine.replace(chaine[k],ReplaceListeAccents[j])
                j=j+1
            k=k+1
        return chaine.replace("  "," ")

    def isnumerique(self,chaine):
        """Fonction de test qui renvoie True si une chaine est entierement numerique"""
        i=0
        #chaine = str(chaine.encode('cp1252'))
        result = True
        while (i<len(str(chaine))):
            if chaine[i] not in "0123456789":
                result = False
                return result
            i= i+1
        return result


class testIban :
    def _init__(self,sIban=""):
        self.sIban= sIban
        pass


    def compact(self,number):
        """Convert the iban number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
        return clean(number, ' -').strip().upper()


    def _to_base10(self,number):
        """Prepare the number to it's base10 representation (also moving the
    check digits to the end) so it can be checked with the ISO 7064
    Mod 97, 10 algorithm."""
        # TODO: find out whether this should be in the mod_97_10 module
        return ''.join(str(_alphabet.index(x)) for x in number[4:] + number[:4])


    def _struct_to_re(self,structure):
        """Convert an IBAN structure to a refular expression that can be used
    to validate the number."""
        def conv(match):
            chars = {
                'n': '[0-9]',
                'a': '[A-Z]',
                'c': '[A-Za-z0-9]',
            }[match.group(2)]
            return '%s{%s}' % (chars, match.group(1))
        return re.compile('^%s$' % _struct_re.sub(conv, structure))


    def validate(self,number):
        """Checks to see if the number provided is a valid IBAN."""
        number = self.compact(number)
        try:
            test_number = self._to_base10(number)
        except:
            raise InvalidFormat()
        # ensure that checksum is valid
        mod_97_10.validate(test_number)
        # look up the number
        info = _ibandb.info(number)
        # check if the bban part of number has the correct structure
        bban = number[4:]
        if not _struct_to_re(info[0][1].get('bban', '')).match(bban):
            raise InvalidFormat()
        # return the compact representation
        return number


    def is_valid(self,number):
        """Checks to see if the number provided is a valid IBAN."""
        try:
            return bool(self.validate(number))
        except ValidationError:
            return False


    def format(self,number, separator=' '):
        """Reformat the passed number to the space-separated format."""
        number = self.compact(number)
        return separator.join(number[i:i + 4] for i in range(0, len(number), 4))
