import requests, telepot, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
id_telegram = os.getenv('ID_TELEGRAM')
token = os.getenv('TOKEN')
bot = telepot.Bot(token)

def get_film(url):
    r = requests.get(url)
    if r.status_code == 200:
        html = BeautifulSoup(r.content, "html.parser")
        film = html.find_all('div', class_="rowl")
        for soup in film:
            a_tag = soup.find('a', href=True)
            title = soup.h2.string
            link = a_tag['href']
            spans = soup.find_all('span', class_='moket')
            genre = spans[0].text
            time = spans[1].text
            playing_at = [i['class'][1] for i in soup.find_all('i', class_='icon')]
            text = '\nTitle: [' + title + '](' + link + ')\n' + \
                'Genre: ' + genre + '\n' + \
                'Time: ' + time + '\n' + \
                'Plating at: ' + ', '.join(playing_at) + '\n' + \
                '~~~~~~~~'
            print(text)

url = 'https://jadwalnonton.com/now-playing/in-jakarta/'
r = requests.get(url, verify=False)
if r.status_code == 200:
    html = BeautifulSoup(r.content, "html.parser")
    total_page = html.find('div', class_="paggingcont").find_all('li')
    if len(total_page) == 0:
        get_film(url)
    else:
        for x in range(len(total_page)-1):
            url_new = url + '?page=' + str(x+1)
            get_film(url_new)