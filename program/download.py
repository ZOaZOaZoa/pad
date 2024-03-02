import urllib.request
from lxml import etree
import time
import pickle
import os
from hit import Hit, hit_to_dict
import pandas as pd

def download_page(url):
    '''
    Returns bytes of requested page
    '''
    downloaded = False
    tries = 0
    while not downloaded and tries < 10:
        try:
            fp = urllib.request.urlopen(url)
            mybytes = fp.read()
            fp.close()
            downloaded = True
        except Exception as exc:
            sleep_time = 5 + tries*6
            print(exc, f'Waiting {sleep_time} s before retry', sep='\n')
            
            time.sleep(5 + tries*6)
            tries += 1

    if tries >= 100:
        print('Too many not successful requests on server')
        exit()

    return mybytes

def prettyprint(element, **kwargs):
    '''
    Pretty print of etree
    '''
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    print(xml.decode(), end='')

def get_hit_info(root, xpath):
    '''
    Return list of dictionaries with text from tags in xpath
    '''
    hits = []

    for hit in root.xpath(xpath):
        data = dict()
        for hit_tag in hit:
            data[hit_tag.tag] = hit_tag.text
        hits.append(data)

    return hits

def download_hits(query, packet_size, prompt=False):
    '''
    Download all hits by given query by packet_size amount per request
    '''
    counter = 0
    hits = []
    
    while True:
        page_xml = download_page(f"http://dblp.org/search/publ/api?q={query}&h={packet_size}&f={counter}")
        root = etree.XML(page_xml)
        if prompt and len(hits) == 0:
            print(f"Found {root.xpath('hits')[0].get('total')} total hits")

        got_hits = get_hit_info(root, 'hits/hit/info')
        if len(got_hits) == 0:
            break
        
        hits += got_hits
        counter += packet_size

        if prompt:
            print(f'Downloaded {len(hits)} hits')
        time.sleep(1.5)
    
    return hits



def get_hit_objects(query, prompt, file_folder='', redownload=False):
    '''
    Reads hits from file or downloads from dblp
    '''
    file_name = f"{file_folder}/{query.replace('|', ' OR ')}.dat"
    if os.path.isfile(file_name) and not redownload:
        Hit.get_from_file(file_name)
    
    hits_dicts = download_hits(query, 1000, prompt)
    print(f'Total hits: {len(hits_dicts)}')

    hits = []
    for hit_dict in hits_dicts:
        hits.append(Hit(hit_dict))

    with open(file_name, 'wb') as file:
        pickle.dump(hits, file)
        print(f'{file_name} saved')
    
    return hits

def download_data(queries, redownload=False):
    for elem in queries:
        query = elem.lower().replace(' ', '+')
        print(f'Searching for {elem} with {query}')
        hits = get_hit_objects(query, True, file_folder='data', redownload=redownload)
        print(*hits[:5], sep='\n')
        print('...')
        print(f'Saved {len(hits)} hits')

'''
{Recomendation (or Recommender or Personalized) System (or Algorithm or Model)}  
or {Concept-based (or Collaborative) Approach (or Filtering)} 
or {User Similarity (or Preferences)} 
or {Cold Start}
'''

if __name__ == '__main__':
    queries = [
        'Recomendation System',
        'Recomendation Algorithm',
        'Recomendation Model',
        'Recommender System',
        'Recommender Algorithm',
        'Recommender Model',
        'Personalized System',
        'Personalized Algorithm',
        'Personalized Model',
        'Concept-based Approach',
        'Concept-based Filtering',
        'Collaborative Approach',
        'Collaborative Filtering',
        'User Similarity',
        'User Preferences',
        'Cold Start'
    ]

    download_data(queries)

    hits_total = set()
    for elem in queries:
        query = elem.lower().replace(' ', '+')
        hits = get_hit_objects(query, True, file_folder='data')
        hits_total.update(hits)

    print()
    print('-'*50)
    print(f'For the total query got {len(hits_total)} hits')
    with open('total.dat', 'wb') as file:
        pickle.dump(hits_total, file)

    hits_pd = pd.DataFrame(map(hit_to_dict, hits_total))
    hits_pd.to_csv('total.csv')