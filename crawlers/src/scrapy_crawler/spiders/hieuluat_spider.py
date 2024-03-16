from typing import Any
from scrapy.http import Response
from scrapy import Request
from scrapy_crawler.utils import clean_data
from scrapy_crawler.configs import PRIVACY_KEYWORKS
from scrapy_crawler.items import QACrawlerItem

from .base_spider import BaseSpider

class HieuLuatCrawlerSpider(BaseSpider):

    privacy_keyworks = PRIVACY_KEYWORKS

    name = "hieuluat_crawler"
    allowed_domains = ["hieuluat.vn"]
    start_urls = [
        (
            "https://hieuluat.vn/tim-tin-tuc.html?CategoryId=559"
            f"&OrderBy=&pSize=10&keywords={keywork}"
        ) for keywork in privacy_keyworks
    ]

    def get_answers(self, question: list, is_multi_page: bool, question_index: int) -> str|bool:
        xpath_string = (
            "following-sibling::div[@id='article-content']/"
            "*[self::p or self::table or self::blockquote]"
            "[not(self::p//em)]"
            "[not(self::p//a[contains(@href, 'tel:')])]"
            "[not(self::p//span/strong[@class='user-profiles'])]"
        )
        if is_multi_page:
            # Lấy tất cả các phần tử <p> sau câu hỏi những thẻ <p> này cũng thỏa mãn
            # điều kiện là số lượng thẻ <h2> trước thẻ <p> này chỉ có {index+1}
            # Ví dụ lấy các thẻ <p> nằm ở giữa thẻ <h2> đầu tiên và thẻ <h2> thứ 2
            answer_elements = question.xpath(
                "following-sibling::*[self::p or self::table or self::blockquote]"
                f"[count(preceding-sibling::h2) = {question_index+1}][not(self::p//em)]"
                "[not(self::p//a[contains(@href, 'tel:')])]"
            )
            xpath_string = (
             "following-sibling::*[self::p or self::table or self::blockquote]"
            f"[count(preceding-sibling::h2) = {question_index+1}][not(self::p//em)]"
            "[not(self::p//a[contains(@href, 'tel:')])]"
        )

        answer_elements = question.xpath(xpath_string)

        # Nếu không có phần tử <p> sau câu hỏi, điều này có thể là câu hỏi cuối cùng
        # hoặc không có câu trả lời
        if not answer_elements:
            return False

        # Khởi tạo biến lưu trữ nội dung của câu trả lời
        answer_text = ""

        # Lặp qua tất cả các phần tử <p> sau câu hỏi để lấy nội dung của câu trả lời
        for answer_element in answer_elements:
            answer_text += self.parse_to_string(answer_element) + "\n"

        return answer_text

    def parse_page(self, response: Response):
        # Chọn tất cả các phần tử <h2> trong phần tử <section class="news-content">
        questions = response.xpath("//div[@id='article-content']/h2[@dir='ltr']")

        # Kiển tra page có nhiều câu hỏi và trả lời hay không
        is_multi_page = len(questions) > 0
        if not is_multi_page:
            questions = response.xpath("//div[@id='article-content']/preceding::h1")
        for index, question in enumerate(questions):
            # Lấy văn bản của câu hỏi (nội dung trong thẻ <h2>)
            question_text = question.xpath("string(.)").extract_first()
            answer_text = self.get_answers(questions, is_multi_page, index)

            if answer_text is False:
                continue

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
        # Lấy danh sách các đường dẫn .html từ trang hiện tại
        page_links = response.css("div.post-thumbnail a[href$='.html']::attr(href)").getall()

        # Tạo URL đầy đủ từ danh sách đường dẫn .html
        for page_link in page_links:
            full_url = response.urljoin(page_link)
            # Gửi yêu cầu đến trang đầy đủ và chuyển hàm parse_page làm hàm xử lý
            yield Request(full_url, callback=self.parse_page)

        # Xác định URL của trang tiếp theo
        next_page_number = response.css(
            "div.pagination form div.pagination-right span.pagination-pages1.active + a.pagination-pages1::text"
        ).get()
        if next_page_number:
            url = response.url
            page_index = url.find("page=")
            print("currnet url", response.url)
            print("next_page_number", next_page_number)
            # print(response.urljoin(form_page_url + f"page={next_page_number}"))
            if page_index != -1:
                # Trích xuất số trang từ sau chuỗi "page="
                url = url[:page_index + len("page=")] + str(next_page_number)
            else:
                # Nếu không tìm thấy chuỗi "page=", thêm chuỗi "page=" vào URL
                url = url + f"&page={next_page_number}"
            # Tạo yêu cầu đến trang tiếp theo
            yield Request(url, callback=self.parse)
