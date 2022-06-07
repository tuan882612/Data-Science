from datasets import load_dataset
import json

def get_metaData(data):
    print(data['table']['column_header'])

def parse(data):
    arr = ['birth_date', 'birth_place', 'name', 'death_date','occupation','profession']
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
    print(int(death.split()[-1])-int(birth.split()[-1]))

def get_input_text():
    data = load_dataset("wiki_bio") #['input_text', 'target_text']

    for i in zip(data['test']['input_text'][:],
                 data['test']['target_text'][:]):
        temp = parse(i[0])
        
        if len(temp) >= 5:
            age = parse_age(temp['birth_date'],temp['death_date'])
            # temp['target_text'] = i[1]
            # print(temp)
            
    # with open('data.json', 'w', encoding='utf-8') as f:
        
    #     for i in zip(data['train']['input_text'],data['train']['target_text']):
    #         temp = parse(i[0])
            
    #         if len(temp) >= 5:
    #             temp['target_text'] = i[1]
    #             json.dump(temp, f, ensure_ascii=False, indent=4)

            
    
if __name__ == "__main__":
    get_input_text()