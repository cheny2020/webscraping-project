import requests
import time
import json
import concurrent.futures
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()


def main_bnf(keyword):
    KEYWORD = keyword
    initurl = f'https://catalogue.bnf.fr/changerPage.do?motRecherche={KEYWORD}&nbResultParPage=1&pageEnCours=1'
    r = requests.get(initurl)
    time.sleep(0.5)
    if r.status_code != 200:
        return f"Failed initialization research ({r.status_code})"
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    nbitem = int(soup.find(id="nbPage").text.strip()[3:].replace(' ', ''))
    print(nbitem)
    MAX_SEARCH = 100
    result = set()
    for index in range(1, int(nbitem / MAX_SEARCH) + 2):
        print(f"searching {index}/{int(nbitem / MAX_SEARCH) + 2}")
        searchurl = f'https://catalogue.bnf.fr/changerPage.do?motRecherche={KEYWORD}&nbResultParPage={MAX_SEARCH}&pageEnCours={index}'
        r = requests.get(searchurl)
        if r.status_code != 200:
            return f"No result found: {r.status_code}" # no result found
        try:
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')

            for item in soup.find_all('div', {"class": "notice-contenu"}):
                for arkdiv in item.find_all('div', {"class": "notice-synthese"}):
                    for ark in arkdiv.find_all('a'):
                        if '/ark:/' in ark['href']:
                            result.add(ark['href'])
            # break
        except Exception as e:
            print(f"Something went wrong: {e}")
            return f"Error: {e}"
        # time.sleep(0.1)
    print(f"there is {len(result)} results found")

    def request_item(id):
        time.sleep(1)
        url = f"https://catalogue.bnf.fr{id}"
        print(url)
        try:
            r = requests.get(url, verify=False, timeout=30)
        except Exception as e:
            return id

        return r

    with concurrent.futures.ThreadPoolExecutor() as executor:
        res = [executor.submit(request_item, id) for id in result]
        concurrent.futures.wait(res)

    resultfinal = []

    error_second_try = []

    for i in range(len(result)):
        element = res[i].result()
        if isinstance(element, str):
            print(f"Error: {element}")
            error_second_try.append(element)
            continue
        if element.status_code != 200:
            print(element.status_code)
            print(res.history[0].url)
            continue
        try:
            temp = {}
            soup = BeautifulSoup(element.text, 'html.parser')
            item = soup.find(id='ancreNotice')
            for p in item.find_all('p'):
                temp[p['id'].strip()] = []
                for sp in p.find_all('span'):
                    temp[p['id'].strip()].append(sp.getText().strip())

            resultfinal.append(temp)
        except Exception as e:
            print(f"Something went wrong: {e}")

    print("number of errors:", len(error_second_try))
    print(f"{len(resultfinal)} finals elements")

    return resultfinal

    # with open("bnf.json", "w") as f:
    #     json.dump(resultfinal, f, indent=4)
