import csv

csvR  = open("tags.csv", "r")
reader = csv.reader(csvR)

csvW = open("result.csv", "w",newline='')
writer = csv.writer(csvW)

fileHeader = ["id", "tags"]
writer.writerow(fileHeader)



first_row=0
for item in reader:
    first_col=0
    id = ""
    if first_row == 0:
        first_row = first_row+1
        continue
    print(item)
    for i in item:
        if first_col==0:
            id = i
        elif i == '':
            continue
        else:
            temp = [id,i]
            writer.writerow(temp)
        first_col = first_col+1

csvW.close()
csvR.close()
