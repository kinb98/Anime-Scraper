from bs4 import BeautifulSoup
import requests 
import json
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)

class Top_anime(Resource):
    def get(self):
        source = requests.get('https://myanimelist.net/topanime.php?type=airing').text 
        soup = BeautifulSoup(source,"lxml")
        table = soup.find('table',class_='top-ranking-table')
        rows = table.find_all('tr',class_='ranking-list')
        titles = []
        l = []
        ratings = []
        for i in rows:
            titles.append(i.find('div',class_='di-ib clearfix').a.text)
            info = i.find('div',class_='information di-ib mt4')
            l.append(info.text.strip().split())
            ratings.append(i.find('td',class_='score ac fs14').div.span.text)
        d = {}
        for i in range(len(titles)):
            d[i+1] = {
                'Name': titles[i],
                'Type' : l[i][0],
                'Rating' : (ratings[i]) ,
                'Number of episodes': (l[i][1].lstrip("'(").rstrip("'")),
                'Start date' : str(l[i][3]) + " " + str(l[i][4]),
                "End date" : str(l[i][6]) + " " + str(l[i][7]),
            }
        return jsonify(d)

class Top_airing_anime(Resource):
    def get(self):
        source = requests.get('https://myanimelist.net/topanime.php?type=airing').text 
        soup = BeautifulSoup(source,"lxml")
        table = soup.find('table',class_='top-ranking-table')
        rows = table.find_all('tr',class_='ranking-list')
        titles = []
        l = []
        ratings = []
        for i in rows:
            titles.append(i.find('div',class_='di-ib clearfix').a.text)
            info = i.find('div',class_='information di-ib mt4')
            l.append(info.text.strip().split())
            ratings.append(i.find('td',class_='score ac fs14').div.span.text)
        d = {}
        for i in range(len(titles)):
            try:
                dae = int(l[i][6].replace(',',''))
                end_date = "Not Available"
            except:
                end_date = str(l[i][6]) + " " + str(l[i][7])
            d[i+1] = {
                'Name': titles[i],
                'Type' : l[i][0],
                'Rating' : (ratings[i]) ,
                'Number of episodes': (l[i][1].lstrip("'(").rstrip("'")),
                'Start date' : str(l[i][3]) + " " + str(l[i][4]),
                "End date" : end_date,
            }
        return jsonify(d)



class Top_manga(Resource):
    def get(self):
        source  = requests.get('https://myanimelist.net/topmanga.php').text 
        soup = BeautifulSoup(source,"lxml")
        table = soup.find('table',class_='top-ranking-table')
        rows = table.find_all('tr',class_='ranking-list')
        titles = []
        info = []
        ratings = []
        for i in rows:
            titles.append(i.find('div',class_='detail').a.text)
            ratings.append(i.find('td',class_='score ac fs14').div.span.text) 
            res = i.find('div',class_='information di-ib mt4')
            info.append(res.text.strip().split())
        d = {}
        for i in range(len(titles)):
            typ = info[i][0]
            volumes = int(info[i][1].lstrip("'(").rstrip("'")) if info[i][1].lstrip("'(").rstrip("'") != '?' else info[i][1].lstrip("'(").rstrip("'")
            start_date = info[i][3] + " " + info[i][4] 
            if i == 36:
                start_date = info[i][3]
                end_date = 'Not available'
            else:
                try:
                    dae = int(info[i][6].replace(',',''))
                    end_date = "Not Available"
                except:
                    end_date = info[i][6] + " " + info[i][7]
            d[i+1] = {
                'Name': titles[i],
                'Ratings' : float(ratings[i]),
                'Type': typ,
                'Volumes' : volumes,
                'Start Date' : start_date,
                'End Date' : end_date
            }
            
        return jsonify(d)

api.add_resource(Top_anime, "/top_anime")
api.add_resource(Top_airing_anime, "/top_airing_anime")
api.add_resource(Top_manga, "/top_manga")

if __name__ == "__main__":
    app.run(debug=True)
