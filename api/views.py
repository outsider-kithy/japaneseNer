import sys
from flask import Blueprint, request
from transformers import BertJapaneseTokenizer, BertForTokenClassification
from transformers import pipeline
import json

api = Blueprint(
    "api",
    __name__
)

@api.route("/")
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

    names_tokens = []
    for output in outputs:
        if output['entity'] == 'B-法人名' or output['entity'] == 'I-法人名':
            names_tokens.append(output['word'])
        else:
            continue

    print(names_tokens)

    # entityがB-法人名の後に続くI-法人名属性を持つ単語を結合し、固有名詞として配列resultsに格納
    results = []
    for i in range(len(outputs)):
        if outputs[i]['entity'] == 'B-法人名':

            name = outputs[i]['word']
            for j in range(i+1, len(outputs)):
                if outputs[j]['entity'] == 'I-法人名':
                    name += outputs[j]['word']
                else:
                    break
            results.append(name)

    #resultsをjson形式で返す
    return json.dumps(results, ensure_ascii=False)
