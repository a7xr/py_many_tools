#!/usr/bin/env python
# -*- coding: cp1252  -*-

import wx
import os,stat,sys,shutil,random,string
 
 

class fonction:
    def __init__(self,parentwidg,dblocal='SUR900_format_db',idcom=0):

        self.parent = parentwidg
        self.dbname = dblocal
        self.fenprincip = self.parent.GetParent()
        self.idcom = idcom
        self.repertoire = 'C:/image/'
        if os.access(self.repertoire,os.F_OK)==False:
            os.makedirs(self.repertoire,777)
         
        self.vvolumeexecute = 0     
        self.vetape = ''
        self.vidfichiercmd = ''
        self.videxecute = 0
        self.vcommande = ''
        self.vmatricule = 0
        
    
    def getwidgetByName(self,name):
        tzChild = self.parent.GetChildren()
        I=0
        while(I<len(tzChild)):
            if(tzChild[I].GetName()==name):
                return tzChild[I]
            I=I+1
        return None

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
    
    def onExit(self,e=None):
        self.fenprincip.Close()
    
    #---------------------- by farinoire ----------------------
    def isNumber(self,e):
        e_obj = e.GetEventObject()
        chaine = e_obj.GetValue()
        
        if self.isnumerique(chaine)== False :
            e_obj.SetValue("")
            e_obj.SetFocus()
            return
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
    #--------------------------------------------------------------
    
    
    def checkMat(self,e=None):
        """ Methode de verification champ matricule"""
        
        key = e.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            e.Skip()
            return
    
    def checkCom(self,e=None):
        """ Methode de verification champ matricule"""
        e_obj= e.GetEventObject()
        key = e.GetKeyCode()
        val = e_obj.GetValue()
            
        if(len(e_obj.GetValue())<3 or val[0] not in string.letters or val[1] not in string.letters or val[2] not in string.letters):
            if  key < 255 and key!=wx.WXK_SPACE:
                e.Skip()
                return
        else:
            if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255 :
                e.Skip()
                return
    
    
   
    def checkEntry(self,e):
        e_obj= e.GetEventObject()
        e_obj.SetValue(e_obj.GetValue().upper())
        val = e_obj.GetValue()
        if e_obj.GetName()=='E_COMMANDE':
            if val!='':
                if(len(e_obj.GetValue())<6 or (val[0] not in string.letters or val[1] not in string.letters or val[2] not in string.letters) ):   
                    e_obj.SetValue('')
                    e_obj.SetFocus()
                    return
    