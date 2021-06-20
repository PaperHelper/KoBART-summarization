import os
import pandas as pd
import json

from kobart import get_kobart_tokenizer

train_files = os.listdir('./data/training_논문/')
test_files = os.listdir('./data/validation_논문/')

train_files = ['./data/training_논문/'+f for f in train_files]
test_files = ['./data/validation_논문/'+f for f in test_files]

train = {'paper':[],'summary':[]}
test = {'paper':[],'summary':[]}

tokenizer = get_kobart_tokenizer()

for f in train_files:
    raw = json.load(open(f))
    whole_data = raw['data']
    for data in whole_data:
        for text in data['summary_entire']:
            try:
                tokenizer.encode(text['orginal_text'])
                tokenizer.encode(text['summary_text'])
            except:
                print(text['orginial_text'])
                print(text['summary_text'])
                break
            train['paper'].append(text['orginal_text'])
            train['summary'].append(text['summary_text'])
        for text in data['summary_section']:
            try:
                tokenizer.encode(text['orginal_text'])
                tokenizer.encode(text['summary_text'])
            except:
                print(text['orginial_text'])
                print(text['summary_text'])
                break
            train['paper'].append(text['orginal_text'])
            train['summary'].append(text['summary_text'])

print(len(train['paper']),len(train['summary']))

for f in test_files:
    raw = json.load(open(f))
    whole_data = raw['data']
    for data in whole_data:
        for text in data['summary_entire']:
            try:
                tokenizer.encode(text['orginal_text'])
                tokenizer.encode(text['summary_text'])
            except:
                print(text['orginial_text'])
                print(text['summary_text'])
                break

            test['paper'].append(text['orginal_text'])
            test['summary'].append(text['summary_text'])
        for text in data['summary_section']:
            try:
                tokenizer.encode(text['orginal_text'])
                tokenizer.encode(text['summary_text'])
            except:
                print(text['orginial_text'])
                print(text['summary_text'])
                break

            test['paper'].append(text['orginal_text'])
            test['summary'].append(text['summary_text'])

print(len(test['paper']),len(test['summary']))
if None in train['summary']:
    print('None in train!')
if None in test['summary']:
    print('None in test!')

train_df = pd.DataFrame(train)
test_df = pd.DataFrame(test)

train_df = train_df.dropna()
test_df = test_df.dropna()

train_df.to_csv('./data/aihub_train.tsv',index=False,sep='\t',encoding='utf-8')
test_df.to_csv('./data/aihub_test.tsv',index=False,sep='\t',encoding='utf-8')
