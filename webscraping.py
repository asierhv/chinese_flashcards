import requests
from bs4 import BeautifulSoup
import os

def html2txt(lang,lvl):
    response = requests.get(url = f"https://hsk.academy/{lang}/hsk-{lvl}-vocabulary-list")
    output_txt = f"./txt/{lang}/hsk_{lvl}_{lang}.txt"
    os.makedirs(os.path.split(output_txt)[0],exist_ok=True)
    if response.status_code == 200:
        with open(output_txt, 'w', encoding='utf-8') as fo:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('#hsk-static-content .table tbody')
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    hanzi_pinyin_td = cols[0]
                    a_tag = hanzi_pinyin_td.find('a')
                    parts = a_tag.decode_contents().strip().split('<br/>')
                    hanzi = parts[0].strip()
                    pinyin = parts[1].strip()
                    meaning = cols[1].get_text(strip=True)
                    outwrite = f"{hanzi}\t{pinyin}\t{meaning}\n"
                    fo.write(outwrite)
        print(f"TXT Saved: {output_txt}")
    else:
        print(f"Error: {response.status_code}")

if __name__=="__main__":
    lang_list = ["en","ar","de","el","es","fr","it","ja","km","ko","pt","ru","th","vi"]
    lvl_list = [1,2,3,4,5,6]
    for lang in lang_list:
        for lvl in lvl_list:
            html2txt(lang,lvl)