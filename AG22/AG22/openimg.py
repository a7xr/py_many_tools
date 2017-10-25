#!/usr/bin/env python
# -*- coding: cp1252  -*-
import wx,os,stat,sys,shutil,psycopg2,psycopg2.extras
wx.Log.EnableLogging(False)
class MainApp(wx.App):
    def OnInit(self):
        """ Création de l application """
        frame = MainWindow('20110504_GJPJ_006..TIF')
        self.SetTopWindow(frame)
        return True


class MainWindow(wx.Frame):
    def __init__(self,urlImage='20110504_GJPJ_006..TIF',lot='',pli='',n_ima=''):
        testimg = wx.Image(urlImage,wx.BITMAP_TYPE_ANY)
        urlorig = urlImage
        self.urlImage = urlImage
        self.nima = os.path.basename(urlorig)
        self.nomimage=n_ima
        self.pli = pli
        self.inc = 1
        self.image = None
        self.facteur =80
        if os.access(urlImage,os.F_OK)==False:
            urlImage = self.getUrlExact(urlImage)
            urlorig =  urlImage
        tscreen =  wx.GetClientDisplayRect()
        if os.access("C:/image/",os.F_OK)==False:
            os.mkdir("C:/image/")
            
        self.SizeXConteneur = tscreen[2]*98/100
        self.SizeYConteneur = tscreen[3]*95/100
        if os.access(urlImage,os.F_OK)==False:
            msg = wx.MessageDialog (None, 'Image non disponible dans '+str(urlImage), caption='Erreur Image',style=wx.ICON_ERROR|wx.OK , pos=wx.DefaultPosition )  
            msg .ShowModal()
        else:

            try:
                shutil.copy(urlImage,"C:/image/x"+os.path.splitext(urlImage)[1])
                if os.path.exists("C:/image/x"+os.path.splitext(urlImage)[1]):
                    urlImage = "C:/image/x"+os.path.splitext(urlImage)[1]
                    test = wx.Image(urlImage,wx.BITMAP_TYPE_ANY)
                    if test.IsOk()==False:
                        os.popen("convert "+urlImage+" -quality 100% "+urlImage+"")    
            except Exception as inst:
                msgs =  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
                msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
                self.errorDlg('erreur',msgs)

            try:
                image = wx.Image(urlImage,wx.BITMAP_TYPE_ANY)
                self.imgORIG = image
                hImg = image.GetHeight()
                self.imgORIX    = self.imgORIG.GetWidth()
                self.imgORIY    = self.imgORIG.GetHeight()
                
                wx.Frame.__init__(self, None, wx.ID_ANY, title=urlorig, size=(self.SizeXConteneur, self.SizeYConteneur/2),pos=(20,self.SizeYConteneur/2+10))
                self.conteneurimage  = wx.ScrolledWindow(self,pos=(5,5),style=wx.BORDER_DOUBLE,size=(self.SizeXConteneur,self.SizeYConteneur)) # image
                self.largeur = (self.imgORIX * self.facteur)/100
                self.hauteur = (self.imgORIY * self.facteur)/100
                self.bmpRESU = self.imgORIG.Scale(self.largeur, self.hauteur).ConvertToBitmap()
                #bmpRESU    = image.ConvertToBitmap()
                self.image = self.Affiche(self.bmpRESU,self.conteneurimage,facteur=self.facteur)
                
                self.Show(True)
                    
            except Exception as inst:
                msgs =  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
                msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
                self.errorDlg('erreur',msgs)
            
            
            self.inc = 5
            self.Bind(wx.EVT_KEY_DOWN,self.keydown)
            self.conteneurimage.Bind(wx.EVT_CHAR,self.keyChar)
            self.Bind(wx.EVT_MOUSEWHEEL,self.molette)
            
    
    def keyChar(self,e):
        """
            Metode permettant de definir des processus lors d'un evennment inFOcus d'une zone de texte
            Parametre : objet evennement  
        """
        
        obj = e.GetEventObject()
        key = e.GetKeyCode()
        print key
        if key==17:
            self.tournerImage(e,False)
        elif key==4:
            self.tournerImage(e)
        else:
            e.Skip()
    
        # ----- CREATION FENETRE PRINCIPALE  / CONTENEUR / INDICATION --- #
    def keydown(self,e):
        if e.GetKeyCode()==315:
            self.decaleMoins('y',self.inc)  
        elif e.GetKeyCode()==317:
            self.decalePlus('y',self.inc)
        elif e.GetKeyCode()==314:
            self.decaleMoins('x',self.inc)
        elif e.GetKeyCode()==316:
            self.decalePlus('x',self.inc)

        elif e.GetKeyCode()==wx.WXK_F7:
            self.zoomMoins(e)
        elif e.GetKeyCode() == wx.WXK_F8:
            self.zoomplus(e)
        elif e.GetKeyCode()==wx.WXK_F12:
            self.imagesuiv(e)
        elif e.GetKeyCode()==wx.WXK_F11:
            self.imageprec(e)
        elif chr(e.GetKeyCode())=='Q':
            self.tournerImage(e,False)
        elif chr(e.GetKeyCode())=='D':
            self.tournerImage(e)
        

        
        else:
            pass
 
    
    def setimage(self,url,facteur):
        """ 
              Methode affichant une image quelconque dans un conteneur avec la methode afficheaide
              parametre:
                  url : le chemin physique de l'image
                  contimg : conteneur
                  facteur : le facteur de zoom
              retour : objet image
        """
        self.facteur = facteur
        if os.access("C:/image/",os.F_OK)==False:
            os.makedirs("C:/image/")
        shutil.copy(url,"C:/image/x%s"%(os.path.splitext(os.path.basename(url))[1]))
        urlaff = "C:/image/x%s"%(os.path.splitext(os.path.basename(url))[1])
        
        if wx.Image(urlaff,wx.BITMAP_TYPE_ANY).IsOk()==False:
            try:
                os.popen("convert "+urlaff+" -quality 100% "+urlaff+"")
            except Exception as inst:
                msgs =  'type ERREUR:'+str(type(inst))+'\n'     # the exception instance
                msgs+=  'CONTENU:'+str(inst)+'\n'           # __str__ allows args to printed directly
                self.errorDlg('erreur',msgs)
        
        self.imgORIG    = wx.Image(urlaff,wx.BITMAP_TYPE_ANY)
        self.imgORIG_0 = wx.Image(url,wx.BITMAP_TYPE_ANY)
        self.imgORIX    = self.imgORIG.GetWidth()
        self.imgORIY    = self.imgORIG.GetHeight()
        self.largeur = (self.imgORIX * self.facteur)/100
        self.hauteur = (self.imgORIY * self.facteur)/100
        self.bmpRESU = self.imgORIG.Scale(self.largeur, self.hauteur).ConvertToBitmap()
        
        #self.bmpRESU    = self.imgORIG.ConvertToBitmap()
        
        # --- Affichage image ---- #
        self.conteneurimage.SetScrollRate(0,0)
        self.image = self.Affiche(self.bmpRESU,self.conteneurimage)
        self.SetLabel(url)

    def nz(self,valeur_o,valeur_pardefaut=''):
        if valeur_o=='' or valeur_o==None:
            return valeur_pardefaut
        else:
            return valeur_o
    
    
    def imagesuiv(self,e):
        sql = "SET client_encoding = 'WIN1252';select * FROM export   where \"pli\"='"+str(self.pli)+"' and \"n_ima\"='"+self.nomimage+"' "
        connexion  = psycopg2.connect("dbname=saisie user=postgres password=123456  host= localhost") #prod 
        connexion.set_isolation_level(0)
        curs = connexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute("SET client_encoding = 'WIN1252';")
        connexion.commit()
        curs.execute(sql)
        data = curs.fetchone()
        
        if data!=None :
            #self.nima = data['N_IMA']
            self.list_ima = self.nz(data['list_ima'])
            tablimage = self.list_ima.split(";")
            z=-1
            for index in range(len(tablimage)):
                if tablimage[index]==self.nima:
                    z=index
                    break
            if z==len(tablimage)-1:
                self.errorDlg("Infos","Vous êtes sur la derniere image de cette pli!")
                return False
            else:
                self.nima = tablimage[z+1]
                self.urlImage = os.path.dirname(self.urlImage)+'\\'+self.nima
                self.urlImage = os.path.dirname((os.path.dirname(self.urlImage)))+"\\"+self.nz(data['n_lot'])+"\\"+self.nima
                self.setimage(self.urlImage,self.facteur)
      
        
        connexion.close()
    
    def imageprec(self,e):
        sql = "SET client_encoding = 'WIN1252';select * from \"export\" where \"pli\"='"+str(self.pli)+"' and \"n_ima\"='"+self.nomimage+"' "
        connexion  = psycopg2.connect("dbname=saisie user=postgres password=123456  host= localhost") #prod 
        connexion.set_isolation_level(0)
        curs = connexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute(sql)
        data = curs.fetchone()
        
        if data!=None :
            self.list_ima = self.nz(data['list_ima'])
            tablimage = self.list_ima.split(";")
            z=-1
            for index in range(len(tablimage)-1,-1,-1):
                if tablimage[index]==self.nima:
                    z=index
                    break
            if z==0:
                self.errorDlg("Infos","Vous êtes sur la premiere image de cette pli!")
                return False
            else:
                self.nima = tablimage[z-1]
                self.urlImage = os.path.dirname(self.urlImage)+'\\'+self.nima
                self.urlImage = os.path.dirname((os.path.dirname(self.urlImage)))+"\\"+self.nz(data['n_lot'])+"\\"+self.nima
                self.setimage(self.urlImage,self.facteur)
            
        
        
        connexion.close()
    
    def tournerImage(self,e,clockwise=True):
        self.imgORIG = self.imgORIG.Rotate90(clockwise)
        self.largeur = (self.imgORIX * self.facteur)/100
        self.hauteur = (self.imgORIY * self.facteur)/100
        self.bmpRESU = self.imgORIG.Scale(self.largeur, self.hauteur).ConvertToBitmap()
        self.Affiche(self.bmpRESU,self.conteneurimage,self.facteur)
    
    def molette(self,e):
        if str(e.GetWheelRotation())=='-120':
            self.decalePlus('y',self.inc)
        elif str(e.GetWheelRotation())=='120':
            self.decaleMoins('y',self.inc)



    def left(self,e):
            """
                Deplacement à gauche
            """
            self.decaleMoins('x',self.inc)
        
    def right(self,e):
        """
            Deplacement à droite
        """
        
        self.decalePlus('x',self.inc)

    def down(self,e):
        """
            Deplacement vers le bas
        """
        self.decaleMoins('y',self.inc)
        
    def up(self,e):
        """
            Deplacement vers le haut
        """
        
        self.decalePlus('y',self.inc)



    def decalePlus(self,orient,distance):
        """
            Deplacement de l'image en cour 
            variable:
                orient: x->horizontal vers la droite, y : vertical vers le haut
                distance: longuer de deplacement
                
        """
        posX, posY = self.conteneurimage.GetViewStart()
        if(orient=='x'):
            self.conteneurimage.Scroll(posX+int(distance), posY)
        else:
            self.conteneurimage.Scroll(posX, posY+int(distance))
                
        self.conteneurimage.Refresh()


    def decaleMoins(self,orient,distance):
        """
            Deplacement de l'image en cour 
            variable:
                orient: x->horizontal vers la gauche, y : vertical vers le bas
                distance: longuer de deplacement
                
        """
        
        posX, posY = self.conteneurimage.GetViewStart()
        if(orient=='x'):
            self.conteneurimage.Scroll(posX-int(distance), posY)
        else:
            self.conteneurimage.Scroll(posX, posY-int(distance))
                
        self.conteneurimage.Refresh()


    def copier(self,src,dst):
        """
            Methode de copie d'un fichier
        """
        if(os.access(src,os.F_OK)==False):
            self.errorDlg('Erreur image','Il n\'y a pas de fichier  dans le repertoire '+ src +' !')
            return False
        shutil.copy(src,dst)
        
    def errorDlg(self,title,message):
        msg = wx.MessageDialog ( None, message, caption=title,style=wx.ICON_ERROR , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg
    
    def InfoDlg(self,title,message):
        msg = wx.MessageDialog ( None, message, caption=title,style=wx.OK , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg
    
    def Warndlg(self,title,message):
        """ Méthode d'affichage d'information"""
        msg = wx.MessageDialog ( None, message, caption=title,style=wx.ICON_WARNING|wx.OK , pos=wx.DefaultPosition )
        msg .ShowModal()
        return msg
    
    def getUrlExact(self,urlrelative):
        repertoire = os.path.dirname(urlrelative)
        try:
            tfiles = os.listdir(repertoire)
        except:
            return urlrelative
        n=0
        while n<len(tfiles):
            if self.NettoyageAcc(tfiles[n])== os.path.basename(urlrelative):
                return os.path.dirname(urlrelative)+'/'+tfiles[n]
            n=n+1
        return urlrelative

    def NettoyageAcc(self,chaine):
        """ Cette fonction enleve les accents dans une chaine"""
        chaine=chaine.encode('cp1252')
        
        ListeAccents = "ËÉÊÈÄÀÂÜÙÛÏÎÖÔÇëéêèäàâüùûïîöôç¨^"
        ReplaceListeAccents = "EEEEAAAUUUIIOOCeeeeaaauuuiiooc  "
        k=0
        while k<len(chaine):
            i=0
            while i<len(ListeAccents):
                if (chaine[k])==(ListeAccents[i]):
                    chaine  = chaine.replace(chaine[k],ReplaceListeAccents[i])
                i=i+1   
            k=k+1
        return chaine
    
    
    def zoomplus(self, evt=None):
        """
            Afficher l'image en cours avec une zoom plus grand.
            parametre : evt: evennement (pas obligatoire)
        """
        self.facteur = self.facteur + self.inc
        self.largeur = (self.imgORIX * self.facteur)/100
        self.hauteur = (self.imgORIY * self.facteur)/100
        self.bmpRESU = self.imgORIG.Scale(self.largeur, self.hauteur).ConvertToBitmap()
        self.Affiche(self.bmpRESU,self.conteneurimage, self.facteur)
    
    def zoomMoins(self, evt=None):
        """
            Afficher l'image en cours avec une zoom plus petit.
            parametre : evt: evennement (pas obligatoire)
        """
        
        if self.facteur > self.inc:
            self.facteur = self.facteur - self.inc
            self.largeur = (self.imgORIX * self.facteur)/100
            self.hauteur = (self.imgORIY * self.facteur)/100
            self.bmpRESU = self.imgORIG.Scale(self.largeur, self.hauteur).ConvertToBitmap()
            self.Affiche(self.bmpRESU,self.conteneurimage, self.facteur)

    def Affiche(self, bmp,conteneur,facteur=100,coordX=None,coordY=None,penCol=(255,0,0)):
        """ 
            Methode affichant une image bmp dans un conteneur  
            Parametres :
                bmp : objet image bitmap
                contenur : contenur pour l'affichage
                facteur : facteur de zoom d'affichage (normalement inferieur ou égale à 100)
            retour : objet image
        """
        step = 15
        posX, posY = conteneur.GetViewStart()
        #self.facteur = facteur
        if(self.image!=None):
            self.image.Destroy()
        

        conteneur.SetVirtualSize(wx.Size(bmp.GetWidth(), bmp.GetHeight()))
        self.image = wx.StaticBitmap(conteneur, 1, bmp)
        #conteneur.SetScrollRate((10*facteur)/100, (10*facteur)/100)
        conteneur.SetScrollbars(step, step, (bmp.GetWidth()+15)/step,(bmp.GetHeight()+15)/step)
        conteneur.Scroll(posX, posY)
        conteneur.Refresh()
        return self.image
        
    

if __name__ == "__main__":
    app = MainApp(0) 
    app.MainLoop()
