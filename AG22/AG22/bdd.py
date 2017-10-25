#!/usr/bin/env python
# -*- coding: cp1252  -*-
import psycopg2
import psycopg2.extras,wx

class bdd:
    def __init__(self):
        pass

    def copietable(self,tableOrig,connOrig,tableDest,connDest,replce=True):
        tzChamps = self.getChamps(tableOrig,connOrig)
        self.CreateTable(tableDest,tzChamps,connDest,replce)


    def getChamps(self,table,connexion):

        """ Renvoie sous forme tableau tridimensionnelle la liste des champs dans la table table """
        sqlget = "SELECT a.attname as Column,pg_catalog.format_type(a.atttypid, a.atttypmod) as Datatype,a.attnotnull as notnull "
        sqlget+= " FROM pg_catalog.pg_attribute a WHERE a.attnum > 0 AND NOT a.attisdropped AND a.attrelid = ("
        sqlget+= " SELECT c.oid FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace "
        sqlget+= " WHERE c.relname ~ '^("+table+")$' AND pg_catalog.pg_table_is_visible(c.oid) ) "

        connexion.set_isolation_level(0)
        curs = connexion.cursor()
        curs.execute(sqlget)
        champs = curs.fetchall()
        I=0
        while(I<len(champs)):
            if(champs[I][0]=='idenr'):
                champs[I]=('idenr',champs[I][1],False)
            I=I+1

        return champs


    def getNomChamps(self,table,connexion):

        """ Renvoie sous forme tableau tridimensionnelle la liste des champs dans la table table """
        sqlget = "SELECT a.attname as Column,pg_catalog.format_type(a.atttypid, a.atttypmod) as Datatype,a.attnotnull as notnull "
        sqlget+= " FROM pg_catalog.pg_attribute a WHERE a.attnum > 0 AND NOT a.attisdropped AND a.attrelid = ( "
        sqlget+= " SELECT c.oid FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace "
        sqlget+= " WHERE c.relname ~ '^("+table+")$' AND pg_catalog.pg_table_is_visible(c.oid) ); "
        connexion.set_isolation_level(0)
        curs = connexion.cursor()
        curs.execute(sqlget)
        champs = curs.fetchall()
        ligne = len(champs)
        i=0
        tableColumn = []
        while(i<ligne):
            tableColumn.append(champs[i][0])
            i=i+1

        return tableColumn



    def CreateTable(self,table,tzChamp,connexion,replace=False):
        """ Cette fonction permet de créer une table nommée table, avec champs le contenu de la variable d'entré tableau tzChamp, et accedé par l'obj connexion ObjConnex, tzChamp de la forme [(ch1 type1 NotNull(true)/Null(False)),(ch2 type2 NotNull(true)/Null(False)),....], connexDest: connexion d'acces  """
        if replace==True:
            connexion.set_isolation_level(0)
            curs = connexion.cursor()
            curs.execute("DROP TABLE IF EXISTS "+table+" ")



        i=0
        sql = ""
        sql+= "CREATE TABLE \"" + table + "\" ("
        while i<len(tzChamp):
            if i== len(tzChamp) - 1:

                if tzChamp[i][2] == True:
                    sql+= "\""+tzChamp[i][0]+ "\" " + tzChamp[i][1] + " NOT NULL"
                    i=i+1
                else:
                    sql+= "\""+tzChamp[i][0]+ "\" " + tzChamp[i][1] + " NULL"
                    i=i+1
            else:
                if tzChamp[i][2] == True:
                    sql+= "\""+tzChamp[i][0]+ "\" " + tzChamp[i][1] + " NOT NULL,"
                    i=i+1
                else:
                    sql+= "\""+tzChamp[i][0]+ "\" " + tzChamp[i][1] + " NULL,"
                    i=i+1
        sql+= ") WITH (OIDS=TRUE ); ALTER TABLE \"" +  table + "\" OWNER TO postgres;"

        if(self.istablexist(table,connexion)==False):
            connexion.set_isolation_level(0)
            curs = connexion.cursor()
            curs.execute(sql)


        return True


    def istablexist(self,ztable,connexion):

        """ Cette fonction permet de tester si une table ztable existe dans la base des données accedé par connex"""
        j=0
        connexion.set_isolation_level(0)
        curs = connexion.cursor()
        curs.execute("SELECT tablename FROM pg_tables WHERE tablename !~ '^pg_'")
        liste =curs.fetchall()
        isexiste = False
        while j<len(liste):
            if liste[j][0] == ztable:
                isexiste = True
                j=j+1
            else:
                j=j+1
        return isexiste

    def createcomafnor(self,connexion):
        """Création table comafnor """
        curs = connexion.cursor()
        sql = "CREATE TABLE \"COM_AFNOR\" (effectif_lotmin integer,effectif_lotmax integer,nb_ech integer,seuil1 integer,nqa character varying(50))"
        sql+= "WITH (OIDS=FALSE);ALTER TABLE \"COM_AFNOR\" OWNER TO postgres;"
        curs.execute(sql)
        sqldata  = "INSERT INTO \"COM_AFNOR\" VALUES (1, 8, 2, 0, '0,01'); "
        sqldata+= "INSERT INTO \"COM_AFNOR\"  VALUES (9, 15, 3, 0, '0,01');"
        sqldata+="INSERT INTO \"COM_AFNOR\" VALUES (16, 25, 5, 0, '0,01');"
        sqldata+= "INSERT INTO \"COM_AFNOR\" VALUES (26, 50, 8, 0, '0,01');"
        sqldata+= "INSERT INTO \"COM_AFNOR\" VALUES (51, 90, 13, 0, '0,01');"
        sqldata+="INSERT INTO \"COM_AFNOR\" VALUES (91, 150, 20, 0, '0,01');"
        sqldata+="INSERT INTO \"COM_AFNOR\" VALUES (151, 280, 32, 1, '0,01');"
        sqldata+="INSERT INTO \"COM_AFNOR\" VALUES (281, 500, 50, 1, '0,01');"
        sqldata+="INSERT INTO \"COM_AFNOR\" VALUES (501, 1200, 80, 2, '0,01');"
        sqldata+="INSERT INTO \"COM_AFNOR\" VALUES (1201, 3200, 125, 3, '0,01');"
        sqldata+="INSERT INTO \"COM_AFNOR\" VALUES (3201, 10000, 200, 5, '0,01');"
        sqldata+="INSERT INTO \"COM_AFNOR\" VALUES (10001, 35000, 315, 7, '0,01');"
        curs.execute(sqldata)



    def createcsta(self,connexion):

        """ Création table controle standard"""
        curs = connexion.cursor()
        sql = "CREATE TABLE \"CONTROLE_STANDARD\" (\"ORDRE\" integer,\"NOM_CHAMP\" character varying(255),\"LIBELLE\" character varying(255),"
        sql+= "\"TYPE_CONTROLE\" character varying(2),\"PAR_DEFAUT\" character varying(50),\"VIDE_AUTORISE\" character(1),\"LIMITE\" character varying(255),"
        sql+= "\"SEPARE\" character(1),\"SEPARATEUR\" character varying(1),\"LONGUEUR_LIMITE\" character(1),\"TYPE_LONGUEUR_LIMITE\" character varying(6),"
        sql+= "\"LONGUEUR\" character varying(3),\"ESPACE_AUTORISE\" character(1),\"ACCENT_AUTORISE\" character(1),\"PONCT_AUTORISE\" character(1),"
        sql+= "\"P_AUTORISEES\" character varying(50),\"P_NON AUTORISEES\" character varying(50),\"TEST_CASSE\" character(1),\"CASSE\" character varying(3)"
        sql+= ")WITH (OIDS=FALSE);ALTER TABLE \"CONTROLE_STANDARD\" OWNER TO postgres;"
        curs.execute(sql)

        sqlinsert = "INSERT INTO \"CONTROLE_STANDARD\" VALUES (6, 'PRENOM', 'PRENOM', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '0', NULL, NULL, '1', 'MAJ'); "
        sqlinsert+= "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (5, 'NOM', 'NOM', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '0', NULL, NULL, '1', 'MAJ');"
        sqlinsert+= "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (10, 'ADR1', 'ADR1 SANS NUMVOIE', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '0', NULL, NULL, '1', 'MAJ');"
        sqlinsert+= "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (12, 'ADR2', 'ADR2 SANS NUMVOIE', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '1', '-', NULL, '1', 'MAJ');"
        sqlinsert+= "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (17, 'VILLE', 'VILLE', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '0', NULL, NULL, '1', 'MAJ');"
        sqlinsert += "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (18, 'TEL', 'TEL', '4', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '0', '0', '0', '.', NULL, '0', NULL);"
        sqlinsert+="INSERT INTO \"CONTROLE_STANDARD\"  VALUES (7, 'EMAIL1', 'EMAIL1', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '0', '0', '1', NULL, NULL, '1', 'MIN');"
        sqlinsert += "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (16, 'CP', 'CP', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '1', NULL, NULL, '1', 'MAJ');"
        sqlinsert += "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (14, 'ADR3', 'ADR3 SANS NUMVOIE', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '0', NULL, NULL, '1', 'MAJ');"
        sqlinsert+= "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (9, 'NUMVOIE', 'NUMVOIE1', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '0', NULL, NULL, '1', 'MAJ');"
        sqlinsert += "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (15, 'ADR4', 'ADR4 SANS NUMVOIE', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '1', '-', NULL, '1', 'MAJ');"
        sqlinsert+= "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (4, 'CIV', 'CIV(Mr=1;Mme=2;Mlle=3)', '7', NULL, '1', '1;2;3', '0', NULL, '0', NULL, NULL, '0', '0', '0', NULL, NULL, '0', NULL);"
        sqlinsert+= "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (11, 'NUMVOIE2', 'NOMVOIE2', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '0', NULL, NULL, '1', 'MAJ');"
        sqlinsert+="INSERT INTO \"CONTROLE_STANDARD\"  VALUES (13, 'NUMVOIE3', 'NOMVOIE3', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '1', '0', '0', NULL, NULL, '1', 'MAJ');"
        sqlinsert+="INSERT INTO \"CONTROLE_STANDARD\"  VALUES (1, 'Q1', 'QUESTION N°1(Réponse N°1=1;Réponse N°2=2;Réponse N°3=3)', '7', NULL, '1', '1;2;3', '0', NULL, '0', NULL, NULL, '0', '1', '1', NULL, NULL, '0', NULL);"
        sqlinsert+="INSERT INTO \"CONTROLE_STANDARD\"  VALUES (2, 'Q2', 'QUESTION N°2(Réponse N°1=1;Réponse N°2=2;Réponse N°3=3)', '7', NULL, '1', '1;2;3', '0', NULL, '0', NULL, NULL, '0', '1', '1', NULL, NULL, '0', NULL);"
        sqlinsert += "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (3, 'Q3', 'QUESTION N°3(Réponse N°1=1;Réponse N°2=2;Réponse N°3=3)', '7', NULL, '1', '1;2;3', '0', NULL, '0', NULL, NULL, '0', '1', '1', NULL, NULL, '0', NULL);"
        sqlinsert += "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (19, 'Opt_Out_Groupe', 'Si toutefois vous ne desirez plus(Si cochée=1;sinon=2)', '7', NULL, '1', '1', '0', NULL, '0', NULL, NULL, '0', '1', '1', NULL, NULL, '0', NULL);"
        sqlinsert += "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (20, 'Opt_In_Partenaire', 'J''accepte de recevoir(Si cochée=1;sinon=2)', '7', NULL, '1', '1', '0', NULL, '0', NULL, NULL, '0', '1', '1', NULL, NULL, '0', NULL);"
        sqlinsert +="INSERT INTO \"CONTROLE_STANDARD\"  VALUES (8, 'EMAIL2', 'EMAIL2', '9', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '0', '0', '1', NULL, NULL, '1', 'MIN');"
        sqlinsert += "INSERT INTO \"CONTROLE_STANDARD\"  VALUES (21, 'DATE_NAISS', 'Date de naissance', '3', NULL, '1', NULL, '0', NULL, '0', NULL, NULL, '0', '1', '1', NULL, NULL, '0', NULL);"

        curs.execute(sqlinsert)

    def copieWithoutdata(self,table,connexionOrig,tableCible,connexionDest,replace=False):
        """ Créer une sauvegarde en fichier texte dans fileDirectory  la table,"""
        champs  = self.getChamps(table,connexionOrig)
        self.CreateTable(tableCible,champs,connexionDest,replace)
        return True


    def copieDatas(self,table_o,table_d,connex_o,connex_d,where=None,tvalareplacer0=['']):
        connex_o.set_isolation_level(0)
        connex_d.set_isolation_level(0)
        cur_o = connex_o.cursor()
        cur_d = connex_d.cursor()
        chmp_o = self.getChamps(table_o,connex_o)
        K=0
        tzChamp=[]
        while(K<len(chmp_o)):
            tzChamp.append(chmp_o[K][0])
            K=K+1
        if(self.istablexist(table_d,connex_d)==False):
            self.errorDlg('Erreur table','La table '+table_d+' n\'existe pas dans la connexion '+str(connex_d)+' ')
            return False

        r = "SELECT * FROM \""+table_o+"\"  "
        if(where!=None):
            r = "SELECT * FROM \""+table_o+"\" WHERE " + where
        cur_o.execute(r)
        datas = cur_o.fetchall()
        tzVal = [];I=0
        length = len(datas)
        while(I<length):
            J=0
            while(J<len(datas[I])):
                tzVal.append(datas[I][J])
                J=J+1
            a = 0
            while(a<len(tzVal)):
                if tzVal[a]==None or str(tzVal[a]) in tvalareplacer0:
                    tzVal[a] = ''
                a=a+1
            self.insertion(table_d,tzChamp,tzVal,connex_d)

            tzVal = []
            I=I+1



    def insertion(self,table,tzChamp,tzValue,connexion):
        """  Insertion des données dans une table;
            parametres:
                table : la table où on veut inserer les données
                tzChamp : les champs concernées par l'insértion (sous forme dde tableau)
                tzValue : les valeurs pour chaque element du tableau champ
                connexion : connexion d'acces à la table

        """
        if(len(tzChamp)==len(tzValue)):
            try:

                i=0
                j=0
                sql = ""
                sql += "SET client_encoding = 'WIN1252';INSERT INTO \"" + table + "\"("
                while(i<len(tzChamp)):
                    if i == len(tzChamp) - 1:
                        sql+= "\""+tzChamp[i]+"\""
                        i = i+1
                    else:
                        sql+="\""+tzChamp[i]+"\","
                        i = i+1
                sql+=") VALUES("
                while(j<len(tzValue)):
                    if tzValue[j]==None:
                        if j == len(tzValue)-1:
                            sql+=" null "
                            j = j+1
                        else:
                            sql+="null,"
                            j = j+1

                    else:

                        if j == len(tzValue)-1:
                            sql+="'%s'" %(str(tzValue[j]).replace("'","''"),)
                            j = j+1
                        else:
                            sql+="'%s'," %(str(tzValue[j]).replace("'","''"),)
                            j = j+1
                sql+= ")"
#                print sql
                curs = connexion.cursor()
                connexion.commit()
                curs.execute(sql)
                connexion.commit()
                
                return True
            except Exception as inst:
                msgs =  'type ERREUR78:'+str(type(inst))+'\n'     # the exception instance
                msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
                self.errorDlg('erreur',msgs)
                return False

        else:
            self.errorDlg("Erreur fatal","Nombres des colonnes non identiques")
            return False



    def update(self,table,tzChamp,tzValue,where,connexion):
        """ Update d'une table, key et keyval determinent les conditions si necessaire"""
        connexion.set_isolation_level(0)
        if(len(tzChamp)==len(tzValue)):
            nbchamp = len(tzChamp)

            i=0
            j=0
            sql = "SET CLIENT_ENCODING='WIN1252';"
            sql += "UPDATE \"" + table + "\" SET "
            sql+=  ""
            while (i<nbchamp ):

                if i == nbchamp-1:
                    if(tzValue[i]!=None ):
                        sql+= "\""+str(tzChamp[i])+"\"= '"+str(tzValue[i]).replace("'","''")+ "'"
                        i = i+1
                else:

                    if(tzValue[i]!=None):
                        sql+= "\""+str(tzChamp[i]) + "\"= '" + str(tzValue[i]).replace("'","''") + "',"
                        i =i + 1

            sql+= "  WHERE  "+where

            curs = connexion.cursor()
            curs.execute(sql)

            return True
        else:
            self.errorDlg('Erreur de champ!','Le nombre des colonnes et les valeurs à insérer doivent être identiques!')
            return False


    def errorDlg(self,title,message):
        """ Méthode d'affichage d'erreur"""
        msg = wx.MessageDialog ( None, message, caption=title,style=wx.ICON_ERROR|wx.OK , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg

    def InfoDlg(self,title,message):
        """ Méthode d'affichage d'information"""
        msg = wx.MessageDialog ( None, message, caption=title,style=wx.OK , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg



    def savetotext(self,table,fileDirectory,connexion,where=None):
        """ Créer une sauvegarde en fichier texte dans fileDirectory  la table,"""
        reqCopie        = "DROP TABLE IF EXISTS tabletemporaire;CREATE TEMP TABLE tabletemporaire AS SELECT * FROM \""+table+ "\""
        if(where!=None):
            reqCopie    += " WHERE "+where

        reqCopie        += ";"
        reqCopie        += "COPY tabletemporaire TO  '"+ fileDirectory + "'   WITH DELIMITER AS ' ' NULL AS '' CSV HEADER  "

        curs = connexion.cursor()
        curs.execute(reqCopie)

    def compter(self,table,connexion,where=''):
        """ Compte les enregistrement dans la table, where->condition """
        connexion.set_isolation_level(0)
        curs = connexion.cursor()
        if(where==''):
            curs.execute("SELECT * FROM \""+table+"\" ")
            result = curs.fetchall()
        else:
            curs.execute("SELECT * FROM \""+table+"\" WHERE "+where+" ")
            result = curs.fetchall()
        return len(result)

    def createstaCtrlGr(self,connexion):

        curs = connexion.cursor()
        sql = "CREATE TABLE standard (\"N_LIGNE\" character varying(50),\"N_ENR\" character varying(50),\"N_IMA\" character varying(255),"
        sql+= " \"MATRICULE\" character varying(4), \"ID_COMMANDE\" character varying(6),\"COMMANDE\" character varying(6),\"ETAPE\" character varying(50),"
        sql+= "\"N_LOT\" character varying(50),\"CHAMP\" character varying(255),\"VALEUR\" character varying(255),\"VALEUR_OLD\" character varying(255),"
        sql+=  " \"OK_KO\" character varying(50),\"__S\" character varying(1),idenr integer,idexecute integer,idexecutec integer) "
        sql+= "WITH (OIDS=TRUE);ALTER TABLE standard OWNER TO postgres;"
        curs.execute(sql)


    def verifhexavia(self,connadr,local,commande):
        curadr = connadr.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curloc = local.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curadr.execute("SELECT * FROM \"LCTRL\" WHERE \"ID_COMMANDE\"='"+str(commande)+"'")
        t=curadr.fetchall()
        Ntctrl = len(t)
        I=0

        while(I<Ntctrl):
            curadr.execute("SELECT * FROM \""+t[I][1]+ "\" WHERE \"ID_"+t[I][1]+"\" ='" +t[I][2]+"'")
            t2=curadr.fetchall()
            Nt2 = len(t2)
            J=0

            while(J<Nt2):
                ID_CTRL = t[I][2]
                if(t[I][1]=="TC1"):
                    self.V_1N(ID_CTRL,connadr,curloc)

                elif(t[I][1]=="TC2"):
                    self.V_2N(ID_CTRL,connadr,curloc)

                elif(t[I][1]=="TC3"):
                    self.V_3N(ID_CTRL,connadr,curloc)
                J=J+1

            I=I+1



    def V_1N(self,ID_CTRL,connSDSI,curloc):
        curlocal = curloc
        cursdsi  = connSDSI.cursor()
        cursdsi.execute("SELECT * FROM \"TC1\" WHERE \"ID_TC1\"='" + ID_CTRL + "'")
        ts=cursdsi.fetchone()
        if(ts!=None):
            if(ID_CTRL !="LDPUSH1"):
                curlocal.execute("UPDATE export SET \"" + ts[4]+"\" ='N'")

            k=0
            curlocal.execute("SELECT \""+ts[1]+"\" FROM export ")
            tloc = curlocal.fetchall()
            while(k<len(tloc)):
                #--"SELECT CHAMPB1 FROM BASE WHERE CHAMPB1=CHAMP1"

                cursdsi.execute("SELECT \""+ts[3]+"\" FROM \""+ts[2]+"\" WHERE \""+ts[3]+"\"= '" + tloc[k][0] + "'")
                tres = cursdsi.fetchone()

                if(tres!=None):
                    isql =  "UPDATE export "
                    isql += " SET \"" + ts[4] + "\"='O'"
                    isql += " WHERE \"" + ts[1] + "\" is not null and \"" + ts[1] + "\" <> '' and  \"" + ts[1] + "\"='"+tloc[k][0]+"'"
                    curlocal.execute(isql)
                k=k+1




    def V_2N(self,ID_CTRL,connSDSI,curloc):
        curlocal = curloc
        cursdsi  = connSDSI.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursdsi.execute("SELECT * FROM \"TC2\" WHERE \"ID_TC2\"='" + ID_CTRL + "'")
        ts=cursdsi.fetchone()

        if(ts!=None):
            curlocal.execute("UPDATE export SET \"" + ts['D']+"\" ='N'")
            k=0
            curlocal.execute("SELECT \""+ts['CHAMP1']+"\",\""+ts['CHAMP2']+"\" FROM export ")
            tloc = curlocal.fetchall()
            while(k<len(tloc)):

                if(tloc[k][0]==None):
                    champ1 = ''
                else:
                    champ1 = tloc[k][0]
                if(tloc[k][1]==None):
                    champ2 = ''
                else:
                    champ2 = tloc[k][1]

                #--"SELECT CHAMPB1,CHAMPB2 FROM BASE WHERE CHAMPB1=CHAMP1 and CHAMPB2=CHAMP2"

                cursdsi.execute("SELECT \""+ts['CHAMPB1']+"\",\""+ts['CHAMPB2']+"\" FROM \""+ts['BASE']+"\" WHERE \""+ts['CHAMPB1']+"\"= '" + champ1 + "' and \""+ts['CHAMPB2']+"\"='"+champ2+"'")
                tres = cursdsi.fetchone()

                if(tres!=None):
                    isql =  "UPDATE export "
                    isql += " SET \"" + ts['D'] + "\"='O'"
                    isql += " WHERE \"" + ts['CHAMP1'] + "\" is not null and \"" + ts['CHAMP1'] + "\" <> '' and  \"" + ts['CHAMP1'] + "\"='"+champ1+"'"
                    isql += "  and  \"" + ts['CHAMP2'] + "\" is not null and \"" + ts['CHAMP2'] + "\" <> '' and  \"" + ts['CHAMP2'] + "\"='"+champ2+"'"
                    curlocal.execute(isql)
                k=k+1


    def V_3N(self,ID_CTRL,connSDSI,curloc):
        curlocal = curloc
        cursdsi  = connSDSI.cursor()
        cursdsi.execute("SELECT * FROM \"TC3\" WHERE \"ID_TC3\"='" + ID_CTRL + "'")
        ts=cursdsi.fetchone()

        if(ts!=None):
            curlocal.execute("UPDATE export SET \"" + ts[8]+"\" ='N'")

            k=0
            curlocal.execute("SELECT \""+ts[1]+"\",\""+ts[2]+"\",\""+ts[3]+"\"  FROM export ")
            tloc = curlocal.fetchall()
            champ1 = tloc[k][0]
            champ2 = tloc[k][1]
            champ3 = tloc[k][2]


            while(k<len(tloc)):

                if(tloc[k][0]==None):
                    champ1 = ''
                else:
                    champ1 = tloc[k][0]
                if(tloc[k][1]==None):
                    champ2 = ''
                else:
                    champ2 = tloc[k][1]

                if(tloc[k][2]==None):
                    champ3 = ''
                else:
                    champ3 = tloc[k][2]


                #--"SELECT CHAMPB1,CHAMPB2 FROM BASE WHERE CHAMPB1=CHAMP1 and CHAMPB2=CHAMP2"

                cursdsi.execute("SELECT \""+ts[5]+"\",\""+ts[6]+"\", \""+ts[7]+"\" FROM \""+ts[4]+"\" WHERE \""+ts[5]+"\"= '" + champ1 + "' and \""+ts[6]+"\"='"+champ2+"' and \""+ts[7]+"\" = '"+champ3+"'")
                tres = cursdsi.fetchone()

                if(tres!=None):
                    isql =  "UPDATE export "
                    isql += " SET \"" + ts[8] + "\"='O'"
                    isql += " WHERE \"" + ts[1] + "\" is not null and \"" + ts[1] + "\" <> '' and  \"" + ts[1] + "\"='"+champ1+"'"
                    isql += "  and  \"" + ts[2] + "\" is not null and \"" + ts[2] + "\" <> '' and  \"" + ts[2] + "\"='"+champ2+"'"
                    isql += "  and  \"" + ts[3] + "\" is not null and \"" + ts[3] + "\" <> '' and  \"" + ts[3] + "\"='"+champ3+"'"
                    curlocal.execute(isql)
                k=k+1


    def creatEch(self,connexion):
        sql = "CREATE TABLE t_ech(commande character varying(50), n_lot character varying(50),nb_ech integer,seuil integer) "
        sql+= "WITH (OIDS=TRUE);ALTER TABLE t_ech OWNER TO postgres;"
        connexion.set_isolation_level(0)
        curs = connexion.cursor()
        curs.execute(sql)


    def DCount(self,table,connexion,where=''):
        curseur = connexion.cursor()
        r = "SELECT COUNT(*) from \""+table+"\" "
        if(where!='' and where.isspace()==False):
            r += " where "+ where + " "
        curseur.execute(r)
        dim = curseur.fetchone()
        return dim[0]


    def DLookup(self,FieldName , TableName ,connexion, criteria=None):
        cur = connexion.cursor()
        r= "SELECT DISTINCT \""+FieldName+"\" FROM \""+TableName+"\" "
        if(criteria!=None):
            r+=" WHERE "+criteria+" "
        cur.execute(r)
        tres = cur.fetchone()
        if(tres==None):
            return ''
        else:
            return tres[0]

    def DCountChamp(self,champ,table,conn,where=None):
        curseur = conn.cursor()

        r = "SELECT COUNT(\""+str(champ)+"\") from \""+table+"\" "
        if(where!=None and where!='' and where.isspace()==False):
            r += " where "+ where + " "

        curseur.execute(r)
        dim = curseur.fetchone()

        return dim[0]

    def lodlanguagepython(self,connexion):
        sql = "DROP  LANGUAGE  IF EXISTS  plpythonu CASCADE ;CREATE  LANGUAGE plpythonu"
        connexion.set_isolation_level(0)
        curs = connexion.cursor()
        curs.execute(sql)

    def createNz0(self,connexion):
        r = "CREATE OR REPLACE FUNCTION nz(ent text, sort text)  RETURNS text AS "
        r+= " $BODY$  if ent == None: return sort return ent $BODY$ LANGUAGE 'plpythonu' VOLATILE COST 100;"
        r+= " ALTER FUNCTION nz(text, text) OWNER TO postgres;"
        connexion.set_isolation_level(0)
        curs = connexion.cursor()
        curs.execute(r)
    def createNz(self,connexion):
        r="CREATE OR REPLACE FUNCTION nz(anyelement, anyelement) RETURNS anyelement AS"
        r+= " ' SELECT case $1 when null then $2 else $1 end ' LANGUAGE 'sql' IMMUTABLE"
        r+= " COST 100;ALTER FUNCTION nz(anyelement, anyelement) OWNER TO postgres; "
        connexion.set_isolation_level(0)
        curs = connexion.cursor()
        curs.execute(r)


    def DMax(self,champ,table,connexion,where=None):
        curs = connexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        r = "SELECT MAX(\""+champ+"\") FROM  \""+table +"\" "
        if(where!=None):
            r+= " WHERE "+ where
        curs.execute(r)
        data = curs.fetchone()

        if(data!=None):
            return data[0]
        else:
            return 0



    def cleanAcc(self,chaine):

        if self.isnumerique(chaine)==True:
            chaine = str(chaine)
        if self.IsAccentPresent((chaine))==True:
            chaine = self.NettoyagePonctPresent(chaine)
        return chaine

    def IsAccentPresent(self,chaine):
        """ Fonction de vérification si un caractere accentué est present dans chaine, retourne True si OUI et False si NON"""
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç¨^"
        res = False
        chaine = str(chaine)
        i=0
        while(i<len(chaine)):
            if(chaine[i] in "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç"):
                res = True
            i=i+1
        return res


    def NettoyagePonctPresent(self,chaine):
        """ Cette fonction enleve les accents dans une chaine"""
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç¨^"
        ReplaceListeAccents = "EEEEAAAUUUIIOOCeeeeaaauuuiiooc  "
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
        chaine = str(chaine)
        while (i<len(str(chaine))):
            if chaine[i] not in "0123456789":
                result = False
                return result
            i= i+1
        return result

    def etatcontrole(self,conn):
        curseur = conn.cursor()

        r = "SELECT * from controle order by traitement"
        curseur.execute(r)
        result = curseur.fetchall()
        return result
