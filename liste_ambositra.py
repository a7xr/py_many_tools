import csv
import string
import requests
from bs4 import BeautifulSoup

# ito dia ahazo ilay code_html izay ho_traitena am bs4
def get_all_fiches(content):
	
	soup = BeautifulSoup(content)
	table_row = soup.find("tbody").findAll("tr")
	if len(table_row)>0:
		for tr in table_row: 
			fiche_url =  tr.find('a')['href']
			fiche_url = fiche_url.replace( "&amp;", "&")
			fichier = fiche_url.replace( "index.php?pgdown=consultation&soc=", "") + ".htm"
			r = requests.get(tld+fiche_url)
			file = open(fichier,"w", encoding="utf-8") 
			#soup = BeautifulSoup(r.content)
			#file.write(soup.find("table", {"class": "simple2"}))
			file.write(r.text) 
			file.close() 
			print(fichier)
	else:
		print("aucune ligne trouvée");
	
	return ""


tld = 'http://www.rcsmada.mg/'
url = 'http://www.rcsmada.mg/index.php?pgdown=liste2'
headers = {'User-Agent': 'Mozilla/5.0'}
req = {'TypeSociete':'A','Greffe':'1', 'DateInscrit':'', 'FormeJuridiq':'Null'}

requete = requests.post(url, headers=headers,data=req)
page = requete.content
# # b'<!DOCTYPE htm.. refa tafiditra ilay data_post dia maaz page
# # # ito dia misy ilay resultat voloo SY ireo list_nombre_page
get_all_fiches(page)

soup = BeautifulSoup(page)
# apdirn ao anaty bs4 loo mten we hatao ilay page_html
#pagination : <span class="butons">

# ireto ambany ireto dia ilay resultat_traitement_bs4
span_list  =soup.findAll("span", {"class": "butons"})
page_list  = [elt.a['href'] for elt in span_list]
print("page_list: ", page_list)
input()

if len(page_list) > 0:

	for page in page_list[1:]:
		r = requests.get(tld+page)
		
		get_all_fiches(r.content)



