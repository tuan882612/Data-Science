from datasets import load_dataset
import pandas as pd
import numpy as np
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

def parse_raw_big5():
    df = pd.read_csv(".\DataScience\Data Sets\\big5_data.csv.csv")
    df1 = pd.read_csv(".\DataScience\Data Sets\\big5_data1.csv")

    #df 17  df1 23
    
    parameters = ['gender', 'age', 'marstatus', 'country', 'state']

    questions = list(df.columns[17:])
    sample = df[parameters+questions][:].fillna('-')

    questions1 = list(df1.columns[23:])
    sample1 = df1[parameters+questions1][:].fillna('-')
    
    arr = []
    
    for i in range(len(sample)):
        temp = dict(sample.iloc[i])
        hash = {}
        
        if temp['country'] != '-' or temp['state'] != '-':
            for key, val in temp.items():
                key = key.lower()

                if val != '-':
                    if type(val) != str:
                        val = int(val)
                            
                        if val >= 5 or key == 'age':
                            hash[key] = val
                    else:
                        val = val.lower()
                        hash[key] = val
                
            arr.append(hash)

    # with open('./format_v2.json', 'w', encoding='utf-8') as f:
    #     json.dump(arr, f, ensure_ascii=False, indent=4)
    
def get_error(data):
    error = []

    for key, val in data.items():
        if val not in data:
            error.append((key, val))
            
    if len(error) == 0: 
        return None
    return error

def build_country_key1():
    c1 = json.load(open('Data-Science\\format_v2.json',encoding="utf8"))
    c2 = json.load(open('Data-Science\\format2_v2.json',encoding="utf8"))
    ref = json.load(open('Data-Science\\temp.json',encoding="utf8"))

    error = set()
    
    for i in c1:
        for j in c2:
            if i["country"] != j["country"]:
                error.add(i["country"] )
                
    # for i in c2:
    #     if i not in c1:
    #         hash[i] = ref[i]
    #     else:
    #         hash[i] = c2[i]
            
    # print(hash)
    
    with open('Data-Science\error.json', 'w', encoding='utf-8') as f:
        json.dump(error, f, ensure_ascii=False, indent=4)
    
def build_big5_key():
    df = pd.read_csv("Data-Science\DataScience\Data Sets\\big5_data.csv").fillna('-')
    data = dict(zip(df['index'],df['item']))

    df2 = pd.read_csv("Data-Science\DataScience\Data Sets\\big5_data1.csv").fillna('-')
    ref = dict(zip(df2['text'],df2['label']))

    if get_error(data) == 0:
        hash = {}
        
        for key, val in data.items():
            hash[key] = ref[val]

        print(hash)
    # with open('./big5_key.json', 'w', encoding='utf-8') as f:
    #     json.dump(hash, f, ensure_ascii=False, indent=4)

def build_big5_final_dataset():
    data = json.load(open('Data-Science\\format_v2.json',encoding="utf8"))
    trait = json.load(open('Data-Science\\big5_key.json',encoding="utf8"))
    country = json.load(open('Data-Science\country_key.json',encoding="utf8"))
    
    headers = ['gender', 'age', 'marstatus', 'country', 'state']
    arr = []
    
    for node in data:
        hash = {}
        temp = []
        
        for key in node:
            if key not in headers and key in trait:
                temp.append(trait[key])
        
        for i in headers:
            if i in node:
                hash[i] = node[i]
            
        hash['trait'] = temp
        hash['country'] = country[hash['country'].upper()]
        arr.append(hash)
        
    with open('Data-Science\\big5_final', 'w', encoding='utf-8') as f:
        json.dump(arr, f, ensure_ascii=False, indent=4)
        
def build_big5_dataset():
    df = pd.read_csv(".\DataScience\Data Sets\\big5_data.csv.csv")
    df1 = pd.read_csv(".\DataScience\Data Sets\\big5_data1.csv")

    #df 17  df1 23
    parameters = ['gender', 'age', 'marstatus', 'country', 'state']

    questions = list(df.columns[17:])
    sample = df[parameters+questions][:].fillna('-')

    questions1 = list(df1.columns[23:])
    sample1 = df1[parameters+questions1][:].fillna('-')

    final = parse_raw_big5(sample)
    print(final)
    
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
        hash[state] = type
       
    personality_types = {}
    
    for type in hash.values():
        
        if type not in personality_types:
            personality_types[type] = 1
            
        else:
            personality_types[type] += 1
            
    with open('us_attributes.json', 'w', encoding='utf-8') as f:
        json.dump(hash, f, ensure_ascii=False, indent=4)
    
def build_career_attr():
    df = pd.read_csv("Data-Science\DataScience\Data Sets\load.csv")
    arr = [
    "artist",
    "actor",
    "counselor",
    "social worker",
    "athletic coach",
    "child care provider",
    "musician",
    "psychologist",
    "human resources specialist",
    "fashion designer"
        ]
    
    hash = {}

    for i in list(df['item']) + arr:
        i = i.lower()
        if i not in hash:
            hash[i] = 1
            
        else:
            hash[i] += 1
            
    with open('./format.json', 'w', encoding='utf-8') as f:
        json.dump(list(sorted(hash.keys())), f, ensure_ascii=False, indent=4)

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
            hash[names[i].lower()] = ehash[max(ehash.keys())].lower()[:4]

        else:
            hash[names[i].lower()] = ihash[max(ihash.keys())].lower()[:4]
            
    with open('attributes2.json', 'w', encoding='utf-8') as f:
        json.dump(hash, f, ensure_ascii=False, indent=4)


def build_dataset2():
    data = json.load(open(
        'Data-Science\states_occupations_no_income.json'
        ,encoding="utf8"))
    
    hash = {}
    var = []
    
    for i in range(len(data)):
        state = data[i]
        hash[state['state'].lower()] = [i.lower() for i in state['occupation']]
        var.append((state['state'],len(state['occupation'])))
        
    with open('Data-Science\\data2.json', 'w', encoding='utf-8') as f:
        json.dump(hash, f, ensure_ascii=False, indent=4)
        
    # count = {}
    
    # for name, lent in var:
    #     arr = list(hash[name])
        
    #     for i in range(lent):
    #         item = arr[i]
            
    #         if item not in count:
    #             count[item] = 1
                
    #         else:
    #             count[item] += 1
                
    #     print(max(count.values()))
    #     count.clear()

def build_dataset3():
    data = json.load(open(
        'Data-Science\median_age_occupations.json'
        ,encoding="utf8"))[1:]
    
    """    
    headers = ['occupation',
               'age_16_19', 'age_20_24',
               'age_25_34', 'age_35_44',
               'age_45_54', 'age_55_64',
               'age_65', 
               'median_age']
    """
    hash = {}
    
    for i in range(len(data)):
        item = list(data[i].values())
        hash[item[0].lower()] = item[1:]
        
    with open('Data-Science\data3.json', 'w', encoding='utf-8') as f:
        json.dump(hash, f, ensure_ascii=False, indent=4)
        
def build_dataset4():
    data = json.load(open(
        'Data-Science\states_occupation.json'
        ,encoding="utf8"))
    hash = {}
    
    for i in range(len(data)):
        state = data[i]['state'].lower()
        occup = {}
    
        for node in data[i]['occupation']:
            occup[node['job'].lower()] = [node['income'],
                                        node['employment']]   
        hash[state] = occup
        
    with open('Data-Science\\data4.json', 'w', encoding='utf-8') as f:
        json.dump(hash, f, ensure_ascii=False, indent=4)
        

def search_data():
    data = json.load(open('Data-Science\data.json',encoding="utf8"))[:]
    
    state = json.load(open('Data-Science\location2.json',encoding="utf8"))
    attr = json.load(open('Data-Science\\attributes.json',encoding="utf8"))
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

def search_data2():
    data = json.load(open(
        'Data-Science\data2.json'
        ,encoding="utf8"))
    
    meta = json.load(open(
        'Data-Science\data3.json'
        ,encoding="utf8"))
    
    # values to use
    state = 'Alabama'
    occuppation = 'Project Management Specialists'
    
    for i in data[state]:
        
        if i == occuppation and i in meta:
            print("found")
            
def test():
    pass

if __name__ == "__main__":
    # build_dataset()
    # build_dataset2()
    # build_dataset3()
    # build_dataset4()
    # build_attributes()
    # build_big5_dataset()
    # build_big5_final_dataset()
    # build_big5_key()
    build_country_key1()
    # build_us_attributes()
    # build_career_attr()
    # build_locations()
    # parse_raw_big5()
    # search_data()
    # search_data2()
    # test()
    pass
    
    """
    dataset json format and data distribute
    
    big5_key
    {
        "q_{ number }":"trait"
    }
    
    format_v2 and format2_v2
    [
        {
            "gender":,
            "age":,
            "marstatus":,
            "country":,
            "state":,
            "q_{ number }":
        }
    ]
    
    big5_final_dataset
    [
        {
            "gender":,
            "age":,
            "marstatus":,
            "country":,
            "state":,
            "trait": [
            ]
        }
    ]
    
    states_occupation
    {
        "state": {
            "occupation": 
            [
                "income",
                "employment"
            ]
        }
    }
    
    states_occupations_no_income
    {
        "state":,
        "occupations":[]
    }
    
    median_age_occupations
    [
        {
            "occupation":"Management, business, and financial operations occupations",
            "age_16_19":"100","age_20_24":"1,052",
            "age_25_34":"5,726","age_35_44":"6,783",
            "age_45_54":"6,603","age_55_64":"5,411",
            "age_65":"2,189",
            "median_age":"45.5"
        }
    ]
    
    data
    {
        "birth_place":
        "name":
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
    
    location1
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
