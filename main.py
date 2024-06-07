import pandas as pd
import text_preprocessing as tp

data = pd.read_json("data/comments_0.json", typ="series", orient="records")
print(data)

for f in tp.PROCESSES:
    data = data.apply(f)

print(data)

# "stiff...but => stiffbut"
# fix this ^