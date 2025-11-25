# %%

from bs4 import BeautifulSoup
import requests
import os
import gzip
import shutil
import io


# %%

def get_html(force_download=False):

    html_save_path = os.path.abspath('../..') + '/data/airbnb-scrap/index.html'
    if os.path.exists(html_save_path) and not force_download:
        with open(html_save_path,'r') as f:
            return f.read()
        

    base_url = 'https://insideairbnb.com/get-the-data/'
    html_doc = requests.get(base_url).text

    with open(html_save_path,'w') as f:
        f.write(html_doc)
    
    return html_doc


def get_all_cities_names(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    main_div = soup.find_all('div','contentcontainer-module--content-container--cf14f')[0]

    city_names = main_div.find_all('h3')

    return [c.text for c in city_names]

def get_links_by_city(html_doc,cities = []):
    soup = BeautifulSoup(html_doc, 'html.parser')
    main_div = soup.find_all('div','contentcontainer-module--content-container--cf14f')[0]

    cities_doc = main_div.find_all('h3')

    data_links = {}

    for c in cities_doc:
        cname = c.text.split(',')[0]

        if cities and cname not in cities: continue

        h4 = c.find_next('h4')

        date = h4.text[:-10].strip('')

        table = h4.find_next('table')

        rows = table.find_all('tr')

        listings_row = rows[1]
        reviews_row = rows[3]

        links = {'listings': listings_row.find('a')['href'], 'reviews': reviews_row.find('a')['href']}

        data_links[cname] = (date,links)

    return data_links

def download_data(data_links,save_folder_path = '../data/airbnb-scrap/'):
    for cname,(date,links) in data_links.items():
        date = date.replace(' ','').replace(',','')

        for x in ['listings','reviews']:
            if not os.path.exists(save_folder_path + x): os.mkdir(save_folder_path + x)
            filename = save_folder_path + f'{x}/{cname}-{x}-{date}.csv'

            if not os.path.exists(filename):
                try:
                    response = requests.get(links[x])
                        
                    if response.status_code == 200:
                        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:

                            content = f.read().decode('utf-8')
                            with open(filename, 'w',newline='',encoding='utf-8') as f_csv:
                                f_csv.write(content)
                    else:
                        print(f"Falha ao baixar o arquivo {cname}: {response.status_code}")
                        
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")



# %%
root_path = os.path.abspath('../..')

save_folder_path = root_path + '/data/airbnb-scrap/'
if not os.path.exists(save_folder_path):
    os.mkdir(save_folder_path)


html_doc = get_html()


links = get_links_by_city(html_doc,cities=['Rio de Janeiro'])

download_data(links,save_folder_path=save_folder_path)

# %%
print(links)
# %%
