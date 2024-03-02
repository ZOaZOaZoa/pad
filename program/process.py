from hit import Hit
import pandas as pd
from bow import BOW
import re
import pickle
import os
from tqdm import tqdm

hits_pd = pd.read_csv('total.csv')
hits_pd = hits_pd[['title', 'year']]
words = set()

reprocess = True
if not os.path.isfile('BOW/bow_list.dat') or reprocess:    
    for hit_title in hits_pd['title']:
        title = re.sub(r'[^\w\s]', '', hit_title).lower()
        words.update(title.split())

    BOW_list = []
    for i in tqdm(range(len(hits_pd))):
        BOW_list.append(BOW(hits_pd['title'][i]))

    with open('BOW/bow_list.dat', 'wb') as fp:
        pickle.dump({'BOW_list': BOW_list, 'words': words}, fp)
else:
    with open('BOW/bow_list.dat', 'rb') as fp:
        data = pickle.load(fp)
        BOW_list = data['BOW_list']
        words = data['words']

print(len(BOW_list))
print(words)