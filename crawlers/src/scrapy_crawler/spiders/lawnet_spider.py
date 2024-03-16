from typing import Any
from scrapy.http import Response
from scrapy import Request
from scrapy_crawler.utils import clean_data
from scrapy_crawler.configs import PRIVACY_KEYWORKS
from scrapy_crawler.items import QACrawlerItem

from .base_spider import BaseSpider

class LawnetCrawlerSpider(BaseSpider):

    privacy_keyworks = PRIVACY_KEYWORKS

    name = "lawnet_crawler"
    allowed_domains = ["lawnet.vn"]
    start_urls = [
        (
            "https://lawnet.vn/laws/search-advice?searchType=1&"
            f"&q={keywork}&searchField=0"
        ) for keywork in privacy_keyworks
    ]

    # + [
    #     "https://lawnet.vn/laws/search-advice?searchType=1"
    # ]

    def parse_page(self, response):
        # Chọn tất cả các phần tử <h2> trong phần tử <section class="news-content">
        questions = response.xpath("//section[@class='news-content']/h2")
        for index, question in enumerate(questions):
            # Lấy văn bản của câu hỏi (nội dung trong thẻ <h2>)
            question_text = question.xpath("string(.)").extract_first()

            # Lấy tất cả các phần tử <p> sau câu hỏi những thẻ <p> này cũng thỏa mãn
            # điều kiện là số lượng thẻ <h2> trước thẻ <p> này chỉ có {index+1}
            # Ví dụ lấy các thẻ <p> nằm ở giữa thẻ <h2> đầu tiên và thẻ <h2> thứ 2
            answer_elements = question.xpath(
                "following-sibling::*[self::p or self::table or self::blockquote]"
                f"[count(preceding-sibling::h2) = {index+1}][not(self::p//em)]"
            )

            # Nếu không có phần tử <p> sau câu hỏi, điều này có thể là câu hỏi cuối cùng
            # hoặc không có câu trả lời
            if not answer_elements:
                continue

            # Khởi tạo biến lưu trữ nội dung của câu trả lời
            answer_text = ""

            # Lặp qua tất cả các phần tử <p> sau câu hỏi để lấy nội dung của câu trả lời
            for answer_element in answer_elements:
                answer_text += self.parse_to_string(answer_element) + "\n"

            # Xử lý nội dung câu trả lời (xóa khoảng trắng thừa, ký tự đặc biệt, ...)
            # pylint: disable=unbalanced-tuple-unpacking
            question_text, answer_text = clean_data(
                [
                    question_text,
                    answer_text
                ]
            )

            # In câu hỏi và câu trả lời tương ứng
            yield QACrawlerItem(
                question=question_text,
                answer=answer_text,
                original_url=response.url
            )

    def parse(self, response: Response, **kwargs: Any) -> Any:
        # Trích xuất dữ liệu từ trang hiện tại
        # Code trích xuất dữ liệu từ HTML ở đây

        # Lấy danh sách các đường dẫn .html từ trang hiện tại
        page_links = response.css("a[href$='.html']::attr(href)").getall()

        # Tạo URL đầy đủ từ danh sách đường dẫn .html
        for page_link in page_links:
            full_url = response.urljoin(page_link)
            # Gửi yêu cầu đến trang đầy đủ và chuyển hàm parse_page làm hàm xử lý
            yield Request(full_url, callback=self.parse_page)

        # Xác định URL của trang tiếp theo
        next_page_url = response.css(
            "ul.pagination li.page-item.active + li.page-item a.page-link::attr(href)"
        ).get()
        if next_page_url:
            # Tạo yêu cầu đến trang tiếp theo
            yield Request(response.urljoin(next_page_url), callback=self.parse)
