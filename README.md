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

3. **Tải wkhtmltopdf**: 
    Chương trình sử dụng `wkhtmltopdf` để tạo file PDF từ HTML. Bạn cần tải `wkhtmltopdf` và cài đặt nó trên hệ thống của mình. Bạn có thể tải phiên bản phù hợp cho hệ điều hành của mình từ trang chính thức của `wkhtmltopdf`. Bạn cần tải và cài đặt `wkhtmltopdf` từ trang chủ của nó. Hoặc bạn có thể cài đặt `wkhtmltopdf` bằng câu lệnh:
    ```
    sudo apt-get update
    sudo apt-get install wkhtmltopdf
    ```

4. **Tải mô hình ngôn ngữ Gguf**: Tải mô hình ngôn ngữ lớn Gguf và lưu vào thư mục `models`. Mô hình ngôn ngữ Gguf là một mô hình ngôn ngữ được huấn luyện đặc biệt để hiểu và trả lời các câu hỏi pháp lý.

Sau khi hoàn thành các bước trên, bạn đã sẵn sàng để chạy project.

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
4. Để thêm quyền thực thi cho tất cả các file `.sh`, bạn sử dụng lệnh sau:

    ```bash
    chmod +x *.sh
    ```

## Chạy chương trình

### Hỏi đáp pháp luật

Chạy file hỏi đáp pháp luật bằng lệnh sau:

```bash
./run_question_answer.sh
```

### Dự đoán văn bản chính sách bảo mật

Chạy file dự đoán văn bản chính sách bảo mật bằng lệnh sau:

```bash
./run_inference_policy.sh
```
