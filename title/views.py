import sys
from flask import Blueprint, request
from transformers import BertJapaneseTokenizer, BertForTokenClassification
from transformers import pipeline

title = Blueprint(
    "title",
    __name__
)

@title.route("/")
def index():
    text = ""
    if request.args.get('q') is not None:
        text = request.args.get('q')
    else:
        text = "No Text"

    model = BertForTokenClassification.from_pretrained("jurabi/bert-ner-japanese")
    tokenizer = BertJapaneseTokenizer.from_pretrained("jurabi/bert-ner-japanese")

    ner_pipeline = pipeline('ner', model=model, tokenizer=tokenizer)
    outputs = ner_pipeline(text)
    print(outputs)
    
    title_tokens = []
    for output in outputs:
        if output['entity'] == 'B-製品名':
            title_tokens.append(output['word'])
        else:
            continue
    
    print(title_tokens)

    results = []
    for i in range(len(outputs)):
        if outputs[i]['entity'] == 'B-製品名':
            
            name = outputs[i]['word']
            for j in range(i+1, len(outputs)):
                if outputs[j]['entity'] == 'I-製品名':
                    name += outputs[j]['word']
                    results.append(name)
                else:
                    break
    
    return results
