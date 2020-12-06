import time
import json
import csv
# Author: Yueting Liao
# Date: 10/17/2020
# Purpose of the program: read json files and writes the data to CSV files (for SQL databse)

layer1_file = 'layer1.json' # layer1
nutrition_file = "recipes_nutrition_202000-203000.json"

start_time = time.time()

f = open(nutrition_file,)
f1 = open(layer1_file,)
nutrition_data = json.load(f)
layer1_data = json.load(f1) # layer1 data is a list of dictionary
print("-> Load json files in [%s] seconds\n"  % (time.time() - start_time))

# -------------------------------- Loading json to data variable -------------------------------- #

start_time = time.time()

# field names
fields = list()

for row in nutrition_data:
    fields.append('id')
    fields.append('title')
    fields.append('url')
    for key in row['recipe_nutrition'].keys():
        fields.append(key)
    for key in row['recipe_nutrition_per100g'].keys():
        fields.append(key)
    break

# for row in layer1_data:
#     print(type(row))
#     print(row['id'])
#     print(row['title'])
#     break


# -------------------------------- Find common id in two Data Set -------------------------------- #

print("It takes about 600s (10 mins) ...")

# print(fields)
# nutrition_data rows of csv file
rows = list() #rows will be list of lists

for nutrition_row in nutrition_data:
    for layer1_row in layer1_data:
        if nutrition_row['id'] == layer1_row['id']:

            recipe_attr_list = list()
            recipe_attr_list.append(layer1_row['id'])
            recipe_attr_list.append(layer1_row['title'])
            recipe_attr_list.append(layer1_row['url'])

            for value in nutrition_row['recipe_nutrition'].values():
                recipe_attr_list.append(value)
            for value in nutrition_row['recipe_nutrition_per100g'].values():
                recipe_attr_list.append(value)
            rows.append(recipe_attr_list)


print(len(rows))
print("\n-> Iterate through two dataset (nested loop) in [%s] seconds"  % (time.time() - start_time))

# -------------------------------- writing to CS file -------------------------------- #
start_time = time.time()

# writing to csv file
csv_filename = 'recipes.csv'
with open(csv_filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(fields)
    # writing the nutrition_data rows
    csvwriter.writerows(rows)
print("\n-> Write data to CSV file in [%s] seconds"  % (time.time() - start_time))


f.close()
f1.close()
