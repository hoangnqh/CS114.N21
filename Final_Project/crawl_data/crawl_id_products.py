import requests
import csv
import pandas as pd

url = "https://shopee.vn/api/v4/recommend/recommend"
params = {
    "bundle": "category_landing_page",
    "cat_level": "1",
    "catid": "",
    # limit : chỉnh số lượng id sản phẩm của một category
    "limit": "5",
    "offset": "60"
}
df_category=pd.read_csv('category_list.csv')
# print(df_category)
for i in df_category.values:
    params['catid']=str(i[0])


    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        # Kiểm tra phản hồi có chứa dữ liệu sản phẩm không
        print('request  thanh cong')
        product_ids=data['data']['sections'][0]['data']['item']
        if product_ids is None:
            print(str(i[0]))
        else:      
            with open('id_products.csv', 'a', encoding='utf-8', newline="") as file:
                writer = csv.writer(file)
                # writer.writerow(['id_product'])
                
                for id in product_ids:
                    id_product=id['itemid']
                    id_shop=id['shopid']
                    writer.writerow([id_product,id_shop])
                    # file.write(str(id['itemid']) +'\n')
            print('xuat file id san pham thanh cong')
        
    else:
        print("Yêu cầu không thành công.")

