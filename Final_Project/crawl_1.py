import requests
import csv
import pandas as pd

from urllib.parse import urlparse

# Liên kết Shopee
shopee_link = "https://shopee.vn/Card-Wifi-laptop-th%C3%A1o-m%C3%A1y-i.624275286.21378098787?sp_atk=0c7a462e-c6d4-4bcc-bf68-2cca1a9e2739&xptdk=0c7a462e-c6d4-4bcc-bf68-2cca1a9e2739"

# Phân tích liên kết Shopee
parsed_url = urlparse(shopee_link)

# Lấy shopId
shop_id = parsed_url.path.split('.')[-2]

# Lấy itemId
item_id = parsed_url.path.split('.')[-1].split('?')[0]

url = "https://shopee.vn/api/v2/item/get_ratings"
params = {
    "exclude_filter": "0",
    "filter": "0",
    "filter_size": "0",
    "flag": "1",
    "fold_filter": "0",
    #chỉnh id sản phẩm và id shop
    "itemid": item_id,
    "shopid": shop_id,
    # limmit :chỉnh số lựong cmt muốn crawl về 
    "limit": "50",
    "offset": "0",
    "relevant_reviews": "false",
    "request_source": "1",

    "tag_filter": "",
    # 
    "type": "0",
    "variation_filters": "",
    
    
}

# params['itemid']= str(i[0])
# params['shopid']= str(i[1])
response = requests.get(url, params=params)
data = response.json()

if response.status_code == 200:
    cmts= data['data']['ratings']
    if cmts is None:
        print(data)
    else:    
        with open('comment_1.csv', 'a', encoding='utf-8-sig', newline="") as file:
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
