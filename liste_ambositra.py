# to delete the commented_lines in python
# # sed -e '/^\s*#/d' file001.py > file001_no_comments.py
#

import csv
import string
import requests
from bs4 import BeautifulSoup

import configparser
config = configparser.ConfigParser()
config.read(
    r'E:\DEV\python\py_many_tools\all_confs.txt'
)


import MySQLdb

# input: code_html izay ho_traitena am bs4
# 

connection_db = MySQLdb.Connection(
	host = 'localhost'
	, user = config['mysql_our_db']['username']
	, passwd = config['mysql_our_db']['password']
	, db = config['mysql_our_db']['database']
	, charset='utf8'
)
cursor_db = connection_db.cursor()
cursor_db.execute("set names utf8;")
cursor_db.execute("SET CHARACTER SET utf8;;")
# cursor_db.execute("insert into rcs_data(immatriculation, link, data_txt) values ('imm001', 'link001', 'data_txt001')")
# connection_db.commit()

def get_all_fiches(
	content
	, req = None
):
	print ('req003: ', req)
	input()
	soup = BeautifulSoup(content)
	table_row = soup.find("tbody").findAll("tr")
	if len(table_row)>0:
		for tr in table_row: 
			# isakn page iray dia misy info(Immatriculation, Nom, ..., lien(+d_infos))

			# print("tr: ", tr)
			# # <tr>
			# # <td>RCS Ambositra 2000A00001</td>
			# # <td>SAHONDRANIAINA</td>
			# # <td></td>
			# # <td>SAHONDRANIAINA Jeanne MarinÃ Â  </td>
			# # <td><a 
			info_list = tr.findAll("td")
			immatriculation = info_list[0].text # <<<<<<<<<<<<<<<

			# for i in info_list:
			# 	print(i)
			fiche_url =  tr.find('a')['href']
			fiche_url = fiche_url.replace( "&amp;", "&")
			fichier = fiche_url.replace( "index.php?pgdown=consultation&soc=", "") + ".htm"
			r = requests.get(tld+fiche_url)

			soup = BeautifulSoup(r.text) # ok
			tr_list = soup.findAll("tr")

			all_txt = ""
			for tr001 in tr_list:
				print(tr001.text) # <<<<<<<<<<<<<<<<<<<<<<< 
				all_txt += tr001.text

			# all_txt
			# #  Immatriculation
			# # : RCS Ambositra 2000A00001
 			# #Civilité
			# # : Madame

			# print(immatriculation) # OK
			url_total = tld+fiche_url
			# print(url_total)
			# # http://www.rcsmada.mg/index.php?pgdown=consultation&soc=1-1
			print("immatriculation: ", immatriculation)
			print("url_total: ", url_total)
			print('all_txt: ', all_txt)
			mysql_req = "insert into rcs_data(immatriculation, link, data_txt, "
			mysql_req += "type_assujetti, greffe_rcs) values ('"+immatriculation+"', '"+url_total.replace("'", "\\'")+"', '"+all_txt.replace("'", "\\'")+"','"
			mysql_req += req['TypeSociete'] +"', '" + req['Greffe'] + "')"
			print('mysql_req: ', mysql_req)
			# input()
			try:
				cursor_db.execute(mysql_req)
				connection_db.commit()
			except Exception:
				print("ERRRRRRROOOOOOR")
				input()
				print(mysql_req)
				pass
			input()

			# file = open(fichier,"w", encoding="utf-8") 
			# #soup = BeautifulSoup(r.content)
			# #file.write(soup.find("table", {"class": "simple2"}))
			# file.write(r.text) 
			# file.close() 
			# print(fichier)
	else:
		print("aucune ligne trouvée");
	
	return ""


tld = 'http://www.rcsmada.mg/'
url = 'http://www.rcsmada.mg/index.php?pgdown=liste2'
headers = {'User-Agent': 'Mozilla/5.0'}


list_type_assujetti = [
	'A'  	# Personne physique
	, 'B'	# B-Personne morale
	, 'C'	# C-Groupement d'intêrét économique
	, 'D'	# D-Personne morale autre qu'un GIE
	, 'E'	# E-Institution de microfinance
]

list_greffe_rcs = [
	'1'		# Ambositra
	, '10' 	# Antananarivo
	, '11' 	# Antsirabe
	, '12' 	# Antsiranana
	, '13' 	# Arivonimamo
	, '14' 	# Betroka
	, '15' 	# Farafangana
	, '16' 	# ...
	, '17' 	# 
	, '18' 	# 
	, '19' 	# 
	, '2' 	# 
	, '20' 	# 
	, '21' 	# 
	, '22' 	# 
	, '23' 	# 
	, '24' 	# 
	, '25' 	# 
	, '26' 	# 
	, '27' 	# 
	, '28' 	# 
	, '29' 	# 
	, '3' 	# 
	, '30' 	# 
	, '31' 	# 
	, '32' 	# 
	, '33' 	# 
	, '34' 	# 
	, '35' 	# 
	, '36' 	# 
	, '37' 	# 
	, '38' 	# 
	, '39' 	# 
	, '4' 	# 
	, '40' 	# 
	, '41' 	# 
	, '5' 	# 
	, '6' 	# 
	, '7' 	# 
	, '8' 	# 
	, '9' 	# 
]



req = {
	'TypeSociete':'B'
	# A = Personne physique # tested
	# B = Personne morale   # tested
	# C = Groupement d'interet personnelle
	# ...
	
	,'Greffe':'1' 
	# 1  = Ambositra
	# 10 = Tana
	# 11 = Antsirabe
	# ...

	, 'DateInscrit':''
	, 'FormeJuridiq':'Null'
}

# if (req['TypeSociete'] == 'A'):
	# type_assujetti = 'personne_physique'
	# pass
# elif (req['TypeSociete'] == 'B'):
	# type_assujetti = 'personne_morale'
	# pass
# elif (req['TypeSociete'] == 'C'):
	# type_assujetti = 'groupement_interet_personnelle'
	# pass
# else:
	# print('Encore pas prise en charge')
	# print("req['TypeSociete']: ", req['TypeSociete'])
	# input("")
	# pass
# 
# if (req['Greffe'] == '1'):
	# greffe = 'ambositra'
	# pass
# elif (req['Greffe'] == '11'):
	# greffe = 'tana'
# elif (req['Greffe'] == '11'):
	# greffe = 'antsirabe'
# else:
	# print("Greffe pas encore pris en charge")
	# print("Greffe = ", req["Greffe"])
	# input()






def general_rcs001(req = None):
	print ('req002: ', req)
	input()
	requete = requests.post(
		url
		, headers=headers
		,data=req
	)
	page = requete.content
	# # b'<!DOCTYPE htm.. refa tafiditra ilay data_post dia maaz page
	# # # ito dia misy ilay resultat voloo SY ireo list_nombre_page
	get_all_fiches(
		page
		, req = req
	)

	soup = BeautifulSoup(page)
	# apdirn ao anaty bs4 loo mten we hatao ilay page_html
	# pagination : <span class="butons">

	# ireto ambany ireto dia ilay resultat_traitement_bs4
	span_list  =soup.findAll("span", {"class": "butons"})
	page_list  = [elt.a['href'] for elt in span_list]

	print("req005555: ", req)
	input()
	if len(page_list) > 0:

		for page in page_list[1:]:
			r = requests.get(tld+page)
			
			get_all_fiches(
				r.content
				, req = req
			)


# general_rcs001(req = req)




for type_assujetti001 in list_type_assujetti:
	for greffe_rcs001 in list_greffe_rcs:
		req001 = {
			'TypeSociete': type_assujetti001
			, 'Greffe': greffe_rcs001
			
			
			, 'DateInscrit': ''
			, 'FormeJuridiq': 'Null'
		}
		print("req001: ", req001)
		input()
		general_rcs001(req = req001)
		pass