import datetime
from typing import Optional
import os
import sys
from abc import abstractmethod, ABC
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
    PathUtils,
    BasePathUtils,
)

class BaseWebsiteScanner(ABC):

    @abstractmethod
    def export_content(self, url: str) -> str:
        """
    	An abstract method for exporting content, with a return type of string.
    	"""

    @abstractmethod
    def export_pdf(self, url: str, output_path: str = LOCAL_GENERATOR_PDF_FOLDER):
        """
        A description of the entire function, its parameters, and its return types.
        """

class WebsiteScanner(BaseWebsiteScanner):
    timeout: int

    def __init__(self, timeout: int = 3) -> None:
        self.timeout = timeout

    def _content_is_null(self, content: Optional[str]) -> bool:
        """
        Check if the content is null or empty.

        :param content: Optional[str] - the content to be checked
        :return: bool - True if the content is None or empty, False otherwise
        """
        return content is None or content.strip() == ''

    def _is_dynamic_web(self, url: str) -> bool:
        """
        Check if the given URL is a dynamic web page by making 
        a request and parsing the HTML content to look for specific tags. 
        Parameters:
            url (str): The URL of the web page to check.
        Returns:
            bool: True if the web page is dynamic, False otherwise.
        """
        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            have_noscript_tag = len(soup.find_all('noscript')) > 0
            have_root_tag = soup.find('div', id='root')
            is_root_tag_empty = have_root_tag is not None and \
                self._content_is_null(have_root_tag.text)

            return have_noscript_tag or is_root_tag_empty

        return False

    def _fetch_response_content(self, url: str) -> Optional[str]:
        """
        Fetches the content from the given URL and returns it as a string,
        or None if the request fails.
        
        Args:
            url (str): The URL to fetch the content from.
        
        Returns:
            Optional[str]: The content of the URL as a string,
                or None if the request fails.
        """
        if self._is_dynamic_web(url=url):
            session = HTMLSession()
            response = session.get(url=url, timeout=self.timeout)
            if response.status_code == 200:
                response.html.render()
                return response.html.html
            return None

        response = requests.get(url, timeout=self.timeout)
        if response.status_code == 200:
            return response.content.decode()
        return None

    def _file_name_generator(self) -> str:
        """
        A function to generate a file name based on the current time.

        :return: A string representing the generated file name.
        """
        # Get the current time
        current_time = datetime.datetime.now()

        # Format the current time into a string
        timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

        # Create a file name based on the current time
        file_name = f"output_{timestamp}.pdf"
        return file_name

    def export_content(self, url: str) -> str:
        """
        Export the content from the specified URL by fetching the response content,
        parsing the HTML syntax using BeautifulSoup, and extracting text elements.
        If there are no text elements, return an error message. Otherwise, format
        the text elements with inserted space characters and return the content of
        the page, excluding any options.
        
        Parameters:
            url (str): The URL of the content to be exported.
        
        Returns:
            str: The exported content from the specified URL.
        """

        response_content = self._fetch_response_content(url=url)

        # Check if there is any error
        if response_content:
            # Use BeautifulSoup to parse HTML syntax
            soup = BeautifulSoup(response_content, 'html.parser')

            # Extract text elements
            text_elements = soup.find_all(
                [
                    'p',
                    'h1',
                    'h2',
                    'h3',
                    'h4',
                    'h5',
                    'h6',
                    'li'
                ]
            )

            if len(text_elements) == 0:
                return "Lỗi khi tải trang web" 

            # Create a list to store text elements with inserted space characters
            formatted_text = []

            # Iterate through each text element and insert space characters between them
            for element in text_elements:
                formatted_text.append(element.get_text())
                formatted_text.append('\n\n')

            # Return the content of the page excluding the option ...
            return ''.join(formatted_text)

        return "Lỗi khi tải trang web"

    # Ingnore error
    def export_pdf(
            self,
            url: str,
            output_path: str = LOCAL_GENERATOR_PDF_FOLDER,
            path_utils: BasePathUtils = PathUtils()
        ):
        """
        A function to export a given URL to a PDF file.

        Args:
            url (str): The URL to be exported to PDF.
            output_path (str, optional): The path where the PDF file will be saved.
                Defaults to LOCAL_GENERATOR_PDF_FOLDER.
            path_utils (BasePathUtils, optional): The utility for handling file paths.
                Defaults to PathUtils().

        Returns:
            str: A message indicating the result of the PDF export process.
        """
        
        success_message = "PDF đã được tạo thành công!"
        load_error_message = "Lỗi khi tải trang web!"
        load_error_css_message = "Không thể tạo PDF vì CSS bị lỗi!"
        return_message = success_message
        try:
            file_name = self._file_name_generator()
            output_file_path = path_utils.create_file_path_in_current_directory(
                foler_name=output_path,
                file_name=file_name
            )
            if not self._is_dynamic_web(url=url):
                pdfkit.from_url(url, output_file_path)

                return return_message
            response_content = self._fetch_response_content(url=url)
            if response_content is None:
                return_message = load_error_message
                return return_message

            """
            1. You need to set options {"enable-local-file-access": ""}.
                pdfkit.from_string(
                    _html, pdf_path, options={"enable-local-file-access": ""
                })
            2. pdfkit.from_string() can't load css from URL.
                It's something like this.
                <link rel="stylesheet" href="https://path/to/style.css">
                css path should be absolute path or write style in same file.
            3. If css file load another file.
                ex: font file. It will be ContentNotFoundError.
            """
            # Thay thế tất cả các chuỗi query '?version=xxx' từ các tệp tĩnh
            # Replace all ?sadasd query strings from static file includes
            # response_content = re.sub(
            #   r'(\.css|\.js)\?[^"]+', r'\1', response_content
            # )
            pdfkit.from_string(
                input=response_content,
                output_path=output_file_path,
                options={"enable-local-file-access": ""}
            )
            
            return return_message
        except OSError:
            return_message = load_error_css_message
            return return_message

if __name__ == "__main__":
    # Sử dụng hàm để quét nội dung của một trang web
    URL = "https://policies.google.com/privacy?hl=vi"
    # URL = "https://fullstack.edu.vn/"
    # URL = "https://help.shopee.vn/portal/4/article/77244"
    web_scanner = WebsiteScanner()
    WEB_CONTENT_1 = web_scanner.export_pdf(url=URL)
    print(WEB_CONTENT_1)
    # WEB_CONTENT = web_scanner.export_content(url=URL)
    # print(WEB_CONTENT)
