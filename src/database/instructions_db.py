import json
import pandas as pd

output = []
f2 = open('RPI-HEALS-Food-Knowledge-master/mg/data/extracted/foodcom/index.json', 'r')
with open('RPI-HEALS-Food-Knowledge-master/mg/data/extracted/recipe1m/layer1.json', 'r') as f:
    distros_dict = json.load(f)
    hashes = json.load(f2)
    for i in range(len(distros_dict)):
        if distros_dict[i]["id"] in hashes:
            output.append(distros_dict[i])
    new = open('resource.json', 'w')
    json.dump(output[:], new)
    new.close()


f = open('resource.json', 'r')
df = pd.DataFrame(columns=['id','instruction_number','instruction'])
distros_dict = json.load(f)
for i in range(len(distros_dict)):
    print(i)
    for j, element in enumerate(distros_dict[i]["instructions"]):
        df2 = pd.DataFrame([[distros_dict[i]["id"], j+1, element["text"]]], columns=['id','instruction_number','instruction'])
        df = df.append(df2)
df.to_csv('instructions.csv', index=False)