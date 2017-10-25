#!/usr/bin/env python
# -*- coding: cp1252  -*-

# Nom : CLASS D'OBJET MENUS
# Descr: Création d'un intérface graphique menu standard
# Domaine : Commande BDD
# Auteur : Jaona IOS
# Date : 27-12-2010
#Date de mis à jour : 23-02-2011          par : Jaona IOS
#--------------------------------------------------------
import os,sys,stat
import psycopg2
import psycopg2.extras
from shutil import *
 
from string import *
import wx



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
    def isNumpos(self,Chaine):
        """Fonction de test et renvoie une valeur True si toutes les caracteres dans une chaine Chaine sont tous des nombres positives, renvoie False si non.  """
        res = False
        chiffre = "123456789"
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
    def isDansMultiple(self,sVal,sCount,sSep,step=1):
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
        strApresavecDom = sMail[posarondbase:len(sMail)]
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
            else:
                connexion       =  psycopg2.connect("dbname=Adresse user=op1 password=aa host=192.168.10.5")
                
                strDomaine      = strApresavecDom[1:len(strApresavecDom)].lower()
                 
                curseur         = connexion.cursor()
                curseur.execute("SELECT * FROM \"EMAIL_DOMAINE\" WHERE \"DOMAINE\" ='"+strDomaine+"'")
                verif           = curseur.fetchone()
                if(verif==None):
                    Test=False
    
        return Test
    
    
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def isDateCorrect(self,sDate,sType):
        """ Fonction de verification si la chaine sDate a un bon format date selon les specification sType : D1-D2-D3-D4-D5-D6 """
        #print 'test date',sDate,' dddddd'
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
                    j = sDate[0:2]
                    m = sDate[3:5]
                    a = sDate[6:8]
            elif(sType=='D2'):#----JJ/MM/AAAA
                if(sDate=="" or sDate.isspace()== True or len(sDate)!=10):
                    Test = False;return Test
                else:
                    j = sDate[0:2]
                    m = sDate[3:5]
                    a = sDate[6:10]
            elif(sType=='D3'):#----AAAA-MM-JJ
                if(sDate=="" or sDate.isspace()== True or len(sDate)!=10):
                    Test = False;return Test
                else:
                    j = sDate[8:10]
                    m = sDate[5:7]
                    a = sDate[0:4]
            elif(sType=='D4'):#-----AAAAMMJJ
                if(sDate=="" or sDate.isspace()== True or len(sDate)!=8):
                    Test = False
                    return Test
                else:
                    j = sDate[6:8]
                    m = sDate[4:6]
                    a = sDate[0:4]
                
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
            elif(sType=='D7'):#----JJ/MM/AAAA ou 00/MM/AAAA OU 00/00/AAAA ou 00/00/0000
                if(sDate=="" or sDate.isspace()== True or len(sDate)!=10):
                    Test = False
                    return Test
                else:
                    j = sDate[0:2]
                    m = sDate[3:5]
                    a = sDate[6:10]
        
            if(self.isNumpos(j) and self.isNumpos(m) and self.isNumpos(a)):
                Test = True
                #return Test
            else:
                Test = False
                return Test
            
        if(int(m)<1 or int(m)>12 or int(j)<1 or int(j)>31 or int(a)<1900 or int(a)>2100):
            Test = False
            return Test
        else:
            if(m in ['04','06','09','11']):
                if(int(j)>30):
                    Test = False
                    return Test
            elif(m=='02'):
                if(int(j)>29):
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
            i=i+1
        return res
    
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsMajus(self,chaine):
        """Retourne True si touts les caracteres dans chaine sont majuscules """
        for i in chaine:
            print i
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
        if(nombVirgule>1):
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
            print "probleme sur " + str(erreur)+  " champ(s) :", zChampErr
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
    def Is0a9ponctA(self,chaine,ponctA,ponctNA,bEspA=False):
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"
        listeAaZ = "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn"
        chiffre = "0123456789"
        Is_0a9PonctA = True
        i=0
        while(i<len(chaine)):
            if(bEspA==False):
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
        chiffre = "0123456789"
        i=0
        is_0a9_Esp = True
        while(i<len(chaine)):
            if(chaine[i] not in chiffre and chaine[i].isspace()==False):
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
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"
        listeAaZ = "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn"
        chiffre = "0123456789"
        isPonctPresent = False
        if(bill==True):
            sCh = self.GetIllOut(chaine)
        else:
            sCh = chaine
            i=0
            while(i<len(sCh)):
                if(sCh[i] not in ListeAccents and sCh[i] not in listeAaZ and sCh[i] not in chiffre ):
                    isPonctPresent = True
                i=i+1
        return isPonctPresent
    
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsPonctInListeAuto(self,sChaine,sListeAuto,Bill=False):
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"
        listeAaZ = "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn"
        chiffre = "0123456789"
        
        if(Bill==True):
            sCh = self.GetIllOut(sChaine)
        else:
            sCh = chaine
            
        IsPonctInListeAuto = True
        i=0
        while(i<len(sCh)):
            if(sCh[i] not in ListeAccents and sCh[i] not in listeAaZ and sCh[i] not in chiffre and sCh[i] not in sListeAuto):
                IsPonctInListeAuto = False
            i=i+1
        return IsPonctInListeAuto
    
    #------------------------------------------------------------------------------------------------------------------------------------------------
    def IsPonctInListeNonAuto(self,sChaine,sListenonAuto,Bill=False):
            ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"
            listeAaZ = "AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn"
            chiffre = "0123456789"
            
            if(Bill==True):
                sCh = self.GetIllOut(sChaine)
            else:
                sCh = chaine
                
            IsPonctInListeNonAuto = False
            i=0
            while(i<len(sCh)):
                if(sCh[i] not in ListeAccents and sCh[i] not in listeAaZ and sCh[i] not in chiffre and sCh[i]  in sListenonAuto):
                    IsPonctInListeNonAuto = True
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
                print ""
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
    
    
    def controle(self,schp,svaleur,bMsg,Bill,conn=None):
        
        sval = svaleur
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cur.execute("SELECT * FROM \"CONTROLE_STANDARD\" WHERE \"NOM_CHAMP\"='" +schp+"'")
        trs_Cont =  cur.fetchone()
      
        
    
        if trs_Cont==None:
            self.errorDlg('Infos','La table de contrôle standard est vide.\nAucun contrôle à faire.')
            return False
        
       
       
        rs_Cont = trs_Cont
        print trs_Cont
        bVideA = trs_Cont["VIDE_AUTORISE"]

        if(rs_Cont["VIDE_AUTORISE"]==None):
            bVideA = ""
        else:
            bVideA = rs_Cont["VIDE_AUTORISE"]


        
        bEspA = rs_Cont["ESPACE_AUTORISE"]
        if(rs_Cont["PAR_DEFAUT"]!=None  and rs_Cont["PAR_DEFAUT"] != "" ):
            print rs_Cont["NOM_CHAMP"]
            if(rs_Cont["PAR_DEFAUT"].strip()!=""):
                bVideA = False

        bAccentA = rs_Cont["ACCENT_AUTORISE"]
        bPonctA = rs_Cont["PONCT_AUTORISE"]
        bLongL = rs_Cont["LONGUEUR_LIMITE"]
        bSep = rs_Cont["SEPARE"]
        bCasse = rs_Cont["TEST_CASSE"]
        print "bcasse," , bCasse
        if(rs_Cont["LONGUEUR"]==None):
            sLong = ""
        else:
            sLong = rs_Cont["LONGUEUR"]

        if(rs_Cont["TYPE_LONGUEUR_LIMITE"]==None):
            sTypeLong = ""
        else:
            sTypeLong = rs_Cont["TYPE_LONGUEUR_LIMITE"] #'Alaina le longueur
        
        if(rs_Cont["SEPARATEUR"]==None):
            sSep = ""
        else:
            sSep = rs_Cont["SEPARATEUR"] #'Alaina le séparateur
        
        
        if(rs_Cont["LIMITE"]==None):
            sLim = ""
        else:
            sLim = rs_Cont["LIMITE"]#'Alaina le limite
        
        if(rs_Cont["CASSE"]==None):
            sCasse = ""
        else:
            sCasse = rs_Cont["CASSE"] #'Alaina le séparateur
                    
        if(rs_Cont["P_AUTORISEES"]==None):
            sPonctA = ""
        else:
            sPonctA = rs_Cont["P_AUTORISEES"]

        if(rs_Cont["P_NON AUTORISEES"]==None):
            sPonctNonA = ""
        else:
            sPonctNonA = rs_Cont["P_NON AUTORISEES"]
         
        #Ireo zay mampiasa an'ilay LONGUEUR_LIMITE
        if(rs_Cont["TYPE_CONTROLE"]== "4" or rs_Cont["TYPE_CONTROLE"] == "6" or rs_Cont["TYPE_CONTROLE"] == "9"):
            if((bLongL=="1") and (sLong == "" or sTypeLong == "")):
            #'Misy diso ny paramétrage
                self.errorDlg("Erreur","ERREUR PARAMETRAGE.Longueur non spécifié pour le champ " +str(sChp))
                return False
        
        #Ireo zay mampiasa ny SEPARATEUR
        if(rs_Cont["TYPE_CONTROLE"] == "8"):
            if(bSep=="1" and sSep == ""):
                #Then 'Misy diso ny paramétrage
                self.errorDlg("Erreur","ERREUR PARAMETRAGE.Séprateur non spécifié pour le champ " +str(sChp))
                return False
        
        #'Test des 2 valeurs limites
        if(rs_Cont["TYPE_CONTROLE"]== "5"):
            if (sLim == ""):    
                self.errorDlg("Erreur","ERREUR PARAMETRAGE.Valeur limite spécifié pour le champ "  +str(sChp))
                return False
            nPos = sLim.find(">")
            if(nPos == 0):
                self.errorDlg("Erreur","ERREUR PARAMETRAGE.Valeur limite INCORRECT pour le champ " +str(sChp))
                return False
            else:
                nVal1 = len(sLim[0:nPos - 1])
                nVal2 = len(sLim[nPos + 1])
                if nVal2 == 0 :
                    self.errorDlg("Erreur","ERREUR PARAMETRAGE.Valeur limite INCORRECT pour le champ " +str(sChp))
                    return False
                 
                if(nVal2 < nVal1) :
                    self.errorDlg("Erreur", "ERREUR PARAMETRAGE.Valeur limite INCORRECT pour le champ " +str(sChp))
                    return False
                
        #'Ho an'ny ALPHANUMERIQUE : raha toa ka tsy testé ny LONGUEUR
        #'no sady accent autorisé no sady ponct autorisé no sady vide autorisé,esp autorisé
        #'donc TOUT EST AUTORISE -> de tsy misy antony ametrahana azy ao
        if(rs_Cont["TYPE_CONTROLE"] == "9"):
            if(bVideA=="1"  and bLongL!="1" and bAccentA=="1" and bPonctA=="1" and bEspA=="1"):
                self.errorDlg("Erreur","ERREUR PARAMETRAGE. Aucun contrôle pour le champ " +str(sChp)+ ".\nVeuillez le supprimer de là.")
                return False
            if(bCasse==True and sCasse == ""):
                self.errorDlg("Erreur", "ERREUR PARAMETRAGE. CASSE non spécifié pour le champ " +str(sChp)+ ".")
                return False
            
        #'VITA ZAY NY TEST REHETRA MOMBA NY PARAMETRAGE N'INY CHAMP INY
        #'Tetezo @ zay ny données
        
        
        #'Avadika Vide aloha zay null mba hanamora zavatra
        if(sval==None):
           sval = ""
        
         #'Tenir compte des illisibles ?
            
        if(Bill==True):
           if(sval.find("<?>") !=-1):
                return True
        sMsg=""
            
        if sval != "" :
                
            #'Tsy manao zavatra raha tsy misy zavatra atao mazava ho azy
            #'Valeur par défaut ve aloha misy zavatra ?
            #'Satria raha misy ka mitovy amin'iny le valeur ho tester-na
            #'de VRAI foana n'inona n'inona mitranga eo
            if((rs_Cont["PAR_DEFAUT"]!=None) and (rs_Cont["PAR_DEFAUT"]) != ""):
                if sval == rs_Cont["PAR_DEFAUT"]:
                    return True   
                       
            typectrl = rs_Cont["TYPE_CONTROLE"]
                
            if(typectrl=='1'):
                #"EMAIL"
                if(self.isMailCorrect(sval)==False):
                    sMsg = "E-Mail incorrect."
                        

            if(typectrl=='2'):
                #"DATE 1 (JJ/MM/AA)"
                if(self.isDateCorrect(sval, "D1")==False):
                    sMsg = "Date Incorrect. Format ""JJ/MM/AA""."
                     
            if(typectrl=='3'):
                #"DATE 2 (JJ/MM/AAAA)"
                if(self.isDateCorrect(sval, "D2")==False):
                    sMsg = "Date Incorrect. Format ""JJ/MM/AAAA""."
                    

            if(typectrl=='4'):
                if(bEspA==False):
                    #'ESP NON AUTORISE
                    if(bPonctA=='0'):
                        #'NOM COCHE NY PONCTUATION
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
                            

            if(typectrl=='5'):
                    #'NUMERIQUE LIMITE ENTRE 2 VAL
                if((int(sval) >= nVal1 and int(sval) <= nVal2)==False):
                    sMsg = "Valeur en dehors de la plage(Entre " +str(nVal1)+ " et "+str(nVal2 )+ ")."
                        
                
            if(typectrl=='6'):
                    
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
                                
                        
            if(typectrl=='7'):
                if(self.isDansUnique(sval, sLim)==False):
                    sMsg = "Valeur NON accepté.Règle : " +str(sLim) +"."
                        
                    
            if(typectrl=='8'):
                #'LIMITE/MULTIPLE
                svar = self.GetLengthLim(sLim)
                if(self.isDansMultiple(sval, sLim, svar, bSep, sSep)==False):
                    sMsg = "Valeur NON accepté.Règle : " + str(sLim) + ". Ou un code se répète plus d'une fois."
                    
                    
                else:
                    pass
                    #'Edit-er na fa sao de tsy valeur trié no tao
                    #'Oh: 13254 no tao
                    #'marina nefa ohatra io fa mila trier na hoe 12345
                    #cur.execute("UPDATE \""+sTab+"\" SET \""+sChp+"\"='"+sval+"' where \"N_ENR\"='"+sEnr+"'")
             
            if(typectrl=='9'):
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
                                
                    
                    
        
            if(typectrl=='10'):
                #date americaine
                if(self.isDateCorrect(sval, "D3")==False):
                    sMsg = "Date Incorrect. Format ""AAAA-MM-JJ""."
                        
                
            if(typectrl=='11'):
                if self.isDateCorrect(sval, "D4")==False:
                    sMsg = "Date Incorrect. Format ""AAAA-MM-JJ""."
                        
                
            if(typectrl=='12'):
                if self.isDateCorrect(sval, "D5")==False:       
                    sMsg = "Date Incorrect. Format ""JJMMAA""."
                        
                    
            if(typectrl=='13'):
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
                                
                    
              
            if(typectrl=='14'):
                #jjmmaaaa
                if(self.isDateCorrect(sval, "D6")==False):
                    sMsg = "Date Incorrect. Format ""JJMMAAAA""."
                        
                    

            if(typectrl=='15'):
                if(sval!=None and sval != ""):
                    sMsg = "Ce champ doit être vide. "
                        
                    

            if(typectrl=='16'):
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
            cur.execute("INSERT INTO erreur(n_enr,n_lot,champ,error) VALUES('"+str(nenr)+"','"+str(nlot)+"','"+str(Chp)+"','"+str(self.cleanAcc(msg))+"')")
        else:
            if(t['champ'].find(Chp)==-1):
                newChamp = t['champ']+'-'+ Chp
                newError = t['error']+'-'+ msg
                cur.execute("UPDATE erreur SET champ='"+newChamp+"',error='"+str(self.cleanAcc(newError))+"'  where n_enr='"+str(nenr)+"' and n_lot='"+str(nlot)+"'")
            else:
                newError = t['error']+'/'+ msg
                cur.execute("UPDATE erreur SET error='"+str(self.cleanAcc(newError))+"'  where n_enr='"+str(nenr)+"' and n_lot='"+str(nlot)+"'")
        
    def IsMontant(self,szChaine):
        
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
        
        if len(szChaine[positionv + 1]) != 2 :
            IsMontant = False
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
    