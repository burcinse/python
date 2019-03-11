import os
import urllib.request
import urllib.error
import pandas as pd


def check_if_exists(url):
    response = urllib.request.urlopen(url)
    if response.getcode() == 200:
        print(response.headers['content-length'])


# Execution file directory
exe_dir = os.path.dirname(os.path.abspath(__file__))


# Pandas read file
data = pd.read_csv(exe_dir + "/csv/list.csv", dtype='object', low_memory=False)
data = data.fillna('')

# print(data.head(5))
# print(data['MainImage'].dtypes)

for i, row in data.iterrows():
    data_headers = [row['SKU'], row['MainImage']]
    sku = row['SKU']
    url = row['MainImage']

    # for index, header_name in enumerate(data_headers):
    # print(f"{sku} {url}")

    try:
        response = urllib.request.urlopen(url)
        if response.getcode() == 200:
            print('Exists')
        else:
            print(response.getcode())
    except urllib.error.URLError as e:
        print(e)


# --------------------
