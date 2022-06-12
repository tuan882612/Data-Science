from datasets import load_dataset
import pandas as pd, numpy as np
import random
import json

def get_metaData(data):
    print(data['table']['column_header'])

def parse(data):
    arr = ['birth_date', 'birth_place', 'name', 'death_date','occupation']
    res = []
    hash = {}
    
    for i in zip(data['table']['column_header'],
                data['table']['content']):
        
        if i[0] in arr:
            res.append(i)
    
    final = sorted(res)
    
    for i in final:
        hash[i[0]] = i[1]
    
    return hash
    
def parse_age(birth, death):
    temp1 = []
    temp2 = []

    birth = birth.split()        
    death = death.split()
   
    for i in range(len(birth)):
        birth[i] = birth[i].split('-')
        
    for i in range(len(death)):
        death[i] = death[i].split('-')    
    
    
    for i in birth:
        for j in i:
            
            if len(j) >= 4 and j[:4].isnumeric():
                temp2.append(j[:4])

    for i in death:
        for j in i:
            
            if len(j) >= 4 and j[:4].isnumeric():
                temp1.append(j[:4])
    
    if len(temp1) == 0 or len(temp2) == 0:
        return str(random.randint(18,40))
    
    else:
        if len(temp1) > 1:
            for i in range(len(temp1)):
                temp1[i] = int(temp1[i])
                
            death = str(max(temp1))
            
        else:
            death = str(temp1[0])
            
        if len(temp2) > 1:
            for i in range(len(temp2)):
                temp2[i] = int(temp2[i])
                
            birth = str(max(temp2))
            
        else:
            birth = str(temp2[0])
            
        return(str(int(death)-int(birth)))

def parse_birth_location(sample):
    data = sample.split(',')
    arr = []
    
    for i in range(len(data)):
        data[i] = data[i].strip()
        
    for i in data:
        
        if ',' not in i and '-' not in i and len(i) != 0:
            arr.append(i)
            
    return arr

def search_data():
    data = json.load(open('Data-Science\data.json',encoding="utf8"))[:]
    
    state = json.load(open('Data-Science\state.json',encoding="utf8"))
    attr = json.load(open('Data-Science\Attributes.json',encoding="utf8"))
    us_attr = json.load(open('Data-Science\\us_attributes.json',encoding="utf8"))
    location = json.load(open('Data-Science\location.json',encoding="utf8"))
    traits = json.load(open('Data-Science\personality.json',encoding="utf8"))
    
    hash = {}
    
    for i in range(len(data)):
        temp = data[i]['birth_place'].split(' ')
        temp = [i for i in temp if len(i)>=4]
        personality = ""
        
        for word in temp:
            
            if word in ["usa", "u.s."]:
                word = "united states"
            
            if word in us_attr:
                personality = us_attr[word]
                
            elif word in state:
                
                if state[word] in attr:
                    personality = attr[state[word]]
                    break
                    
            elif word in location:
                
                if word in attr:
                    personality = attr[word]
                    break
        
        if len(personality) == 0:
            
            for k in temp:
                
                for j in us_attr.keys():
                    
                    if k in j:
                        personality = us_attr[j]
                        
                    else:
                        if k not in hash:
                            hash[k] = 1
                            
                        else:
                            hash[k] += 1
    print(hash)
    # with open('error.json', 'w', encoding='utf-8') as f:
    #     json.dump(hash, f, ensure_ascii=False, indent=4)

def build_locations():
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

def build_dataset():
    data = load_dataset("wiki_bio") #['input_text', 'target_text']
    
    # for i in zip(data['train']['input_text'][:],
    #              data['train']['target_text'][:]):
    #     temp = parse(i[0])
        
    #     if len(temp) >= 5:
    #         age = parse_age(temp['birth_date'],temp['death_date'])
    #         del temp['birth_date']
    #         del temp['death_date']
    #         temp['age'] = age
    #         temp['target_text'] = i[1]
            
    #         print(temp)
            
    with open('temp.json', 'w', encoding='utf-8') as f:
        
        for i in zip(data['train']['input_text'][:],
                    data['train']['target_text'][:]):
            temp = parse(i[0])
            
            if len(temp) >= 5:
                age = parse_age(temp['birth_date'],temp['death_date'])
                del temp['birth_date']
                del temp['death_date']
                temp['age'] = age
                temp['target_text'] = i[1]
            
                json.dump(temp, f, ensure_ascii=False, indent=4)

def build_us_attributes():
    df = pd.read_csv("Data-Science\DataScience\Data Sets\load.csv")['state']
    hash = {}

    for i in range(6,len(df)+1,6):
        data = list(df[i-6:i])
        state = data[1].lower()
        type = data[4].lower()
        hash[state] = type+'-t'
       
    personality_types = {}
    
    for type in hash.values():
        
        if type not in personality_types:
            personality_types[type] = 1
            
        else:
            personality_types[type] += 1
            
    with open('us_attributes.json', 'w', encoding='utf-8') as f:
        json.dump(hash, f, ensure_ascii=False, indent=4)
    
def build_attributes():
    df = pd.read_csv('Data-Science\DataScience\Data Sets\mbti-countries.csv')
    
    hash = {}
    names = [df['Country'][i] for i in range(len(df))]

    for i in range(len(df)):

        header = list(df.loc[df['Country'] == names[i]])
        data = list(df.loc[i])

        extro = 0
        intro = 0
        
        ehash = {}
        ihash = {}
        
        for j in zip(header, data):
            col = j[0]
            num = j[1]

            if col[0] == 'E':
                extro += num
                ehash[num] = col
                
            elif col[0] == 'I':
                intro += num
                ihash[num] = col
                
        if extro > intro:
            hash[names[i].lower()] = ehash[max(ehash.keys())].lower()

        else:
            hash[names[i].lower()] = ihash[max(ihash.keys())].lower()
            
    with open('attributes2.json', 'w', encoding='utf-8') as f:
        json.dump(hash, f, ensure_ascii=False, indent=4)
    
if __name__ == "__main__":
    # build_dataset()
    # build_attributes()
    # build_us_attributes()
    # build_locations()
    search_data()
    
    """
    
    dataset json format and data distribute
    
    data
    {
        "birth_place"
        "name"
        "occupation":
        "age":
        "target_text":
    }
    
    location -> old format
    {
        "country":[
            "state"
        ]
    }
    
    location
    {
        "state":"country"
    }
    
    distribution for attribute dataset ->
    [
        'estj-a': 3,    'esfj-a': 20,   'enfp-t': 60,
        'infp-t': 75
    ] 
    
    attribute
    {
        "country":[
           "attribute"
           "personality type"
        ]
    }
    
    distribution for us_attributes dataset ->
    [
        'esfp-t': 3,    'intp-t': 3,    'entj-t': 3, 
        1'estj-t': 5,    'entp-t': 1,    'istp-t': 7,
        'enfj-t': 1,    'isfj-t': 6,    'isfp-t': 2,
        'istj-t': 6,    1'esfj-t': 8,    1'infp-t': 1, 
        'estp-t': 4
    ]
    
    us_attribues
    {
        "state":"type"
    }
    
    personality
    {
        "type":{
            "career":[]
            "personalitys":[]
        }
    }
    """