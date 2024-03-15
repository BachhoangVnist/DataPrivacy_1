import streamlit as st
import requests

# Địa chỉ URL của API FastAPI
API_URL = "http://localhost:8000/llm/question_answer"
_init_messages = []

def init_page():
    # Tiêu đề của ứng dụng
    st.title("Hỏi và đáp với FastAPI")
    st.sidebar.title("Options")

def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = _init_messages

def show_home_page():
    # Tiêu đề của ứng dụng
    st.title("Hỏi và đáp với FastAPI")
    # Khung văn bản để nhập câu hỏi
    question = st.text_input("Nhập câu hỏi của bạn:")

    # Nút để gửi câu hỏi đến API và nhận câu trả lời
    if st.button("Gửi câu hỏi"):
        # Gửi request đến API và nhận câu trả lời
        # Hiển thị spinner khi đang chờ phản hồi từ server
        with st.spinner('Đang xử lý...'):
            # Gọi API từ server
            response = requests.post(
                API_URL,
                json={"question": question},
                timeout=10000000
            )

        # Kiểm tra xem request có thành công không
        if response.status_code == 200:
            # Hiển thị câu trả lời từ API
            st.write("Câu trả lời:", response.json()["result"])
        else:
            # Hiển thị thông báo lỗi nếu request không thành công
            st.error("Đã xảy ra lỗi khi gửi câu hỏi đến máy chủ.")

def main():
    init_page()
    init_messages()
    if user_input := st.chat_input("Input your question!"):
        st.session_state.messages.append(user_input)
        with st.spinner('Đang xử lý...'):
            # Gọi API từ server
            response = requests.post(
                API_URL,
                json={"question": user_input},
                timeout=10000000
            )

        # Kiểm tra xem request có thành công không
        if response.status_code == 200:
            # Hiển thị câu trả lời từ API
            st.write("Câu trả lời:", response.json()["result"])
        else:
            # Hiển thị thông báo lỗi nếu request không thành công
            st.error("Đã xảy ra lỗi khi gửi câu hỏi đến máy chủ.")
            st.session_state.messages.append(user_input)

    # Display chat history
    messages = st.session_state.get("messages", [])
    for message in messages:
        with st.chat_message("word"):
            st.markdown(message)

if __name__ == "__main__":
    main()
