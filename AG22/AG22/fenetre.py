#!/usr/bin/env python
# -*- coding: cp1252  -*-
import wx,os
import psycopg2
import psycopg2.extras
import wx.grid
import sys
import warnings
wx.Log.EnableLogging(True)

class MainApp(wx.App):
    def OnInit(self,title='FORMULAIRE DE SAISIE',size=(600,300),dbname='SUR900_format_db',top=False):
        """ Création de la fenêtre principale """
        frame = MainWindow(title,size,dbname,top)
        self.TopWindow(frame)
        return True
        
         

class MainWindow(wx.Frame):
    
    def __init__(self, title,size=(600,300),dbname=''):
        self.size = size
        self.incH = 15
        self.incW = 15   
        self.inc = 1
        self.defaultcol1size = 150
        self.defaultcol1pos = 0
        self.image = None
        self.imgORIG = None
        self.facteur = 100
        self.conteneurimage = None
        self.dbname= dbname
        self.idtext = 1
        
        tscreen =  wx.GetClientDisplayRect()
        wx.Frame.__init__(self, None, wx.ID_ANY, title=title, size=size)
        
        self.Show(True)
        
    
      

    def conteneurPanel(self,pos,size,id=wx.ID_ANY):
        
        return wx.Panel(self,pos=pos,style=wx.BORDER_DOUBLE|wx.TAB_TRAVERSAL,size=size,id=id)



    def seticone(self,pathicon):
        frameicon = wx.Icon(pathicon, wx.BITMAP_TYPE_ICO)
        self.SetIcon(frameicon)
    

    def menubars(self):
        menu = wx.Menu() 
        

        self.itemMenuCsta = wx.MenuItem(menu, wx.ID_ANY, "Controle Standard")
        self.itemMenuQuitter = wx.MenuItem(menu, wx.ID_ANY, "&Quitter")
        
        menu.AppendItem(self.itemMenuCsta)
        menu.AppendSeparator()
        menu.AppendItem(self.itemMenuQuitter)
        

        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&Menu");
        
        menuBar.SetSize((100,30))
        self.SetMenuBar(menuBar)
    
    def events(self,type,fonction,compos):
        return self.Bind(type, fonction, compos)

    def fermer(self,e):
        self.Close()
    
    def addLabel(self,parent,texte='',colaling=0,bordercolor='black',fg='black',fcolor=(0,0,255),fstyle=wx.NORMAL,debut=0,pos=0,size=0):
        x=25
        y=45
        tzComp = parent.GetChildren()
        nbComp = len(tzComp)
        if(nbComp>0):
            dernierComp = tzComp[nbComp-1]
            xypos = dernierComp.GetPosition()
            sizewh = dernierComp.GetSize()
            
            if colaling==0:
                y= xypos[1] + sizewh[1]+self.incH
            else:
                x = xypos[0] + sizewh[0] + self.incW

                y = xypos[1]
        if debut==1:
            y=25
        if pos!=0:
            x,y = pos
        
        label = wx.StaticText(parent, wx.ID_ANY,texte,pos=(x,y),style=wx.BORDER)
        label.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, fstyle))
        label.SetForegroundColour(fcolor)
        return label



    def AddTexte(self,parent,colaling=0,sizeX = 200,col=2,bg=(255,255,255),isnum=0,table='',max=0,min=0,name='',outext=None,vide=1,D2=0):
        x=25
        y=45
        tzComp = parent.GetChildren()
        nbComp = len(tzComp)
        
        if(nbComp>0):
            dernierComp = tzComp[nbComp-1]
            xypos = dernierComp.GetPosition()
            sizewh = dernierComp.GetSize()
            if colaling==0:
                y= xypos[1] + sizewh[1]+self.incH
            else:
                if(sizewh[0]<self.defaultcol1size and col==2):
                    x = xypos[0] +self.defaultcol1size+ self.incW
                else:
                    x = xypos[0] + sizewh[0] + self.incW
                y = xypos[1]

        label = wx.TextCtrl(parent, value='', pos=(x,y),size=(sizeX,25), style=0,name='E_'+name)
        label.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL,wx.NORMAL))
        label.SetBackgroundColour(bg)
        if max>0 :
            label.SetMaxLength(max)
        
        
        
        return label
    


    def AddButton(self,parent,labels='',colaling=0,sizeX = 150,col=0):
        x=25
        y=25
        tzComp = parent.GetChildren()
        nbComp = len(tzComp)
        if(nbComp>0):
            dernierComp = tzComp[nbComp-1]
            xypos = dernierComp.GetPosition()
            sizewh = dernierComp.GetSize()
             
                
            if colaling==0:
                y= xypos[1] + sizewh[1]+self.incH
            else:
                x = xypos[0] + sizewh[0] + self.incW

                y = xypos[1]
        
        btn = wx.Button(parent, id=-1, label=labels, pos=(x,y),size=(sizeX,30)) 
        
        return btn

    
    def AddListeCtrl(self,parent,colaling=0,sizeX = 200,col=2,bg=(255,255,255),max=0,min=0,name='',defaultposX =None,defaultposY =None,sizeY=200):
        """ methode d'ajout d'un widget liste controle 
            parametres:
                parent : conteneur
                sizeX : largeur
                col : alignement vertical (pour une interface standard, sa valeur par defaut est dejà mieux
                colaling : 0 ou 1 : si 1 le widget sera placé aligné au controle precedant dans le conteneur, si non, le widget sera placé à la ligne
                bg : couleur de la bachground
                fcolor: couleur du texte
                fstyle : style du widget
                max : nombre max de caracter
                min nombre min de caractere
                name : identifiant du controle
            valeur de retour : objet controle zone de texte
        """
        x=25
        y=25
        tzComp = parent.GetChildren()
        nbComp = len(tzComp)
        
        if(nbComp>0):
            dernierComp = tzComp[nbComp-1]
            xypos = dernierComp.GetPosition()
            sizewh = dernierComp.GetSize()
            if colaling==0:
                y= xypos[1] + sizewh[1]+self.incH
            else:
                if(sizewh[0]<self.defaultcol1size and col==2):
                    x = xypos[0] +self.defaultcol1size+ self.incW
                else:
                    x = xypos[0] + sizewh[0] + self.incW
                y = xypos[1]
        if defaultposX!= None:
            x= defaultposX 
        if defaultposY!= None:
            y= defaultposY 
        
        label = wx.ListCtrl(parent,  pos=(x,y),size=(sizeX,sizeY), name='L_'+name,style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|wx.SUNKEN_BORDER|wx.LC_AUTOARRANGE)
        label.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL,wx.NORMAL))
        label.SetBackgroundColour(bg)
        if max>0 :
            label.SetMaxLength(max)
        if min>0:
            label.SetMinLength(min) 
        
        return label
    


if __name__ == "__main__":
    app = MainApp() 
    app.MainLoop()
