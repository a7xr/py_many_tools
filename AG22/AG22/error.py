#! /usr/bin/env python
# -*- coding: cp1252 -*-
import openimg
import wx
import wx.grid
import psycopg2
import psycopg2.extras
import sys
#class afficheGrid(wx.grid.Grid):
class afficheGrid(wx.grid.Grid):
    """ Classe modele d'affichage des données d'une table dans une base des données postgresql realisée avec wxPython"""
    def __init__(self, parent,table=None,db='',bErr=True,tchampsVeruoille=[]):
        wx.grid.Grid.__init__(self, parent, -1)
        self.rep = 'C:/image/'
        self.table = table
        self.tri = 'ASC'
        # ---- Base des données ------
        try:
            self.connexion      = psycopg2.connect("dbname="+db+" user=postgres password=123456  host= localhost") #prod
            self.connexion2      = psycopg2.connect("dbname=sdsi  user=op1 password=aa  host= 192.168.10.5") #prod
            self.connexion.set_isolation_level(0)
        except BaseException:
            dialogue       = wx.MessageDialog(None, 'Serveur prod introuvable!', "Connexion!",wx.OK)
            result         = dialogue.ShowModal()
            return False

        self.curseur       = self.connexion.cursor(cursor_factory=psycopg2.extras.DictCursor)




        tzResults          = self.extraction(self.connexion,table,None,tri=self.tri)
        self.tableColumn   = self.getNomColumn(table)
        #tzResults          = self.extraction(self.connexion,table,None,tri=self.tri)

        nbLigne            = self.getNligne(tzResults)
        nbCols             = len(self.tableColumn)
        self.CreateGrid(nbLigne,nbCols)
        self.createTable(nbLigne,nbCols,self.tableColumn,tzResults)
        #self.SetDefaultColSize(150,resizeExistingCols=True)
        self.SetColSize(0,150)
        self.SetColSize(1,200)

        self.SetColSize(2,800)
        p=0
        while(p<nbLigne):
            self.SetRowSize(p,30)
            p=p+1
        p=0
        champmin = ['CC','__S']
        champmoy = ['N_ENR','MATRICULE','COMMANDE','idenr','idexecute','idexecutec']
        champlarge = ['ID_COMMANDE','N_LOT','ETAPE','date_saisie']
        while(p<nbCols):
            if self.tableColumn[p] in champmin or self.tableColumn[p].find('__')==0:
                self.SetColSize(p,30)
            elif self.tableColumn[p] in champmoy:
                self.SetColSize(p,70)
            elif self.tableColumn[p] in champlarge:
                self.SetColSize(p,90)

            else:
                self.SetColSize(p,150)
            p=p+1

        if bErr==True:
            self.SetColSize(3,600)
        for i in range(nbLigne):
            for j in range(nbCols):
                if self.tableColumn[j] in tchampsVeruoille:
                    self.SetReadOnly(i,j)

        self.Show(True)

        # ----- EVENNEMENT POUR CHANGER LES DONNEES -----
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.changer)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK ,self.trier)
        if(self.table!='erreur'):
            self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK ,self.opens)


    def getNligne(self,tzResults):
        if(len(tzResults)==0):
            nbLigne        = 1
        else:
            nbLigne        = len(tzResults)
        return nbLigne

    def getNCol(self,tabCol,strCol):
        str = ''
        I=0
        while(I<len(tabCol)):
            if(tabCol[I]==strCol):
                str=strCol
                return I
            I=I+1
        return I

    def changer(self,e):
        ligne = e.GetRow()
        cols  = e.GetCol()
        new = self.GetCellValue(ligne,cols)
        colId = self.getNCol(self.tableColumn,'n_enr')
        id  = self.GetCellValue(ligne,colId)
        self.curseur.execute("UPDATE \"" +str(self.table)+ "\" SET \""+str(self.tableColumn[cols])+"\"='"+str(new)+"' WHERE \"n_enr\" = '"+str(id)+"'")


    def trier(self,e):
        if(self.tri=='ASC'):
            self.tri = 'DESC'
        else:
            self.tri = 'ASC'
        ordre = self.tableColumn[e.GetCol()]

        self.ClearGrid()
        tzResults          = self.extraction(self.connexion,self.table,ordre,self.tri)
        nbLigne            = self.getNligne(tzResults)
        nbCols             = len(self.tableColumn)
        self.createTable(nbLigne,nbCols,self.tableColumn,tzResults)

    def getColImage(self,zChampImage):
        tzCol = self.tableColumn
        I=0
        for elm in tzCol:
            if elm==zChampImage:
                return I
            I=I+1
        return I

    def opens(self,e):
        obj=e.GetEventObject()
        self.SelectRow(e.GetRow())
        lot = self.GetCellValue(e.GetRow(),self.getColImage("n_lot"))
        img = self.GetCellValue(e.GetRow(),self.getColImage("n_ima"))
        pli = self.GetCellValue(e.GetRow(),self.getColImage("pli"))
        #n_ima = self.GetCellValue(e.GetRow(),self.getColImage("PLI"))
        cursdsi = self.connexion2.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursdsi.execute("select * from fichier where idfichiercmd='"+str(lot)+"'")
        datafile = cursdsi.fetchone()
        if datafile==None:
            self.Warndlg("WARNING!!!","Le lot "+str(lot)+" n'existe pas .")
            xComm.SetFocus()
            return
        servimage = r""+str(datafile['pathauto'])

        servimage_abs=servimage+"\\"+img
#            print servimage_abs
        openimg.MainWindow(servimage_abs,lot,pli=pli,n_ima=img)
        obj.SetFocus()

    def opens0(self,e):
        self.SelectRow(e.GetRow())
        openimg.MainWindow(self.rep+self.GetCellValue(e.GetRow(),6)+'/'+self.GetCellValue(e.GetRow(),1))


    def getNomColumn(self,table,connexion=None):
            """ Renvoie sous forme tableau tridimensionnelle la liste des champs dans la table table """
            self.sqlget = "SELECT a.attname as Column,pg_catalog.format_type(a.atttypid, a.atttypmod) as Datatype,a.attnotnull as notnull "
            self.sqlget+= " FROM pg_catalog.pg_attribute a WHERE a.attnum > 0 AND NOT a.attisdropped AND a.attrelid = ( "
            self.sqlget+= " SELECT c.oid FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace "
            self.sqlget+= " WHERE c.relname ~ '^("+table+")$' AND pg_catalog.pg_table_is_visible(c.oid) ); "
            self.curseur.execute(self.sqlget)
            champs = self.curseur.fetchall()
            ligne = len(champs)
            i=0
            tableColumn = []
            while(i<ligne):
                tableColumn.append(champs[i][0])
                i=i+1
            return tableColumn



    def extraction(self,conex,table,ordre=None ,tri = 'ASC'):

        self.curseur        = conex.cursor(cursor_factory=psycopg2.extras.DictCursor)
        conex.set_client_encoding('WIN1252')
        self.tableColumn        = self.getNomColumn(table)
        self.table          = table
        if(ordre==None or ordre.isspace()==True or ordre==''):
            ordre = str(self.tableColumn[0])
        if(self.table!='erreur'):
            req                 = "SELECT * FROM  \""+str(table)+"\" WHERE (((\""+str(table)+"\".\"n_enr\"),(\""+str(table)+"\".\"n_lot\")) In (SELECT n_enr,n_lot FROM erreur))  ORDER BY \""+str(table)+"\".\"n_enr\" "
        else:
            req                 = "SELECT * FROM  \""+str(table)+"\"   ORDER BY \""+str(table)+"\".\"n_enr\" "




        nbCols              = len(self.tableColumn)
        datas               = self.curseur.execute(req)
        tzResults           = self.curseur.fetchall()
        return tzResults


    def createTable(self,nbLigne,nbCols,tablecolumns,tzResults):

        #sys.exit()
        # ---- CREATION DU TABLEAU ------

        nCol = 0
        while(nCol<len(tablecolumns)):
            string = tablecolumns[nCol]
            self.SetColLabelValue(nCol, string.upper())
            nCol = nCol+1
        # ---- INSERTION DES DONNEES ------
        I=0
        while(I<len(tzResults)):
            J=0
            while(J<len(tablecolumns)):
                self.SetCellValue(I, J, str(tzResults[I][J]))
                J=J+1
            I=I+1




class fenetre(wx.Frame):
    def __init__(self, parent,table,db,bErr=True,tchampsVeruoille=[]):
        tscreen =  wx.GetClientDisplayRect()
        SizeXConteneur = tscreen[2]*0.95
        SizeYConteneur = tscreen[3]*0.3

        wx.Frame.__init__(self, parent, -1, table,size=(SizeXConteneur, SizeYConteneur))
        grid = afficheGrid(self,table,db,bErr,tchampsVeruoille=tchampsVeruoille)



