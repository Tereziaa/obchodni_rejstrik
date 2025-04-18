import json
import requests
    
ico = input("IČO? ")
adresa1 = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/" + ico
response1 = requests.get(adresa1)
data1 = response1.json()

try:
    print(data1['obchodniJmeno'])
    print(data1['sidlo']['textovaAdresa'])
except KeyError:
    print("Zkus název subjektu.")

nazev = input("Název subjektu? ")

adresa2 = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
data2 = {"obchodniJmeno": nazev}
data2 = json.dumps(data2)
response2 = requests.post(adresa2, headers=headers, data=data2)
data3 = response2.json()

print(f"Nalezeno subjektů: {data3['pocetCelkem']}")

adresa_ciselnik = "https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ciselniky-nazevniky/vyhledat"
data4 = {
    "kodCiselniku": "PravniForma", 
    "zdrojCiselniku": "res"
}
data4 = json.dumps(data4)
reponse3 = requests.post(adresa_ciselnik, headers=headers, data=data4)
data5 = reponse3.json()

subjects = data3.get('ekonomickeSubjekty', [])
polozkyCiselniku = data5['ciselniky'][0]['polozkyCiselniku']

def find_legal_form(pravniForma, polozkyCiselniku):
    for number in range(len(polozkyCiselniku)):
        if polozkyCiselniku[number]['kod'] == pravniForma:
            return polozkyCiselniku[number]['nazev'][0]['nazev']

for subject in subjects:
    pravniForma = subject['pravniForma']
    print(subject['obchodniJmeno'], subject['ico'], find_legal_form(pravniForma, polozkyCiselniku), sep=", ")
    

