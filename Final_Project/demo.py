# Họ và tên: Nguyễn Quốc Huy Hoàng
# MSSV: 20520051
# Lớp: CS116.N11.KHTN

import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import codecs
from joblib import load
import requests
import csv
import re
import underthesea # Thư viện tách từ
import torch
from transformers import AutoModel, AutoTokenizer
from transformers.tokenization_utils_base import TruncationStrategy
from urllib.parse import urlparse
from pyvi import ViTokenizer, ViPosTagger # thư viện NLP tiếng Việt

col1, col2, col3 = st.columns([1, 5, 1])
col1.write("")
col2.write("""# Phân loại đánh giá của khách hàng trên Shopee""")
col3.write("")

# st.write('### Phân loại theo số sao mà khách hàng đánh giá')
# Hiển thị danh sách checkbox
# Hiển thị danh sách checkbox với giá trị mặc định là chọn tất cả
# options = ['1 sao', '2 sao', '3 sao', '4 sao', '5 sao']
# selected_options = st.multiselect('Chọn các tùy chọn:', options, default=options)
# st.write("")
# st.write("")
# st.markdown("<hr>", unsafe_allow_html=True)

######################################################
st.write('### Nhập link sản phẩm')
url = st.text_input("Nhập đường link:")

def is_valid_shopee_link(url):
    # Biểu thức chính quy để kiểm tra đường link Shopee
    shopee_regex = r"(?:https?:\/\/)?(?:www\.)?(?:shopee\.vn|shopee\.com\.vn)\/.*"
    
    # Kiểm tra khớp với biểu thức chính quy
    if re.match(shopee_regex, url):
        response = requests.get(url)
        # Kiểm tra mã trạng thái HTTP của phản hồi
        if response.status_code == 200:
            return True
        else:
            return False
    else:
        return False
    
    
def get_data(url):
    # Phân tích liên kết Shopee
    parsed_url = urlparse(url)

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
        "limit": "59",
        "offset": "0",
        "relevant_reviews": "false",
        "request_source": "1",

        "tag_filter": "",
        # 
        "type": "0",
        "variation_filters": ""
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200:
        cmts= data['data']['ratings']
        if cmts is None:
            print(data)
        else:
            df = {}
            stars = []
            comments = []
            responds = []
            for cmt in cmts:
                star=str(cmt['rating_star'])
                comment=str(cmt['comment'])
                
                if cmt['ItemRatingReply'] is not None:
                    respond=str(cmt['ItemRatingReply']['comment'])
                    # print('check phan hoi',cmt['ItemRatingReply']['comment'])
                else:
                    respond=''
                stars.append(star)
                comments.append(comment)
                responds.append(respond)  
                # file.write(str('-'+cmt['comment']) +'\n')
            df['star'] = stars
            df['comment'] = comments
            df['respond'] = responds
            df = pd.DataFrame(df)
            return df
        
    else:
        st.write("Lấy dữ liệu không thành công")
    return []

###################################################################################

tichcuc = "sản phẩm tốt chất lượng tốt "
tieucuc = "sản phẩm tệ kém chất lượng "
with open('icon_tieu_cuc.txt', 'r', encoding='utf-8') as file:
    icon_tieu_cuc = file.read()
with open('icon_tich_cuc.txt', 'r', encoding='utf-8') as file:
    icon_tich_cuc = file.read()
# Hàm chuẩn hoá câu
def standardize_data(row):
    # Icon biểu tượng
    for val in row:
        if val in icon_tich_cuc:
            row = tichcuc + row
        if val in icon_tieu_cuc:
            row = tieucuc + row
    # Xoá hết những cái không phải chữ và số
    row =  re.sub(r"[^\w\s]", " ", row)
    
    # # Xóa dấu chấm, phẩy, hỏi ở cuối câu
    # row = re.sub(r"[\.,\?]+$-", "", row)
    # # Xóa tất cả dấu chấm, phẩy, chấm phẩy, chấm thang, ... trong câu
    # row = row.replace(",", " ").replace(".", " ") \
    #     .replace(";", " ").replace("“", " ") \
    #     .replace(":", " ").replace("”", " ") \
    #     .replace('"', " ").replace("'", " ") \
    #     .replace("!", " ").replace("?", " ") \
    #     .replace("-", " ").replace("?", " ")
    # # Nếu có nhiều khoảng trắng thì rút gọn còn 1
    row = row.replace('\n'," ")
    row = re.sub(r"\s+", " ", row)
    # Đưa hết về chữ thường
    row = row.strip().lower()
    str = ""
    str += row[0]
    for i in range(1, len(row)):
        if row[i] != row[i - 1]:
            str += row[i]
    # pprint(str)
    # print(ascii(row[16]))
    # Chuyển thành dạng không dấu
    # str = unidecode(str)
    return str


# Hàm tạo ra bert features
def make_bert_features(v_text):
    model_trans = AutoModel.from_pretrained("vinai/phobert-base-v2")
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
    v_tokenized = []
    max_len = 150 # Mỗi câu dài tối đa 200 từ
    for i_text in v_text:
        # print("Đang xử lý line = ", i_text)
        # Chuẩn hóa
        
        i_text = i_text.replace("\n"," ")
        i_text = standardize_data(i_text)

        # # Phân thành từng từ
        # line = underthesea.word_tokenize(i_text)

        # # Lọc các từ vô nghĩa
        # # filtered_sentence = [w for w in line if not w in sw]
        # filtered_sentence = line

        # # Ghép lại thành câu như cũ sau khi lọc
        # line = " ".join(filtered_sentence[:100])
        # line = underthesea.word_tokenize(line, format="text")
        line = ViTokenizer.tokenize(i_text)[:150]
    

        # print("Word segment  = ", line)
        # Tokenize bởi BERT
        line = tokenizer.encode(line)
        v_tokenized.append(line)

    padded = []
    # Chèn thêm số 1 vào cuối câu nếu như không đủ từ hoặc xóa nếu dư
    for line in v_tokenized:
        if len(line) < max_len:
            padded.append(line + [1] * (max_len - len(line)))
        else:
            padded.append(line[: max_len])
    padded = np.array(padded)

    # print('padded:', padded[0])
    # print('len padded:', padded.shape)

    # Đánh dấu các từ thêm vào = 0 để không tính vào quá trình lấy features
    attention_mask = np.where(padded == 1, 0, 1)
    # print('attention mask:', attention_mask[0])

    # Chuyển thành tensor
    padded = torch.tensor(padded).to(torch.long)
    print("Padd = ",padded.size())
    attention_mask = torch.tensor(attention_mask)

    # Lấy features dầu ra từ BERT
    with torch.no_grad():
        last_hidden_states = model_trans(input_ids= padded, attention_mask=attention_mask)

    v_features = last_hidden_states[0][:, 0, :].numpy()
    print(v_features.shape)
    return v_features

def predict(data):
    test = []
    for val in data:
        test.append(val)
    test = make_bert_features(test)
    file_path = './save_model.joblib'
    model = load(file_path)
    pred = model.predict(test)
    return pred

# Xử lý khi người dùng nhấn nút "Submit"
if st.button("Phân loại"):
    # Kiểm tra xem đường link có hợp lệ hay không
    if is_valid_shopee_link(url):
        st.write("#### Lấy dữ liệu")
        data = get_data(url)
        st.write(data)

        st.write("#### Phân loại")
        # for i in range(len(data)):
        #     data['comment'][i] = 'a ' + data['comment'][i]
        data_cmt = []
        for i in range(len(data['comment'])):
            val = data['comment'][i]
            val = val.replace(" ", "")
            if val == "":
                continue
            # st.write(val)
            data_cmt.append(data['comment'][i])

        label = predict(data_cmt)
        new_label = []
        cnt = 0
        for i in range(len(data['comment'])):
            val = data['comment'][i]
            val = val.replace(" ", "")
            if val == "":
                if int(data['star'][i]) < 4:
                    new_label.append(1)
                else:
                    new_label.append(0)
            else:
                new_label.append(label[cnt])
                cnt += 1
            
        data['label'] = new_label
        # Hàm áp dụng màu cho hàng

        list_a = []
        for i in range(len(data)):

            if data['star'][i] == '5' and data['label'][i] == 1:
                list_a.append(i)
                # Áp dụng hàm cho DataFrame
        styled_df = data.style.apply(lambda x: ['background-color: red' if x.name in list_a else '' for _ in x], axis=1)
        st.write(styled_df)
        
    else:
        st.error("Đường link không hợp lệ!")

        
    
st.write("")
st.write("")
st.markdown("<hr>", unsafe_allow_html=True)
st.write('### Dự đoán qua file')


uploaded_file = st.file_uploader("Select file")
if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)

    st.write("Coming soon")
    # st.write("Dữ liệu bạn cung cấp")
    # st.write(df)

    # sinh_vien = pd.DataFrame(df.iloc[:, :2].copy())

    # new_df = df.drop(df.columns[:2], axis=1)

    # dtbhk_thu1 = []
    # dtbhk_thu2 = []

    # def remove_nan_none(arr):
    #     arr = np.array(arr)
    #     arr = arr[~np.isnan(arr)]
    #     arr = arr[arr != None]
    #     return arr.tolist()

    # for index, row in new_df.iterrows():
    #     arr = row.values
    #     arr = arr.flatten()
    #     arr = remove_nan_none(arr)
    #     val1, val2 = predict(arr)
    #     dtbhk_thu1.append(val1)
    #     dtbhk_thu2.append(val2)
        
    # sinh_vien['dtbhk_thu'+str(num_sem+1)] = dtbhk_thu1
    # if num_target == 2:
    #     sinh_vien['dtbhk_thu'+str(num_sem+2)] = dtbhk_thu2
    # st.write("Kết quả dự đoán")
    # st.write(sinh_vien)
    
    # # Lưu DataFrame thành file CSV với mã hóa UTF-8 BOM
    # filename = 'predicted_results.csv'
    # with codecs.open(filename, 'w', 'utf-8-sig') as file:
    #     sinh_vien.to_csv(file, index=False, sep=',', encoding='utf-8-sig')

    # # Tạo nút tải xuống
    # with open(filename, 'rb') as file:
    #     csv = file.read()
    # st.download_button('Tải file kết quả xuống', csv, file_name=filename, mime='text/csv')
else:
    st.write("Định dạng file yêu cầu:")  
    st.write("<p style='font-size: 15px;'>- File ở định dạng .csv</p>", unsafe_allow_html=True)
    st.write("<p style='font-size: 15px;'>- Đường link ở cột đầu tiên</p>", unsafe_allow_html=True)
    st.write("<p style='font-size: 15px;'>- Mỗi hàng là một link</p>", unsafe_allow_html=True)

    st.write("Dữ liệu mẫu")
    df_demo = {
        'link_shopee': [
            'https://shopee.vn/(MI%E1%BB%84N-SHIP-TO%C3%80N-QU%E1%BB%90C)-X%E1%BA%A2-H%E1%BA%BET-KHO)-micro-cho-m%E1%BB%8Di-lo%E1%BA%A1i-loa-MICRO-CHO-LOA-K%C3%89O-BLUETOOTH-P88-P89-MICRO-d%C3%A0n-i.697521605.15190730746?sp_atk=67387503-4591-49e0-abaf-abd61a37597b&xptdk=67387503-4591-49e0-abaf-abd61a37597b',
            'https://shopee.vn/Loa-Bluetooth-kh%C3%B4ng-d%C3%A2y-TG271-c%C3%B4ng-su%E1%BA%A5t-10W-Extra-Bass-pin-tr%C3%A2u-d%C3%B9ng-%C4%91%C6%B0%E1%BB%A3c-5h-h%E1%BB%97-tr%E1%BB%A3-Bluetooth-Th%E1%BA%BB-Nh%E1%BB%9B-USB-AUX-%C4%91%C3%A0i-FM-i.80458786.20450663119?sp_atk=0a52b9e8-261b-445c-864b-2d827e923d06&xptdk=0a52b9e8-261b-445c-864b-2d827e923d06',
            'https://shopee.vn/Loa-Bluetooth-Zealot-S51-Bass-Si%C3%AAu-Tr%E1%BA%A7m-%C3%82m-Thanh-Ch%E1%BA%A5t-H%E1%BB%97-Tr%E1%BB%A3-K%E1%BA%BFt-N%E1%BB%91i-2-Loa-TWS-Ho%C3%A0ng-Y%E1%BA%BFn-Computer-i.8563637.23305112150?sp_atk=08fd6013-cbb7-4dd4-b0b6-4ae6d5edc01f&xptdk=08fd6013-cbb7-4dd4-b0b6-4ae6d5edc01f'
        ]
    }
    df = pd.DataFrame(df_demo)
    st.write(df)