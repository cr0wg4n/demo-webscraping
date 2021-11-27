from bs4 import BeautifulSoup
import requests
import json
import random
import wget
import os 
import re

def load_user_agents():
    with open('user-agents.json', 'r', encoding='utf-8') as file:
        data = file.read()
        data = json.loads(data)
    data = [data["browsers"][key] for key in data["browsers"].keys()]
    return sum(data, [])

def write_json(name, json_data, base_dir="./data"):
    path = os.path.join(base_dir, "{}.json".format(name))
    with open(path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(json_data, ensure_ascii=False, indent=2))
    return path

uas = load_user_agents()

def get_user_agent(user_agents):
    return user_agents[random.randint(0, len(user_agents) - 1)]

def parse_html(url):
    html = get_request(url)
    return BeautifulSoup(html, "html.parser")

def download_file(url, name="", base_dir="./data"):
    dir_name = os.path.join(base_dir, name)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    return wget.download(url, out=dir_name)

def get_request(url):
    headers = {
        "User-Agent": get_user_agent(uas)
    }
    response = requests.get(url, headers=headers)
    return response.content

pages = {
    "netflix": [
        {
            "name": "naruto",
            "url": "https://www.netflix.com/title/70205012"
        }
    ]
}

def get_episodies_netflix(soup):
    data = []
    seasons = soup.findAll("div", { "class": "episodes-container"})
    for index, season in enumerate(seasons):
        episodes = season.findAll("div", { "class": "episode" })
        for episode in episodes:
            item = {}
            image = episode.find('img')["src"]
            item["image"] = image
            item["name"] = episode.h3.text
            item["description"] = episode.p.text
            data.append(item)
    return data


def get_video_description(soup):
    image = soup.find('img', {"class": "logo"})["src"]
    return {
        "logo": image,
        "title": soup.find('h1', {"class": "title-title"}).text,
        "description": soup.find('div', {"class": "title-info-synopsis"}).text
    }

def get_urls(soup):
    return [url["href"] for url in soup.findAll("a", { "class": "nm-collections-title nm-collections-link" })]




# naruto_url = "https://www.netflix.com/title/70205012"
# soup = parse_html(naruto_url)
# naruto = get_episodies_netflix(soup)
# write_json("naruto", naruto)


# naruto_url_es = "https://www.netflix.com/bo/title/70205012"
# soup = parse_html(naruto_url_es)
# naruto = get_episodies_netflix(soup)
# write_json("naruto_es", naruto)


# la_mascara_url = "https://www.netflix.com/title/70027007"
# soup = parse_html(la_mascara_url)
# la_mascara = get_video_description(soup)
# write_json("la_mascara", la_mascara)


all_tv = "https://www.netflix.com/browse/genre/83"
soup = parse_html(all_tv)

for url in get_urls(soup):
    soup = parse_html(url)
    description = get_video_description(soup)
    episodies = get_episodies_netflix(soup)
    print(write_json(description["title"], description))
    name = description["title"]
    name = re.sub('[\\/:"*?<>|]+', '', name)
    _dir = './data/{}'.format(name)
    _dir = os.path.normpath(_dir)
    if not os.path.exists(_dir):
        os.mkdir(_dir)
    for index, episode in enumerate(episodies):
        url = episode["image"]
        # name = re.sub('[\\/:"*?<>|]+', '', episode["name"])
        name = "Ep - {}".format(index)
        download_file(url, name, _dir)





# Instagram decodeURI 
# https://www.instagram.com/cr0wg4n/?__a=1
# Instagram