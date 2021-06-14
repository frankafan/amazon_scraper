import json

START_YEAR = 2017
END_YEAR = 2021

books = []
for year in range(START_YEAR, END_YEAR + 1):
    for month in range(1, 13):
        try:
            file = open(f'{year}-{month}.txt', 'r')
            books.extend(json.loads(file.read()))
        except:
            print(f'Missing {year}-{month}.txt')
            continue

with open('data.txt', 'w') as outfile:
    json.dump(books, outfile)

print(f'{len(books)} books scraped')