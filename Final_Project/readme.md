# CS114.N21 - Machine learning

## Members of group H2O
| Full name               | Student ID     |
| :---------------------- | -------------- |
| `Nguyễn Quốc Huy Hoàng` | `20520051`     |
| `Ngô Quang Vinh`        | `19522523`     |

## Đồ án cuối kỳ

### Tên đề tài: Phân loại đánh giá của khách hàng trên Shopee

### Tóm tắt đồ án

#### Nội dung mà nhóm đã làm:
-	Đề tài của nhóm là phân loại đánh giá của khách hàng về một sản phẩm (tiêu cực/ không tiêu cực) trên shopee.
-	Nhóm đã thực hiện thu thập dữ liệu bằng cách crawl các đánh giá của khách hàng trên shopee, sau đó tiến hành gán nhãn và kiểm tra chéo.
-	Từ dữ liệu có được, nhóm đã qua một số bước tiền xử lý, sau đó tiếp tục dùng PhoBERT[1], ViDeBERTa[2] để chuyển đổi văn bản thành vector đặc trưng sau đó tiến hành sử dụng các model SVM, LogisticRegression, RandomForest để huấn luyện, đánh giá, tinh chỉnh, dự đoán từ đó đưa ra được model tốt nhất mà nhóm đã thực nghiệm được.
-	Trong nội dung nhóm đã nêu ra được các câu trả lời cho câu hỏi: WHY (Tại sao lại làm đề tài này) bằng cách đưa ra các trường hợp gặp phải trong thực tế; WHAT (Đề tài này làm cái gì) bằng cách nêu rõ input, output của bài toán; HOW (Làm đề tài này như thế nào) bằng cách đưa ra hướng giải quyết.

#### Các đường dẫn:
-	Github của nhóm: https://github.com/hoangnqh/CS114.N21
-	Link đồ án: https://github.com/hoangnqh/CS114.N21/tree/master/Final_Project
-	Dataset: https://docs.google.com/spreadsheets/d/1bFf9ikhHDx9IRK6Y7wJE6jDpzME9rAAg/edit?usp=sharing&ouid=117264281666718723761&rtpof=true&sd=true
-	Notebook: https://colab.research.google.com/drive/1xXNeTfU4TVi5g6odZ0cFacTT6m3BPUGV?usp=sharing

### Nội dung, ý nghĩa của các file/thư mục:
- NhomH2O_Report.pdf: File báo cáo của nhóm
- notebook.ipynb: Notebook chứa code mà nhóm đã thực hiện
- demo.py: Code demo bằng streamlit của nhóm
- dataset.txt: Dữ liệu nhóm đã thu thập và gán nhãn
- crawl_data: Code mà nhóm đã dùng để thu thập dữ liệu
- vietnamese-stopwords.txt: file chứa các stop word mà nhóm đã tham khảo
- positive_icon: Các icon mang tính tích cực
- negative icon.txt các icon mang tính tiêu cực