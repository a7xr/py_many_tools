
import random
import time
import csv
import string
import requests
from bs4 import BeautifulSoup
import sys

import configparser
config = configparser.ConfigParser()
config.read(
	r'confs_mmt_smartit.txt'
)


import MySQLdb


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

def get_all_fiches(
	content
	, req = None
):
	print ('req003: ', req)
	soup = BeautifulSoup(content)
	table_row = soup.find("tbody").find_all("tr")
	if len(table_row)>0:
		for tr in table_row:	# isakn page irai misy ligne maro2 

			info_list = tr.find_all("td")
			immatriculation = info_list[0].text # <<<<<<<<<<<<<<<

			fiche_url =  tr.find('a')['href']
			fiche_url = fiche_url.replace( "&amp;", "&")
			fichier = fiche_url.replace( "index.php?pgdown=consultation&soc=", "") + ".htm"
			r = requests.get(tld+fiche_url)

			soup = BeautifulSoup(r.text) # ok
			tr_list = soup.find_all("tr")

			all_txt = ""
			for tr001 in tr_list:
				all_txt += tr001.text


			url_total = tld+fiche_url
			print("immatriculation: ", immatriculation)
			print("url_total: ", url_total)
			mysql_req = "insert into rcs_data(immatriculation, link, data_txt, "
			mysql_req += "type_assujetti, greffe_rcs) values ('"+immatriculation+"', '"+url_total.replace("'", "\\'")+"', '"+all_txt.replace("'", "\\'")+"','"
			mysql_req += req['TypeSociete'] +"', '" + req['Greffe'] + "')"
			try:
				print(
					"immatriclation: ", immatriculation, "\nurl: ", url_total.replace("'", "\\'")
					, file = open('data_inserted.txt', 'a')
				)
				
				print(mysql_req, file=open('rcs_query_normal.txt', 'a'))
				cursor_db.execute(mysql_req)
				connection_db.commit()
				# sys.exit(0)
			except Exception:
				print("ERRRRRRROOOOOOR")
				print(mysql_req, file = open('error_special_char.txt', 'a'))
				# sys.exit(0)
				pass

	else:
		print("aucune ligne trouvee");
	
	return ""


tld = config['link']['tld']
url = config['link']['url']
headers = {'User-Agent': 'Mozilla/5.0'}


list_type_assujetti = [
	'A'  	# Personne physique
	# , 'B'	# B-Personne morale
	# , 'C'	# C-Groupement d'intêrét économique
	# , 'D'	# D-Personne morale autre qu'un GIE
	# # , 'E'	# E-Institution de microfinance
]

list_greffe_rcs = [
	# '1'		# Ambositra
	'10' 	# Antananarivo
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
	
	,'Greffe':'1' 

	, 'DateInscrit':''
	, 'FormeJuridiq':'Null'
}







def general_rcs001(req = None, compteur = 0):
	print ('req002: ', req)
	# input()
	requete = requests.post(
		url
		, headers=headers
		,data=req
	)
	page = requete.content

	if compteur == 1:
		pass
	else:
		get_all_fiches(
			page
			, req = req
		)

	soup = BeautifulSoup(page)

	span_list  =soup.find_all("span", {"class": "butons"})
	page_list  = [elt.a['href'] for elt in span_list]

	print("req005555: ", req)
	if len(page_list) > 0:

		if compteur == 1:
			depart = 235
		else:
			depart = 1

		for page in page_list[depart:]:
			r = requests.get(tld+page)
			
			get_all_fiches(
				r.content
				, req = req
			)
			num_random = random.choice(range(5))
			time.sleep(num_random)






compteur = 0
for type_assujetti001 in list_type_assujetti:
	for greffe_rcs001 in list_greffe_rcs:


		compteur += 1
		req001 = {
			'TypeSociete': type_assujetti001
			, 'Greffe': greffe_rcs001
			
			
			, 'DateInscrit': ''
			, 'FormeJuridiq': 'Null'
		}
		print("req001: ", req001)
		# input()
		general_rcs001(req = req001, compteur = compteur)
		pass
