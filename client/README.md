# Chương Trình Kiến Trúc RAG

## Giới thiệu

Chương trình này được xây dựng dựa trên kiến trúc RAG, sử dụng langchain, MongoDB và LLM để trả lời các câu hỏi về quyền riêng tư của Việt Nam.

## Các công nghệ sử dụng

- **RAG (Retrieval-Augmented Generation)**: Một kiến trúc mạng nơ-ron được sử dụng để trả lời các câu hỏi phức tạp.
- **Langchain**: Một công cụ xử lý ngôn ngữ tự nhiên giúp chương trình hiểu và trả lời các câu hỏi.
- **MongoDB**: Một hệ thống quản lý cơ sở dữ liệu NoSQL, được sử dụng để lưu trữ và truy xuất dữ liệu.
- **LLM (Legal Language Model)**: Một mô hình ngôn ngữ được huấn luyện đặc biệt để hiểu và trả lời các câu hỏi pháp lý.

## Lưu trữ dữ liệu

Chương trình tiến hành lưu trữ dữ liệu bao gồm pdf, csv, raw text trên MongoDB. Điều này giúp chương trình có thể truy xuất và sử dụng dữ liệu một cách nhanh chóng và hiệu quả.

# Hướng dẫn cài đặt và môi trường

## Môi trường

### Python

Đảm bảo bạn đã cài đặt Python 3.10.12 trước khi tiếp tục. Bạn có thể tìm hiểu cách cài đặt Python tại [python.org](https://www.python.org/downloads/).
Hoặc bạn có thể làm theo hướng dẫn sau
```bash
sudo apt update && sudo apt upgrade
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install python3.10.12
python3 --version
```

### pip

pip là trình quản lý gói cho Python. Đảm bảo bạn đã cài đặt pip phiên bản 24.0. Nếu chưa, bạn có thể cài đặt bằng cách chạy lệnh sau:

```bash
python3 -m pip install --upgrade pip==24.0
```

# Hướng dẫn cài đặt project

Dưới đây là các bước cần thực hiện để cài đặt và chạy project:

1. **Tạo file .env**: 
    Đầu tiên, bạn cần tạo một file `.env` từ file `env.example` và cung cấp các thông tin cấu hình cần thiết. Đảm bảo rằng các thông tin như đường dẫn đến MongoDB, API keys, và các thông tin khác đã được cung cấp đầy đủ và chính xác trong file `.env.`. Sao chép nội dung từ file `env.example` và tạo một file mới có tên là `.env` bằng câu lệnh sau:
    ```
    cp env.example .env
    ```

2. **Cài đặt các gói cần thiết**:
    Sử dụng lệnh sau để cài đặt các packet cần thiết từ file `requirements.txt`:
    ```
    pip install -r requirements.txt
    ```

# Hướng dẫn chạy chương trình RAG Vietnamese Legal

## Cài đặt

1. Clone repository từ GitHub:

    ```bash
    https://github.com/bachhoang0606/RAG_Vietnamese_Legal.git
    ```

2. Di chuyển vào thư mục của project:

    ```bash
    cd RAG_Vietnamese_Legal
    ```

3. Cài đặt các dependencies từ file requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

## Chạy chương trình

# Hướng Dẫn Chạy API Bằng Command Line

Để chạy API bằng dòng lệnh, bạn có thể sử dụng Uvicorn. Dưới đây là cách chạy API bằng Uvicorn:

1. Mở terminal hoặc command prompt.

2. Di chuyển đến thư mục gốc của dự án.

3. Chạy lệnh sau:

```bash
uvicorn server.main:app --reload
```

# Chạy giao diện streamlit

Chạy lệnh sau:

```bash
streamlit run client/app/main.py
```