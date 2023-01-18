import re
import requests

regex = r",\"([a-zA-Z0-9]{9})\","


def main_europeana(keyword):
    r = requests.get("https://www.europeana.eu/en")
    print(r.status_code)
    if r.status_code != 200:
        return f"Failed initialization research ({r.status_code})"

    matches = re.finditer(regex, r.text, re.MULTILINE)
    potential_token = []
    for matchNum, match in enumerate(matches, start=1):
        print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                            end=match.end(), match=match.group()))
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                            start=match.start(groupNum),
                                                                            end=match.end(groupNum),
                                                                            group=match.group(groupNum)))
            print(match.group(groupNum))
            potential_token.append(match.group(groupNum))
    print(potential_token)

    # find potential token from html
    token = None

    for tok in potential_token:
        url = f'https://api.europeana.eu/record/search.json?wskey={tok}&page=1&view=grid&query=test&profile=minimal&rows=1&start=1'
        r = requests.get(url)
        print(tok, r.status_code)
        if r.status_code == 200:
            token = tok
            break
    keyword = "forêt de rambouillet"
    initurl = f"https://api.europeana.eu/record/search.json?wskey={token}&page=1&view=grid&query={keyword}&qf=contentTier%3A%281%20OR%202%20OR%203%20OR%204%29&profile=minimal&rows=1&start=1"
    r = requests.get(initurl)
    if r.status_code != 200:
        return f"Failed initialization research ({r.status_code})"

    datainit = r.json()
    if datainit["success"] == "False":
        print("no result")
        return f"No result"

    totalc = datainit["totalResults"]
    print(f"total result is {totalc}")
    import time
    result = []
    index = 1

    MAX_SEARCH = 100
    while len(result) < totalc:
        searchurl = f"https://api.europeana.eu/record/search.json?wskey={token}&page=1&view=grid&query={keyword}&qf=contentTier%3A%281%20OR%202%20OR%203%20OR%204%29&profile=minimal&rows={MAX_SEARCH}&start={index}"

        r = requests.get(searchurl)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)
            return f"Something went wrong : {r.status_code}"

        data = r.json()
        print(f"retrive {data['itemsCount']} items")
        index += data["itemsCount"]
        result += data["items"]

        time.sleep(0.1)

    print(len(result))
    return result
