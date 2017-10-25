#! /usr/bin/env python
# -*- coding: cp1252 -*-
import openimg
import wx
import wx.grid
import psycopg2
import psycopg2.extras
import random
import datetime

class afficheGrid(wx.grid.Grid):
    """ Classe modele d'affichage des données d'une table dans une base des données postgresql realisée avec wxPython"""
    def __init__(self, parent,table=None,db='',key='n_enr',idcom=0,nomcommande=0,wdgchecksta=None,where='',tchampvue=[],isctrlann=True,pos=(10,10)):
        prsize =  parent.GetSize()
        wx.grid.Grid.__init__(self, parent, -1,pos=pos,size=(prsize[0]*98/100,prsize[1]*88/100))
        self.table = table
        self.key = key
        self.checksta = wdgchecksta
        self.tri = 'ASC'
        self.rep = 'C:/image/'
        self.change = False
        self.repserveur = str(nomcommande)+'/'
        self.insert = False
        self.dbname = db
        self.servimage = r"\\servbase3\images$\\"
        self.rowfind = 0
        self.colfind  = 0
        self.tXsearch = []
        self.cellfind = 0
        self.zXSearch = ''
        self.iscass = False
        self.isentier = False
        #self.servimage = r"\\192.168.10.42\webmaster\testopensource\\"
        # ---- Base des données ------
        try:
            self.connexion      = psycopg2.connect("dbname="+db+" user=postgres password=123456  host= localhost") #prod
            self.connexion.set_isolation_level(0)
            self.connexion2      = psycopg2.connect("dbname=sdsi  user=op1 password=aa  host= 192.168.10.5") #prod


        except BaseException:
            dialogue       = wx.MessageDialog(None, 'Serveur prod introuvable!', "Connexion!",wx.OK)
            result         = dialogue.ShowModal()
            return False
        self.curseur       = self.connexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.tableColumn   = self.getNomColumn(table)

        tzResults          = self.extraction(self.connexion,table,None,tri=self.tri,where=where,tchampvue=tchampvue)

        nbLigne            = self.getNligne(tzResults)
        nbCols             = len(self.tableColumn)
        self.rowCount = nbLigne
        self._table = MegaTable(tzResults, self.tableColumn, plugins=None,dbname=self.dbname,tablename=self.table,key=self.key,gr=self)
        self.SetTable(self._table)
        self._plugins = None
        p=0
        champmin = ['CC','__s']
        champmoy = ['n_enr','matricule','commande','idenr','idexecute','idexecutec']
        champlarge = ['id_commande','n_lot','etape','date_saisie']
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
        nl=0

        self.EnableEditing(False)

        self.SetLabelFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        # ----- EVENNEMENT POUR CHANGER LES DONNEES -----

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.changer)
        self.Bind(wx.EVT_CHAR, self.charact)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK,self.OnLabelRightClicked)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK ,self.opens)

        self.EnableDragColMove()
        self.AutoSizeColumns()
        self.SetDefaultRowSize(30)
        self.SetMargins(30,15)
        #parent.SetScrollbars(15, 15, (prsize[0]+55)/15,(prsize[1]+55)/15)
    def getcurseur(self,e):
        row, col = e.GetRow(), e.GetCol()
        self.SetGridCursor(row,col)

    def sortir(self,e):
        self.SetSortingColumn(2)

    def OnLabelRightClicked(self, evt):
        # Did we click on a row or a column?
        row, col = evt.GetRow(), evt.GetCol()
        if row == -1: self.colPopup(col, evt)
        elif col == -1: self.rowPopup(row, evt)

    def rowPopup(self, row, evt,fin=True):
        """(row, evt) -> display a popup menu when a row label is right clicked"""
        appendID = wx.NewId()
        appendID2 = wx.NewId()
        deleteID = wx.NewId()
        x = self.GetRowSize(row)/2

        if not self.GetSelectedRows():
            self.SelectRow(row)

        menu = wx.Menu()
        xo, yo = evt.GetPosition()
        menu.Append(appendID, "Ajouter un enregistrement")
        menu.Append(appendID2, "Ajouter un enregistrement en fin des lignes")
        menu.Append(deleteID, "Supprimer un ou des enregistrement(s)")

        def appendfin(event, self=self, row=row):
            self.curseur.execute("select * from \""+self.table+"\"")
            res = self.curseur.fetchall()
            if len(res)!=self.GetNumberRows():
                self.errorDlg("Erreur","Veuillez afficher tous les enregistrements!")
                return False
            if fin==True:
                conf = wx.MessageDialog ( None, 'Voulez vous insérer une ligne à la fin des ernregistrements ?', caption='Confirmation',style=wx.YES_NO | wx.ICON_QUESTION , pos=wx.DefaultPosition )
                if(conf.ShowModal() == wx.ID_NO):
                    return False
                self._table.AppendRowfin(self.rowCount-1)
                self.Reset()
                self.MakeCellVisible(self._table.GetNumberRows()-1,0)
                self.SelectRow(self._table.GetNumberRows()-1)


        def append(event, self=self, row=row):
            self.curseur.execute("select * from \""+self.table+"\"")
            res = self.curseur.fetchall()
            if len(res)!=self.GetNumberRows():

                self.errorDlg("Erreur","Veuillez afficher tous les enregistrements!")
                return False

            conf = wx.MessageDialog ( None, 'Voulez vous insérer une ligne avant cette ligne selectionnée ?', caption='Confirmation',style=wx.YES_NO | wx.ICON_QUESTION , pos=wx.DefaultPosition )
            if(conf.ShowModal() == wx.ID_NO):
                return False
#            if row==0:
#                return False
            self._table.AppendRow(row)

            self.MakeCellVisible(row-1,0)
            self.SelectRow(row)
            self.Reset()


        def delete(event, self=self, row=row):
            rows = self.GetSelectedRows()
            self._table.DeleteRows(rows)
            self.Reset()

        self.Bind(wx.EVT_MENU, appendfin, id=appendID2)
        self.Bind(wx.EVT_MENU, append, id=appendID)
        self.Bind(wx.EVT_MENU, delete, id=deleteID)
        self.PopupMenu(menu)
        menu.Destroy()
        return



    def colPopup(self, col, evt):
        """(col, evt) -> display a popup menu when a column label is
        right clicked"""
        x = self.GetColSize(col)/2
        menu = wx.Menu()
        id1 = wx.NewId()
        id2 = wx.NewId()
        sortIDA = wx.NewId()
        sortIDD = wx.NewId()
        FiltId = wx.NewId()
        sortAll = wx.NewId()

        xo, yo = evt.GetPosition()
        #self.SelectCol(col)
        cols = self.GetSelectedCols()
        self.Refresh()
        #menu.Append(id1, "Ajouter une colonne")
        menu.Append(FiltId, "Filtrer (F7)" )
        #menu.Append(id2, "Supprimer la colonne")
        menu.Append(sortIDA, "Trier ASC")
        menu.Append(sortIDD, "Trier DESC")
        menu.Append(sortAll, "Afficher tous (F8)")

        def delete(event, self=self, col=col):
            cols = self.GetSelectedCols()
            nomcols =  self.tableColumn[cols[0]]
            #return
            conf = wx.MessageDialog ( None, 'Voulez-vous vraiment supprimer la colonne '+nomcols+ ' de la table '+self.table+' ?', caption='Confirmation',style=wx.YES_NO | wx.ICON_WARNING , pos=wx.DefaultPosition )
            if(conf.ShowModal() == wx.ID_NO):
                return False

            self._table.DeleteCols(cols)
            self.Reset()

        def sortAsc(event, self=self, col=col):
            self._table.SortColumn(col)
            self._table.ResetView(self)

        def sortDesc(event, self=self, col=col):
            self._table.SortColumn(col,rev=True)
            self._table.ResetView(self)

        def affiche(event):
            self._table.affiche()
            self._table.ResetView(self)


        def filtrer(event,self=self,col=col):
            if col==self.GetGridCursorCol():
                valeur = self.GetCellValue(self.GetGridCursorRow(),self.GetGridCursorCol())
                self._table.filtrer(col,valeur)
                self._table.ResetView(self)

        def addCol(event,self=self,col=col):
            DialogBox(self,self._table,col=col,dbname=self.dbname,nomtable=self.table)

        self.Bind(wx.EVT_MENU, delete, id=id2)
        self.Bind(wx.EVT_MENU, addCol, id=id1)

        #if len(cols) == 1:
        self.Bind(wx.EVT_MENU, sortAsc, id=sortIDA)
        self.Bind(wx.EVT_MENU, sortDesc, id=sortIDD)
        self.Bind(wx.EVT_MENU, filtrer, id=FiltId)
        self.Bind(wx.EVT_MENU, affiche, id=sortAll)

        self.PopupMenu(menu)
        menu.Destroy()
        return


    def Reset(self):
            """reset the view based on the data in the table.  Call
            this when rows are added or destroyed"""
            self._table.ResetView(self)


    def charact(self,e):
        if e.GetKeyCode()==104 or e.GetKeyCode()==72:
            self.searchreplace(e)

        elif e.GetKeyCode()==102 or e.GetKeyCode()==340 or e.GetKeyCode()==70:
            self.searchSimple(e)

        elif e.GetKeyCode()==342:
            self.searchOneTouch()
        elif e.GetKeyCode()==wx.WXK_F5:
            self.insertData(e)
        elif e.GetKeyCode()==wx.WXK_F6:
            self.inserfin(e)
        elif e.GetKeyCode()==wx.WXK_F7:
            self.filtrer(e)
        elif e.GetKeyCode()==wx.WXK_F8:
            self.displayAll(e)
        elif e.GetKeyCode()==wx.WXK_DELETE:
            self.deleteligne(e)


    def insertData(self,e=None):
        tzRowSelected = self.GetSelectedRows()
        if len(tzRowSelected)>0:
            row = tzRowSelected[len(tzRowSelected)-1]
            conf = wx.MessageDialog ( None, 'Voulez vous insérer une ligne après la (les) ligne(s) selectionnée ?', caption='Confirmation',style=wx.YES_NO | wx.ICON_QUESTION , pos=wx.DefaultPosition )
            if(conf.ShowModal() == wx.ID_NO):
                return False
            self._table.AppendRow(row)


    def filtrer(self,e=None):
        tzRowSelected = self.GetSelectedRows()
        col=self.GetGridCursorCol()
        if col!=-1:
            valeur = self.GetCellValue(self.GetGridCursorRow(),self.GetGridCursorCol())
            self._table.filtrer(col,valeur)
            self._table.ResetView(self)

    def displayAll(self,e=None):
        self._table.affiche()
        self._table.ResetView(self)

    def inserfin(self,e=None):
        conf = wx.MessageDialog ( None, 'Voulez vous insérer une ligne à la fin des ernregistrements ?', caption='Confirmation',style=wx.YES_NO | wx.ICON_QUESTION , pos=wx.DefaultPosition )
        if(conf.ShowModal() == wx.ID_NO):
            return False
        self._table.AppendRowfin()


    def deleteligne(self,e=None):
        tzRowSelected = self.GetSelectedRows()
        if len(tzRowSelected)>0:
            self._table.DeleteRows(tzRowSelected)



    def searchreplace(self,e=None):
        self.dial = wx.Dialog(self,title='Rechercher et remplacer',size=(330,220))
        wx.StaticText(self.dial,label='Rechercher:',pos=(20,30))
        self.search = wx.TextCtrl(self.dial,pos=(110,30),name='search')
        wx.StaticText(self.dial,label='Remplacer par:',pos=(20,60))
        self.replace = wx.TextCtrl(self.dial,pos=(110,60),name='replace')
        self.searchent = wx.CheckBox(self.dial,label='Mot entier',pos=(110,90))
        btnsearch = wx.Button(self.dial,label='Rechercher',pos=(20,120),id=1)
        btnreplace = wx.Button(self.dial,label='Remplacer',pos=(120,120),id=2)
        btnreplacets = wx.Button(self.dial,label='Tous remplacer',pos=(20,150),id=3)
        btnexit = wx.Button(self.dial,label='Fermer',pos=(120,150))
        btnexit.Bind(wx.EVT_BUTTON,self.closedial)
        btnsearch.Bind(wx.EVT_BUTTON,self.rechercher)
        btnreplace.Bind(wx.EVT_BUTTON,self.remplacer)
        btnreplacets.Bind(wx.EVT_BUTTON,self.rechercher)
        self.searchent.SetValue(True)
        self.dial.ShowModal()



    def searchSimple(self,e=None):
        self.dialsimple = wx.Dialog(self,title='Rechercher',size=(320,200))
        wx.StaticText(self.dialsimple,label='Rechercher:',pos=(20,30))
        self.search1 = wx.TextCtrl(self.dialsimple,pos=(110,30),name='search')
        self.searchent = wx.CheckBox(self.dialsimple,label='Mot entier',pos=(110,60))
        self.searchcasse = wx.CheckBox(self.dialsimple,label='Vérification casse',pos=(110,90))
        btnsearch = wx.Button(self.dialsimple,label='Rechercher',pos=(20,120),id=1)
        btnexit = wx.Button(self.dialsimple,label='Fermer',pos=(100,120))
        btnexit.Bind(wx.EVT_BUTTON,self.closedial2)
        btnsearch.Bind(wx.EVT_BUTTON,self.recherchersimple)
        self.tXsearch = []
        self.searchent.SetValue(True)
        self.searchcasse.SetValue(True)
        self.dialsimple.ShowModal()



    def closedial(self,e=None):
        try:

            self.dial.Destroy()

        except:
            pass
    def closedial2(self,e=None):
        try:

            self.dialsimple.Destroy()

        except:
            pass


    def rechercher(self,e=None):
        imodif = 0
        #self.cellfind = 0
        bt = e.GetEventObject()
        id =  bt.GetId()

        nbligne = self.GetNumberRows()
        ncol    = self.GetNumberCols()
        oldtext = self.search.GetValue()
        newtext = self.replace.GetValue()
        I=0
        if self.searchent.GetValue()==True:
            while I<nbligne:
                J=0
                while J<ncol:
                    cellvalue = self.GetCellValue(I,J).strip()
                    if cellvalue==oldtext or cellvalue.find(" "+oldtext+" ")!=-1 or  (cellvalue.find(" "+oldtext)!=-1 and cellvalue.find(" "+oldtext)+len(" "+oldtext)==len(cellvalue)) or cellvalue.find(oldtext+" ")==0:
                        cpl = (I,J)
                        if cpl not in self.tXsearch:
                            self.ClearSelection()
                            self.SelectBlock(I,J,I,J)
                            self.tXsearch.append(cpl)
                            if self.IsVisible(I,J)==False:
                                self.MakeCellVisible(I,J)
                            if id!=3:
                                return
                            else:
                                selectedval     = self.GetCellValue(I,J)
                                slct = self.GetSelectionBlockBottomRight ()
                                if len(slct)>0:
                                    ligne = slct[0][0]
                                    col  =  slct[0][1]
                                    selectedval     = self.GetCellValue(ligne,col)


                                if selectedval==oldtext:
                                    self.SetCellValue(I,J,newtext)
                                    self.changer(e,I,J)
                                    self.cellfind = self.cellfind+1
                                    imodif = imodif+1
                                else:
                                    newword = newtext
                                    deb = selectedval.find(oldtext)
                                    fin = deb+(len(oldtext)-1)
                                    if deb==0:
                                        new = newword+selectedval[fin+1:]
                                    else:
                                        new = selectedval[0:deb]+newword+selectedval[fin+1:]
                                    self.SetCellValue(I,J,new)
                                    self.changer(e,I,J)
                                    self.cellfind = self.cellfind+1

                    J=J+1
                I=I+1

        elif self.searchent.GetValue()==False:
            while I<nbligne:
                J=0
                while J<ncol:
                    if self.GetCellValue(I,J).find(oldtext)!=-1 :
                        if oldtext == '':
                            if self.GetCellValue(I,J)=='':
                                cpl = (I,J)
                                if cpl not in self.tXsearch:
                                    self.ClearSelection()
                                    self.SelectBlock(I,J,I,J)
                                    self.tXsearch.append(cpl)
                                    if self.IsVisible(I,J)==False:
                                        self.MakeCellVisible(I,J)
                                    if id!=3:
                                        return
                                    else:
                                        selectedval     = self.GetCellValue(I,J)
                                        self.SetCellValue(I,J,newtext)
                                        self.changer(e,I,J)
                                        self.cellfind = self.cellfind+1
                                        imodif = imodif+1

                        else:
                            cpl = (I,J)
                            if cpl not in self.tXsearch:
                                self.ClearSelection()
                                self.SelectBlock(I,J,I,J)
                                self.tXsearch.append(cpl)
                                if self.IsVisible(I,J)==False:
                                    self.MakeCellVisible(I,J)
                                if id!=3:
                                    return
                                else:
                                    newword = newtext
                                    selectedval     = self.GetCellValue(I,J)
                                    deb = selectedval.find(oldtext)
                                    fin = deb+(len(oldtext)-1)
                                    if deb==0:
                                        new = newword+selectedval[fin+1:]
                                    else:
                                        new = selectedval[0:deb]+newword+selectedval[fin+1:]
                                    self.SetCellValue(I,J,new)
                                    self.changer(e,I,J)
                                    self.cellfind = self.cellfind+1
                    J=J+1
                I=I+1


        if imodif>0:
            msag = 'La recherche est terminée,\n nombre des modifications: '+str(imodif)
        else:
            self.ClearSelection()
            msag = 'La recherche est terminée,\n Nombres des valeurs trouvées:'+str(self.cellfind)
        self.tXsearch = []
        self.InfoDlg('Recherche',msag)
        imodif = 0;self.cellfind = 0

        return


    def recherchersimple(self,e=None):
#        print "recherche simple"
        imodif = 0
        bt = e.GetEventObject()
        id =  bt.GetId()
        res = False
        nbligne = self.GetNumberRows()
        ncol    = self.GetNumberCols()
        searchtext = self.search1.GetValue()
        iscasse = self.searchcasse.GetValue()
        isentier = self.searchent.GetValue()
        self.zXSearch = searchtext
        self.iscass = iscasse
        self.isentier = isentier
        self.dialsimple.Destroy()
#        print self.iscass
#        print self.isentier
        if self.isentier == True:
#            print 'mot entier'
            if self.iscass==True:
#                print 'mot entier avec casse'
                I=0
                while I<nbligne:
                    J=0
                    while J<ncol:

                        entryword = self.GetCellValue(I,J).strip()
                        if entryword==searchtext or entryword.find(" "+searchtext+" ")!=-1 or (entryword.find(searchtext+" ")==0) or (entryword.find(" "+searchtext)!=-1 and entryword.find(" "+searchtext)+len(searchtext)+1==len(entryword)):
                            cpl = (I,J)
                            if cpl not in self.tXsearch:
                                self.ClearSelection()
                                self.SelectBlock(I,J,I,J)
                                self.tXsearch.append(cpl)
                                if self.IsVisible(I,J)==False:
                                    self.MakeCellVisible(I,J)
                                    res = True
                                return
                        J=J+1
                    I=I+1
            else:
                I=0
                searchtext2 = searchtext.lower()
                searchtext1 = searchtext.upper()
                while I<nbligne:
                    J=0
                    while J<ncol:
                        entryword = self.GetCellValue(I,J).strip().upper()
                        if entryword==searchtext1 or entryword.find(" "+searchtext1+" ")!=-1 or entryword.find(searchtext1+" ")==0 or (entryword.find(" "+searchtext1)!=-1 and entryword.find(" "+searchtext1)+len(" "+searchtext1)==len(entryword) ):
                            cpl = (I,J)
                            if cpl not in self.tXsearch:
                                self.ClearSelection()
                                self.SelectBlock(I,J,I,J)
                                self.tXsearch.append(cpl)
                                if self.IsVisible(I,J)==False:
                                    self.MakeCellVisible(I,J)
                                    res = True
                                return

                        J=J+1
                    I=I+1
        else:
            if iscasse==True:
                I=0
                while I<nbligne:
                    J=0
                    while J<ncol:
                        entryword = self.GetCellValue(I,J).strip()
                        if entryword.find(searchtext)!=-1:
                            cpl = (I,J)
                            if cpl not in self.tXsearch:
                                self.ClearSelection()
                                self.SelectBlock(I,J,I,J)
                                self.tXsearch.append(cpl)
                                if self.IsVisible(I,J)==False:
                                    self.MakeCellVisible(I,J)
                                    res = True
                                return
                        J=J+1
                    I=I+1
            else:
                I=0
                searchtext1 = searchtext.lower()
                searchtext2 = searchtext.upper()
                while I<nbligne:
                    J=0
                    while J<ncol:

                        if self.GetCellValue(I,J).find(searchtext1)!=-1 or self.GetCellValue(I,J).find(searchtext2)!=-1:
                            cpl = (I,J)
                            if cpl not in self.tXsearch:
                                self.ClearSelection()
                                self.SelectBlock(I,J,I,J)
                                self.tXsearch.append(cpl)
                                if self.IsVisible(I,J)==False:
                                    self.MakeCellVisible(I,J)
                                    res = True
                                return
                        J=J+1
                    I=I+1


        msag = 'La recherche est terminée'
        self.tXsearch = []

        self.InfoDlg('Recherche',msag)


    def recherchertouche(self,texte,iscasse,isentier):
        imodif = 0
        nbligne = self.GetNumberRows()
        ncol    = self.GetNumberCols()
        searchtext = texte
        self.zXSearch = searchtext
        self.iscass = iscasse
        self.isentier = isentier
        if isentier == True:
            if iscasse==True:
                I=0
                while I<nbligne:
                    J=0
                    while J<ncol:
                        entryword = self.GetCellValue(I,J).strip()
                        if entryword==searchtext or entryword.find(" "+searchtext+" ")!=-1 or (entryword.find(searchtext+" ")!=-1 and entryword.find(searchtext+" ")==0) or (entryword.find(" "+searchtext)!=-1 and entryword.find(" "+searchtext)+len(searchtext)+1==len(entryword)):
                            cpl = (I,J)
                            if cpl not in self.tXsearch:
                                self.ClearSelection()
                                self.SelectBlock(I,J,I,J)
                                self.tXsearch.append(cpl)
                                if self.IsVisible(I,J)==False:
                                    self.MakeCellVisible(I,J)
                                return
                        J=J+1
                    I=I+1
            else:
                I=0
                searchtext1 = searchtext.lower()
                searchtext2 = searchtext.upper()
                while I<nbligne:
                    J=0
                    while J<ncol:
                        entryword = self.GetCellValue(I,J).strip().upper()
                        if entryword==searchtext2 or entryword.find(" "+searchtext2+" ")!=-1 or (entryword.find(searchtext2+" ")==0) or (entryword.find(" "+searchtext2) + len(" "+searchtext2) == len(entryword) ) :
                            cpl = (I,J)
                            if cpl not in self.tXsearch:
                                self.ClearSelection()
                                self.SelectBlock(I,J,I,J)
                                self.tXsearch.append(cpl)
                                if self.IsVisible(I,J)==False:
                                    self.MakeCellVisible(I,J)
                                return

                        J=J+1
                    I=I+1
        else:
            if iscasse==True:
                I=0
                while I<nbligne:
                    J=0
                    while J<ncol:
                        if self.GetCellValue(I,J).find(searchtext)!=-1:
                            cpl = (I,J)
                            if cpl not in self.tXsearch:
                                self.ClearSelection()
                                self.SelectBlock(I,J,I,J)
                                self.tXsearch.append(cpl)
                                if self.IsVisible(I,J)==False:
                                    self.MakeCellVisible(I,J)
                                return
                        J=J+1
                    I=I+1

            else:
                I=0
                searchtext1 = searchtext.lower()
                searchtext2 = searchtext.upper()
                while I<nbligne:
                    J=0
                    while J<ncol:

                        if self.GetCellValue(I,J).find(searchtext1)!=-1 or self.GetCellValue(I,J).find(searchtext2)!=-1:
                            cpl = (I,J)
                            if cpl not in self.tXsearch:
                                self.ClearSelection()
                                self.SelectBlock(I,J,I,J)
                                self.tXsearch.append(cpl)
                                if self.IsVisible(I,J)==False:
                                    self.MakeCellVisible(I,J)
                                return
                        J=J+1
                    I=I+1


        msag = 'La recherche est terminée'

        self.InfoDlg('Recherche',msag)
        self.tXsearch = []



    def searchOneTouch(self,e=None):
        searchtext = self.zXSearch
        iscass = self.iscass
        isentier = self.isentier
        self.recherchertouche(searchtext,iscass,isentier)

    def remplacer(self,e):
        slct = self.GetSelectionBlockBottomRight ()
        if len(slct)==0:
            try:
                self.rechercher(e)
                slct = self.GetSelectionBlockBottomRight ()
            except:
                return
        ligne = slct[0][0]
        col  =  slct[0][1]
        old = self.search.GetValue()
        new = self.replace.GetValue()
        #print 'new orig:',new
        if new=='':
            new = ""
        selectedval     = self.GetCellValue(ligne,col)
        if old == selectedval:
            self.SetCellValue(ligne,col,new)
            self.changer(e,ligne,col)
            self.cellfind = self.cellfind+1

        else:
            if selectedval.find(old)!=-1:
                if self.searchent.GetValue()==False:
                    newword = new
                    deb = selectedval.find(old)
                    fin = deb+(len(old)-1)
                    if deb==0:
                        new = newword+selectedval[fin+1:]
                    else:
                        new = selectedval[0:deb]+newword+selectedval[fin+1:]

                    self.SetCellValue(ligne,col,new)
                    self.changer(e,ligne,col)
                    self.cellfind = self.cellfind+1
                else:
                    if selectedval.find(" "+old+" ")!=-1 or selectedval.find(old+" ")!=-1 or selectedval.find(" "+old)!=-1 :
                        newword = new
                        deb = selectedval.find(old)
                        fin = deb+(len(old)-1)
                        if deb==0:
                            new = newword+selectedval[fin+1:]
                        else:
                            new = selectedval[0:deb]+newword+selectedval[fin+1:]

                        self.SetCellValue(ligne,col,new)
                        self.changer(e,ligne,col)
                        self.cellfind = self.cellfind+1



        if len(self.tXsearch)> 0:
            self.rechercher(e)


        #print selectedval
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

    def changer(self,e,ln=None,col=None):

        if ln==None or col==None:
            ligne = e.GetRow()
            cols  = e.GetCol()
        else:
            ligne = ln
            cols  = col

        self.change = True
        new = self.GetCellValue(ligne,cols).encode('cp1252')
        colId = self.getNCol(self.tableColumn,self.key)
        id  = self.GetCellValue(ligne,colId)
        self.curseur.execute("UPDATE \"" +str(self.table)+ "\" SET   \""+str(self.tableColumn[cols])+"\"='"+str(new).replace("'","''")+"' WHERE \""+str(self.key)+"\" = '"+str(id)+"'")
        if self.checksta!=None:
            self.checksta.SetValue(False)
            self.curseur.execute("UPDATE controle SET etat='N' where traitement='5'")

        self.MakeCellVisible(ligne, cols)


    def changer0(self,e,ln=None,col=None):
        if self.insert==False:
            if ln==None or col==None:
                ligne = e.GetRow()
                cols  = e.GetCol()
            else:
                ligne = ln
                cols  = col

            self.change = True
            new = self.GetCellValue(ligne,cols)
            colId = self.getNCol(self.tableColumn,self.key)
            id  = self.GetCellValue(ligne,colId)
            try:

                self.curseur.execute("UPDATE \"" +str(self.table)+ "\" SET \""+str(self.tableColumn[cols])+"\"='"+str(new.encode('cp1252'))+"' WHERE \""+str(self.key)+"\" = '"+str(id)+"'")
            except:
                pass

            if self.checksta!=None:
                self.checksta.SetValue(False)
                self.curseur.execute("UPDATE controle SET etat='N' where traitement='5'")
            #self.SelectBlock(ligne, cols, ligne, cols)
            #self.ShowCellEditControl()
            #self.SelectRow(ligne)
            #self.SelectCol(cols)
            #self.SetGridCursor(ligne, cols)
            self.MakeCellVisible(ligne, cols)

                #self.SetGridCursor(ligne,cols)
        else:

            if ln==None or col==None:
                ligne = e.GetRow()
                cols  = e.GetCol()
            else:
                ligne = ln
                cols  = col

            self.change = True
            new = self.GetCellValue(ligne,cols)
            colId = self.getNCol(self.tableColumn,self.key)
            id  = self.GetCellValue(ligne,colId)
            #print "INSERT INTO \"" +str(self.table)+ "\" (\""+str(self.tableColumn[cols])+"\")Values('"+str(new.encode('cp1252'))+"')"
            self.curseur.execute("INSERT INTO \"" +str(self.table)+ "\" (\""+str(self.tableColumn[cols])+"\")Values('"+str(new.encode('cp1252'))+"')")
            self.insert= False
            if self.checksta!=None:
                self.checksta.SetValue(False)
                self.curseur.execute("UPDATE controle SET etat='N' where traitement='5'")




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

    def opens(self,e):
        obj=e.GetEventObject()
        self.SelectRow(e.GetRow())
        lot = self.GetCellValue(e.GetRow(),self.getColImage("n_lot"))
        img = self.GetCellValue(e.GetRow(),self.getColImage("n_ima"))
        pli = self.GetCellValue(e.GetRow(),self.getColImage("pli"))
        cursdsi = self.connexion2.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursdsi.execute("select * from fichier where idfichiercmd='"+str(lot)+"'")
        datafile = cursdsi.fetchone()
        if datafile==None:
            self.Warndlg("WARNING!!!","Le lot "+str(lot)+" n'existe pas .")
            xComm.SetFocus()
            return
        servimage = r""+str(datafile['pathauto'])

        servimage_abs=servimage+"\\"+img
        openimg.MainWindow(servimage_abs,lot,pli=pli,n_ima=img)
        obj.SetFocus()

    def opens0(self,e):
        obj=e.GetEventObject()
        self.SelectRow(e.GetRow())
        lot = self.GetCellValue(e.GetRow(),self.getColImage("n_lot"))
        pli = self.GetCellValue(e.GetRow(),self.getColImage("pli"))
        timg = self.GetCellValue(e.GetRow(),self.getColImage("list_ima")).split(";")
        cursdsi = self.connexion2.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursdsi.execute("select * from fichier where idfichiercmd='"+str(lot)+"'")
        datafile = cursdsi.fetchone()
        if datafile==None:
            self.Warndlg("WARNING!!!","Le lot "+str(lot)+" n'existe pas .")
            xComm.SetFocus()
            return
        servimage = r""+str(datafile['pathauto'])
        for i in range(len(timg)):
            servimage_abs=servimage+"\\"+timg[i]
            openimg.MainWindow(servimage_abs,lot)
        obj.SetFocus()

    def getColImage(self,zChampImage):
        tzCol = self.tableColumn
        I=0
        for elm in tzCol:
            if elm==zChampImage:
                return I
            I=I+1
        return I

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



    def extraction(self,conex,table,ordre=None ,tri = 'ASC',where='',tchampvue=[]):

        self.curseur        = conex.cursor(cursor_factory=psycopg2.extras.DictCursor)
        conex.set_client_encoding('WIN1252')
        self.tableColumn        = self.getNomColumn(table)
        self.table          = table
        if(ordre==None or ordre.isspace()==True or ordre==''):
            ordre = str(self.tableColumn[0])
        if len(tchampvue)==0:
            req                 = "SELECT * FROM  \""+str(table)+"\" "
        else:
            self.tableColumn = tchampvue
            req = " SELECT "
            x=0
            while x<len(tchampvue):
                if x==len(tchampvue)-1:
                    req+=" \""+tchampvue[x]+"\""
                else:
                    req+=" \""+tchampvue[x]+"\","
                x=x+1
            req += " from \""+table+"\" "

        if where!='':
            req += " where  "+where+" "
        req += " ORDER BY \""+ordre+"\" "+tri + " "
        nbCols              = len(self.tableColumn)
        datas               = self.curseur.execute(req)
        tzResults           = self.curseur.fetchall()
        return tzResults



    def createTable(self,nbLigne,nbCols,tablecolumns,tzResults):

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
            while(J<nbCols):
                if tzResults[I][J]!=None:
                    self.SetCellValue(I, J, str(tzResults[I][J]))
                else:
                    self.SetCellValue(I, J, '')
                J=J+1
            I=I+1



    def gotoContxMenu(self,e):
        self.colomn =  e.GetCol()
        self.row = e.GetRow()

        if self.colomn ==-1:
            self.OnRowMenu(e)
        else:
            self.OnContextMenu(e)


    def OnPopupAsc(self, event):
        self.tri_column(self.colomn,'ASC')


    def OnPopupDesc(self, event):
        self.tri_column(self.colomn,'DESC')


    def OnPopupDel(self, event):
        rowselected =  self.GetSelectedRows()
        nombselected = len(rowselected)
        if len(rowselected)==1 and rowselected[0]==self.row:
            conf = wx.MessageDialog ( None, "Voulez-vous vraiment Supprimer l'enregistrement "+str(self.key)+" ='"+self.GetCellValue(self.row,0)+"' ? ", caption='Confirmation',style=wx.YES_NO | wx.ICON_QUESTION , pos=wx.DefaultPosition )
            if(conf.ShowModal() == wx.ID_NO):
                return False
            try:
                self.suppr(self.dbname,self.table," \""+self.key+"\"= '"+self.GetCellValue(self.row,0)+"'")
            except:
                pass
            self.tri_column(0,'ASC')
            nbrow = self.GetNumberRows()
            self.DeleteRows(nbrow-1,nbrow-1,True)
        elif len(rowselected)>1 and self.row in rowselected:
            conf = wx.MessageDialog ( None, "Voulez-vous vraiment Supprimer les  "+str(len(rowselected))+" enregistrements  ? ", caption='Confirmation',style=wx.YES_NO | wx.ICON_QUESTION , pos=wx.DefaultPosition )
            if(conf.ShowModal() == wx.ID_NO):
                return False
            k=0
            while(k<len(rowselected)):
                self.suppr(self.dbname,self.table," \""+self.key+"\"= '"+self.GetCellValue(rowselected[k],0)+"'")
                nbrow = self.GetNumberRows()
                k=k+1
            self.curseur.execute("select count(\""+self.key+"\") as nb from \""+str(self.table)+"\"")
            res =  self.curseur.fetchone()
            if res['nb'] >0:
                self.tri_column(0,'ASC')
                self.DeleteRows(self.GetNumberRows()-nombselected,nombselected,True)
            else:
                self.DeleteRows(0,self.GetNumberRows(),True)

        else:
            self.errorDlg('Error','La ligne à supprimer doit être selectionnée!')



    def OnPopupRow2(self, event):
        self.tri_column(self.colomn,'DESC')
    def OnPopupRow3(self, event):
        self.tri_column(self.colomn,'DESC')


    def OnContextMenu(self, event):

        if not hasattr(self, "ascID"):
            self.ascID = wx.NewId()
            self.descID = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnPopupAsc, id=self.ascID)
            self.Bind(wx.EVT_MENU, self.OnPopupDesc, id=self.descID)


        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.ascID,"Tri ASC")

        menu.AppendItem(item)
        # add some other items
        menu.Append(self.descID, "Tri DESC")




        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def OnRowMenu(self, event):

        if not hasattr(self, "ROWID"):
            self.ROWID1 = wx.NewId()
            self.ROWID2 = wx.NewId()
            self.ROWID3 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.OnPopupDel, id=self.ROWID1)
            self.Bind(wx.EVT_MENU, self.OnAddRow, id=self.ROWID2)
            self.Bind(wx.EVT_MENU, self.OnPopupRow3, id=self.ROWID3)


        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.ROWID1,"Supprimer")

        menu.AppendItem(item)
        # add some other items
        menu.Append(self.ROWID2, "Ajouter")





        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def OnAddRow(self,e):
        self.InsertRows(self.row+1, 1,True)
        self.insert = True



    def suppr(self,db,table,where):
        r = "DELETE from \""+table+"\"  where "+ where + ""
        conn      = psycopg2.connect("dbname="+db+" user=postgres password=123456  host= localhost") #prod
        conn.set_isolation_level(0)
        curseur = conn.cursor()
        curseur.execute(r)
        conn.close()

    def tri_column(self,colunm,tri='ASC'):
        """
            Trier l'affichage en fonction du champ double cliqué
        """
        ordre = self.tableColumn[colunm]
        self.ClearGrid()
        tzResults          = self.extraction(self.connexion,self.table,ordre,tri)
        nbLigne            = self.getNligne(tzResults)
        nbCols             = len(self.tableColumn)
        self.createTable(nbLigne,nbCols,self.tableColumn,tzResults)

    def errorDlg(self,title,message):
       msg = wx.MessageDialog ( None, message, caption=title,style=wx.ICON_ERROR|wx.OK , pos=wx.DefaultPosition )
       msg .ShowModal()
       return msg

    def InfoDlg(self,title,message):
       msg = wx.MessageDialog ( None, message, caption=title,style=wx.OK , pos=wx.DefaultPosition )
       msg .ShowModal()
       return msg




    def Warndlg(self,title,message):
        """
            Message d'avertissement (warninbg)
        """
        msg = wx.MessageDialog ( None, message, caption=title,style=wx.ICON_WARNING|wx.OK , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg



class MegaTable(wx.grid.PyGridTableBase):
    """
    A custom wx.Grid Table using user supplied data
    """
    def __init__(self, data, colnames, plugins,dbname='',tablename='',key='',gr=None):
        """data is a list of the form
        [(rowname, dictionary),
        dictionary.get(colname, None) returns the data for column
        colname
        """
        # The base class must be initialized *first*
        wx.grid.PyGridTableBase.__init__(self)
        if gr!=None:
            self.gr = gr
        self.data = data
        for row in range(len(self.data)):
            for col in range(len(self.data[row])):
                if self.data[row][col]==None:
                    self.data[row][col]=''

        self.data0 = data
        self.colnames = colnames
        self.plugins = plugins or {}
        # we need to store the row length and column length to
        # see if the table has changed size
        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()
        self.dbname    = dbname
        self.tablename = tablename
        self.keyname   = key
        self.idcom = 'EDF001'

    def GetNumberCols(self):
        return len(self.colnames)

    def GetNumberRows(self):
        return len(self.data)

    def GetColLabelValue(self, col):
        return self.colnames[col]

    #def GetRowLabelValue(self, row):
        #pass
        #return "row %03d" % int(self.data[row][0])

    def GetValue(self, row, col):

        return (self.data[row][col])

    def GetRawValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        #self.SetValue(row, col, value)
        self.data[row][col] = value
        pass

    def ResetView(self, grid):
        """
        (Grid) -> Reset the grid view.   Call this to
        update the grid if rows and columns have been added or deleted
        """
        grid.BeginBatch()

        for current, new, delmsg, addmsg in [
            (self._rows, self.GetNumberRows(), wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
            (self._cols, self.GetNumberCols(), wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED, wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED),
        ]:

            if new < current:
                msg = wx.grid.GridTableMessage(self,delmsg,new,current-new)
                grid.ProcessTableMessage(msg)
            elif new > current:
                msg = wx.grid.GridTableMessage(self,addmsg,new-current)
                grid.ProcessTableMessage(msg)
                self.UpdateValues(grid)

        grid.EndBatch()

        self._rows = self.GetNumberRows()
        self._cols = self.GetNumberCols()
        # update the column rendering plugins
        self._updateColAttrs(grid)

        # update the scrollbars and the displayed part of the grid
        grid.AdjustScrollbars()
        grid.ForceRefresh()


    def UpdateValues(self, grid):
        """Update all displayed values"""
        # This sends an event to the grid table to update all of the values
        msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
        grid.ProcessTableMessage(msg)

    def _updateColAttrs(self, grid):
        """
        wx.Grid -> update the column attributes to add the
        appropriate renderer given the column name.  (renderers
        are stored in the self.plugins dictionary)

        Otherwise default to the default renderer.
        """
        col = 0

        for colname in self.colnames:
            attr = wx.grid.GridCellAttr()
            if colname in self.plugins:
                renderer = self.plugins[colname](self)

                if renderer.colSize:
                    grid.SetColSize(col, renderer.colSize)

                if renderer.rowSize:
                    grid.SetDefaultRowSize(renderer.rowSize)

                attr.SetReadOnly(True)
                attr.SetRenderer(renderer)

            grid.SetColAttr(col, attr)
            col += 1


    def getColImage(self,zChampImage):
        tzCol = self.colnames
        I=0
        for elm in tzCol:
            if elm==zChampImage:
                return I
            I=I+1
        return I

    # ------------------------------------------------------
    # begin the added code to manipulate the table (non wx related)


    def affiche(self,col=0):
        name = self.colnames[col]
        _data = []
        for row in self.data0:
            rowname, entry = row , row
            part1 =  (row[col])
#            _data.append((entry.get(name, None), row))
            _data.append((part1, row))
        #_data = sorted(_data, key=lambda name: name[0],reverse=rev)
        _data.sort()
        self.data = []
        for sortvalue, row in _data:
            self.data.append(row)

    def AppendRow0(self, row):
        #print 'append'
        entry = {}

        for name in self.colnames:
            entry[name] = "Appended_%i"%row

        # entry["A"] can only be between 1..4
        entry["A"] = random.choice(range(4))
        self.data.insert(row, ["Append_%i"%row, entry])



    def AppendRow(self,row,fin=False):
        enr = self.GetValue(row,self.getColImage("n_enr"))
        nima = self.GetValue(row,self.getColImage("n_ima"))

        #connexion en base ------------------#
        local      = psycopg2.connect("dbname="+self.dbname+" user=postgres password=123456  host= localhost") #prod
        local.set_client_encoding('WIN1252')
        local.set_isolation_level(0)
        curlocal  = local.cursor(cursor_factory=psycopg2.extras.DictCursor);

        #---- ENR
        curlocal.execute("select max(\"n_enr\") as enrmax from \""+self.tablename+"\" where \"n_ima\" ='"+nima+"'")
        tzEnrMax = curlocal.fetchone()
        if tzEnrMax!=None:
            if tzEnrMax[0]!=None:
                newenr = self.formatesLigne(int(tzEnrMax[0])+1)
            else:
                newenr = '0001'
        else:
            newenr = '0001'
        newenr = self.formatesLigne(int(enr)+1)
         #---- IDENR
        curlocal.execute("select max(\"idenr\") as idenrmax from \""+self.tablename+"\"  ")
        tzIdenrMax = curlocal.fetchone()

        curlocal.execute("select * from \""+self.tablename+"\" where  \"n_enr\">'"+enr+"' order by \"n_enr\"")
        tzData2Update = curlocal.fetchall()
        i= int(newenr)+1
        for enregistrement  in tzData2Update:
            curlocal.execute("update \""+self.tablename+"\" set \"n_enr\"='"+self.formatesLigne(i)+"' where idenr='"+str(enregistrement['idenr'])+"' ")
            i=i+1
        if tzIdenrMax!=None:
            if tzIdenrMax[0]!=None:
                newidenr = (int(tzIdenrMax[0])+1)
            else:
                newidenr = 1
        else:
            newidenr = 1

        curlocal.execute("select * from \""+self.tablename+"\" where \"n_enr\"='"+enr+"' and \"n_ima\"='"+nima+"'")
        tzSelect = curlocal.fetchone()
        #Invention des données à manipuler ------------------------#
        tablcols = []
        colonnesStatic = ['MATRICULE','ID_COMMANDE','COMMANDE','ETAPE','N_LOT','LIST_IMA','IDEXECUTE','IDEXECUTEC','DATE_SAISIE','__S','DATE_CREA','X','Y','Z']

        for champ in self.colnames:
            if champ.upper() in colonnesStatic:
                tablcols.append(tzSelect[champ])
            elif champ =='n_enr':
                tablcols.append(newenr)
            elif champ.upper()=='IDENR':
                tablcols.append(newidenr)
            else:
                tablcols.append('')

        #Insertion des données sur la table en vue -------------"
        if row==0:
            #self.data.insert(1, tablcols)
            self.data.insert(1, tablcols)
        else:
            #self.data.insert(row+1, tablcols)
            self.data.insert(row+1, tablcols)
        self.insertTotable(self.tablename,self.colnames,tablcols,local)
        #Récupération clé d'enregistrement-------------------------#
        curlocal.execute("select * from \""+self.tablename+"\" order by \"n_enr\" ")
        tzNewData = curlocal.fetchall()
        self.data = tzNewData
        self.data0 = tzNewData
        if self.gr != None:

            self.gr.SelectRow(row+1)
            self.ResetView(self.gr)
            self.gr.MakeCellVisible(row+1,0)

        #clôture connexion ------------------#
        local.close()


    def AppendRowfin(self, row=0,fin=True):
        rowfin = self.GetNumberRows()-1
        enr = self.GetValue(rowfin,self.getColImage("n_enr"))
        nima = self.GetValue(rowfin,self.getColImage("n_ima"))
#        print 'fin:',enr
        #connexion en base ------------------#
        local      = psycopg2.connect("dbname="+self.dbname+" user=postgres password=123456  host= localhost") #prod
        local.set_client_encoding('WIN1252')
        local.set_isolation_level(0)
        curlocal  = local.cursor(cursor_factory=psycopg2.extras.DictCursor);

        #---- ENR
        curlocal.execute("select max(\"n_enr\") as enrmax from \""+self.tablename+"\" where \"n_ima\" ='"+nima+"'")
        tzEnrMax = curlocal.fetchone()
        if tzEnrMax!=None:
            if tzEnrMax[0]!=None:
                newenr = self.formatesLigne(int(tzEnrMax[0])+1)
            else:
                newenr = '0001'
        else:
            newenr = '0001'
        newenr = self.formatesLigne(int(enr)+1)
         #---- IDENR
        curlocal.execute("select max(\"idenr\") as idenrmax from \""+self.tablename+"\"  ")
        tzIdenrMax = curlocal.fetchone()


        if tzIdenrMax!=None:
            if tzIdenrMax[0]!=None:
                newidenr = (int(tzIdenrMax[0])+1)
            else:
                newidenr = 1
        else:
            newidenr = 1
        curlocal.execute("select * from \""+self.tablename+"\" where \"n_enr\"='"+enr+"' and \"n_ima\"='"+nima+"'")
        tzSelect = curlocal.fetchone()
        #Invention des données à manipuler ------------------------#
        tablcols = []
        colonnesStatic = ['MATRICULE','ID_COMMANDE','COMMANDE','ETAPE','N_LOT','LIST_IMA','IDEXECUTE','IDEXECUTEC','DATE_SAISIE','__S','DATE_CREA','X','Y','Z']

        for champ in self.colnames:
            if champ.upper() in colonnesStatic:
                tablcols.append(tzSelect[champ])
            elif champ =='n_enr':
                tablcols.append(newenr)
            elif champ.upper()=='IDENR':
                tablcols.append(newidenr)
            else:
                tablcols.append('')

        #Insertion des données sur la table en vue -------------"
        self.data.insert(self.GetNumberRows(), tablcols)
        self.insertTotable(self.tablename,self.colnames,tablcols,local)
        #Récupération clé d'enregistrement-------------------------#
        curlocal.execute("select * from \""+self.tablename+"\" order by \"n_enr\" ")
        tzNewData = curlocal.fetchall()
        self.data = tzNewData
        self.data0 = tzNewData
        if self.gr != None:
            self.ResetView(self.gr)
            self.gr.SelectRow(rowfin+1)
            self.gr.MakeCellVisible(rowfin+1,0)

        #clôture connexion ------------------#
        local.close()


    def insertTotable(self,table,tzChamp,tzValue,connexion):
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
                curser = connexion.cursor()
                curser.execute("SET client_encoding = 'WIN1252'; ")
                connexion.commit()
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
                #print sql
                curs = connexion.cursor()
                curs.execute(sql)
                return True
            except Exception as inst:
                msgs =  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
                msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
                self.errorDlg('erreur',msgs)
                return False

        else:
            self.errorDlg("Erreur fatal","Nombres des colonnes non identiques")
            return False

    def getIndiceCol(self,sCol):
        i=0
        while i<len(self.colnames):
            if self.colnames[i]==sCol:
                return i
            i=i+1
        return None

    def getNCol(self,tabCol,strCol):
        str = ''
        I=0
        while(I<len(tabCol)):
            if(tabCol[I]==strCol):
                str=strCol
                return I
            I=I+1
        return I

    def formatesLigne(self,iNombre):
        """ Formater un chiffre en format de 3 chiffre """
        if(iNombre<10):
            zFormt = '000'+str(iNombre)
            return zFormt
        elif(iNombre<100):
            zFormt = '00'+ str(iNombre)
            return zFormt
        elif(iNombre<1000):
            zFormt = '0'+ str(iNombre)
            return zFormt
        else:
            return iNombre

    def DeleteCols(self, cols):
        """
        cols -> delete the columns from the dataset
        cols hold the column indices
        """
        # we'll cheat here and just remove the name from the
        # list of column names.  The data will remain but
        # it won't be shown
        deleteCount = 0
        cols = cols[:]
        cols.sort()
        local      = psycopg2.connect("dbname="+self.dbname+" user=postgres password=123456  host= localhost") #prod
        local.set_client_encoding('WIN1252')
        local.set_isolation_level(0)
        curlocal  = local.cursor(cursor_factory=psycopg2.extras.DictCursor);

        for i in cols:
            curlocal.execute("ALTER TABLE \""+self.tablename+"\" DROP COLUMN \""+self.colnames[i]+"\";")
            self.colnames.pop(i-deleteCount)
            for j in self.data:
                j.pop(i-deleteCount)
            deleteCount += 1
        if not len(self.colnames):
            self.data = []
        local.close()


    def DeleteRows0(self, rows):
        """
        rows -> delete the rows from the dataset
        rows hold the row indices
        """
        deleteCount = 0
        rows = rows[:]
        rows.sort()

        for i in rows:
            self.data.pop(i-deleteCount)
            # we need to advance the delete count
            # to make sure we delete the right rows
            deleteCount += 1


    def DeleteRows(self, rows):
        """
        rows -> delete the rows from the dataset
        rows hold the row indices
        """
        numkeycol = self.getIndiceCol(self.keyname)
        rows = rows[:]
        deleteCount = 0
        if numkeycol!=None:
            valkey = self.GetValue(rows[0],numkeycol)
        else:
            valkey = ' '
        deleteCount = 0
        rows = rows[:]
        rows.sort()
        conf = wx.MessageDialog ( None, 'Voulez-vous vraiment supprimer '+str(len(rows))+' enregistrement(s) selectioné(es) ?', caption='Confirmation',style=wx.YES_NO | wx.ICON_WARNING , pos=wx.DefaultPosition )
        if(conf.ShowModal() == wx.ID_NO):
            return False
        local      = psycopg2.connect("dbname="+self.dbname+" user=postgres password=123456  host= localhost") #prod
        local.set_client_encoding('WIN1252')
        local.set_isolation_level(0)
        curlocal  = local.cursor(cursor_factory=psycopg2.extras.DictCursor);

        for i in rows:
            valkey = self.GetValue(i-deleteCount,numkeycol)
#            conf = wx.MessageDialog ( None, 'Voulez-vous vraiment executer la requette:'+REQ+' ?', caption='Confirmation',style=wx.YES_NO | wx.ICON_WARNING , pos=wx.DefaultPosition )
#            if(conf.ShowModal() == wx.ID_NO):
#                return False
            REQ = "delete from \""+self.tablename+"\" where \""+self.keyname+"\"='"+str(valkey)+"'"
            curlocal.execute(REQ)

            # we need to advance the delete count
            # to make sure we delete the right rows
            self.data.pop(i-deleteCount)
            deleteCount += 1
        curlocal.execute("select * from \""+self.tablename+"\" order by \"n_enr\" ")
        tzNewData = curlocal.fetchall()
        self.data = tzNewData
        self.data0 = tzNewData

        if self.gr!=None:
            self.gr.ClearSelection()
            self.ResetView(self.gr)
        local.close()

    def SortColumn(self, col,rev=False):
        """
        col -> sort the data based on the column indexed by col
        """
        name = self.colnames[col]
        name2 = self.colnames[col+2]
        _data = []
        for row in self.data:
            rowname, entry = row , row
            part1 =  (row[col])
            _data.append((part1, row))
        #sorted(_data, key=lambda name: name[0],reverse=rev).sort(reverse=rev,key=lambda name2: name2[0])
#        _data.sort(key=lambda name:name[0].encode('cp1252'), reverse=rev)
        _data.sort(reverse=rev)
        #_data
        self.data = []
        for sortvalue, row in _data:
            self.data.append(row)


    def filtrer(self,col,value=None,rev=False):
        if value!=None:
            name = self.colnames[col]
            _data = []
            for row in self.data:
                if row[col]==value.encode('cp1252'):
                    rowname, entry = row , row
                    part1 =  (row[col])
                    _data.append((part1, row))
            #_data = sorted(_data, key=lambda name: name[0],reverse=rev)
            _data.sort(reverse=rev)
            self.data = []
            for sortvalue, row in _data:
                self.data.append(row)
        else:
            pass




class MegaGrid(wx.grid.Grid):
    def __init__(self, parent, data, colnames, plugins=None):
        """parent, data, colnames, plugins=None
        Initialize a grid using the data defined in data and colnames
        (see MegaTable for a description of the data format)
        plugins is a dictionary of columnName -> column renderers.
        """
        # The base class must be initialized *first*
        wx.grid.Grid.__init__(self, parent, -1)
        self._table = MegaTable(data, colnames, plugins)
        self.SetTable(self._table)
        self._plugins = plugins

        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClicked)

    def Reset(self):
        """reset the view based on the data in the table.  Call
        this when rows are added or destroyed"""
        self._table.ResetView(self)

    def OnLabelRightClicked(self, evt):
        # Did we click on a row or a column?
        row, col = evt.GetRow(), evt.GetCol()
        if row == -1: self.colPopup(col, evt)
        elif col == -1: self.rowPopup(row, evt)

    def rowPopup(self, row, evt):
        """(row, evt) -> display a popup menu when a row label is right clicked"""
        appendID = wx.NewId()
        deleteID = wx.NewId()
        x = self.GetRowSize(row)/2

        if not self.GetSelectedRows():
            self.SelectRow(row)

        menu = wx.Menu()
        xo, yo = evt.GetPosition()
        menu.Append(appendID, "Append Row")
        menu.Append(deleteID, "Delete Row(s)")

        def append(event, self=self, row=row):
            self._table.AppendRow(row)
            self.Reset()

        def delete(event, self=self, row=row):
            rows = self.GetSelectedRows()
            self._table.DeleteRows(rows)
            self.Reset()

        self.Bind(wx.EVT_MENU, append, id=appendID)
        self.Bind(wx.EVT_MENU, delete, id=deleteID)
        self.PopupMenu(menu)
        menu.Destroy()
        return


    def colPopup(self, col, evt):
        """(col, evt) -> display a popup menu when a column label is
        right clicked"""
        x = self.GetColSize(col)/2
        menu = wx.Menu()
        id1 = wx.NewId()
        sortID = wx.NewId()

        xo, yo = evt.GetPosition()
        self.SelectCol(col)
        cols = self.GetSelectedCols()
        self.Refresh()
        #menu.Append(id1, "Delete Col(s)")
        menu.Append(sortID, "Sort Column")

        def delete(event, self=self, col=col):
            cols = self.GetSelectedCols()
            self._table.DeleteCols(cols)
            self.Reset()

        def sort(event, self=self, col=col):
            self._table.SortColumn(col)
            self.Reset()

        self.Bind(wx.EVT_MENU, delete, id=id1)

        if len(cols) == 1:
            self.Bind(wx.EVT_MENU, sort, id=sortID)

        self.PopupMenu(menu)
        menu.Destroy()
        return


    def affiche(self,col=0):
        name = self.colnames[col]
        _data = []
        for row in self.data0:
            rowname, entry = row , row
            _data.append((entry.get(name, None), row))
        #_data = sorted(_data, key=lambda name: name[0],reverse=rev)
        _data.sort()
        self.data = []
        for sortvalue, row in _data:
            self.data.append(row)


class DialogBox(wx.Dialog):
    """
        Classe d'affichage d'un popup d'aide cp - villeDat
        parametre constructeur :
            parent : window conteneur :(peut être None)
            tzRecord : les enregistrement à afficher
            tzCol : tableau contenant les elements du titre du tableau
            widgville : objet controle zone de texte ville
    """
    def __init__(self, parent,tzTable=[],col=-1,dbname ='',nomtable=''):
        """ Constructeur : controle : champs destination,tzRecord: tableau des valeurs à afficher,tzCol : tableau contenant les entetes,Ndata : numéro de colonne contenant le donné à renvoyer"""
        largeur = 300
        hauteur = 190
        tscreen =  wx.GetClientDisplayRect()
        self.SizeXConteneur = tscreen[2]*62.5/100
        self.SizeYConteneur = tscreen[3]*58.6/100
        #largeur = self.SizeXConteneur+20
        #hauteur = self.SizeYConteneur+35
        self.parent = parent
        self._table = tzTable
        self.dbname = dbname
        self.tablename = nomtable
        wx.Dialog.__init__(self, parent, title = "Ajout d'une colonne",style = wx.WANTS_CHARS|wx.SYSTEM_MENU|wx.CAPTION | wx.CLOSE_BOX, size = (largeur, hauteur))
        wx.StaticText(self,-1,'Nom:',pos=(30,30))
        self.nom = wx.TextCtrl(self,-1,pos=(90,25),size=(150,25))
        wx.StaticText(self,-1,'Data type:',pos=(30,60))
        self.type = wx.TextCtrl(self,-1,pos=(90,55),size=(150,25))

        self.btok = wx.Button(self,-1,'Valider',pos=(30,100))
        self.btnotOk = wx.Button(self,-1,'Annuler',pos=(130,100))

        # --- Evennement
        if col==-1:
            self.colcible = len(self._table.colnames)
        else:
            self.colcible = col
        self.btok.Bind(wx.EVT_BUTTON,  lambda event:self.ajouterCol(event,self.colcible,self.nom.GetValue()))
        self.btnotOk.Bind(wx.EVT_BUTTON, self.fermer)

        #try:
        self.local  = psycopg2.connect("dbname="+self.dbname+" user=postgres password=123456  host= localhost") #prod
        self.local.set_client_encoding('WIN1252')
        self.local.set_isolation_level(0)
        self.curlocal  = self.local.cursor(cursor_factory=psycopg2.extras.DictCursor);
        #except:
        #    pass


        self.ShowModal()

    def fermer(self,e):
        self.local.close()
        self.Destroy()

    def ajouterCol(self,e,iCol,sCol='',sType='Text'):
        self._table.colnames.insert(iCol+1,sCol)
        for i in self._table.data:
            i.insert(iCol+1,'')
        self._table.ResetView(self.parent)
        sql ="ALTER TABLE \""+self.tablename+"\" ADD COLUMN \""+sCol+"\" "+sType+";"
        self.curlocal.execute(sql)
        self.local.close()
        self.Destroy()





class MegaFontRenderer(wx.grid.PyGridCellRenderer):
    def __init__(self, table, color="blue", font="ARIAL", fontsize=10):
        """Render data in the specified color and font and fontsize"""
        wx.grid.PyGridCellRenderer.__init__(self)
        self.table = table
        self.color = color
        self.font = wx.Font(fontsize, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, font)
        self.selectedBrush = wx.Brush("blue", wx.SOLID)
        self.normalBrush = wx.Brush(wx.WHITE, wx.SOLID)
        self.colSize = None
        self.rowSize = 50

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        # Here we draw text in a grid cell using various fonts
        # and colors.  We have to set the clipping region on
        # the grid's DC, otherwise the text will spill over
        # to the next cell
        dc.SetClippingRect(rect)

        # clear the background
        dc.SetBackgroundMode(wx.SOLID)

        if isSelected:
            dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
        dc.DrawRectangleRect(rect)

        text = self.table.GetValue(row, col)
        dc.SetBackgroundMode(wx.SOLID)

        # change the text background based on whether the grid is selected
        # or not
        if isSelected:
            dc.SetBrush(self.selectedBrush)
            dc.SetTextBackground("blue")
        else:
            dc.SetBrush(self.normalBrush)
            dc.SetTextBackground("white")

        dc.SetTextForeground(self.color)
        dc.SetFont(self.font)
        dc.DrawText(text, rect.x+1, rect.y+1)

        # Okay, now for the advanced class :)
        # Let's add three dots "..."
        # to indicate that that there is more text to be read
        # when the text is larger than the grid cell

        width, height = dc.GetTextExtent(text)

        if width > rect.width-2:
            width, height = dc.GetTextExtent("...")
            x = rect.x+1 + rect.width-2 - width
            dc.DrawRectangle(x, rect.y+1, width+1, height)
            dc.DrawText("...", x, rect.y+1)

        dc.DestroyClippingRegion()


class fenetre(wx.Frame):
    def __init__(self, parent,table,db,key='idenr',idcom=0,nomcommande=0,wdgchecksta=None,where='',tchampvue=[]):
        tscreen =  wx.GetClientDisplayRect()
        self.SizeXConteneur = tscreen[2]*98/100
        self.SizeYConteneur = tscreen[3]*95/100


        wx.Frame.__init__(self, None, -1, table,size=(self.SizeXConteneur, self.SizeYConteneur/2),pos=(10,10))
        grid = afficheGrid(self,table,db,key,nomcommande=nomcommande,where=where,tchampvue=tchampvue,pos=(10,70))



