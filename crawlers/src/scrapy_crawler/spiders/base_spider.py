from abc import abstractmethod
from typing import Any
from scrapy.spiders import Spider
from scrapy.http import Response

class BaseSpider(Spider):
    def parse_table(self, table: Response) -> str:
        """
        Parse the given table and return its content as a string.

        Args:
            table (Response): The table to be parsed.

        Returns:
            str: The content of the table as a string.
        """
        # Lặp qua từng bảng
        # Lấy danh sách các hàng <tr> trong bảng
        rows = table.xpath(".//tr")
        table_data = []
        # Lặp qua từng hàng trong bảng
        for row in rows:
            # Lấy danh sách các ô <td> hoặc <th> trong hàng
            cells = row.xpath(".//td|th")

            # Khởi tạo biến lưu trữ dữ liệu từ mỗi hàng
            row_data = []

            # Lặp qua từng ô trong hàng để lấy dữ liệu
            for cell in cells:
                # Trích xuất văn bản từ ô
                cell_text = cell.xpath("string(.)").get()
                # Thêm dữ liệu vào danh sách
                row_data.append(cell_text)
            # Xử lý dữ liệu từ mỗi hàng
            table_data.append("\t".join(row_data))

        output = "\n".join(table_data)

        return output

    def parse_to_string(self, element: Response) -> str:
        """
        Parses the given `element` to a string.

        Args:
            element (Response): The element to parse to a string.

        Returns:
            str: The parsed string.
        """
        if element.xpath("self::table"):
            return self.parse_table(element)

        return element.xpath("string(.)").get()

    @abstractmethod
    def parse(self, response: Response, **kwargs: Any) -> Any:
        pass
