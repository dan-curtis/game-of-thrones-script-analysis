''' https://www.kaggle.com/datasets/albenft/game-of-thrones-script-all-seasons
https://www.kaggle.com/code/redwankarimsony/nlp-101-tweet-sentiment-analysis-preprocessing/notebook
https://www.kaggle.com/code/bryanb/eda-and-preprocessing-tweets/notebook
https://www.kaggle.com/code/sudalairajkumar/getting-started-with-text-preprocessing/notebook
https://www.kaggle.com/code/zikazika/tutorial-on-topic-modelling-lda-nlp/notebook
https://towardsdatascience.com/create-your-custom-python-package-that-you-can-pip-install-from-your-git-repository-f90465867893
https://www.kaggle.com/code/skylord89/latent-dirichlet-allocation-nlp/data
http://www.morganclaypoolpublishers.com/catalog_Orig/samples/9781627054218_sample.pdf'''


from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests

base_url_list = ['https://genius.com/albums/Game-of-thrones/Season-','-scripts']

episode_urls = {}

for season in range(1,9):
    episode_urls[season] = {}
    r = requests.get(base_url_list[0] + str(season) + base_url_list[1])
    soup = BeautifulSoup(r.text, "html.parser")

    tmp_list = soup.find_all('a', attrs={'class':'u-display_block'})
    url_list = [i.get('href') for i in tmp_list if not any(substring in i.get('href') for substring in ['preview','trailer'])]
    for ix, i in enumerate(url_list):
        episode_urls[season][ix+1] = i

# test_list = ['hello','python:','people','this','is:','Dan']

def check_list_substrings(string_list):
    checker = [ix for ix, string in enumerate(string_list) if string[-1] == ':']
    if any(checker):
        return checker[0]
    else:
        return -1

def assign_speakers(string_list):
    while True:
        ix = check_list_substrings(string_list)
        if ix <0:
            break
        else:
            pre_list = string_list[:ix]
            new_list = [str(string_list[ix]) + str(string_list[ix+1])]
            post_list = string_list[ix+2:]
            string_list = pre_list + new_list + post_list
    return [str(i) for i in string_list]



def script_to_df(string_list):
    df = pd.DataFrame(assign_speakers(string_list), columns=['text'])
    df['season'] = season
    df['episode'] = episode
    # split speaker from dialogue
    df[['speaker', 'dialogue']] = df[df['text'].str.contains(":",regex=False)]['text'].str.split(':', 1, expand=True)
    # split speaker from direction
    # df[['speaker', 'direction']] = df[(df['text'].str.contains(":",regex=False))&(df['speaker'].str.contains("(",regex=False))]['speaker'].str.split('(', 1, expand=True)
    # df['speaker'] = df['speaker'].str.strip()
    # df['direction'] = np.select([df['direction'].notna()], ['(' + df['direction']], df['direction'])

    df['action'] = df[~df['text'].str.contains(":")]['text']
    df['order'] = df.index + 1
    df = df[['text','season','episode','order','action','speaker','direction','dialogue']]
    return df

df_master = pd.DataFrame([],columns = ['text','season','episode','order','action','speaker','direction','dialogue'])

for season, episodes in episode_urls.items():
    for episode, url in episodes.items():
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find_all('div', attrs={'data-lyrics-container':True})
        script_list = content[0].find_all(text=True)
        df = script_to_df(script_list)
        df_master = pd.concat([df_master,df])
        break
    break

# df_master.speaker.unique().tolist()

df_master

# tag_set = set()
# for i in script_list:
#     tag_set.add(i.parent.name)
# tag_set

# for i in script_list:
#     print(i.parent.name, i)
#     print(' ')
