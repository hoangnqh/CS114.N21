import requests
import csv
import pandas as pd
#  crawl chi danh gia

url = "https://shopee.vn/api/v2/item/get_ratings"
params = {
    "exclude_filter": "0",
    "filter": "0",
    "filter_size": "0",
    "flag": "1",
    "fold_filter": "0",
    # "itemid": "11504674171",
    # limmit :chỉnh số lựong cmt muốn crawl về 
    "limit": "20",
    "offset": "0",
    "relevant_reviews": "false",
    "request_source": "1",

    "tag_filter": "",
    # 
    "type": "0",
    "variation_filters": "",
    
    
}
df_id = pd.read_csv('id_products.csv')
print(df_id)
for i in df_id.values :
    print(i)
    params['itemid']= str(i[0])
    params['shopid']= str(i[1])
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        cmts= data['data']['ratings']
        if cmts is None:
            print(data)
        else:    
            with open('comment.csv', 'a', encoding='utf-8', newline="") as file:
                writer = csv.writer(file)
                for cmt in cmts:
                    star=str(cmt['rating_star'])
                    comment=str(cmt['comment'])
                    
                    if cmt['ItemRatingReply'] is not None:
                        respond=str(cmt['ItemRatingReply']['comment'])
                        # print('check phan hoi',cmt['ItemRatingReply']['comment'])
                    else:
                        respond=''
                    writer.writerow([star,comment,respond])
                    
                    # file.write(str('-'+cmt['comment']) +'\n')
            print('xuat file cmts  thanh cong')
        
    else:
        print("Yêu cầu không thành công.")
