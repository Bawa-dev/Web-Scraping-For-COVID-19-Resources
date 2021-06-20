import requests
import pandas as pd
from bs4 import BeautifulSoup

# Part 1: Scraping Covid-19 Data Country-wise
url1 = "https://www.worldometers.info/coronavirus/#countries"

req1 = requests.get(url1)
htmlContent1 = req1.content
soup1 = BeautifulSoup(htmlContent1, 'html.parser')

table1 = soup1.find('tbody')
table_data1 = []

for row in table1.find_all('tr'):
    rows = []

    for cell in row.find_all('td'):
        rows.append(cell.text)
    if(len(rows) > 0):
        data_elem = {
        "Country": rows[1],
        "TotalCases": rows[2],
        "NewCases": rows[3],
        "TotalDeaths": rows[4],
        "NewDeaths": rows[5],
        "TotalRecovered": rows[6],
        "ActiveCases": rows[7],
        "CriticalCases": rows[8],
        "NewRecovered": rows[9],
        "TotCase1M": rows[10],
        "TotDeath1M": rows[11],
        "TotalTests": rows[12],
        "Tests1M": rows[13]
        }
    table_data1.append(data_elem)

df1 = pd.DataFrame(table_data1)
df1 = df1.drop([0,1,2,3,4,5,6], axis=0)

df1.to_excel('Covid19_data.xlsx',index=False)