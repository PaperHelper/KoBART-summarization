import torch
import streamlit as st
from kobart import get_kobart_tokenizer
from transformers.models.bart import BartForConditionalGeneration
import re
import nltk
nltk.download('punkt')
from math import ceil
import os

def load_model():
    model = BartForConditionalGeneration.from_pretrained('./kobart_summary')
    return model

model = load_model()
tokenizer = get_kobart_tokenizer()

def summarize(filename):

    text = open(f'./paper_kor/{filename}','rt').read()

    paragraphs = re.split('\n{4}',text)
    paragraphs = [re.split('\n{3}',p) for p in paragraphs]
    paragraphs = [[re.split('\n{2}',p2) for p2 in p1] for p1 in paragraphs]
    paragraphs = [[[t.replace('\n','') for t in p2] for p2 in p1] for p1 in paragraphs]

    to_be_summarized = []

    for first in paragraphs:
        joined = ' '.join([' '.join(second) for second in first])
        if len(tokenizer.encode(joined)) <= 512:
            to_be_summarized.append(joined)
            continue
        p = ''
        for second in first:
            joined = ' '.join(second)
            if len(tokenizer.encode(joined)) > 512:
                for third in second:
                    if len(tokenizer.encode(third)) > 512:
                        if p != '':
                            to_be_summarized.append(p)
                            p = ''
                        sents = nltk.sent_tokenize(third)
                        num = len(tokenizer.encode(third)) // 512
                        num += 1
                        num_sents = ceil(len(sents)/num)
                        index = 0
                        while index < len(sents):
                            to_be_summarized.append(' '.join(sents[index:index+num_sents]))
                            index += num_sents
                    else:
                        if p != '':
                            if len(tokenizer.encode(p)) + len(tokenizer.encode(third)) > 512:
                                to_be_summarized.append(p)
                                p = ''
                                p = third
                            else:
                                p += third
                        else:
                            p = third
            else:
                if p != '':
                    if len(tokenizer.encode(p)) + len(tokenizer.encode(joined)) > 512:
                        to_be_summarized.append(p)
                        p = joined
                    else:
                        p += joined
                else:
                    p = joined

    for p in to_be_summarized:
        print(p)
        print()

    summarized = []

    for text in to_be_summarized:
        input_ids = tokenizer.encode(text)
        input_ids = torch.tensor(input_ids)
        input_ids = input_ids.unsqueeze(0)
        output = model.generate(input_ids, eos_token_id=1, max_length=512, num_beams=5)
        output = tokenizer.decode(output[0], skip_special_tokens=True)
        summarized.append(output)
        print(output)
        print()

    return summarized

files = os.listdir('./paper_kor/')
files = [f for f in files if f.endswith('.txt')]

for f in files:
    summarized = summarize(f)
    
    with open(f'./kobart_summarized/summarized_{f}','w') as of:
        for s in summarized:
            of.write(s+'\n\n')

