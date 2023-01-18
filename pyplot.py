import re
import json
import matplotlib.pyplot as plt
import collections
from tabulate import tabulate
import pandas as pd
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
from matplotlib.figure import Figure


def get_all_providers(data_europeana, data_bnf):
    print("len europea", len(data_europeana))
    print("len bnf", len(data_bnf))
    type_dict = {}
    for i in range(0, len(data_europeana)):
        if 'type' in data_europeana[i]:
            key = data_europeana[i]['type']
            if key in type_dict:
                type_dict[key] += 1
            else:
                type_dict[key] = 1

    type_dict2 = {}
    for i in range(0, len(data_bnf)):
        if 'typologie' in data_bnf[i]:
            key = data_bnf[i]['typologie'][1]
            if key in type_dict2:
                type_dict2[key] += 1
            else:
                type_dict2[key] = 1

    # Generate plot
    fig = Figure()

    axis = fig.add_subplot(1, 2, 1)
    labels = []
    sizes = []
    for x, y in type_dict.items():
        labels.append(x)
        sizes.append(y)
    axis.pie(sizes, labels=labels, autopct='%1.1f%%')
    axis.set_title('Europeana')

    axis2 = fig.add_subplot(1, 2, 2)
    labels = []
    sizes = []
    for x, y in type_dict2.items():
        labels.append(x)
        sizes.append(y)
    axis2.pie(sizes, labels=labels, autopct='%1.1f%%')
    axis2.set_title('BNF')

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    # pngImageB64String = "data:image/png;base64,"
    pngImageB64String = base64.b64encode(pngImage.getvalue()).decode('utf8')

    return pngImageB64String

def bar_graph(data_europeana, data_bnf):
    print("len europea", len(data_europeana))
    print("len bnf", len(data_bnf))
    year_dict = {}
    for i in range(0, len(data_europeana)):
        if 'year' in data_europeana[i]:
            key = data_europeana[i]['year'][0]
            if key in year_dict:
                year_dict[key] += 1
            else:
                year_dict[key] = 1
    print("len year_dict", len(year_dict))
    sorted_year_dict = collections.OrderedDict(sorted(year_dict.items()))
    print("len sorted year_dict", len(sorted_year_dict))

    year_dict2 = {}
    for i in range(0, len(data_bnf)):
        if 'date' in data_bnf[i]:
            date = data_bnf[i]['date'][1]
            # print(date)
            year = re.match(r'.*([1-3][0-9]{3})', date)
            if year is not None:
                # print(year.group(1))
                key = year.group(1)
                if key in year_dict2:
                    year_dict2[key] += 1
                else:
                    year_dict2[key] = 1
    sorted_year_dict2 = collections.OrderedDict(sorted(year_dict2.items()))
    print("len year_dict2", len(year_dict2))
    print("len sorted year_dict2", len(sorted_year_dict2))


    # Generate plot
    fig = Figure()

    axis = fig.add_subplot(1, 1, 1)
    d = {
        'Europeana': sorted_year_dict,
        'BNF': sorted_year_dict2
    }
    axis = pd.DataFrame(d).plot(kind='bar')
    axis.set_title('Results by year')
    axis.set_ylabel("values")

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    # Encode PNG image to base64 string
    # pngImageB64String = "data:image/png;base64,"
    pngImageB64String = base64.b64encode(pngImage.getvalue()).decode('utf8')

    return pngImageB64String