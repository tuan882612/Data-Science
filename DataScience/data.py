from datasets import load_dataset
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
    arr = []
    arr2 = []
    
    for i in birth.split():
    
        if len(i) == 4 and i[0].isnumeric():
            arr2.append(i)
            
    for i in death.split():
    
        if len(i) == 4 and i[0].isnumeric():
            arr.append(i)
    
    if len(arr) == 0 or len(arr2) == 0:
        return
    
    else:
        if len(arr) > 1:
            for i in range(len(arr)):
                arr[i] = int(arr[i])
                
            death = str(max(arr))
            
        else:
            death = str(arr[0])
            
        if len(arr2) > 1:
            for i in range(len(arr2)):
                arr[i] = int(arr2[i])
                
            birth = str(max(arr2))
            
        else:
            birth = str(arr2[0])

        print(str(int(death)-int(birth)))

def get_input_text():
    data = load_dataset("wiki_bio") #['input_text', 'target_text']
    count = 0
    
    for i in zip(data['train']['input_text'][:],
                 data['train']['target_text'][:]):
        temp = parse(i[0])
        
        if len(temp) >= 5:
            # print(temp['birth_date'],temp['death_date'])
            # age = parse_age(temp['birth_date'],temp['death_date'])
            # temp['target_text'] = i[1]
            if 'occupation' in temp:
                print(temp['occupation'])
            
    # with open('data.json', 'w', encoding='utf-8') as f:
        
    #     for i in zip(data['train']['input_text'],data['train']['target_text']):
    #         temp = parse(i[0])
            
    #         if len(temp) >= 5:
    #             temp['target_text'] = i[1]
    #             json.dump(temp, f, ensure_ascii=False, indent=4)

            
    
if __name__ == "__main__":
    get_input_text()
