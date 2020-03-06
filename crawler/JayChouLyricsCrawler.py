# coding = utf-8
import requests
from bs4 import BeautifulSoup
import re

root_url = 'https://mojim.com'
root_href = '/cnh100951.htm'
file_to_save = "../resources/lyrics/JayChou/"
begin_title = "可爱女人"

all_lyrics_file_to_save = "../resources/lyrics/JayChou/all_lyrics.txt"
all_lyrics_file = open(all_lyrics_file_to_save, "a", encoding="utf-8")

def run():
    html_str = requests.get(root_url + root_href).content.decode("utf-8")
    html_soup = BeautifulSoup(html_str, 'html.parser')
    songs_elements_list_1 = html_soup.find_all("span", class_="hc3")
    songs_elements_list_2 = html_soup.find_all("span", class_="hc4")
    songs_elements_list_1.pop(0)
    songs_elements_list_2.pop(0)
    urls = []
    for song_elememt in songs_elements_list_1:
        a_tags = song_elememt.find_all('a')
        for a in a_tags:
            title = a.text
            href = a["href"]
            urls.append([title, href])
    for song_elememt in songs_elements_list_2:
        a_tags = song_elememt.find_all('a')
        for a in a_tags:
            title = a.text
            href = a["href"]
            urls.append([title, href])
    crawl_lyrics(urls)

def crawl_lyrics(urls):
    check_point_flag = False
    for title, href in urls:
        print("-----title: {}-----".format(title))
        title.replace("/", "")
        if title == "(提供)":
            continue
        if re.match("Intro", title):
            continue
        if re.match("免费教学", title):
            continue
        if re.match("我要夏天", title):
            continue
        if title == "可爱女人(可爱い女/ひと)":
            title = "可爱女人"
        if title == "七里香":
            check_point_flag = True

        if check_point_flag:
            crawl_lyric(title, href)

def crawl_lyric(title, href):
    html_str = requests.get(root_url + href).content.decode("utf-8")
    html_soup = BeautifulSoup(html_str, 'html.parser')
    content = str(html_soup.find("div", {"id": "fsZ"})).replace("<br/>", "\n")
    content = re.search("</dt>([^[]*)", content)[1]
    content = re.sub("\n{3,}", "\n", content)
    content = content.split("\n\n")
    with open(file_to_save+title+".txt", "w", encoding="utf-8") as file:
        for s in content[1:]:
            s = s.split("\n")
            for line in s:
                if re.match("更多更详尽歌词", line):
                    continue
                line = line.strip()
                file.write(line)
                file.write("\n")
                all_lyrics_file.write(line)
                all_lyrics_file.write("\n")
            file.write("\n\n")
            all_lyrics_file.write("\n\n")


if __name__ == "__main__":
    run()
    all_lyrics_file.close()
