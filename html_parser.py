from bs4 import BeautifulSoup
import requests

# ---------------Created Document of Links--------------------------------------
speeches_html_file = open('Presidential Speeches _ Miller Center.html')
soup = BeautifulSoup(speeches_html_file,'html.parser')
links_file = open("links.txt",'w')
for i in range(0,len(soup.find_all('span',class_='field-content'))):
    if(i%2==0):
        links_file.write((list(soup.find_all('span',class_='field-content')[i].children)[0].get('href'))+"\n")

# ---------------Created a seperate document for each Speech---------------------------
file =  open('links.txt')
lines = file.read().splitlines()
for i in range(len(lines)):
    page = requests.get(lines[i])
    soup = BeautifulSoup(page.content, 'html.parser')
    file = open("Speeches_Master/" + (soup.find_all('p',class_='president-name')[0].get_text()).replace(" ","_") + "_" + str(i+1) + ".txt","w") 
    file.write(soup.find_all('p', class_='episode-date')[0].get_text())
    try:
        file.write((soup.find_all('div',class_='transcript-inner')[0].get_text()).encode('utf-8'))
    except IndexError:
        file.write("\n" + list(soup.find_all('div',class_='view-transcript')[0].children)[0].get_text().encode('utf-8') + "\n")
        for j in range(1,len(list(soup.find_all('div',class_='view-transcript')[0].children))):
            try:
                file.write(list(soup.find_all('div',class_='view-transcript')[0].children)[j].get_text().encode('utf-8').replace("\n\n","\n"))
            except AttributeError:
                pass