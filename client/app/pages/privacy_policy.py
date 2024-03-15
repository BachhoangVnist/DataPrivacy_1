import streamlit as st
import requests
import re

# Địa chỉ URL của API FastAPI
API_URL = "http://localhost:8000/llm/policy"

# Hàm kiểm tra định dạng URL
def is_valid_url(url):
    regex = r"^(http|https)://"
    return re.match(regex, url) is not None

def show_home_page():
    # Tiêu đề của ứng dụng
    st.title("Phân tích văn bản quyền riêng tư")
    # Khung văn bản để nhập câu hỏi
    url_input = st.text_input("Nhập đường dẫn")

    # Kiểm tra và hiển thị kết quả
    if url_input:
        if is_valid_url(url_input):
            st.success("Đây là một URL hợp lệ: " + url_input)
        else:
            st.error("Đây không phải là một URL hợp lệ.")

    # Nút để gửi câu hỏi đến API và nhận câu trả lời
    if st.button("Gửi câu hỏi"):
        # Gửi request đến API và nhận câu trả lời
        # Hiển thị spinner khi đang chờ phản hồi từ server
        with st.spinner('Đang xử lý...'):
            # Gọi API từ server
            response = requests.post(
                API_URL,
                json={"url": url_input},
                timeout=10000000
            )

        # Kiểm tra xem request có thành công không
        if response.status_code == 200:
            # Hiển thị câu trả lời từ API
            st.write("Câu trả lời:", response.json()["result"])
        else:
            # Hiển thị thông báo lỗi nếu request không thành công
            st.error("Đã xảy ra lỗi khi gửi câu hỏi đến máy chủ.")

if __name__ == "__main__":
    show_home_page()
