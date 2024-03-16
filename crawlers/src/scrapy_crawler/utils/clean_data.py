def clean_data(data_list: list) -> list:
    """
    Hàm này nhận vào một danh sách các chuỗi dữ liệu và thực hiện các bước làm sạch.
    :param data_list: Danh sách các chuỗi dữ liệu thu thập từ các nền tảng
    :return: Danh sách sau khi đã làm sạch
    """
    cleaned_data = []
    for item in data_list:
        cleaned_item = item
        # # Loại bỏ các ký tự đặc biệt không cần thiết
        # cleaned_item = ''.join(c for c in cleaned_data if c.isalnum() or c.isspace())

        # Chuyển đổi chuỗi thành chữ thường (lowercase)
        cleaned_item = cleaned_item.lower()

        # Loại bỏ khoảng trắng thừa ở đầu và cuối chuỗi
        cleaned_item = cleaned_item.strip()

        # Kiểm tra xem chuỗi có rỗng không
        if cleaned_item:
            cleaned_data.append(cleaned_item)

    return cleaned_data
