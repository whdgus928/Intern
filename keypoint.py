import json
from collections import defaultdict
import pandas as pd
import numpy as np

'''functions'''
#직사각형 중심점 계산
def rec_center_calculator(dic):
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


#키포인트 중심점 계산
def center_calculator(dic):
    x=(dic['keypoints'][0][0]+dic['keypoints'][2][0])/2
    y=(dic['keypoints'][0][1]+dic['keypoints'][2][1])/2
    return [x, y]

#거리계산
def distance_checker(rec_x, rec_y, key_x, key_y):
    return ((rec_x - key_x) ** 2 + (rec_y - key_y) ** 2) **(1/2)


'''main'''

keypoint_df = pd.DataFrame(columns=('area','category_id','num_keypoints','bbox','iscrowd','segmentation','id','image_id','keypoints','x','y','teeth_number'))
rec_df=pd.DataFrame(columns=('area','category_id','bbox','iscrowd','segmentation','id','image_id','x','y'))

with open('C:\\Users\\user\\Desktop\\python\\test\\이대목동병원\\dentistry_dataset_KP_1408.json', 'r', encoding = 'utf-8-sig') as json_file:
    st_python = json.load(json_file)

with open('C:\\Users\\user\\Desktop\\python\\test\\이대목동병원\\dentistry_dataset_RP_1408 (1).json', 'r', encoding = 'utf-8-sig') as json_file:
    rec_python = json.load(json_file)

teeth_number_list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
disease_list = [34, 35, 36, 37, 38, 39]
normal_teeth_list = []
problem_teeth_list = []

#키포인트 불러와서 데이터프레임 만들기
for idx, annotation in enumerate(st_python['annotations']):
    if len(annotation['keypoints']) > 0:
        x, y = center_calculator(annotation)
        
        keypoint_df.loc[idx, 'area'] = annotation['area']
        keypoint_df.loc[idx, 'category_id'] = annotation['category_id']
        keypoint_df.loc[idx, 'num_keypoints'] = annotation['num_keypoints']
        keypoint_df.loc[idx, 'bbox'] = annotation['bbox']
        keypoint_df.loc[idx, 'iscrowd'] = annotation['iscrowd']
        keypoint_df.loc[idx, 'segmentation'] = annotation['segmentation']
        keypoint_df.loc[idx, 'id'] = annotation['id']
        keypoint_df.loc[idx, 'image_id'] = annotation['image_id']
        keypoint_df.loc[idx, 'keypoints'] = annotation['keypoints']
        keypoint_df.loc[idx, 'x'] = x
        keypoint_df.loc[idx, 'y'] = y
        # if category_number in teeth_number_list:
        #     normal_teeth_list.append([x, y, category_number, annotation['image_id']])
        # elif category_number in disease_list:
        #     problem_teeth_list.append([x, y, category_number, annotation['image_id'], annotation['area'], annotation['category_id'], annotation['bbox'], annotation['iscrowd'], annotation['segmentation'], annotation['id']])


# 직사각형 라벨링정보 불러와서 데이터프레임 만들기
for idx, annotation in enumerate(rec_python['annotations']):
    if len(annotation['segmentation']) > 0:
        x, y, category_number = rec_center_calculator(annotation)
        
        rec_df.loc[idx, 'area'] = annotation['area']
        rec_df.loc[idx, 'category_id'] = annotation['category_id']
        rec_df.loc[idx, 'bbox'] = annotation['bbox']
        rec_df.loc[idx, 'iscrowd'] = annotation['iscrowd']
        rec_df.loc[idx, 'segmentation'] = annotation['segmentation']
        rec_df.loc[idx, 'id'] = annotation['id']
        rec_df.loc[idx, 'image_id'] = annotation['image_id']
        rec_df.loc[idx, 'x'] = x
        rec_df.loc[idx, 'y'] = y
        # if category_number in teeth_number_list:
        #     normal_teeth_list.append([x, y, category_number, annotation['image_id']])
        # elif category_number in disease_list:
        #     problem_teeth_list.append([x, y, category_number, annotation['image_id'], annotation['area'], annotation['category_id'], annotation['bbox'], annotation['iscrowd'], annotation['segmentation'], annotation['id']])

check_dic = {0:999999,2: 11, 3: 12, 4 : 13, 5 : 14, 6 : 15, 7 : 16, 8 : 17, 9 : 18, 10 : 21, 11 : 22, 12 : 23, 13 : 24, 14 : 25, 15 : 26, 16 : 27, 17 : 28,
18 : 31, 19 : 32, 20 : 33, 21 : 34, 22 : 35, 23 : 36, 24 : 37, 25 : 38, 26 : 41, 27 : 42, 28 : 43, 29 : 44, 30 : 45, 31 : 46, 32 : 47, 33 : 48}
#거리계산
for keypoint_df_index in keypoint_df.index:
    #이미지가 같은 rp 리스트
    same_image=[]
    index_list=[]
    #직사각형df에서 이미지 번호 같은 인덱스 찾기
    for rec_df_index in rec_df.index:
        if rec_df.loc[rec_df_index,'image_id']==keypoint_df.loc[keypoint_df_index, 'image_id']:
            same_image.append(distance_checker(rec_df.loc[rec_df_index,'x'],rec_df.loc[rec_df_index,'y'],keypoint_df.loc[keypoint_df_index,'x'],keypoint_df.loc[keypoint_df_index,'y']) )
            index_list.append(rec_df_index)
    tmp=index_list[same_image.index(min(same_image))]
    #print(tmp)
    keypoint_df.loc[keypoint_df_index,'teeth_number']=rec_df.loc[tmp,'category_id']

# csv 파일로 저장
keypoint_df.to_csv('keypoint.csv',index=False,encoding = 'utf-8-sig')
rec_df.to_csv('rec.csv',index=False,encoding = 'utf-8-sig')
print(keypoint_df)