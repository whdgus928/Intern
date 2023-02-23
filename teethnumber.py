import json
from collections import defaultdict
import pandas as pd
import numpy as np
'''functions'''
#중심점 계산
def center_calculator(dic):
    sum_x = 0
    x_count = 0
    sum_y = 0
    y_count = 0
    for idx, i in enumerate(dic['segmentation'][0]):
        if idx % 2 == 0:
            sum_x += i
            x_count += 1
        elif idx % 2 == 1:
            sum_y += i
            y_count += 1
    return [sum_x/x_count, sum_y/y_count, dic["category_id"]]
def distance_checker(one_point_x, one_point_y, another_point_x, another_point_y):
    return ((one_point_x - another_point_x) ** 2 + (one_point_y - another_point_y) ** 2) **(1/2)
def write_json(data, filename='file.json'): 
    # function to add to JSON 
    with open(filename,'w') as f: 
        json.dump(data, f, cls = NpEncoder, indent=4) 
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
    
    
    
    
'''main'''
with open('C:/Users/82106/Documents/PythonProject/dentistry_dataset_RP_1408.json', 'r', encoding = 'utf-8-sig') as json_file:
    st_python = json.load(json_file)
normal_teeth_list = []
problem_teeth_list = []



for annotation in st_python['annotations']:
    if len(annotation['segmentation']) > 0:
        x, y, category_number = center_calculator(annotation)
        if category_number in teeth_number_list:
            normal_teeth_list.append([x, y, category_number, annotation['image_id']])
        elif category_number in disease_list:
            problem_teeth_list.append([x, y, category_number, annotation['image_id'], annotation['area'], annotation['category_id'], annotation['bbox'], annotation['iscrowd'], annotation['segmentation'], annotation['id']])
base_df = pd.DataFrame(normal_teeth_list, columns = ['x','y','category_number','img_name'])
new_problem_teeth_list = []
for problem_teeth_list_index , problem_teeth in enumerate(problem_teeth_list):
    distance_list = []
    point_x = problem_teeth[0]
    point_y = problem_teeth[1]
    for index2 in base_df[base_df['img_name'] == problem_teeth[3]].index:
        distance_list.append([distance_checker(base_df.loc[index2,'x'], base_df.loc[index2, 'y'], point_x, point_y), base_df.loc[index2,'category_number']])
    # print(min(distance_list))
    problem_teeth.append(distance_list[distance_list.index(min(distance_list))][1])
    new_problem_teeth_list.append(problem_teeth)
# 검증용 코드
back_df = pd.DataFrame(columns = ['이미지아이디', '문제유형' ,'치아번호', 'id', '일치', '비고'])
# 검증용 코드
with open('C:/Users/82106/Documents/PythonProject/dentistry_dataset_RP_1408.json', encoding = 'utf-8-sig') as json_file: 
    data = json.load(json_file)
    length_of_id = len(st_python['annotations']) + 1
    for back_df_index, new_problem_teeth in enumerate(new_problem_teeth_list):
        dic = {}
        dic['area'] = new_problem_teeth[4]
        dic['category_id'] = new_problem_teeth[10]
        dic['bbox'] = new_problem_teeth[6]
        dic['iscrowd'] = new_problem_teeth[7]
        # dic['segmentation'] = new_problem_teeth[8]
        dic['segmentation'] = []
        dic['id'] = length_of_id
        dic['image_id'] = new_problem_teeth[3]
        # 검증용 코드
        back_df.loc[back_df_index, '이미지아이디'] = new_problem_teeth[3]
        back_df.loc[back_df_index, '문제유형'] = new_problem_teeth[5]
        back_df.loc[back_df_index, '치아번호'] = new_problem_teeth[10]
        back_df.loc[back_df_index, 'id'] = length_of_id
        # 검증용 코드
        length_of_id += 1
        data['annotations'].append(dic)
write_json(data, filename = 'C:/Users/82106/Documents/PythonProject/dentistry_dataset_RP_1408_afterProcess.json')
# 검증용 코드
check_dic = {2: '11번', 3: '12번', 4 : '13번', 5 : '14번', 6 : '15번', 7 : '16번', 8 : '17번', 9 : '18번', 10 : '21번', 11 : '22번', 12 : '23번', 13 : '24번', 14 : '25번', 15 : '26번', 16 : '27번', 17 : '28번',
18 : '31번', 19 : '32번', 20 : '33번', 21 : '34번', 22 : '35번', 23 : '36번', 24 : '37번', 25 : '38번', 26 : '41번', 27 : '42번', 28 : '43번', 29 : '44번', 30 : '45번', 31 : '46번', 32 : '47번', 33 : '48번',
34 : '충치 1단계', 35 : '충치 2단계', 36 : '충치 3단계', 37 : '보철물 아말감', 38 : '보철물 골드인레이', 39 : '치근 노출'}
back_df['문제유형'] = back_df['문제유형'].apply(lambda x : check_dic[x])
back_df['치아번호'] = back_df['치아번호'].apply(lambda x : check_dic[x])
back_df.to_csv('backs_logic.csv', encoding = 'utf-8-sig', index = False)
# 검증용 코드
''''''