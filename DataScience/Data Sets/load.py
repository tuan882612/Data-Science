import numpy as np, pandas as pd, json

def main():
    df = json.load(open('Data-Science\data.json',encoding="utf8"))
    occupations = json.load(open('Data-Science\occupations.json',encoding="utf8"))
    exclude = ['the','and','of','at',
               'for','el', 'de','war',
               'us','in','ss', '-','man',
               'con','to','disc', 'jockey',
               'f','/', 'a','on','as','an',
               'die','i','ed','ex','c', 
               'coffee', 'watch','clock', 'vice line']
    hash = {}
    final = set()
    
    for i in range(len(df)):
        temp = df[i]['occupation'].split()
        arr = set()
        
        for j in occupations:
             
            for k in temp:
                
                if k in j and len(k)>3:
                    arr.add(k)
                    
            if len(arr) > 1:
                hash[i] = " ".join(arr)
                break
                
            else:
                arr.clear()

    for i in hash.values():
        
        final.add(i)
        
    print(final)
    
    # with open('Data-Science\profession.json', 'w', encoding='utf-8') as f:
    #     json.dump(hash, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()