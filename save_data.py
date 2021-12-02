#-*- coding:utf-8 -*-

import re, os
import pandas as pd
from glob import glob


def PreProcess(text):
    text = re.sub(pattern='Posted on [0-9]{4} [0-9]{2} [0-9]{2} .+ Posted in \S+ \s?', \
                  repl='', string=text)
    text = re.sub(pattern='Posted on [0-9]{8} .+ Posted in \S+ \s?', \
                  repl='', string=text)
    text = re.sub(pattern='[0-9]{4}년 [0-9]{,2}월 [0-9]{,2}일 [0-9]{,2}시 [0-9]{,2}분 [0-9]{,2}초', \
                  repl='', string=text)
    text = re.sub(pattern='[0-9]{4}. [0-9]{,2}. [0-9]{,2}', \
                  repl='', string=text)
    _filter = re.compile('[ㄱ-ㅣ]+')
    text = _filter.sub('', text)
    _filter = re.compile('[^가-힣 0-9 a-z A-Z \. \, \' \" \? \!]+')
    text = _filter.sub('', text)
    return text


def save_data(dir_path, save_path):
    files = [f for f in glob(dir_path + "*", recursive=True)]

    data = ''

    for file in files:
        suffix = file.split("/")[-1].split(".")[-1]

        if suffix == 'csv':
            df = pd.read_csv(file).reset_index()
            print('{} data saving. size:'.format(file.split('/')[-1]), df.shape[0])

            for i, text in enumerate(df['content'].values):
                text = PreProcess(text)
                df.loc[i, 'content'] = text

            data += "\n".join(df['content'].values)

        elif (suffix == 'txt') and (not file.split("/")[-1].startswith("data")):
            print('{} data saving.'.format(file.split('/')[-1]))
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
                text = PreProcess(text)
                data += text

    with open(save_path, 'w') as f:
        f.write(data)

    print("\nAll saved.".format(dir_path.split('/')[-1]))


data_dir = './Crawling/textcrawler/use_data/'
save_path = './Crawling/textcrawler/use_data/data.txt'

if __name__ == "__main__":
    save_data(data_dir, save_path)
