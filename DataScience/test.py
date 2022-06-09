import pandas as pd, numpy as np, json

def parse(sample):
    data = sample.split(',')
    arr = []
    
    for i in range(len(data)):
        data[i] = data[i].strip()
        
    for i in data:
        
        if ',' not in i and '-' not in i and len(i) != 0:
            arr.append(i)
            
    return arr
    
def main():
    data = json.load(open('Data-Science\data.json',encoding="utf8"))
    hash = {}
    
    for sample in data:
        place = parse(sample['birth_place'])

        for i in place:
            
            if i not in hash:
                hash[i] = 1
            else:
                hash[i] += 1
    
    hash = dict(sorted(hash.items(), key= lambda x:x[1], reverse=True))
    
    # with open('states-countries.json', 'w', encoding='utf-8') as f:
    #     json.dump(hash, f, ensure_ascii=False, indent=4)
    
if __name__ == "__main__":
    main()