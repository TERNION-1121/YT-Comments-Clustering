from json import loads, dump
import pandas as pd
import text_preprocessing as tp

print("Reading data...")
data = pd.read_json("raw-data/comments_2.json", typ="series", orient="records")
print("Data read successfully\n")

print("Processing data...")
for func in tp.PROCESSES:
    data = data.apply(func)
print("Data processed successfully\n")

print("Writing data to data/comments.json ...")
result = data.to_json(orient="values")
result = loads(result)

with open("data/comments.json", 'w', encoding='utf-8') as json_file:
    dump(result, json_file, ensure_ascii=False, indent=4)
print("Task complete")