import datetime
from typing import Optional
import os
import sys
import pdfkit
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=wrong-import-position
from configs import (
    LOCAL_GENERATOR_PDF_FOLDER
)
from utils import (
    create_file_path_in_current_directory
)

class WebsiteScanner:
    url: str
    timeout: int

    def __init__(self, url: str, timeout: int = 3) -> None:
        self.url = url
        self.timeout = timeout

    def _content_is_null(self, content: Optional[str]) -> bool:
        return content is None or content.strip() == ''

    def _is_dynamic_web(self) -> bool:
        response = requests.get(self.url, timeout=self.timeout)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            have_noscript_tag = len(soup.find_all('noscript')) > 0
            have_root_tag = soup.find('div', id='root')
            is_root_tag_empty = have_root_tag is not None and \
                self._content_is_null(have_root_tag.text)

            return have_noscript_tag or is_root_tag_empty

        return False

    def _fetch_response_content(self) -> Optional[str]:
        if self._is_dynamic_web():
            session = HTMLSession()
            response = session.get(self.url, timeout=self.timeout)
            if response.status_code == 200:
                response.html.render()
                return response.html.html
            return None

        response = requests.get(self.url, timeout=self.timeout)
        if response.status_code == 200:
            return response.content.decode()
        return None

    def _file_name_generator(self) -> str:
        # Get the current time
        current_time = datetime.datetime.now()

        # Format the current time into a string
        timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

        # Create a file name based on the current time
        file_name = f"output_{timestamp}.pdf"
        return file_name

    def export_content(self) -> str:

        response_content = self._fetch_response_content()

        # Check if there is any error
        if response_content:
            # Use BeautifulSoup to parse HTML syntax
            soup = BeautifulSoup(response_content, 'html.parser')

            # Extract text elements
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])

            # Create a list to store text elements with inserted space characters
            formatted_text = []

            # Iterate through each text element and insert space characters between them
            for element in text_elements:
                formatted_text.append(element.get_text())
                formatted_text.append('\n\n')  # Insert newline character between elements

            # Return the content of the page excluding the option ...
            return ''.join(formatted_text)

        return "Lỗi khi tải trang web"

    # Ingnore error
    def export_pdf(self, output_path: str = LOCAL_GENERATOR_PDF_FOLDER):
        try:
            file_name = self._file_name_generator()
            output_file_path = create_file_path_in_current_directory(
                foler_name=output_path,
                file_name=file_name
            )
            if not self._is_dynamic_web():
                pdfkit.from_url(self.url, output_file_path)

                return "PDF đã được tạo thành công!"

            response_content = self._fetch_response_content()
            if response_content:
                """
                1. You need to set options {"enable-local-file-access": ""}.
                    pdfkit.from_string(_html, pdf_path, options={"enable-local-file-access": ""})
                2. pdfkit.from_string() can't load css from URL. It's something like this. 
                    <link rel="stylesheet" href="https://path/to/style.css"> css path should be absolute 
                    path or write style in same file.
                3. If css file load another file. ex: font file. It will be ContentNotFoundError.
                """
                # Thay thế tất cả các chuỗi query '?version=xxx' từ các tệp tĩnh
                # Replace all ?sadasd query strings from static file includes
                # response_content = re.sub(r'(\.css|\.js)\?[^"]+', r'\1', response_content)
                pdfkit.from_string(
                    input=response_content,
                    output_path=output_file_path,
                    options={"enable-local-file-access": ""}
                )

                return "PDF đã được tạo thành công!"

            return "Lỗi khi tải trang web"
        except OSError:

            return "Lỗi khi load css local url"

if __name__ == "__main__":
    # Sử dụng hàm để quét nội dung của một trang web
    # URL = "https://policies.google.com/privacy?hl=vi"
    URL = "https://fullstack.edu.vn/"
    web_scanner = WebsiteScanner(url=URL)
    WEB_CONTENT = web_scanner.export_pdf()
    print(WEB_CONTENT)
