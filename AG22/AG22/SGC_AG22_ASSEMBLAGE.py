#!/usr/bin/env python
# -*- coding: cp1252  -*-
import wx
import psycopg2
import psycopg2.extras
import os,sys,shutil
import time


import wx.html
import wx.lib.wxpTag



import fenetre
import fonctions
import random
import bdd
import source
import services
import error
import xlwt
import csv
import datetime
from datetime import date
import sys
reload(sys)
sys.setdefaultencoding("cp1252")


wx.Log.EnableLogging(False)

class MainApp(wx.App):
    def OnInit(self):
        """ Création de la fenêtre principale """
        frame = menu()

        return True

class menu:
    def __init__(self,commande='',matricule=4546):
        step = 5
        tscreen =  wx.GetClientDisplayRect()
        SizeXConteneur = tscreen[2]*75/100

        SizeYConteneur = tscreen[3]*90/100

        self.nomcommande = 0
        idcom        = 'sgag22'

        dbname='saisie'
        self.incH = 25
        self.incV = 30
        self.idcom = idcom

        self.dbname = dbname
        self.pathoutils = r"\\mctana\prod$\CSDT\\"+idcom+"\\"
        self.pathimages = r"\\servbase3\images$\\"
        self.path_controle_sta = self.pathoutils+'controle_standard_ff.sql'
        self.path_controle = self.pathoutils+'controle_ass2.sql'
        self.path_controlesta = self.pathoutils + 'CONTROLE_STANDARD.sql'

        self.createdb(self.dbname)
        self.path_controle_export = ''
        self.service = services.Fonction()
        self.fonc = services.Fonction()
        self.repertoiretoexport = r"\\bigserver\push$"
        repertoire  = "C:/image/"
        fenetremenu = fenetre.MainWindow('ASSEMBLAGE/UNIFORMISATION SGC TYPE AG22 02-03-2017',(SizeXConteneur, SizeYConteneur),self.dbname)
        fenetremenu.menubars()
        self.fenprincip = fenetremenu
        self.db = bdd.bdd()

        #CONTENEUR
        contwdg     = fenetremenu.conteneurPanel((0,0),(SizeXConteneur,SizeYConteneur))

        #fonction de traitement des composantes
        traitement  = fonctions.fonction(contwdg,dbname,idcom)
        self.traitement = traitement

        #---- Titre --- #
        self.lblTitle = fenetremenu.addLabel(contwdg,texte='ASSEMBLAGE/UNIFORMISATION SGC TYPE AG22',debut=1,pos=(230,20),size=(150,15))
        self.lblTitle.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.lblTitle.SetForegroundColour((0,0,255))
        self.lblTitle.SetBackgroundColour((255,255,255))

        # --- Composante -----#
        fenetremenu.addLabel(contwdg,texte='COMMANDE:')
        COMMANDE    = fenetremenu.AddTexte(contwdg,colaling=1,sizeX=100,max=6,name = 'COMMANDE')
        COMMANDE.Bind(wx.EVT_KILL_FOCUS,traitement.checkEntry)

        fenetremenu.addLabel(contwdg,texte='MATRICULE:')
        MATRICULE   = fenetremenu.AddTexte(contwdg,colaling=1,sizeX=100,max=5,name = 'MATRICULE')
        MATRICULE.Bind(wx.EVT_KILL_FOCUS,traitement.checkEntry)
#        COMMANDE.SetValue("SGC057")
#        MATRICULE.SetValue("6109")

        self.commande = COMMANDE
        self.matricule= MATRICULE

        POS0 = MATRICULE.GetPosition()
        siecomm = MATRICULE.GetSize()
        y= POS0[1]
        x= 1.8*POS0[0]
        bt_init     = wx.Button(contwdg, id=-1, label='&Lister', pos=(x,y),size=(100,30))
        self.panelRight = wx.Panel(contwdg,wx.ID_ANY,pos=(540,140),size=(200,315),style = wx.SIMPLE_BORDER|wx.TAB_TRAVERSAL)

        # --- Boutons et checkbox ---#
        bt_ext              = wx.Button(self.panelRight, id=-1, label='&Extraction', pos=(25,10),size=(120,30))
        bt_lot              = wx.Button(self.panelRight, id=-1, label='&Quantité Lot', pos=(25,45),size=(120,30))
        self.checklot       = wx.CheckBox(self.panelRight, id=-1, pos=(155,55))
        bt_cons_export      = wx.Button(self.panelRight, id=-1, label='&Consult export', pos=(25,80),size=(120,30))
        self.checkcons_export    = wx.CheckBox(self.panelRight, id=-1, pos=(155,85))
        #bt_ctrl1             = wx.Button(self.panelRight, id=-1, label='&Verif Combinaison', pos=(25,115),size=(120,30))
        #self.checkcomb       = wx.CheckBox(self.panelRight, id=-1, pos=(155,115))
        #self.checkcomb.Enable(False)
        #bt_ctrl             = wx.Button(self.panelRight, id=-1, label='&Controle Standard', pos=(25,150),size=(120,30))
        #self.checksta       = wx.CheckBox(self.panelRight, id=-1, pos=(155,150))
        #self.checksta.Enable(False)

        bt_export           = wx.Button(self.panelRight, id=-1, label='&Exportation', pos=(25,115),size=(120,30))

        QUIITER             = wx.Button(self.panelRight, id=-1, label='QUITTER', pos=(25,150),size=(120,30))

        ## --- Evennements --#
        QUIITER.Bind(wx.EVT_BUTTON,self.onClose)
        bt_init.Bind(wx.EVT_BUTTON,self.Onliste)
        bt_ext.Bind(wx.EVT_BUTTON,self.OnExtract)
        bt_lot .Bind(wx.EVT_BUTTON,self.nombrelots)
        bt_cons_export.Bind(wx.EVT_BUTTON,self.consult_export)
        #bt_ctrl1.Bind(wx.EVT_BUTTON,self.verifierInterdep)
        #bt_ctrl.Bind(wx.EVT_BUTTON,self.controle_standard)
        bt_export.Bind(wx.EVT_BUTTON,self.exporter)

        fenetremenu.events(wx.EVT_MENU,self.ctrlsta,fenetremenu.itemMenuCsta)
        fenetremenu.events(wx.EVT_MENU,traitement.onExit,fenetremenu.itemMenuQuitter)

        #self.tzobjet=[self.checklot,self.checkcons_export,self.checkcomb,self.checksta]
        self.tzobjet=[self.checklot,self.checkcons_export]
        for c in self.tzobjet:
            c.Enable(False)

        #Modification grid en liste
        self.liste = fenetremenu.AddListeCtrl(contwdg,sizeX=500,defaultposX=25,defaultposY=180,sizeY=0.6*SizeYConteneur)
        tabClm = ['Nom Fichier','Etat CTRL','Etat CQ']
        I=0
        while I<len(tabClm):
            self.liste.InsertColumn(I,tabClm[I])
            self.liste.SetColumnWidth(I,120)
            I=I+1

##        COMMANDE.SetValue('SGC055')
##        MATRICULE.SetValue('5340')

        COMMANDE.SetFocus()
        bConnect = self.connexion()
        if bConnect == False:
            return
        else:
#            self.createcsta()
            # --- Affichage --#
            fenetremenu.Show(True)
            if self.db.istablexist("controle",self.local)==True:
                if self.db.DCount("controle",self.local)==len(self.tzobjet):
                    tzetatcontrole=self.db.etatcontrole(self.local)
                    self.affcontrole(tzetatcontrole,self.tzobjet)
                else:
                    self.createcontrole()
                    tzetatcontrole=self.db.etatcontrole(self.local)
                    self.affcontrole(tzetatcontrole,self.tzobjet)

            else:
                self.createcontrole()
                tzetatcontrole=self.db.etatcontrole(self.local)
                self.affcontrole(tzetatcontrole,self.tzobjet)

            self.iif()
            self.sqlNz()

    def select(self,e=None):
        if self.ldeb.GetValue()=='' or self.ldeb.GetValue()==0:
            return
        self.nldeb=int(self.ldeb.GetValue())
        if self.lfin.GetValue()=='':
            self.nlfin=self.nldeb
        else:
            self.nlfin=int(self.lfin.GetValue())
        I=self.nldeb-1
        while(I<self.nlfin):
            self.grid.SelectRow(I,True)
            I=I+1

    def deasabletable(self,e):
        pass

    def createdb(self,name):
        conn     = psycopg2.connect("dbname=template1 user=postgres password=123456 host=localhost") #local
        curlocal  = conn.cursor()
        conn.set_isolation_level(0)
        curlocal.execute("SELECT datname from pg_database")
        tdb = curlocal.fetchall()
        I=0
        while(I<len(tdb)):
            if(name == tdb[I][0]):
                conn.close()
                return False
            I=I+1
        dlg = wx.Dialog(None,-1, 'Création de la base locale en cours.....!',size=(340,30))
        dlg.Show(True)
        curlocal.execute("CREATE DATABASE \""+name+"\"  WITH OWNER = postgres")
        dlg.Destroy()
        conn.close()

    def TimerHandler(self, event):
        self.count = self.count + 1

        if self.count >= 50:
            self.count = 0
        self.g1.SetValue(self.count)

    def ctrlsta(self,e):
        tableau = source.fenetre(self.fenprincip,'CONTROLE_STANDARD',self.dbname,'ORDRE')
        tableau.Show(True)
        self.checksta.SetValue(False)
        self.curlocal.execute("UPDATE controle SET etat='N' where traitement='5'")

    def OnCheck(self,evt):
        e_obj = evt.GetEventObject()
        e_obj.SetValue(e_obj.GetValue())

    def connexion(self):


        try:
            self.local      = psycopg2.connect("dbname="+self.dbname+" user=postgres password=123456  host= localhost") #prod
            self.local.set_client_encoding('WIN1252')
            self.local.set_isolation_level(0)
            self.curlocal  = self.local.cursor(cursor_factory=psycopg2.extras.DictCursor);

            self.prod      = psycopg2.connect("dbname=production user=op1 password=aa  host= 192.168.10.5") #prod
            self.prod.set_isolation_level(0);
            self.curprod   = self.prod.cursor(cursor_factory=psycopg2.extras.DictCursor);
            self.prod.set_client_encoding('WIN1252')

            self.sdsi      = psycopg2.connect("dbname=sdsi user=prep1 password=pp1p  host=192.168.10.5") #sdsi
            self.sdsi.set_isolation_level(0)
            self.cursdsi   = self.sdsi.cursor(cursor_factory=psycopg2.extras.DictCursor);

            self.adresse      = psycopg2.connect("dbname=Adresse user=op1 password=aa  host=192.168.10.5") #sdsi
            self.adresse.set_isolation_level(0)
            self.curadresse   = self.adresse.cursor(cursor_factory=psycopg2.extras.DictCursor);

        except :
            dialogue       = wx.MessageDialog(None, 'Serveur prod introuvable!', "Connexion!",wx.OK)
            result         = dialogue.ShowModal()
            return False


    def nextposition(self,widget,orient='H'):
        orient = orient.upper()
        posCurr = widget.GetPosition()
        sizeCurr = widget.GetSize()
        tres = []
        if orient=='H':
            y= posCurr[1]
            x= posCurr[0]+sizeCurr[0]+ self.incH
            tres.append(x)
            tres.append(y)
        else:
            x = posCurr[0]
            y = posCurr[1]+sizeCurr[1]+self.incV
            tres.append(x)
            tres.append(y)
        return tres

    def GetEtatPousse(self,setape,sidfichiercmd):
        commande    = self.commande.GetValue().upper()
        r_q_pousse = "SELECT pousse.* FROM pousse INNER JOIN fichier ON pousse.idfichiercmd = fichier.idfichiercmd "
        r_q_pousse += " WHERE pousse.idetape='" + setape + "' AND fichier.idcommande='"+ commande+"' and pousse.idfichiercmd='"+sidfichiercmd+"' ORDER BY pousse.idfichiercmd;"
        self.cursdsi.execute(r_q_pousse)
        tpousse =  self.cursdsi.fetchone()
        if tpousse==None:
            return "erreur"
        else:
            if tpousse['flagfinpousse']==None and tpousse['flagrejetpousse']==None and tpousse['flagencours']==None:
                return "Non traité"
            elif str(tpousse['flagfinpousse'])+str(tpousse['flagrejetpousse'])+str(tpousse['flagencours'])=="":
                return "Non traité"
            elif str(tpousse['flagfinpousse'])+str(tpousse['flagrejetpousse'])+str(tpousse['flagencours'])=="100":
                return "Fini"
            elif str(tpousse['flagfinpousse'])+str(tpousse['flagrejetpousse'])+str(tpousse['flagencours'])=="000":
                return "A suivre"
            elif str(tpousse['flagfinpousse'])+str(tpousse['flagrejetpousse'])+str(tpousse['flagencours'])=="001":
                return "En Cours"
            elif str(tpousse['flagfinpousse'])+str(tpousse['flagrejetpousse'])+str(tpousse['flagencours'])=="101":
                return "Rejet"
            else:
                return str(tpousse['flagfinpousse'])+str(tpousse['flagrejetpousse'])+str(tpousse['flagencours'])

    def GetMatricule(self,setape,sidfichiercmd):
            r_q_pousse = "SELECT * FROM pousse INNER JOIN fichier ON pousse.idfichiercmd = fichier.idfichiercmd "
            r_q_pousse += " WHERE pousse.idetape='" + setape + "' and pousse.idfichiercmd='"+sidfichiercmd+"' ORDER BY pousse.idfichiercmd;"
            self.cursdsi.execute(r_q_pousse)
            tpousse =  self.cursdsi.fetchone()
            if tpousse==None:
                return "erreur"
            else:
                return str(tpousse['matricule'])

    def Onliste(self,event):
        commande    = self.commande.GetValue().upper()
        matricule   = self.matricule.GetValue().upper()

        if commande=='' or matricule=='':
            return False

        r= "SElECT distinct fichesuiveuse_numerisation.valeur  from lot_numerisation inner join fichesuiveuse_numerisation on lot_numerisation.id_lot_numerisation=fichesuiveuse_numerisation.id_lot_numerisation"
        r+=" WHERE lot_numerisation.idcommande_reception='" + commande + "' and lot_numerisation.statut_reception='OK' and lot_numerisation.idsousdossier='AG22' and fichesuiveuse_numerisation.rubrique='LOT_OPERATION'  ORDER BY fichesuiveuse_numerisation.valeur "
#        print "r0:", r
        self.curprod.execute(r)
        tenrs = self.curprod.fetchall()
        I=0
        tzObj=[]
        tzSObj = []

        while(I<len(tenrs)):
            tzSObj.append(tenrs[I]['valeur'])
            r= "SElECT  lot_numerisation.id_lot_numerisation  from lot_numerisation inner join fichesuiveuse_numerisation on lot_numerisation.id_lot_numerisation=fichesuiveuse_numerisation.id_lot_numerisation"
            r+=" WHERE lot_numerisation.idcommande_reception='" + commande + "' and lot_numerisation.statut_reception='OK' and lot_numerisation.idsousdossier='AG22' and fichesuiveuse_numerisation.rubrique='LOT_OPERATION' and fichesuiveuse_numerisation.valeur='"+tenrs[I]['valeur']+"'  ORDER BY lot_numerisation.id_lot_numerisation"
            self.curprod.execute(r)
            tlot = self.curprod.fetchall()
            betape1=True
            betape2=True
            tid_lot_numerisation=""
            J=0
            while J < len(tlot):
                tid_lot_numerisation=tid_lot_numerisation+ "," + str(tlot[J]["id_lot_numerisation"])
                J+=1

            tid_lot_numerisation="(" + tid_lot_numerisation[1:] +")"
            r= "SElECT count(*) nbenrnontraite from pli_numerisation"
            r+=" WHERE id_lot_numerisation in " + tid_lot_numerisation + " and pli <> '0000' and statut not in ('PR','CO')"
#            print "r1:", r
            self.curprod.execute(r)
            tpli = self.curprod.fetchone()
            if tpli["nbenrnontraite"] == 0:
                r= "SELECT count(*) as nblotnontraite from pousse"
                r+= " INNER JOIN fichier on  pousse.idfichiercmd=fichier.idfichiercmd"
                r+=" WHERE"
                r+=" CASE WHEN pousse.flagfinpousse is null THEN '' ELSE pousse.flagfinpousse END"
                r+="||"
                r+=" CASE WHEN pousse.flagencours is null THEN '' ELSE pousse.flagencours END"
                r+="||"
                r+=" CASE WHEN pousse.flagrejetpousse is null THEN '' ELSE pousse.flagrejetpousse END"
                r+="<>'100'"
                r+=" and pousse.idetape='CONTROLE GROUPE' and fichier.id_lot_numerisation in " + tid_lot_numerisation
#                print "r2:", r
                self.cursdsi.execute(r)
                tctrl= self.cursdsi.fetchone()

                if tctrl["nblotnontraite"] > 0:
                    tzSObj.append("Non traite")
                    tzSObj.append("Non traite")
                else:
                    tzSObj.append("Fini")
                    r= "SELECT count(*) as nblotnontraite from pousse"
                    r+= " INNER JOIN fichier on  pousse.idfichiercmd=fichier.idfichiercmd"
                    r+=" WHERE"
                    r+=" CASE WHEN pousse.flagfinpousse is null THEN '' ELSE pousse.flagfinpousse END"
                    r+="||"
                    r+=" CASE WHEN pousse.flagencours is null THEN '' ELSE pousse.flagencours END"
                    r+="||"
                    r+=" CASE WHEN pousse.flagrejetpousse is null THEN '' ELSE pousse.flagrejetpousse END"
                    r+="<>'100'"
                    r+=" and pousse.idetape='ASSEMBLAGE/UNIFORMISATION' and fichier.id_lot_numerisation in " + tid_lot_numerisation
#                    print "r3:", r
                    self.cursdsi.execute(r)
                    tcq= self.cursdsi.fetchone()
                    if tcq["nblotnontraite"] > 0:
                        tzSObj.append("Non traite")
                    else:
                        tzSObj.append("Fini")
            else:
                tzSObj.append("Non traite")
                tzSObj.append("Non traite")

            tzObj.append(tzSObj)
            tzSObj = []
            I+=1
#        print "here"
        self.tzObj=tzObj
        # --- AFFICHAGE ------#
        self.liste.DeleteAllItems()
        k=len(tzObj)-1
        while k>=0:
            j=0
            while j<len(tzObj[k]):
                if j==0:
                    prim =  self.liste.InsertStringItem(0,str(tzObj[k][0]))
                if j>0:
                    self.liste.SetStringItem(0,j,str(tzObj[k][j]))
                j=j+1
            k=k-1


    def Onliste10122013(self,event):
        commande    = self.commande.GetValue().upper()
        matricule   = self.matricule.GetValue().upper()

        if commande=='' or matricule=='':
            return False

        r= "SElECT distinct fichesuiveuse_numerisation.valeur  from lot_numerisation inner join fichesuiveuse_numerisation on lot_numerisation.id_lot_numerisation=fichesuiveuse_numerisation.id_lot_numerisation"
        r+=" WHERE lot_numerisation.idcommande_reception='" + commande + "' and lot_numerisation.statut_reception='OK' and lot_numerisation.idsousdossier='AG22' and fichesuiveuse_numerisation.rubrique='LOT_OPERATION'  ORDER BY fichesuiveuse_numerisation.valeur "

        self.curprod.execute(r)
        tenrs = self.curprod.fetchall()
        I=0
        tzObj=[]
        tzSObj = []
        while(I<len(tenrs)):

            tzSObj.append(tenrs[I]['valeur'])
            r= "SElECT  lot_numerisation.id_lot_numerisation  from lot_numerisation inner join fichesuiveuse_numerisation on lot_numerisation.id_lot_numerisation=fichesuiveuse_numerisation.id_lot_numerisation"
            r+=" WHERE lot_numerisation.idcommande_reception='" + commande + "' and lot_numerisation.statut_reception='OK' and lot_numerisation.idsousdossier='AG22' and fichesuiveuse_numerisation.rubrique='LOT_OPERATION' and fichesuiveuse_numerisation.valeur='"+tenrs[I]['valeur']+"'  ORDER BY lot_numerisation.id_lot_numerisation"
            self.curprod.execute(r)
            tlot = self.curprod.fetchall()
            betape1=True
            betape2=True
            tid_lot_numerisation=""
            J=0
            while J < len(tlot):
                tid_lot_numerisation=tid_lot_numerisation+ "," + str(tlot[J]["id_lot_numerisation"])
                J+=1

            tid_lot_numerisation="(" + tid_lot_numerisation[1:] +")"

            r= "SElECT count(*) nbenrnontraite from pli_numerisation"
            r+=" WHERE id_lot_numerisation in " + tid_lot_numerisation + " and pli <> '0000' and statut not in ('PR','CO')"
            self.curprod.execute(r)
            tpli = self.curprod.fetchone()
            if tpli["nbenrnontraite"] == 0:
                r= "SELECT count(*) as nblotnontraite from pousse"
                r+= " INNER JOIN fichier on  pousse.idfichiercmd=fichier.idfichiercmd"
                r+=" WHERE"
                r+=" CASE WHEN pousse.flagfinpousse is null THEN '' ELSE pousse.flagfinpousse END"
                r+="||"
                r+=" CASE WHEN pousse.flagencours is null THEN '' ELSE pousse.flagencours END"
                r+="||"
                r+=" CASE WHEN pousse.flagrejetpousse is null THEN '' ELSE pousse.flagrejetpousse END"
                r+="<>'100'"
                r+=" and pousse.idetape='CONTROLE GROUPE' and fichier.id_lot_numerisation in " + tid_lot_numerisation

                self.cursdsi.execute(r)
                tctrl= self.cursdsi.fetchone()

                if tctrl["nblotnontraite"] > 0:
                    tzSObj.append("Non traite")
                    tzSObj.append("Non traite")
                else:
                    tzSObj.append("Fini")
                    r= "SELECT count(*) as nblotnontraite from pousse"
                    r+= " INNER JOIN fichier on  pousse.idfichiercmd=fichier.idfichiercmd"
                    r+=" WHERE"
                    r+=" CASE WHEN pousse.flagfinpousse is null THEN '' ELSE pousse.flagfinpousse END"
                    r+="||"
                    r+=" CASE WHEN pousse.flagencours is null THEN '' ELSE pousse.flagencours END"
                    r+="||"
                    r+=" CASE WHEN pousse.flagrejetpousse is null THEN '' ELSE pousse.flagrejetpousse END"
                    r+="<>'100'"
                    r+=" and pousse.idetape='ASSEMBLAGE/UNIFORMISATION' and fichier.id_lot_numerisation in " + tid_lot_numerisation
                    #print tid_lot_numerisation
                    self.cursdsi.execute(r)

                    tcq= self.cursdsi.fetchone()
                    #print str(tenrs[I]['valeur'])+"------------"+str(tcq)
                    if tcq["nblotnontraite"] > 0:
                        tzSObj.append("Non traite")
                    else:
                        tzSObj.append("Fini")


            else:
                tzSObj.append("Non traite")
                tzSObj.append("Non traite")

            tzObj.append(tzSObj)
            tzSObj = []
            I+=1

        self.tzObj=tzObj
        # --- AFFICHAGE ------#
        self.liste.DeleteAllItems()
        k=len(tzObj)-1
        while k>=0:
            j=0
            while j<len(tzObj[k]):
                if j==0:
                    prim =  self.liste.InsertStringItem(0,str(tzObj[k][0]))
                    #print prim
                if j>0:
                    self.liste.SetStringItem(0,j,str(tzObj[k][j]))
                j=j+1
            k=k-1

    def OnExtract(self,event):
        self.prod.set_isolation_level (0)
        self.sdsi.set_isolation_level (0)
        self.local.set_isolation_level (0)

        tzSelect = []
        if self.checklot.GetValue()==True:
            self.checklot.SetValue(False)
        if self.checkcons_export.GetValue()==True:
            self.checkcons_export.SetValue(False)


        if(self.liste.GetItemCount()==0):
            self.traitement.errorDlg('Erreur!','Vous avez oublié une étape, aucune donnée à extraire dans la liste!')
            return False

        nRows = self.liste.GetItemCount()
        I=0
        while I<nRows:
            if self.liste.IsSelected(I)==True:
                tzSelect.append(self.liste.GetItemText(I))
            I=I+1

        nbSelect =   len(tzSelect)
        if(nbSelect==0):
            self.traitement.errorDlg('Erreur!','Il faut au moins une ligne selectionnée!')
            return False

        commande    = self.commande.GetLineText(0).upper()
        matricule   = self.matricule.GetLineText(0).upper()

        if(commande=='' or matricule==''):
            return False

        iidexecute = self.Nz(self.db.DLookup("idexecute", "execute",self.sdsi,"idcommande='" +str(commande)+ "' and matricule=" +str(matricule)+ " AND datefinexe is null"), 0)
        if(iidexecute==0):
            self.traitement.errorDlg('Erreur!','Vous n\'avez pas debuté votre travail sur la GPAO')
            self.commande.SetFocus()
            return False
        self.idexecutec = iidexecute
        self.curlocal.execute("DROP TABLE IF EXISTS export")
        self.db.copietable(self.idcom+"_q",self.prod,"export",self.local)

        self.curlocal.execute("DROP TABLE IF EXISTS source")
        self.curlocal.execute("DROP TABLE IF EXISTS source_o")
        self.curlocal.execute("DROP TABLE IF EXISTS \""+self.idcom+"\"")
        self.db.copietable(self.idcom + "_c",self.prod,self.idcom,self.local)
        self.db.copietable(self.idcom,self.local,"source_o",self.local)
        self.db.copietable("source_o",self.local,"source",self.local)
        self.curlocal.execute("ALTER TABLE source ADD COLUMN idexecutec integer")
        self.curlocal.execute("ALTER TABLE source_o ADD COLUMN idexecutec integer")

        self.curlocal.execute("DROP TABLE IF EXISTS controle")
        self.createcontrole()

        I=0
        while(I<nbSelect):
            idlot_scan =tzSelect[I]
            K=0
            while K < len(self.tzObj):
                if idlot_scan==self.tzObj[K][0]:
                    if self.tzObj[K][1]=='Non traite':
                        self.traitement.errorDlg('Erreur','Etape CONTROLE GROUPE non finie pour le lot ' +idlot_scan)
                        return False

                    if self.tzObj[K][2]=='Fini':
                        msg = "Etape ASSEMBLAGE/UNIFORMISATION deja finie pour le lot "
                        self.traitement.errorDlg('Erreur',msg.encode('cp1252')+idlot_scan)
                        return False
                    break
                K+=1

            r= "SElECT  lot_numerisation.id_lot_numerisation  from lot_numerisation inner join fichesuiveuse_numerisation on lot_numerisation.id_lot_numerisation=fichesuiveuse_numerisation.id_lot_numerisation"
            r+=" WHERE lot_numerisation.idcommande_reception='" + commande + "' and lot_numerisation.statut_reception='OK' and lot_numerisation.idsousdossier='AG22' and fichesuiveuse_numerisation.rubrique='LOT_OPERATION' and fichesuiveuse_numerisation.valeur='"+idlot_scan+"'  ORDER BY lot_numerisation.id_lot_numerisation"
            tid_lot_numerisation=""
            self.curprod.execute(r)
            tlot=  self.curprod.fetchall()
            J=0
            while J < len(tlot):
                tid_lot_numerisation=tid_lot_numerisation+ "," + str(tlot[J]["id_lot_numerisation"])
                J+=1
            tid_lot_numerisation="(" + tid_lot_numerisation[1:] +")"

            sql="select * from fichier where idcommande='"+commande+"' and id_lot_numerisation in " +tid_lot_numerisation+" order by idfichiercmd"
            self.cursdsi.execute(sql)
            tlot=  self.cursdsi.fetchall()
            L=0
            while L < len(tlot):
                idFIchcmd     = tlot[L]["idfichiercmd"]
                where= "\"n_lot\"='"+idFIchcmd+"'  order by \"n_enr\""
                self.db.copieDatas(self.idcom+"_c","source_o",self.prod,self.local,where,tvalareplacer0=['<?>'])
                self.cursdsi.execute("update pousse set flagfinpousse='0', flagrejetpousse='0', flagencours='1', matricule='" + str(matricule) + "' where idetape='ASSEMBLAGE/UNIFORMISATION' and idfichiercmd='" + idFIchcmd + "'")
                L+=1
            I=I+1

        self.curlocal.execute("select * from source_o order by \"n_lot\",\"n_ima\"")
        tzsource_o = self.curlocal.fetchall()

        I=0
        dlg = self.dlgprogress(None,"Mise à jour source_o","Veuillez patienter....("+str(len(tzsource_o))+" enrgs!)",len(tzsource_o))
        for tzdata  in tzsource_o:
            self.curlocal.execute("update source_o set \"matricule\"='"+str(matricule)+ "', \"idexecutec\"="+ str(iidexecute)+", \"n_enr\"='"+self.formatesLigne(I+1)+"' where \"n_lot\"='"+tzdata['n_lot']+"' and \"n_ima\"='"+tzdata['n_ima']+"'")
            dlg.Update(I)
            I=I+1
        dlg.Destroy()

        self.curlocal.execute("DELETE FROM source")
        self.curlocal.execute("INSERT INTO source SELECT * FROM source_o")

        # *********************assemblage***************
        sqlExport = "INSERT INTO export (\"n_enr\", \"n_ima\", \"matricule\", \"id_commande\", \"commande\", \"etape\", \"n_lot\", \"list_ima\",\"pli\","
        sqlExport+= "\"lot_courrier\","
        sqlExport+= "\"id_web\","
        sqlExport+= "\"matr_operateur\","
        sqlExport+= "\"num_sequence\","

        sqlExport+= "\"date_cachet_poste\","
        sqlExport+= "\"civilite\","
        sqlExport+= "\"nom\","
        sqlExport+= "\"prenom\","
        sqlExport+= "\"adr1\","
        sqlExport+= "\"adr2\","
        sqlExport+= "\"adr3\","
        sqlExport+= "\"adr4\","
        sqlExport+= "\"cp\","
        sqlExport+= "\"ville\","
        sqlExport+= "\"pays\","
        sqlExport+= "\"code_pays\","
        sqlExport+= "\"email\","
        sqlExport+= "\"mobile\","
        sqlExport+= "\"j_accepte_de_recevoir\","
        sqlExport+= "\"remboursement_timbre\","
        sqlExport+= "\"iban\","
        sqlExport+= "\"bic\","
        sqlExport+= "\"presence_facture_ou_tc\","
        sqlExport+= "\"presence_enseigne\","
        sqlExport+= "\"saisie_code_point_de_vente\","
        sqlExport+= "\"date_sur_ticket_de_caisse\","
        sqlExport+= "\"presence_achat_accessoire\","
        sqlExport+= "\"presence_achat_mobile\","
        sqlExport+= "\"achat_simultane\","
        sqlExport+= "\"montant_ttc_accessoire\","
        sqlExport+= "\"montant_ht_accessoire\","
        sqlExport+= "\"presence_contrat_de_souscription\","
        sqlExport+= "\"presence_forfait\","
        sqlExport+= "\"presence_code_barre_accessoire\","
        sqlExport+= "\"original_code_barre_accessoire\","
        sqlExport+= "\"presence_code_barre_mobile\","
        sqlExport+= "\"saisie_code_barre_accessoire\","
        sqlExport+= "\"saisie_code_barre_mobile\","
        sqlExport+= "\"presence_bulletin\","
        sqlExport+= "\"codage_facture\","
        sqlExport+= "\"codage_forfait\","

        sqlExport+= "\"index_image\","
        sqlExport+= "\"doublon\","
        sqlExport+= "\"cnil\","






        sqlExport+= "\"id_lot_numerisation\","
        sqlExport+= "\"idenr\","
        sqlExport+= "\"idexecute\","
        sqlExport+= "\"nom_fichier_csv\","
        sqlExport+= "\"__s\")"


        #--------------------------------------

        sqlExport += " SELECT \"n_enr\", \"n_ima\", \"matricule\", 'sgae06',\"commande\", 'ASSEMBLAGE/UNIFORMISATION', \"n_lot\",\"list_ima\",\"pli\","
        sqlExport+="'',"
        sqlExport+="'',"
        sqlExport+="'',"
        sqlExport+="'',"
        sqlExport+="\"date_cachet_poste\","
        sqlExport+=" CASE WHEN \"civilite\"='1' THEN 'MR' WHEN \"civilite\"='2' THEN 'MME' WHEN \"civilite\"='3' THEN 'MLLE' ELSE '' END,"
        sqlExport+="\"nom\","
        sqlExport+="\"prenom\","
        sqlExport+="trim(TRIM(\"numvoie\") || ' ' || TRIM(\"adr1\")),"
        sqlExport+="trim(TRIM(\"numvoie2\") || ' ' || TRIM(\"adr2\")),"
        sqlExport+="trim(TRIM(\"numvoie3\") || ' ' || TRIM(\"adr3\")),"
        sqlExport+="TRIM(\"adr4\"),"
        sqlExport+="\"cp\","
        sqlExport+="\"ville\","
        sqlExport+= "\"pays\","
        sqlExport+="'',"
        sqlExport+="CASE WHEN \"email1\" <>'' And \"email2\" <>'' THEN \"email1\" || '@' || \"email2\" ELSE '' END,"
        sqlExport+= "\"mobile\","
        sqlExport+= "\"j_accepte_de_recevoir\","
        sqlExport+= "\"remboursement_timbre\","
        sqlExport+= "\"iban\","
        sqlExport+= "\"bic\","
        sqlExport+= "\"presence_facture_ou_tc\","
        sqlExport+= "\"presence_enseigne\","
        sqlExport+= "\"saisie_code_point_de_vente\","
        sqlExport+= "\"date_sur_ticket_de_caisse\","
        sqlExport+= "\"presence_achat_accessoire\","
        sqlExport+= "\"presence_achat_mobile\","
        sqlExport+= "\"achat_simultane\","
        sqlExport+= "\"montant_ttc_accessoire\","
        sqlExport+= "\"montant_ht_accessoire\","
        sqlExport+= "\"presence_contrat_de_souscription\","
        sqlExport+= "\"presence_forfait\","
        sqlExport+= "\"presence_code_barre_accessoire\","
        sqlExport+= "\"original_code_barre_accessoire\","
        sqlExport+= "\"presence_code_barre_mobile\","
        sqlExport+= "\"saisie_code_barre_accessoire\","
        sqlExport+= "\"saisie_code_barre_mobile\","
        sqlExport+= "\"presence_bulletin\","
        sqlExport+= "\"codage_facture\","
        sqlExport+= "\"codage_forfait\","


        sqlExport+= "'',"
        sqlExport+= "'0',"
        sqlExport+= "\"cnil\","



        sqlExport+= "\"id_lot_numerisation\","
        sqlExport+= "\"idenr\","
        sqlExport+= "\"idexecutec\","
        sqlExport+= "'',"
        sqlExport+= "'Q'"
        sqlExport+=" FROM \"source\" "
        sqlExport+=" ORDER BY \"n_enr\" "

        #print "sql: ", sqlExport
        self.curlocal.execute(sqlExport)

#        return

        # ---------------Traitements specials------------------

        #------------------------Maj boolean---------------------------------
        vivetic_prestation_id=1396 #à définir
        self.curprod .execute("select libelle from vivetic_champs where vivetic_prestation_id="+str(vivetic_prestation_id)+ " and vivetic_type_id=17")
        t=self.curprod.fetchall()
        sql="UPDATE"
        sql+=" export"
        sql+=" SET"
        s=0
        for enr in t:
            s=s+1
            if s==len(t):
                sql+=" \""+enr[0]+"\"=(CASE WHEN \""+enr[0]+"\"='' OR \""+enr[0]+"\" IS NULL THEN '0' ELSE \""+enr[0]+"\" END)"
            else:
                sql+=" \""+enr[0]+"\"=(CASE WHEN \""+enr[0]+"\"='' OR \""+enr[0]+"\" IS NULL THEN '0' ELSE \""+enr[0]+"\" END),"

        if len(t)>0:
            self.curlocal.execute(sql)
        #------------------------------------------------------------

        self.curlocal.execute("select * from export order by \"n_lot\",\"n_ima\"")
        tzexport = self.curlocal.fetchall()

        I=0
        dlg = self.dlgprogress(None,"Mis à jour sequence export","Veuillez patienter....("+str(len(tzexport))+" enrgs!)",len(tzexport))
        for tzdata  in tzexport:
            self.curlocal.execute("update export set \"num_sequence\"='"+ ("000000000"+str(int(I+1)))[-9:]+"' where \"n_lot\"='"+tzdata['n_lot']+"' and \"n_ima\"='"+tzdata['n_ima']+"' and \"idenr\"='"+str(tzdata['idenr'])+"'")
            dlg.Update(I)
            I=I+1
        dlg.Destroy()

        self.cursdsi.execute("select current_date as date, substr(localtime::varchar,1,8)::time as time")
        tdate = self.cursdsi.fetchone()
        dateNow=str(tdate[0])
        timereel=str(tdate[1])

        self.curlocal.execute("SELECT * FROM \"export\"")
        lesenrs= self.curlocal.fetchall()

        I=0
        while I < len(lesenrs):
            code_pays=""
            sql="select \"CODE\" FROM \"PAYS\" WHERE \"PAYS\"='"+lesenrs[I]["pays"]+"'"
            self.curadresse.execute(sql)
            tpays = self.curadresse.fetchone()
#            print tpays
            if tpays!=None:
                code_pays="%s"%(self.nz(tpays["CODE"]))
            else:
                code_pays=""

            if code_pays=="FR":
                code_pays=""
            else:
                code_pays=code_pays.strip()

            sql = "select * from lot_numerisation where statut_reception='OK' and id_lot_numerisation="+str(lesenrs[I]["id_lot_numerisation"])
            self.curprod.execute(sql)
            tdatereception = self.curprod.fetchone()
            datereception=str(tdatereception["datereception"])
            lot_scan=tdatereception["lot_scan"]

            sql = "select * from fichesuiveuse_numerisation where rubrique='ID_SOUS_DOSSIER' and id_lot_numerisation="+str(lesenrs[I]["id_lot_numerisation"])
            self.curprod.execute(sql)
            toperation = self.curprod.fetchone()
            operation=toperation["valeur"]

            sql1 = "select * from fichesuiveuse_numerisation where rubrique='LOT_OPERATION' and id_lot_numerisation="+str(lesenrs[I]["id_lot_numerisation"])
            self.curprod.execute(sql1)
            toperation1 = self.curprod.fetchone()
            operation1=toperation1["valeur"]
            lot_courrier = operation1.split("_")[0]


            sql= "select count(*) as numero_lot from lot_numerisation inner join fichesuiveuse_numerisation"
            sql+=" on lot_numerisation.id_lot_numerisation=fichesuiveuse_numerisation.id_lot_numerisation"
            sql+=" where lot_scan <='" + lot_scan+"' and  lot_numerisation.idcommande_reception like 'SGC%' and datereception='"+datereception+"'::date and fichesuiveuse_numerisation.rubrique='ID_SOUS_DOSSIER' and fichesuiveuse_numerisation.valeur='"+operation+"'"
            self.curprod.execute(sql)
            tnumero_lot = self.curprod.fetchone()
            numero_lot=str(tnumero_lot["numero_lot"]).rjust(4,"0")

            #***************************************************************************************************************#
            idfichiercmd = self.nz(lesenrs[I]["n_lot"])
            lot_client = "%s"%(self.nz(self.DLookup("lot_client","fichier",self.sdsi,"idfichiercmd='%s'"%(idfichiercmd))))
            pos1=lot_client.find("_")
            if pos1==-1:
                #msg = "La structure du lot client du fichier %s est incorrecte (aucune _ : %s ).\n"%(idfichiercmd,lot_client)
                #self.errorDlg("Erreur de prepa",msg)
                #return
                lot_vivetic = lot_client
            else:
                lot_vivetic = lot_client[pos1+1:]
            index="%s_%s_%s_%s"%(operation,datereception.replace("-",""),lot_vivetic,lesenrs[I]["pli"])
            #***************************************************************************************************************#
            sql="update \"export\" set \"code_pays\"='"+code_pays+"',\"index_image\"='"+index+"',\"date_reception\"='"+datereception + "', \"lot_courrier\"='"+str(lot_courrier)+"', \"lot_operation\"='"+str(operation1)+"'  where \"n_enr\"='"+lesenrs[I]["n_enr"]+"'"
            self.local.commit()
            self.curlocal.execute(sql)
            self.local.commit()

            I+=1

        nbsrc = self.db.DCount(table="source",connexion=self.local)
        self.curlocal.execute("UPDATE controle SET etat='N'")

        sql="UPDATE"
        sql+=" export"
        sql+=" SET"
        sql+="  \"__s\"='R'"
        sql+=" WHERE "
        sql+="   (\"date_cachet_poste\"='' or \"date_cachet_poste\" IS NULL)"
        sql+="   OR (\"lot_courrier\"='' or \"lot_courrier\" IS NULL)"
        sql+="   OR ((\"nom\"='' or \"nom\" IS NULL) ) "
        sql+="   OR (\"cp\"='' or \"cp\" IS NULL)"
        sql+="   OR (\"ville\"='' or \"ville\" IS NULL)"
        sql+="   OR ((adr1='' or adr1 IS NULL) and (adr2='' or adr2 IS NULL) and (adr3='' or adr3 IS NULL))"

        self.curlocal.execute(sql)
        self.local.commit()
        #----------------adresse-------------------------
        self.curlocal.execute("select * from export order by n_lot, n_ima, n_enr")
        t_adr=self.curlocal.fetchall()

        for enr in t_adr:
            liste_adr=[]
            liste_adr.append(self.nz(enr["adr1"]))
            liste_adr.append(self.nz(enr["adr2"]))
            liste_adr.append(self.nz(enr["adr3"]))
            for y in range(2):
                for x in range(len(liste_adr)):
                    if x<len(liste_adr)-1 and liste_adr[x]=="":
                        liste_adr[x]=liste_adr[x+1]
                        liste_adr[x+1]=""

            self.curlocal.execute("update export set adr1='"+liste_adr[0]+"', adr2='"+liste_adr[1]+"', adr3='"+liste_adr[2]+"' where idenr="+str(enr["idenr"]))
            self.local.commit()
        #----------------------


        # ------------------------ màj pour les dates sogec----------------------
        vivetic_prestation_id=1396 #à définir
        self.curprod.execute("select libelle from vivetic_champs where vivetic_prestation_id="+str(vivetic_prestation_id)+ " and vivetic_type_id=30")
        t2=self.curprod.fetchall()
        sql2="UPDATE"
        sql2+=" export"
        sql2+=" SET"
        s=0
        for enr2 in t2:
            s=s+1
            if s==len(t2):
                sql2+=" \""+enr2[0]+"\"=replace(\""+enr2[0]+"\", '-', '/')"
            else:
                sql2+=" \""+enr2[0]+"\"=replace(\""+enr2[0]+"\", '-', '/'),"
        if len(t2)>0:
            self.curlocal.execute(sql2)
        # -------------------------------------------------------------------

        #-----------maj achat simultanee--------
        #sql3="UPDATE"
        #sql3+=" export"
        #sql3+=" SET"
        #sql3+=" \"achat_et_souscription_simultanes\"=(CASE WHEN \"presence_achat_tablette_galaxy_sur_facture_ou_tdc\"='1' and \"presence_forfait_bt_engagement_12mois\"='1' THEN '1' ELSE '0' END)"
        #self.curlocal.execute(sql3)
        #self.local.commit()
        #---------------------------------------

        #---------------indexation image--------------
        cDos = commande
        if(os.access("C:\USERS\\"+str(cDos)+"\\",os.F_OK)==True):
            shutil.rmtree("C:\USERS\\"+str(cDos)+"\\")

        os.makedirs("C:\USERS\\"+str(cDos)+"\\",777)
        REP = "C:/USERS/"+str(cDos)+"/"

        srvimage="//192.168.10.12/sogec/"

        self.nomcommande = self.commande.GetValue()
        operation="AG22"

        sql="select distinct \"lot_courrier\" from \"export\" order by \"lot_courrier\""
        self.curlocal.execute(sql)
        tlot_courrier=self.curlocal.fetchall()
        ilot=0

        while ilot < len(tlot_courrier):
            NUM_LOT_COURRIER="%s"%(self.nz(tlot_courrier[ilot]["lot_courrier"]))

            self.cursdsi.execute("select current_date as date, substr(localtime::varchar,1,8)::time as time")
            tdate = self.cursdsi.fetchone()
            dateNow=str(tdate[0])
            timereel=str(tdate[1])

            nomcsv=operation+"_02_" +dateNow.replace("-","")+timereel.replace(":","")+".csv"
            nomcsv_ano=operation+"_02_" +dateNow.replace("-","")+timereel.replace(":","")+"_Anomalie.csv"

            NUM_LOT_COURRIER=tlot_courrier[ilot]["lot_courrier"]

            if(os.access("C:\USERS\\"+str(cDos)+"\\"+tlot_courrier[ilot]["lot_courrier"]+"\\",os.F_OK)==False):
                os.makedirs("C:\USERS\\"+str(cDos)+"\\"+tlot_courrier[ilot]["lot_courrier"]+"\\",777)
            if(os.access("C:\USERS\\"+str(cDos)+"\\"+tlot_courrier[ilot]["lot_courrier"]+"\\anomalie\\",os.F_OK)==False):
                os.makedirs("C:\USERS\\"+str(cDos)+"\\"+tlot_courrier[ilot]["lot_courrier"]+"\\anomalie\\",777)

            if(os.access(srvimage+operation+"/"+ tlot_courrier[ilot]["lot_courrier"],os.F_OK)==False):
                os.makedirs(srvimage+operation+"/"+ tlot_courrier[ilot]["lot_courrier"],777)
            if(os.access(srvimage+operation+"/"+ tlot_courrier[ilot]["lot_courrier"]+"/anomalie",os.F_OK)==False):
                os.makedirs(srvimage+operation+"/"+ tlot_courrier[ilot]["lot_courrier"]+"/anomalie",777)

            sql="select * from \"export\" WHERE \"lot_courrier\"='%s' order by \"id_lot_numerisation\",\"pli\""%(tlot_courrier[ilot]["lot_courrier"])
            self.curlocal.execute(sql)
            tenrs=self.curlocal.fetchall()
            volume=len(tenrs)
            I=0
            dlg = self.dlgprogress(None,"Copie image %s"%(tlot_courrier[ilot]["lot_courrier"]),"",len(tenrs))
            while I < len(tenrs):
                sk,gn=dlg.Update(I,"Traitement %s sur %s enrgs..."%(I+1,len(tenrs)))
                if sk==False:
                    dlg.Destroy()
                    return

                sql = "select pathauto,idsousdossier from fichier where idfichiercmd='"+str(tenrs[I]["n_lot"])+"'"
#                print "sql:", sql
                self.cursdsi.execute(sql)
                tnumero_lot = self.cursdsi.fetchone()
                pathauto=tnumero_lot["pathauto"].replace("\\","/")
                tlist_ima=tenrs[I]["list_ima"].split(";")
                idfichiercmd=str(tenrs[I]["n_lot"])
                stype=str(tenrs[I]["__s"])

                im=0
                for n_ima in tlist_ima:

                    nomimage=tenrs[I]["index_image"]+"_"+ str(im+1).rjust(4,'0')+os.path.splitext(n_ima)[1]
                    if stype=='Q':
                        shutil.copy (pathauto+"/"+ n_ima,REP+NUM_LOT_COURRIER+"/"+tenrs[I]["index_image"]+"_"+ str(im+1).rjust(4,'0')+os.path.splitext(n_ima)[1])
                        shutil.copy (pathauto+"/"+ n_ima,srvimage+operation+"/"+NUM_LOT_COURRIER+"/"+tenrs[I]["index_image"]+"_"+ str(im+1).rjust(4,'0')+os.path.splitext(n_ima)[1])
#                        sql="INSERT INTO sgc_carton_livraison_fichiers(id_sgc_carton_livraison,idfichiercmd,fichier) values ('%s','%s','%s')"%(id_sgc_carton_livraison,idfichiercmd,nomimage)
                        #self.curprod.execute(sql)
                    else:
                        shutil.copy (pathauto+"/"+ n_ima,REP+NUM_LOT_COURRIER+"/anomalie/"+tenrs[I]["index_image"]+"_"+ str(im+1).rjust(4,'0')+os.path.splitext(n_ima)[1])
                        shutil.copy (pathauto+"/"+ n_ima,srvimage+operation+"/"+NUM_LOT_COURRIER+"/anomalie/"+tenrs[I]["index_image"]+"_"+ str(im+1).rjust(4,'0')+os.path.splitext(n_ima)[1])

                    im+=1
                I+=1
            dlg.Destroy()


            ilot+=1
        #---------------------------------------------

        tzetatcontrole=self.db.etatcontrole(self.local)
        self.affcontrole(tzetatcontrole,self.tzobjet)

        self.traitement.InfoDlg('Infos:','Extraction terminée \n'+'Nb enr: '+ str(nbsrc))



    def DLookup(self,champ,table,connexion,where=''):
        sql = "select \""+champ+"\" from \""+table+"\" "
        if where!='':
            sql+=" where "+ where
        curseur = connexion.cursor()
        curseur.execute(sql)
        tzRes = curseur.fetchone()
        if tzRes!=None:
            return tzRes[0]
        else:
            return None

    def dlgprogress(self,parent,stitle='',smessage='',max=100,):
        dlg = wx.ProgressDialog(stitle,smessage,maximum = max,parent=parent,style = wx.PD_CAN_ABORT| wx.PD_APP_MODAL| wx.PD_ESTIMATED_TIME| wx.PD_REMAINING_TIME)
        return dlg


    def nz(self,valeur_o,valeur_pardefaut=''):
        if valeur_o=='' or valeur_o==None:
            return valeur_pardefaut
        else:
            return valeur_o


    def copier(self,src,dst):
        """
            Methode de copie d'un fichier
        """
        if(os.access(src,os.F_OK)==False):
            self.errorDlg('Erreur image','Il n\'y a pas de fichier  dans le repertoire '+ src +' !')
            return False
        try:
            shutil.copy(src,dst)
        except Exception as inst:
            msgs = 'copie image:\n'
            msgs +=  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
            msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
            self.errorDlg('erreur',msgs)
            return False

        return True

    def nombrelots(self,event):
        # ---- table temporaire ----
        commande    = self.commande.GetLineText(0).upper()
        matricule   = self.matricule.GetLineText(0).upper()
        if commande=='' or matricule=='':
            return False
        lottemp = 'lot_prepare_'+str(int((random.random()*10000)))+'_'+str(int((random.random()*10000)))
        lotsaisietemp = 'lot_saisie_'+str(int((random.random()*10000)))+'_'+str(int((random.random()*10000)))

        # ---- table temporaire  q_qte_lot_prepare
        sqltemplot = "CREATE TEMP TABLE "+str(lottemp)+" (idfichiercmd character varying(50),qte_preparee character varying(100));"
        self.cursdsi.execute(sqltemplot)

        r = "SELECT fichierimage.idfichiercmd as idfichiercmd, Count(fichierimage.nomimage) AS qte_preparee FROM fichierimage "
        r += " WHERE (fichierimage.idcommande='"+str(commande)+"') GROUP BY fichierimage.idfichiercmd ORDER BY fichierimage.idfichiercmd;"
        self.cursdsi.execute(r)
        qtelot = self.cursdsi.fetchall()
        nlotprep = len(qtelot)
        I=0
        while(I<nlotprep):
            datacurr = qtelot[I]
            rinsert = "INSERT INTO "+str(lottemp)+"(idfichiercmd,qte_preparee)Values('"+str(datacurr['idfichiercmd'])+"','"+str(datacurr['qte_preparee'])+"')"
            self.cursdsi.execute(rinsert)
            I=I+1

        # ---- table temporaire  r_qte_lot_saisie
        sqltempsaisie = "CREATE TEMP TABLE "+str(lotsaisietemp)+" (N_LOT character varying(50),qte_type character varying(50));"
        self.cursdsi.execute(sqltempsaisie)

        sqllotsaisie = "SELECT \"n_lot\" as n_lot, Count(\"n_enr\") AS qte_type FROM \"source\" GROUP BY \"n_lot\"; "
        self.curlocal.execute(sqllotsaisie)
        qtesaisie = self.curlocal.fetchall()
        nbqte = len(qtesaisie)

        J=0
        while(J<nbqte):
            datasCurr = qtesaisie[J]
            rinsert = "INSERT INTO "+str(lotsaisietemp)+"(n_lot,qte_type)Values('"+str(datasCurr['n_lot'])+"','"+str(datasCurr['qte_type'])+"')"
            self.cursdsi.execute(rinsert)
            J=J+1
        self.cursdsi.execute("SELECT * FROM "+str(lotsaisietemp)+"")

        reqfin = "SELECT "+str(lottemp)+".idfichiercmd, "+str(lottemp)+".qte_preparee, "+str(lotsaisietemp)+".qte_type "
        reqfin += "FROM "+str(lottemp)+" INNER JOIN "+str(lotsaisietemp)+" ON "+str(lottemp)+".idfichiercmd = "+str(lotsaisietemp)+".n_lot"
        reqfin += " ORDER BY "+str(lottemp)+".idfichiercmd"


        self.cursdsi.execute(reqfin)
        resultats = self.cursdsi.fetchall()
        DialogBox(self,resultats,['IDFICHIERCMD','Qté_préparé','Qté_type'],3)

        # --- Cocher checkbutton
        if len(resultats)>0:
            self.curlocal.execute("UPDATE controle SET etat='O' where traitement='1'")
            self.local.commit()
            tzetatcontrole=self.db.etatcontrole(self.local)

            self.affcontrole(tzetatcontrole,self.tzobjet)

    def OnAbout(self):
        description = """
            Si vous avez un problème sur cet outil,
        merci d'envoyer un mail à l'adresse suivante:
                    harifetra_iam@vivetic.mg

                Cliquez sur [OK] pour quitter ;-)


        """

        licence = """This is not a free software; you can't redistribute
        it and/or modify it.

        In the hope that it will be useful,
        only a member of personnal in vivetic can use this program.
        """


        info = wx.AboutDialogInfo()

##        info.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG))
        info.SetName('AG22 [2017-January-Monday-16]')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2017 -  harifetra:9085')
        info.SetWebSite('SkypePseudo: haric0d3')
        info.SetLicence(licence)
        info.AddDeveloper('har1f3tra')
        info.AddDocWriter('haricod3r@gmail.com')
        info.AddArtist('HARIFETRA - INFO DEV - harifetra_iam@vivetic.mg')
        info.AddTranslator('haricod3r@gmail.com')

        wx.AboutBox(info)

    def onExit(self,e=None):
#        self.OnAbout()

        dlg = MyAboutBox(None)
        dlg.ShowModal()

        self.fenprincip.Close()

    def onClose(self,e=None):
        self.local.close()
        self.prod.close()
        self.sdsi.close()
#        self.OnAbout()
        dlg = MyAboutBox(None)
        dlg.ShowModal()
        dlg.Destroy()

        self.fenprincip.Destroy()



    def Nz(self,valeur_o,valeur_pardefaut=''):
        if valeur_o=='':
            return valeur_pardefaut
        else:
            return valeur_o

    def nz(self,valeur_o,valeur_pardefaut=''):
        if valeur_o=='' or valeur_o==None:
            return valeur_pardefaut
        else:
            return valeur_o


    def createcontrole(self):
        self.curlocal.execute("DROP TABLE IF EXISTS controle;")
        procedures  = open(self.path_controle,'r').read()
        self.curlocal.execute(procedures)


    def formatesLigne(self,iNombre):
        """ Formater un chiffre en format de 3 chiffre """
        if(iNombre<10):
            zFormt = '00000'+str(iNombre)
            return zFormt
        elif(iNombre<100):
            zFormt = '0000'+ str(iNombre)
            return zFormt
        elif(iNombre<1000):
            zFormt = '000'+ str(iNombre)
            return zFormt
        elif(iNombre<10000):
            zFormt = '00'+ str(iNombre)
            return zFormt

        else:
            return iNombre

    def qualite_dCQ(self,connexion):
        self.cur = connexion.cursor()
        req = "DROP TABLE IF EXISTS qualite_d;"
        req += "CREATE TABLE qualite_d (idexecute integer,idenr integer,nomimage character varying(255),"
        req+= "nomchamp character varying(50),ancvaleur text,nouvaleur text,idexecutec integer)"
        req += "WITH (OIDS=FALSE);ALTER TABLE qualite_d OWNER TO postgres;"
        self.cur.execute(req)


    def majqualite_formatage(self,idenr,idexecute,idexecutec,table="source"):
        self.curlocal.execute("DELETE  FROM qualite_d where idenr=" + str(idenr))
        sdern_idenr = self.db.DMax("idenr", table,self.local)

        tqua = []
        tvalqua = []
        cht1 = self.db.getNomChamps(table,self.local)
        chInterdit = ['n_ima','n_enr','id_commande','commande','etape','N_LOT', 'N_IMA','N_IMA1','N_ENR','ID_COMMANDE','COMMANDE','ETAPE','N_LOT','idenr','idexecute','MATRICULE','FILTRE_MAIL','X','Y','Z','idexecutec','date_saisie']
        J = 0
        while(J<len(cht1)):
            if(cht1[J] not in chInterdit and cht1[J][0:2]!='__'):
                #print 'verif1'
                if(self.db.DLookup(cht1[J],table+"_o",self.local, "idenr="+str(idenr))!='<?>'):
                    if(self.db.DLookup(cht1[J],table+"_o",self.local,"idenr="+str(idenr)) != self.db.DLookup(cht1[J],table,self.local,"idenr="+str(idenr))):
                        tqua.append("idexecute") ;tvalqua.append(idexecute)
                        if(self.Nz(idenr) == 0):
                            sdern_idenr = sdern_idenr + 1
                        tqua.append("idenr") ; tvalqua.append(self.Nz(idenr, sdern_idenr))
                        tqua.append("nomchamp");tvalqua.append(cht1[J])
                        tqua.append("ancvaleur"); tvalqua.append(self.db.DLookup(cht1[J], table+"_o",self.local, "idenr=" + str(idenr)))
                        tqua.append("nouvaleur"); tvalqua.append(self.db.DLookup(cht1[J], table,self.local, "idenr=" + str(idenr)))
                        tqua.append("nomimage") ; tvalqua.append(self.db.DLookup("N_IMA", table,self.local, "idenr=" + str(idenr)))
                        tqua.append("idexecutec") ; tvalqua.append(idexecutec)
                        self.db.insertion("qualite_d",tqua,tvalqua,self.local)
                        tvalqua = []
                        tqua = []
            J=J+1





    def consult_export(self,event):
        if(self.checklot.GetValue()==False):
            self.traitement.errorDlg('Erreur','Vous avez oublié l\'étape de controle standard ')
            return False
        self.nomcommande = self.commande.GetValue()
        frame = source.fenetre(None,table="export",db=self.dbname,wdgchecksta=self.checklot,idcom=self.idcom,nomcommande=self.nomcommande)
        frame.Show(True)
        self.curlocal.execute("UPDATE controle SET etat='O' where traitement='2'")
        self.local.commit()
        tzetatcontrole=self.db.etatcontrole(self.local)
        self.affcontrole(tzetatcontrole,self.tzobjet)

        app.MainLoop()

    def createrror(self):

        sql = "CREATE TABLE erreur(n_enr character varying(50),N_LOT character varying(50),champ text,error text)"
        sql+= "WITH (OIDS=FALSE);ALTER TABLE erreur OWNER TO postgres;"
        self.curlocal.execute(sql)


#    def createcsta(self):
#
#        """ Création table controle standard"""
#        self.curlocal.execute("DROP TABLE IF EXISTS \"CONTROLE_STANDARD\";")
#        procedures  = open(self.path_controle_sta,'r').read()
#        self.curlocal.execute(procedures)

    def createcsta(self,connexion):

        """
            Création table standard
            parametre : l'objet connexion d'acces vers la base
        """
        curs = connexion.cursor()
        procedures  = open(self.path_controlesta,'r').read()
        curs.execute(procedures)
        connexion.commit()

    def export2xlsMadcom(self,path):

        cDos = self.commande.GetValue()
        dateNow = date.today()
        ttitre = self.db.getNomChamps('export',self.local)
        self.curlocal.execute("SELECT * FROM export")
        tdata = self.curlocal.fetchall()
        tzfeuille=['EXPORT']
        tzdata=[tdata]
        tztitre=[ttitre]

        if self.doxls(tztitre,tzdata,path+cDos+'_sauvegarde_'+str(dateNow)+'.xls',tzfeuille)==False:
            return False
        return True

    def DCount(self,champ="*",table="",connexion=None,where=''):
        if where!='':
            if champ!="*":
                sql = "select count(\""+str(champ)+"\") from \""+str(table)+"\" where  "+where+" "
            else:
                sql = "select count(*) from \""+str(table)+"\" where  "+where+" "
        else:
            if champ!="*":
                sql = "select count(\""+str(champ)+"\") from \""+str(table)+"\" "
            else:
                sql = "select count(*) from \""+str(table)+"\"  "
        curseur = connexion.cursor()
        curseur.execute(sql)
        res = curseur.fetchone()
        return res[0]

    def exporter(self,event):
        """Methode exportation """
        commande    = self.commande.GetValue().upper()
        matricule   = self.matricule.GetValue().upper()

        #verification
        #self.curlocal.execute("select * from controle where traitement='3' and etat='O'")
        #statu = self.curlocal.fetchone()
        #if statu ==None:
        #    self.traitement.errorDlg('Erreur','Vous avez oublié l\'étape Vérification combinaison !')
        #    return

        #self.curlocal.execute("select * from controle where traitement='4' and etat='O'")
        #statu = self.curlocal.fetchone()
        #if statu ==None:
        #    self.traitement.errorDlg('Erreur','Vous avez oublié l\'étape Controle standard !')
        #    return

        idcom       = self.idcom
        if(commande=='' or matricule==''):
            return False

        cDos = commande
        #if(os.access("C:\USERS\\"+str(cDos)+"\\",os.F_OK)==True):
        #    shutil.rmtree("C:\USERS\\"+str(cDos)+"\\")

        #os.makedirs("C:\USERS\\"+str(cDos)+"\\",777)
        REP = "C:/USERS/"+str(cDos)+"/"

        srvimage="//192.168.10.12/sogec/"
        volume=self.db.DCount("export",self.local)

        if volume==0:
            self.traitement.InfoDlg("Exportation","Exportation déjà faite")
            return False

        self.nomcommande = self.commande.GetValue()
        operation="AG22"

        # todo controle standard
        self.curlocal.execute("DELETE from erreur")
        self.curlocal.execute("DROP TABLE IF EXISTS \"CONTROLE_STANDARD\"")
        self.createcsta(self.local)

        if(self.DCount('*','export',self.local)>0):
            self.service.controle_batch("export",bMsg=False,Bill=True,conn=self.local)
            if(self.DCount('*','erreur',self.local)>0):
                frame = source.fenetre(None,table="export",db="saisie",wdgchecksta=None,idcom=self.idcom,nomcommande=commande,where=" \"n_enr\" in (select distinct \"n_enr\" from erreur)")
                frame.Show(True)

                frame = source.fenetre(None,table="erreur",db="saisie",wdgchecksta=None,idcom=self.idcom,nomcommande=commande)
                frame.Show(True)
                return False
        # fin to do


        sql="select distinct \"lot_courrier\",lot_operation from \"export\" order by \"lot_courrier\""
        self.curlocal.execute(sql)
        tlot_courrier=self.curlocal.fetchall()
        ilot=0

        while ilot < len(tlot_courrier):
            NUM_LOT_COURRIER="%s"%(self.nz(tlot_courrier[ilot]["lot_courrier"]))
            N_LOT_OPERATION="%s"%(self.nz(tlot_courrier[ilot]["lot_operation"]))

            self.cursdsi.execute("select current_date as date, substr(localtime::varchar,1,8)::time as time")
            tdate = self.cursdsi.fetchone()
            dateNow=str(tdate[0])
            timereel=str(tdate[1])

            if len(str(N_LOT_OPERATION).split("_"))==2:
                nomcsv=operation+"_"+str(N_LOT_OPERATION)+"_" +dateNow.replace("-","")+timereel.replace(":","")+".csv"
                nomcsv_ano=operation+"_"+str(N_LOT_OPERATION)+"_" +dateNow.replace("-","")+timereel.replace(":","")+"_Anomalie.csv"
            else:
                nomcsv=operation+"_"+str(NUM_LOT_COURRIER)+"_" +str(NUM_LOT_COURRIER)+"_"+dateNow.replace("-","")+timereel.replace(":","")+".csv"
                nomcsv_ano=operation+"_"+str(NUM_LOT_COURRIER)+"_" +str(NUM_LOT_COURRIER)+"_"+dateNow.replace("-","")+timereel.replace(":","")+"_Anomalie.csv"

            sql="update \"export\" set \"nom_fichier_csv\"='"+str(nomcsv)+ "' where \"lot_courrier\"='"+str(NUM_LOT_COURRIER)+"'"
            self.curlocal.execute(sql)

            NUM_LOT_COURRIER=tlot_courrier[ilot]["lot_courrier"]

            if(os.access("C:\USERS\\"+str(cDos)+"\\"+tlot_courrier[ilot]["lot_courrier"]+"\\",os.F_OK)==False):
                os.makedirs("C:\USERS\\"+str(cDos)+"\\"+tlot_courrier[ilot]["lot_courrier"]+"\\",777)
            if(os.access("C:\USERS\\"+str(cDos)+"\\"+tlot_courrier[ilot]["lot_courrier"]+"\\anomalie\\",os.F_OK)==False):
                os.makedirs("C:\USERS\\"+str(cDos)+"\\"+tlot_courrier[ilot]["lot_courrier"]+"\\anomalie\\",777)

            if(os.access(srvimage+operation+"/"+ tlot_courrier[ilot]["lot_courrier"],os.F_OK)==False):
                os.makedirs(srvimage+operation+"/"+ tlot_courrier[ilot]["lot_courrier"],777)
            if(os.access(srvimage+operation+"/"+ tlot_courrier[ilot]["lot_courrier"]+"/anomalie",os.F_OK)==False):
                os.makedirs(srvimage+operation+"/"+ tlot_courrier[ilot]["lot_courrier"]+"/anomalie",777)

            # --------------------------+ POUR LES SANS ANOMALIES ----------


            sqlExport="SELECT "
            sqlExport+= "\"lot_courrier\","
            sqlExport+= "\"id_web\","
            sqlExport+= "\"matr_operateur\","
            sqlExport+= "\"num_sequence\","

            sqlExport+= "\"date_cachet_poste\","
            sqlExport+= "\"civilite\","
            sqlExport+= "\"nom\","
            sqlExport+= "\"prenom\","
            sqlExport+= "\"adr1\","
            sqlExport+= "\"adr2\","
            sqlExport+= "\"adr3\","
            sqlExport+= "\"adr4\","
            sqlExport+= "\"cp\","
            sqlExport+= "\"ville\","
            sqlExport+= "\"code_pays\","
            sqlExport+= "\"email\","
            sqlExport+= "\"mobile\","
            sqlExport+= "\"remboursement_timbre\","
            sqlExport+= "\"presence_facture_ou_tc\","
            sqlExport+= "\"presence_enseigne\","
            sqlExport+= "\"saisie_code_point_de_vente\","
            sqlExport+= "\"date_sur_ticket_de_caisse\","
            sqlExport+= "\"presence_achat_mobile\","
            sqlExport+= "\"presence_achat_accessoire\","
            sqlExport+= "\"achat_simultane\","
            sqlExport+= "\"montant_ttc_accessoire\","
            sqlExport+= "\"montant_ht_accessoire\","
            sqlExport+= "\"presence_contrat_de_souscription\","
            sqlExport+= "\"presence_forfait\","
            sqlExport+= "\"iban\","
            sqlExport+= "\"bic\","
            sqlExport+= "\"presence_code_barre_accessoire\","
            sqlExport+= "\"original_code_barre_accessoire\","
            sqlExport+= "\"saisie_code_barre_accessoire\","
            sqlExport+= "\"presence_code_barre_mobile\","
            sqlExport+= "\"saisie_code_barre_mobile\","
            sqlExport+= "\"presence_bulletin\","
            sqlExport+= "\"j_accepte_de_recevoir\","

            sqlExport+= "'C',"
            sqlExport+= "\"codage_facture\","
            sqlExport+= "\"codage_forfait\","


            sqlExport+= "\"cnil\","
            sqlExport+= "\"index_image\","
            sqlExport+= "\"doublon\""




            sqlExport+=" FROM \"export\""
            sqlExport+=" WHERE \"__s\"='Q' AND \"lot_courrier\"='"+NUM_LOT_COURRIER+"' ORDER BY \"id_lot_numerisation\", \"pli\""
            self.curlocal.execute(sqlExport)
            tdata1 = self.curlocal.fetchall()

            # titre
            ttitre1 = ["N° Lot Courrier","Identifiant WEB","Matricule opératrice","Numéro de séquence","Date cachet de la poste","Civilité","Nom ou Raison sociale","Prénom","Adresse 1","Adresse 2","Adresse 3","Adresse 4","Code postal","Ville","Code ISO Pays","Email","Numéro du mobile","CNIL","Identifiant du compte IBAN","Identifiant de la banque BIC","Remboursement du timbre","Présence bulletin promotionnel","Présence copie contrat de souscription  BT ou avenant renouvellement","Présence forfait Bouygues Telecom engagement 12 mois minimum","Date de souscription","Présence facture d'achat ou ticket de caisse ou email de confirmation commande","Présence enseigne Bouygues Telecom sur facture, TC ou email confirmation","Code point de vente","Présence achat tablette Galaxy Tab 3 4G 8 sur factue ou TC ou email confirmation","Achat et souscription simultanés","Date d'achat sur facture ou TC ou email confirmation","Prix TTC tablette","Prix HT Tablette","Présence code à barres de la tablette","Original code à barres de la tablette","Saisie code à barres","Codage forfait","Codage facture","Canal d'achat","Forçage doublon","Index image"]
#            ttitre1 = ["N° Lot Courrier","Identifiant WEB","Matricule opératrice","N° séquence","Date cachet de la poste","Civilité","Nom ou Raison sociale","Prénom","Adresse 1","Adresse 2","Adresse 3","Adresse 4","Code postal","Ville","Code ISO Pays","Téléphone","Numéro du mobile","Email","CNIL","Est-ce un professionnel ?","Numéro de siren","Présence copie contrat service","Présence forfait Bouygues Telecom","Date de souscription","Portabilité numéro de mobile","Photocopie de l une des trois dernières factures du précédent opérateur","La facture précédent opérateur est-elle émise après le 22/01/2014","Codage forfait","Codage contrat","Canal achat","Forçage doublon","Index image"]

            if self.docsv(ttitre1,tdata1,REP+NUM_LOT_COURRIER+"/"+nomcsv)==False:
                return False

#            print "fiiin";return
            shutil.copy (REP+NUM_LOT_COURRIER+"/"+nomcsv,srvimage+operation+"/"+NUM_LOT_COURRIER+"/"+nomcsv)


            # --------------------------+ POUR LES ANOMALIES ---------------
#            sql="INSERT INTO sgc_carton_livraison_fichiers(id_sgc_carton_livraison,idfichiercmd,fichier) values ('%s','%s','%s')"%(id_sgc_carton_livraison,idfichiercmd,nomcsv)
            #self.curprod.execute(sql)

            sqlExport="SELECT "
            sqlExport+= "\"lot_courrier\","
            sqlExport+= "\"id_web\","
            sqlExport+= "\"matr_operateur\","
            sqlExport+= "\"num_sequence\","

            sqlExport+= "\"date_cachet_poste\","
            sqlExport+= "\"civilite\","
            sqlExport+= "\"nom\","
            sqlExport+= "\"prenom\","
            sqlExport+= "\"adr1\","
            sqlExport+= "\"adr2\","
            sqlExport+= "\"adr3\","
            sqlExport+= "\"adr4\","
            sqlExport+= "\"cp\","
            sqlExport+= "\"ville\","
            sqlExport+= "\"code_pays\","
            sqlExport+= "\"email\","
            sqlExport+= "\"mobile\","
            sqlExport+= "\"remboursement_timbre\","
            sqlExport+= "\"presence_facture_ou_tc\","
            sqlExport+= "\"presence_enseigne\","
            sqlExport+= "\"saisie_code_point_de_vente\","
            sqlExport+= "\"date_sur_ticket_de_caisse\","
            sqlExport+= "\"presence_achat_mobile\","
            sqlExport+= "\"presence_achat_accessoire\","
            sqlExport+= "\"achat_simultane\","
            sqlExport+= "\"montant_ttc_accessoire\","
            sqlExport+= "\"montant_ht_accessoire\","
            sqlExport+= "\"presence_contrat_de_souscription\","
            sqlExport+= "\"presence_forfait\","
            sqlExport+= "\"iban\","
            sqlExport+= "\"bic\","
            sqlExport+= "\"presence_code_barre_accessoire\","
            sqlExport+= "\"original_code_barre_accessoire\","
            sqlExport+= "\"saisie_code_barre_accessoire\","
            sqlExport+= "\"presence_code_barre_mobile\","
            sqlExport+= "\"saisie_code_barre_mobile\","
            sqlExport+= "\"presence_bulletin\","
            sqlExport+= "\"j_accepte_de_recevoir\","

            sqlExport+= "'C',"
            sqlExport+= "\"codage_facture\","
            sqlExport+= "\"codage_forfait\","


            sqlExport+= "\"cnil\","
            sqlExport+= "\"index_image\","
            sqlExport+= "\"doublon\""




            sqlExport+=" FROM \"export\""


            sqlExport+=" WHERE \"__s\"='R' AND \"lot_courrier\"='"+NUM_LOT_COURRIER+"' ORDER BY \"id_lot_numerisation\", \"pli\""
            self.curlocal.execute(sqlExport)
            tdata1 = self.curlocal.fetchall()

            if self.docsv(ttitre1,tdata1,REP+NUM_LOT_COURRIER+"/anomalie/"+nomcsv_ano)==False:
                return False
            shutil.copy (REP+NUM_LOT_COURRIER+"/anomalie/"+nomcsv_ano,srvimage+operation+"/"+NUM_LOT_COURRIER+"/anomalie/"+nomcsv_ano)
            ilot+=1

        #Exportation madcom
        if self.export2xlsMadcom(REP)==False:
            return False



        if self.ajoutformatage()==False:
            return False

#        print "FIN"
#        return
        #------------ pour test -----------------------

        if self.majexecute()==False:
            return False
        if self.majpousse()==False:
            return False

        self.curlocal.execute("delete from source")
        self.curlocal.execute("delete from source_o")
        self.curlocal.execute("delete from export")

        self.prod.commit()
        self.sdsi.commit()
        self.local.commit()

        self.sdsi.set_isolation_level(0)
        self.prod.set_isolation_level(0)
        self.local.set_isolation_level(0)

        self.traitement.InfoDlg("EXPORTATION","Exportation terminée dans\n"+str(REP+"")+"\n Avec nombre d\'enregistrements : "+ str(volume))

    def errorDlg(self,title,message):
        """
            Message d'erreur
        """
        msg = wx.MessageDialog ( None, message, caption=title,style=wx.ICON_ERROR , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg

    def controle_standard(self,event):

#        xComm = self.commande
#        xMat  = self.matricule
#        commande = xComm.GetValue()
#        matricule = xMat.GetValue()
#
#
#        if commande=='':
#            xComm.SetFocus()
#            return False
#        if matricule=='':
#            xMat.SetFocus()
#            return False
       # self.curlocal.execute("select * from controle where etat='O' and traitement='3'")
#        tstatu  = self.curlocal.fetchone()
#        if tstatu==None:
#            self.errorDlg("Erreur","Etape vérification combinaison non finie!")
#            return
#        self.createrror()
        self.curlocal.execute("DELETE from erreur")
        self.curlocal.execute("DROP TABLE IF EXISTS \"CONTROLE_STANDARD\"")
        self.createcsta(self.local)
        #self.curlocal.execute("UPDATE controle set \"etat\"='N' where traitement='4' ")
        if(self.DCount('*','export',self.local)>0):
            self.service.controle_batch("export",bMsg=False,Bill=True,conn=self.local)
            if(self.DCount('*','erreur',self.local)>0):
                frame = source.fenetre(None,table="export",db="saisie",wdgchecksta=None,idcom=self.idcom,nomcommande=commande,where=" \"n_enr\" in (select distinct \"n_enr\" from erreur)")
                frame.Show(True)

                frame = source.fenetre(None,table="erreur",db="saisie",wdgchecksta=None,idcom=self.idcom,nomcommande=commande)
                frame.Show(True)

            else:
                self.curlocal.execute("UPDATE controle set \"etat\"='O' where traitement='4' ")
                self.InfoDlg('Contrôle standard','Tout est OK.')

        else:
            self.errorDlg('Contrôle standard','Aucun enregistrement à traiter')

        tzetatcontrole=self.db.etatcontrole(self.local)
        self.affcontrole(tzetatcontrole,self.tzobjet)


    def veriCombinaison(self,ligne):
        nenr = self.nz(ligne["n_enr"])
        nlot = self.nz(ligne["n_lot"])
#TO DO idpresta
        vivetic_prestation_id=1396
        # ----+ LES CHAMPS OBLIGATOIRES +------
        self.curprod .execute("select libelle from vivetic_champs where vivetic_prestation_id="+str(vivetic_prestation_id)+ " and obligatoire=1")
        t=self.curprod.fetchall()
        for enr in t:
            if self.nz(ligne[enr[0]]).strip()=="":
                msg = "Champ vide "+str(enr[0])+"  "
                champ = str(enr[0])
                self.writeError(nenr,champ,msg,self.local,nlot)
        #---------------------------------------

        # ---------------+ les INTERDEPENDANCES cas impossible+---------------------------

        identifiant_compte_iban= self.nz(ligne["identifiant_compte_iban"]).strip()
        identifiant_compte_bic= self.nz(ligne["identifiant_compte_bic"]).strip()
        presence_contrat_souscription_bt_ou_avenant= self.nz(ligne["presence_contrat_souscription_bt_ou_avenant"]).strip()
        presence_forfait_bt_engagement_12mois= self.nz(ligne["presence_forfait_bt_engagement_12mois"]).strip()
        date_de_souscription= self.nz(ligne["date_de_souscription"]).strip()
        presence_facture_ou_tdc= self.nz(ligne["presence_facture_ou_tdc"]).strip()
        presence_enseigne_bouygues_tel_big_ben_facture= self.nz(ligne["presence_enseigne_bouygues_tel_big_ben_facture"]).strip()
        presence_achat_tablette_galaxy_sur_facture_ou_tdc= self.nz(ligne["presence_achat_tablette_galaxy_sur_facture_ou_tdc"]).strip()
        code_point_de_vente= self.nz(ligne["code_point_de_vente"]).strip()
        date_achat_sur_facture_tdc_ou_email= self.nz(ligne["date_achat_sur_facture_tdc_ou_email"]).strip()
        prix_ttc_tablette= self.nz(ligne["prix_ttc_tablette"]).strip()
        prix_ht_tablette= self.nz(ligne["prix_ht_tablette"]).strip()
        presence_code_barre_tablette= self.nz(ligne["presence_code_barre_tablette"]).strip()
        original_code_barre_tablette= self.nz(ligne["original_code_barre_tablette"]).strip()
        saisie_code_barre_tablette= self.nz(ligne["saisie_code_barre_tablette"]).strip()
        achat_et_souscription_simultanes= self.nz(ligne["achat_et_souscription_simultanes"]).strip()

        if identifiant_compte_iban!="" and identifiant_compte_bic=="":
        	msg = "identifiant_compte_iban (%s), identifiant_compte_bic (%s)"%(identifiant_compte_iban,identifiant_compte_bic)
        	champ = "identifiant_compte_iban,identifiant_compte_bic"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if identifiant_compte_iban=="" and identifiant_compte_bic!="":
        	msg = "identifiant_compte_iban (%s), identifiant_compte_bic (%s)"%(identifiant_compte_iban,identifiant_compte_bic)
        	champ = "identifiant_compte_iban,identifiant_compte_bic"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False


        if presence_contrat_souscription_bt_ou_avenant=="0" and presence_forfait_bt_engagement_12mois=="1" and date_de_souscription!="":
        	msg = "presence_contrat_souscription_bt_ou_avenant (%s), presence_forfait_bt_engagement_12mois (%s), date_de_souscription (%s)"%(presence_contrat_souscription_bt_ou_avenant,presence_forfait_bt_engagement_12mois,date_de_souscription)
        	champ = "presence_contrat_souscription_bt_ou_avenant,presence_forfait_bt_engagement_12mois,date_de_souscription"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_contrat_souscription_bt_ou_avenant=="0" and presence_forfait_bt_engagement_12mois=="0" and date_de_souscription!="":
        	msg = "presence_contrat_souscription_bt_ou_avenant (%s), presence_forfait_bt_engagement_12mois (%s), date_de_souscription (%s)"%(presence_contrat_souscription_bt_ou_avenant,presence_forfait_bt_engagement_12mois,date_de_souscription)
        	champ = "presence_contrat_souscription_bt_ou_avenant,presence_forfait_bt_engagement_12mois,date_de_souscription"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False


        if presence_facture_ou_tdc=="0" and presence_enseigne_bouygues_tel_big_ben_facture=="1" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="1" and code_point_de_vente!="" and date_achat_sur_facture_tdc_ou_email!="":
        	msg = "presence_facture_ou_tdc (%s), presence_enseigne_bouygues_tel_big_ben_facture (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), code_point_de_vente (%s), date_achat_sur_facture_tdc_ou_email (%s)"%(presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email)
        	champ = "presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_facture_ou_tdc=="0" and presence_enseigne_bouygues_tel_big_ben_facture=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="1" and code_point_de_vente!="" and date_achat_sur_facture_tdc_ou_email!="":
        	msg = "presence_facture_ou_tdc (%s), presence_enseigne_bouygues_tel_big_ben_facture (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), code_point_de_vente (%s), date_achat_sur_facture_tdc_ou_email (%s)"%(presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email)
        	champ = "presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_facture_ou_tdc=="0" and presence_enseigne_bouygues_tel_big_ben_facture=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="1" and code_point_de_vente=="" and date_achat_sur_facture_tdc_ou_email=="":
        	msg = "presence_facture_ou_tdc (%s), presence_enseigne_bouygues_tel_big_ben_facture (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), code_point_de_vente (%s), date_achat_sur_facture_tdc_ou_email (%s)"%(presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email)
        	champ = "presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_facture_ou_tdc=="0" and presence_enseigne_bouygues_tel_big_ben_facture=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="0" and code_point_de_vente!="" and date_achat_sur_facture_tdc_ou_email!="":
        	msg = "presence_facture_ou_tdc (%s), presence_enseigne_bouygues_tel_big_ben_facture (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), code_point_de_vente (%s), date_achat_sur_facture_tdc_ou_email (%s)"%(presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email)
        	champ = "presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_facture_ou_tdc=="1" and presence_enseigne_bouygues_tel_big_ben_facture=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="0" and code_point_de_vente!="" and date_achat_sur_facture_tdc_ou_email!="":
        	msg = "presence_facture_ou_tdc (%s), presence_enseigne_bouygues_tel_big_ben_facture (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), code_point_de_vente (%s), date_achat_sur_facture_tdc_ou_email (%s)"%(presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email)
        	champ = "presence_facture_ou_tdc,presence_enseigne_bouygues_tel_big_ben_facture,presence_achat_tablette_galaxy_sur_facture_ou_tdc,code_point_de_vente,date_achat_sur_facture_tdc_ou_email"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False


        if presence_facture_ou_tdc=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="1" and date_achat_sur_facture_tdc_ou_email!="" and prix_ttc_tablette!="" and prix_ht_tablette!="":
        	msg = "presence_facture_ou_tdc (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), date_achat_sur_facture_tdc_ou_email (%s), prix_ttc_tablette (%s), prix_ht_tablette (%s)"%(presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette)
        	champ = "presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_facture_ou_tdc=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="0" and date_achat_sur_facture_tdc_ou_email!="" and prix_ttc_tablette!="" and prix_ht_tablette!="":
        	msg = "presence_facture_ou_tdc (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), date_achat_sur_facture_tdc_ou_email (%s), prix_ttc_tablette (%s), prix_ht_tablette (%s)"%(presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette)
        	champ = "presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_facture_ou_tdc=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="0" and date_achat_sur_facture_tdc_ou_email=="" and prix_ttc_tablette!="" and prix_ht_tablette!="":
        	msg = "presence_facture_ou_tdc (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), date_achat_sur_facture_tdc_ou_email (%s), prix_ttc_tablette (%s), prix_ht_tablette (%s)"%(presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette)
        	champ = "presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_facture_ou_tdc=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="0" and date_achat_sur_facture_tdc_ou_email=="" and prix_ttc_tablette=="" and prix_ht_tablette!="":
        	msg = "presence_facture_ou_tdc (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), date_achat_sur_facture_tdc_ou_email (%s), prix_ttc_tablette (%s), prix_ht_tablette (%s)"%(presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette)
        	champ = "presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_facture_ou_tdc=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="0" and date_achat_sur_facture_tdc_ou_email!="" and prix_ttc_tablette!="" and prix_ht_tablette=="":
        	msg = "presence_facture_ou_tdc (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), date_achat_sur_facture_tdc_ou_email (%s), prix_ttc_tablette (%s), prix_ht_tablette (%s)"%(presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette)
        	champ = "presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_facture_ou_tdc=="0" and presence_achat_tablette_galaxy_sur_facture_ou_tdc=="0" and date_achat_sur_facture_tdc_ou_email!="" and prix_ttc_tablette==" vide" and prix_ht_tablette!="":
        	msg = "presence_facture_ou_tdc (%s), presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), date_achat_sur_facture_tdc_ou_email (%s), prix_ttc_tablette (%s), prix_ht_tablette (%s)"%(presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette)
        	champ = "presence_facture_ou_tdc,presence_achat_tablette_galaxy_sur_facture_ou_tdc,date_achat_sur_facture_tdc_ou_email,prix_ttc_tablette,prix_ht_tablette"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False


        if presence_code_barre_tablette=="1" and original_code_barre_tablette=="0" and saisie_code_barre_tablette!="":
        	msg = "presence_code_barre_tablette (%s), original_code_barre_tablette (%s), saisie_code_barre_tablette (%s)"%(presence_code_barre_tablette,original_code_barre_tablette,saisie_code_barre_tablette)
        	champ = "presence_code_barre_tablette,original_code_barre_tablette,saisie_code_barre_tablette"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_code_barre_tablette=="0" and original_code_barre_tablette=="1" and saisie_code_barre_tablette!="":
        	msg = "presence_code_barre_tablette (%s), original_code_barre_tablette (%s), saisie_code_barre_tablette (%s)"%(presence_code_barre_tablette,original_code_barre_tablette,saisie_code_barre_tablette)
        	champ = "presence_code_barre_tablette,original_code_barre_tablette,saisie_code_barre_tablette"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_code_barre_tablette=="0" and original_code_barre_tablette=="0" and saisie_code_barre_tablette!="":
        	msg = "presence_code_barre_tablette (%s), original_code_barre_tablette (%s), saisie_code_barre_tablette (%s)"%(presence_code_barre_tablette,original_code_barre_tablette,saisie_code_barre_tablette)
        	champ = "presence_code_barre_tablette,original_code_barre_tablette,saisie_code_barre_tablette"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False


        if presence_achat_tablette_galaxy_sur_facture_ou_tdc=="1" and presence_forfait_bt_engagement_12mois=="0" and achat_et_souscription_simultanes=="1":
        	msg = "presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), presence_forfait_bt_engagement_12mois (%s), achat_et_souscription_simultanes (%s)"%(presence_achat_tablette_galaxy_sur_facture_ou_tdc,presence_forfait_bt_engagement_12mois,achat_et_souscription_simultanes)
        	champ = "presence_achat_tablette_galaxy_sur_facture_ou_tdc,presence_forfait_bt_engagement_12mois,achat_et_souscription_simultanes"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False
        if presence_achat_tablette_galaxy_sur_facture_ou_tdc=="0" and presence_forfait_bt_engagement_12mois=="1" and achat_et_souscription_simultanes=="1":
        	msg = "presence_achat_tablette_galaxy_sur_facture_ou_tdc (%s), presence_forfait_bt_engagement_12mois (%s), achat_et_souscription_simultanes (%s)"%(presence_achat_tablette_galaxy_sur_facture_ou_tdc,presence_forfait_bt_engagement_12mois,achat_et_souscription_simultanes)
        	champ = "presence_achat_tablette_galaxy_sur_facture_ou_tdc,presence_forfait_bt_engagement_12mois,achat_et_souscription_simultanes"
        	self.writeError(nenr,champ,msg,self.local,nlot)
        	return False








    def writeError(self,nenr , Chp, msg,conn,nlot):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #print "SELECT * FROM erreur WHERE n_enr='"+nenr+"' and n_lot='"+str(nlot)+"'"
        cur.execute("SET CLIENT_ENCODING='WIN1252';SELECT * FROM erreur WHERE n_enr='"+nenr+"' and n_lot='"+str(nlot)+"'")
        t = cur.fetchone()
        #print Chp
        if(t==None):
            cur.execute("SET CLIENT_ENCODING='WIN1252';INSERT INTO erreur(n_enr,n_lot,champ,error) VALUES('"+str(nenr)+"','"+str(nlot)+"','"+str(Chp)+"','"+str(self.removeAccent(msg))+"')")
        else:
            if(t['champ'].find(Chp)==-1):
                newChamp = t['champ']+'-'+ Chp
                newError = t['error']+'-'+ msg
                cur.execute("SET CLIENT_ENCODING='WIN1252';UPDATE erreur SET champ='"+newChamp+"',error='"+str(self.removeAccent(newError)).replace("'","''")+"'  where n_enr='"+str(nenr)+"' and n_lot='"+str(nlot)+"'")
            else:
                newError = t['error']+'/'+ msg
                cur.execute("SET CLIENT_ENCODING='WIN1252';UPDATE erreur SET error='"+str(self.removeAccent(newError)).replace("'","''")+"'  where n_enr='"+str(nenr)+"' and n_lot='"+str(nlot)+"'")

    def removeAccent(self,chaine,is2Maj=False):
        """ Cette fonction enleve les accents dans une chaine"""
        a=chaine
        a=a.replace("é","e")
        a=a.replace("è","e")
        a=a.replace("ê","e")
        a=a.replace("ë","e")

        a=a.replace("â","a")
        a=a.replace("à","a")
        a=a.replace("ä","a")

        a=a.replace("ü","u")
        a=a.replace("û","u")
        a=a.replace("ù","u")

        a=a.replace("ï","i")
        a=a.replace("î","i")
        a=a.replace("ö","o")
        a=a.replace("ô","o")
        a=a.replace("ç","c")


        a=a.replace("¨","")
        a=a.replace("^","")



        a=a.replace("Ë","E")
        a=a.replace("É","E")
        a=a.replace("Ê","E")
        a=a.replace("È","E")
        a=a.replace("Ä","A")
        a=a.replace("À","A")
        a=a.replace("Â","A")
        a=a.replace("Ü","U")
        a=a.replace("Ù","U")
        a=a.replace("Û","U")
        a=a.replace("Ï","I")
        a=a.replace("Î","I")
        a=a.replace("ÖÔÇ","O")
        a=a.replace("ÖÔÇ","O")
        a=a.replace("ÖÔÇ","C")
        a=a.replace("È","E")
        a=a.replace("&","&")
        if is2Maj==True:
            a=a.upper()
        return a

    def verifierInterdep(self,event):
        xComm = self.commande
        xMat  = self.matricule
        commande = xComm.GetValue()
        matricule = xMat.GetValue()

        if commande=='':
            xComm.SetFocus()
            return False
        if matricule=='':
            xMat.SetFocus()
            return False

        if self.checkcons_export.GetValue()==False:
            self.errorDlg("Erreur","La table export n'est pas encore consultée!")
            return

        try:
            local     = psycopg2.connect("dbname="+self.dbname+" user=postgres password=123456 host=localhost") #local
            local.set_isolation_level(0)
            local.set_client_encoding('WIN1252')
            curlocal  = local.cursor(cursor_factory=psycopg2.extras.DictCursor)
            curlocal.execute("DROP TABLE IF EXISTS erreur")
            local.commit()
        except BaseException:
                self.errorDlg('Connexion!','Probleme sur la connexion au serveur de base des données!')
                return False

        curlocal.execute(" update controle set etat='N' where traitement='3'")
        local.commit()
        self.createrror()
        self.local.commit()
        curlocal.execute("DELETE from erreur")
        local.commit()
        if(self.DCount('*','export',connexion=local)>0):
            curlocal.execute("select * from export order by \"n_enr\" ")
            t = curlocal.fetchall()
            dlg = self.dlgprogress(None,"Vérification combinaison","",len(t))
            k=0
            for ligne in t:
                sk,gn = dlg.Update(k,"Verification enr %s sur %s"%(k+1,len(t)))
                if sk==False:
                    dlg.Destroy()
                    return
                self.veriCombinaison(ligne)
                k=k+1
            dlg.Destroy()
            if(self.db.DCount(table='erreur',connexion=local)>0):
                formexport = error.fenetre(None,table="export",db=self.dbname,bErr=False)
                formexport.Show(True)
                formerr = error.fenetre(None,table="erreur",db=self.dbname)
                formerr.Show(True)
            else:
                self.curlocal.execute("UPDATE controle SET etat='O' where traitement='3'")
                self.local.commit()
                self.InfoDlg('Contrôle standard','Tout est OK.')
            tzetatcontrole=self.db.etatcontrole(self.local)
            self.affcontrole(tzetatcontrole,self.tzobjet)
        else:
            self.errorDlg('Contrôle standard','Aucun enregistrement à traiter')

    def InfoDlg(self,title,message):
        """
            Message d'infos
        """

        msg = wx.MessageDialog ( None, message, caption=title,style=wx.OK , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg

    def docsv(self,tzTitre,tzDatas,path,delimiter=';'): #from OES : by farinoire
        tGen = []
        I=0
        while(I<len(tzDatas)):
            tGen.append(tzDatas[I])
            I=I+1
        try:
            w_file=open((path), 'wb')
            c = csv.writer(w_file, delimiter=delimiter)
            for liste in tGen:
                c.writerow(liste)

        except Exception as inst:
            msgs =  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
            msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
            self.traitement.errorDlg('erreur',msgs)
            return False
        w_file.close()
        return True

    def doxls(self,tzTitre,tzDatas,path,tzfeuille):
        wb = xlwt.Workbook(encoding='cp1252')
        nbfeille=1
        F=0
        while (F<nbfeille):
            ws = wb.add_sheet("Livraison")
            I=0
            while (I<len(tzTitre[F])):
                ws.write(0, I, tzTitre[F][I])
                I=I+1
            K=0
            dlg = self.dlgprogress(None,"Génération excel","Veuillez patienter..."+str(len(tzDatas[F]))+" enregistrement(s)!",max=len(tzDatas[F]))
            for tzDataLigne  in tzDatas[F]:
                dlg.Update(K)
                L=0
                for zCell in tzDataLigne:
                    try:
                        ws.write(K+1, L, (zCell))
                    except Exception as inst:
                        msgs =  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
                        msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
                        self.traitement.errorDlg('erreur',msgs)
                        return False
                    L=L+1
                K=K+1
            dlg.Destroy()
            F=F+1
        try:
            wb.save(path)
        except Exception as inst:
                msgs =  'Erreur d\'ecriture xls(un fichier de même nom peut être en cours d\'utilisation!):\n'     # the exception instance
                msgs+=  ''+str(inst)+'\n'           # __str__ allows args to printed directly
                self.traitement.errorDlg('erreur',msgs)
                return False
        return True


    def dlgprogress(self,parent,stitle='',smessage='',max=100,):
        dlg = wx.ProgressDialog(stitle,smessage,maximum = max,parent=parent,style = wx.PD_CAN_ABORT| wx.PD_APP_MODAL| wx.PD_ESTIMATED_TIME| wx.PD_REMAINING_TIME)
        return dlg



    def ajoutformatage(self):
        try:

            self.curlocal.execute("SELECT DISTINCT \"n_lot\" FROM export")
            t = self.curlocal.fetchall()
            J=0

            while(J<len(t)):
                self.curprod.execute("delete from \""+self.idcom+"_q\" where \"n_lot\"='" + t[J]["n_lot"] + "'")
                self.curprod.execute("delete from \""+self.idcom+"_r\" where \"n_lot\"='" + t[J]["n_lot"] + "'")
                J=J+1

            #-------------
            tc = self.db.getChamps('export',self.local)
            tcN = [];tzVal = []
            count = 0
            while(count<len(tc)):
                if tc[count][0]!="idenr":
                    tcN.append(tc[count][0])
                count = count+1
            requette = "SELECT "
            count = 0
            while(count<len(tcN)):
                if(count == len(tcN)-1):
                    requette+=" \""+str(tcN[count])+"\""
                else:
                    requette+= "\""+str(tcN[count])+"\","
                count = count+1
            requette+= "  FROM export order by \"n_enr\""
            self.curlocal.execute(requette)
            tenreg = self.curlocal.fetchall()
            NbEnrg = len(tenreg)
            j = 0;tzChamp = []
            while(j<len(tenreg)):
                cnt = 0
                while(cnt<len(tenreg[j])):
                    if(tenreg[j][cnt]!= None):
                        tzVal.append(tenreg[j][cnt])
                        tzChamp.append(tcN[cnt])
                    cnt=cnt+1
                self.db.insertion(self.idcom+"_q",tzChamp,tzVal,self.prod)

                self.db.insertion(self.idcom+"_r",tzChamp,tzVal,self.prod)

                tzChamp=[]
                tzVal = []
                j =j+1

        except Exception as inst:
            msgs =  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
            msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
            self.traitement.errorDlg('erreur',msgs)
            return False

        return True

    def majpousse(self):
        """Mis à jour pousse """
        try:
            self.curlocal.execute("SELECT DISTINCT \"n_lot\" FROM export")
            datas = self.curlocal.fetchall()
            I=0
            while(I<len(datas)):
                self.sdsi.commit()
                self.cursdsi.execute("update pousse set flagfinpousse='1',flagrejetpousse='0',flagencours='0', matricule=" +str(self.matricule.GetValue())+ " where idfichiercmd='" +str(datas[I]["n_lot"])+ "' and idetape='ASSEMBLAGE/UNIFORMISATION'")
                self.sdsi.commit()
                I=I+1
        except Exception as inst:
            msgs =  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
            msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
            self.traitement.errorDlg('erreur',msgs)
            return False

        return True


    def majexecute(self):
        try:
            """Mis à jour execute """

            self.cursdsi.execute("select current_date as date, substr(localtime::varchar,1,8)::time as time")
            tdate = self.cursdsi.fetchone()
            dateNow=tdate[0]
            timereel=str(tdate[1])
            SQL = "update execute set idttt='Traitement',rqfichierok='Fini', datefinexe='" +str(dateNow)+ "',hrfinexe='" +timereel+"',volumeexe=" + str(self.db.DCount(table='export',connexion=self.local)) + " WHERE idexecute=" + str(self.db.DMax('idexecutec','source_o',self.local))
            self.cursdsi.execute(SQL)

        except Exception as inst:
            msgs =  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
            msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
            self.traitement.errorDlg('erreur',msgs)
            return False


    def tablexport(self):
        self.curlocal.execute("DROP TABLE IF EXISTS \"export\";")
        procedures  = open(self.path_export,'r').read()
        self.curlocal.execute(procedures)



    def sqlNz(self):
        sql = "DROP FUNCTION IF EXISTS nz(anyelement, anyelement);"
        sql += "CREATE OR REPLACE FUNCTION nz(anyelement, anyelement) RETURNS anyelement AS "
        sql += "' SELECT case when $1 is null then $2 else $1 end ' LANGUAGE 'sql' IMMUTABLE COST 100;"
        sql += "ALTER FUNCTION nz(anyelement, anyelement) OWNER TO postgres;"
        self.curlocal.execute(sql)

    def iif(self):
        sql ="DROP FUNCTION IF EXISTS iif(boolean, anyelement, anyelement);"
        sql += "CREATE OR REPLACE FUNCTION iif(boolean, anyelement, anyelement) RETURNS anyelement AS"
        sql+="' SELECT case $1 when true then $2 else $3 end ' LANGUAGE 'sql' IMMUTABLE COST 100;"
        sql+="ALTER FUNCTION iif(boolean, anyelement, anyelement) OWNER TO postgres;"
        self.curlocal.execute(sql)

    def affcontrole(self,tzetat,tzobj):
        I=0
        while I <len(tzetat):
            if tzetat[I][1]=="O":
                tzobj[I].SetValue(True)
            else:
                tzobj[I].SetValue(False)
            I=I+1

class MyAboutBox(wx.Dialog):
    text = '''
            <html>
            <body bgcolor="#AC76DE">
            <center><table bgcolor="#458154" width="100%%" cellspacing="0"
            cellpadding="0" border="1">
            <tr>
            <td align="center">
            <h1>&clubs; %s</h1>
            &copy; Harif&pound;tra 2017 -&lt;- %s ->- %s<br>
            </td>
            </tr>
            </table>
            <p>Si vous avez un probleme sur cet outil,
                    merci de me contacter:<br>
                <b> &spades; Pseudo_Skype: haric0d3</b>


            .</p>
            <p>Cliquez sur <b>[OK]</b> pour quitter ;-)</p>
            <p><b>Terms and conditions:</b></p>
            <p>Les modalit&eacute;s et conditions de la GPL doivent &ecirc;tre mises &agrave;
            la disposition de quiconque re&ccedil;oit
            une copie de l'&oelig;uvre qui lui est soumise (&lsaquo;&lsaquo;la titulaire&rsaquo;&rsaquo;).
            Tout titulaire de licence qui adh&egrave;re aux termes et conditions est
            autoris&eacute; &agrave; modifier l'&oelig;uvre, ainsi qu'&agrave; copier et redistribuer
            l'&oelig;uvre ou toute version d&eacute;riv&eacute;e. La titulaire est
            autoris&eacute;e &agrave; facturer des frais pour ce service,
            ou le faire gratuitement. Ce dernier point distingue
            la GPL des licences de logiciels qui interdisent la redistribution commerciale.</p>
            <p><font size="-1">Pour plus d'information: <i>harifetra_iam@vivetic.mg</i>
                        .</font></p><br>



            <b>"The higher the heels , the closer to heaven..."</b>
            <p><<b>9085  &reg; 2017.</b> <br>
            <p><wxp module="wx" class="Button">
            <param name="label" value="Okay">
            <param name="id" value="ID_OK">
            </wxp></p>
            </center>
            </body></html>
            '''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title='Harifetra:9085 - IT C0d3r',)
        html = wx.html.HtmlWindow(self, size=(420, -1))
        py_version = sys.version.split()[0]
        #html.SetPage(self.text % (wx.VERSION_STRING,"TOOLS NAME", py_version))
        html.SetPage(self.text % ("SGC","AG22", py_version))
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)



class createtable(wx.grid.Grid):
    """ Classe modele d'affichage des données d'une table dans une base des données postgresql realisée avec wxPython"""
    def __init__(self, parent,record,col,dim=(415,300)):
        wx.grid.Grid.__init__(self, parent, -1,size=dim)
        self.nbLigne = len(record)
        self.nbCols = col
        self.CreateGrid(self.nbLigne,self.nbCols)


class DialogBox(wx.Dialog):
    """ FENETRE D'AIDE en dialogBox pour afficher des aide sur le choix cp/ville/rue"""
    def __init__(self, parent,record,tabcol,col):
        """ Constructeur : controle : champs destination,tzRecord: tableau des valeurs à afficher,tzCol : tableau contenant les entetes,Ndata : numéro de colonne contenant le donné à renvoyer"""
        self.tzRecord = record
        self.col = col
        tscreen =  wx.GetClientDisplayRect()
        SizeXConteneur = tscreen[2]*98/100

        SizeYConteneur = tscreen[3]*44/100

        wx.Dialog.__init__(self, None, title = "INFORMATION",style = wx.WANTS_CHARS|wx.SYSTEM_MENU|wx.CAPTION | wx.CLOSE_BOX, size = (SizeXConteneur, SizeYConteneur))
        self.grid = createtable(self,self.tzRecord,self.col,(SizeXConteneur,SizeYConteneur))
        #self.grid.SetColMinimalAcceptableWidth(245)
        self.createBodyTable(len(self.tzRecord),self.col,tabcol,self.tzRecord)

        self.grid.SetColSize(0,100)
        self.grid.SetColSize(1,100)
        self.grid.SetColSize(2,100)

        # --- Evennement
        self.grid.Bind(wx.EVT_KEY_DOWN, self.pushOnTouche)
        self.ShowModal()

    def createBodyTable(self,nbLigne,nbCols,tablecolumns,tzResults):
        # ---- CREATION DU TABLEAU ------
        nCol = 0
        while(nCol<len(tablecolumns)):
            string = tablecolumns[nCol]
            self.grid.SetColLabelValue(nCol, string.upper())
            nCol = nCol+1
        # ---- INSERTION DES DONNEES ------
        I=0
        while(I<nbLigne):
            J=0
            while(J<nbCols):
                self.grid.SetCellValue(I, J, str(tzResults[I][J]))
                J=J+1
            I=I+1

    def pushOnTouche(self,e):
        self.Close()



class MyDialect(csv.Dialect):
    delimiter = ";"
    quotechar = "'"
    escapechar = "\\"
    doublequote = None
    lineterminator = "\r\n"
    quoting = csv.QUOTE_NONNUMERIC
    skipinitialspace = False

if __name__ == "__main__":
    app = MainApp(0)
    app.MainLoop()
