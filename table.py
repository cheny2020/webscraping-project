def table_bnf(data_bnf):
    data2 = []
    for i in range(0, len(data_bnf)):
        element = []
        element.append(i + 1)

        if 'titre' in data_bnf[i]:
            title = data_bnf[i]['titre'][1][:40]
            element.append(title)
        else:
            element.append(" ")

        if 'auteur' in data_bnf[i]:
            auteur = data_bnf[i]['auteur'][1][:20]
            element.append(auteur)
        else:
            element.append(" ")

        if 'publication' in data_bnf[i]:
            publication = data_bnf[i]['publication'][1][:20]
            element.append(publication)
        else:
            element.append(" ")

        if 'editeur' in data_bnf[i]:
            editeur = data_bnf[i]['editeur'][1][:20]
            element.append(editeur)
        else:
            element.append(" ")

        if 'date' in data_bnf[i]:
            date = data_bnf[i]['date'][1]
            year = re.match(r'.*([1-3][0-9]{3})', date)
            element.append(year.group(1))
        else:
            element.append(" ")

        if 'typologie' in data_bnf[i]:
            type = data_bnf[i]['typologie'][1]
            element.append(type)
        else:
            element.append(" ")

        if 'link_bnf' in data_bnf[i]:
            link = data_bnf[i]['link_bnf']
            element.append(link)
        else:
            element.append(" ")

        data2.append(element)
    return data2

def table_europea(data_europea):
    # europeana, show result in table
    data =[]
    for i in range(0 ,len(data_europea)):
        element =[]
        element.append( i +1)

        if 'title' in data_europea[i]:
            title =data_europea[i]['title'][0]
            title =title[0:40]
            if len(title ) ==40:
                title+="..."
            element.append(title)
        else:
            element.append(" ")

        if 'provider' in data_europea[i]:
            provider =data_europea[i]['provider'][0]
            element.append(provider)
        else:
            element.append(" ")

        if 'type' in data_europea[i]:
            type =data_europea[i]['type']
            element.append(type)
        else:
            element.append(" ")

        if 'year' in data_europea[i]:
            year =data_europea[i]['year'][0]
            element.append(year)
        else:
            element.append(" ")

        if 'guid' in data_europea[i]:
            link =data_europea[i]['guid']
            element.append(link)
        else:
            element.append(" ")

        data.append(element)
    return data
    # print(tabulate(data, headers=["title", "provider", "type", "year" ,"link"]))