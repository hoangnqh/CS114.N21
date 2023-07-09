#get id category_list
# url: https://shopee.vn/api/v4/pages/get_category_tree

import csv
import requests 
url = "https://shopee.vn/api/v4/pages/get_category_tree"

res = requests.get(url)
data= res.json()
list=[]
if res.status_code==200:
    print("gui request thanh cong")
    
        
    with open('category_list.csv','w',encoding='utf-8',newline='') as file:
        writer= csv.writer(file)
        for i in data['data']['category_list']:
            category =str(i['catid'])
            writer.writerow([category])
    print("xuat file category list thanh cong",list)
else:
    print('gui requset that bai')
