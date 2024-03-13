from abc import abstractmethod, ABC
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    DirectoryLoader
)
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.vectorstores import VectorStore
from tqdm import tqdm
from langchain_mongodb import MongoDBAtlasVectorSearch
import pandas as pd
from pymongo.collection import Collection
from utils import (
    BasePathUtils,
    PathUtils
)
from embeddings import (
    EmbeddingModel
)
from mongodb_connector import vietnamese_legal_collection as collection
from configs import (
    VECTOR_SEARCH_INDEX_NAME,
    LOCAL_VECTOR_PATH,
    EMBEDDING_MODEL_PATH
)

class VectorDatabaseBuilder(ABC):

    embedding_model: EmbeddingModel
    path_util: BasePathUtils

    def __init__(
            self,
            embedding_model: EmbeddingModel,
            path_util: BasePathUtils
        ) -> None:
        super().__init__()
        self.embedding_model = embedding_model
        self.path_util = path_util

    # Generic documents split method
    def default_text_splitter(self) -> RecursiveCharacterTextSplitter:
        """
        A function that returns a RecursiveCharacterTextSplitter object for splitting text.
        """
        # Chia nho van ban
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
            length_function=len
        )

        return text_splitter

    @abstractmethod
    def get_vector_db(self) -> VectorStore:
        """
        Get the vector database.

        Returns:
            VectorStore: The vector database.
        """

    """
        Create vector data from raw text, file, csv
    """

    @abstractmethod
    def insert_db(self, documents: list[Document]):
        """
        Insert documents into the database.

        Args:
            documents (list[Document]): The documents to be inserted into the database.

        Returns:
            None
        """

    @abstractmethod
    def create_db_from_text(self, text: str, source: str):
        """
        Create a database from the given text and source.
        
        Args:
            text (str): The text to be used for creating the database.
            source (str): The source of the text.

        Returns:
            None
        """

    @abstractmethod
    def create_db_from_files(self, folder_path: str):
        """
        This function creates a database from files located in the specified folder_path.

        Parameters:
            folder_path (str): The path to the folder containing the files to be used for database creation.

        Returns:
            None
        """

    @abstractmethod
    def create_db_from_csvs(self, folder_path: str, file_name: str = ''):
        """
        This method creates a database from CSV files.

        Args:
            folder_path (str): The path to the folder containing the CSV files.
            file_name (str, optional): The name of the output database file. Defaults to ''.

        Returns:
            None
        """


class MongoDBAtlasVectorSearchBuilder(VectorDatabaseBuilder):

    collection: Collection
    vector_search_index_name: str

    def __init__(
            self,
            embedding_model: EmbeddingModel,
            collection: Collection,
            vector_search_index_name: str,
            path_util: BasePathUtils = PathUtils()
        ) -> None:
        super().__init__(
            embedding_model=embedding_model,
            path_util=path_util
        )
        self.collection = collection
        self.vector_search_index_name = vector_search_index_name
        self.path_util = path_util

    def get_vector_db(self) -> VectorStore:
        return MongoDBAtlasVectorSearch(
            collection=self.collection,
            embedding=self.embedding_model,
            index_name=self.vector_search_index_name
        )

    # Insert splited documents to mongodb serve
    def insert_db(self, documents: list[Document]):

        # split documents to small chunks
        text_splitter = self.default_text_splitter()
        chunks = text_splitter.split_documents(documents)

        # Dua vao Faiss Vector DB
        db = MongoDBAtlasVectorSearch.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            collection=self.collection,
            index_name=self.vector_search_index_name,
        )
        return db

    def create_db_from_text(self, text: str, source: str = "local"):
        # create Document from Str
        document = Document(page_content=text, metadata={"source": source})

        # Insert text to mongodb
        db = self.insert_db([document])
        return db

    def create_db_from_files(self, folder_path: str):
        # Khai bao loader de quet toan bo thu muc dataa
        loader = DirectoryLoader(folder_path, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()

        # Insert text to mongodb
        db = self.insert_db(documents)
        return db

    def create_db_from_csvs(self, folder_path: str, file_name: str = ''):
        csv_files = []
        path_util = self.path_util
        csv_files_in_folder = path_util.get_csv_files_in_directory(folder_path)

        if file_name == '':
            csv_files.extend(csv_files_in_folder)
        else:
            if file_name in csv_files_in_folder:
                csv_files.append(file_name)
        print(csv_files)

        for file_path in tqdm(csv_files, desc="Processing files"):
            file_sys_path = path_util.create_file_path_in_current_directory(
                folder_path,
                file_path
            )
            df = pd.read_csv(file_sys_path, encoding="UTF-8")
            for text in tqdm(df["text"], desc="Processing texts"):
                self.create_db_from_text(text=text, source=file_path)


class FAISSVectorSearchBuilder(VectorDatabaseBuilder):

    vector_database_path: str

    def __init__(
            self,
            embedding_model: EmbeddingModel,
            path_util: BasePathUtils = PathUtils(),
            vector_database_path: str = LOCAL_VECTOR_PATH,
        ) -> None:
        super().__init__(
            embedding_model=embedding_model,
            path_util=path_util
        )
        self.vector_database_path = vector_database_path

    def get_vector_db(self) -> VectorStore:
        db = FAISS.load_local(
            folder_path=self.vector_database_path,
            embeddings=self.embedding_model,
        )
        return db

    def insert_db(self, documents: list[Document]):
        text_splitter = self.default_text_splitter()
        chunks = text_splitter.split_documents(documents)

        db = FAISS.from_documents(
            documents=chunks,
            embedding=self.embedding_model
        )
        db.save_local(self.vector_database_path)
        return db

    def create_db_from_text(self, text: str, source: str):
        # create Document from Str
        document = Document(page_content=text, metadata={"source": source})

        # Insert text to mongodb
        db = self.insert_db([document])
        return db

    def create_db_from_files(self, folder_path: str):
        # Khai bao loader de quet toan bo thu muc dataa
        loader = DirectoryLoader(folder_path, glob="*.pdf", loader_cls = PyPDFLoader)
        documents = loader.load()

        # Insert text to mongodb
        db = self.insert_db(documents)
        return db

    def create_db_from_csvs(self, folder_path: str, file_name: str = ''):
        csv_files = []
        path_util = self.path_util
        csv_files_in_folder = path_util.get_csv_files_in_directory(folder_path)

        if file_name == '':
            csv_files.extend(csv_files_in_folder)
        else:
            if file_name in csv_files_in_folder:
                csv_files.append(file_name)
        print(csv_files)

        for file_path in tqdm(csv_files, desc="Processing files"):
            file_sys_path = path_util.create_file_path_in_current_directory(
                folder_path,
                file_path
            )
            df = pd.read_csv(file_sys_path, encoding="UTF-8")
            for text in tqdm(df["text"], desc="Processing texts"):
                self.create_db_from_text(text=text, source=file_path)

if __name__ == "__main__":
    embedding_model = EmbeddingModel(
        model_file=EMBEDDING_MODEL_PATH
    ).embedding_model
    VECTOR_BULDER = MongoDBAtlasVectorSearchBuilder(
        embedding_model=embedding_model,
        collection=collection,
        vector_search_index_name=VECTOR_SEARCH_INDEX_NAME,
    )
    # VECTOR_BULDER = FAISSVectorSearchBuilder(
    #     embedding_model=embedding_model,
    # )
    # VECTOR_BULDER.create_db_from_files(folder_path="data")
    VECTOR_DB = VECTOR_BULDER.get_vector_db()

    # TEXT = (
    #     "Nhằm đáp ứng nhu cầu và thị hiếu của khách hàng về việc sở hữu số tài khoản đẹp, dễ nhớ, giúp tiết kiệm "
    #     "thời gian, mang đến sự thuận lợi trong giao dịch. Ngân hàng Sài Gòn – Hà Nội (SHB) tiếp tục cho ra mắt "
    #     "tài khoản số đẹp 9 số và 12 số với nhiều ưu đãi hấp dẫn."
    #     "\nCụ thể, đối với tài khoản số đẹp 9 số, SHB miễn phí mở tài khoản số đẹp trị giá 880.000đ; giảm tới 80% "
    #     "phí mở tài khoản số đẹp trị giá từ 1,1 triệu đồng; phí mở tài khoản số đẹp siêu VIP chỉ còn 5,5 triệu đồng."
    #     "\nĐối với tài khoản số đẹp 12 số, SHB miễn 100% phí mở tài khoản số đẹp, khách hàng có thể lựa chọn tối đa toàn bộ dãy "
    #     "số của tài khoản. Đây là một trong những điểm ưu việt của tài khoản số đẹp SHB so với thị trường. Ngoài ra, khách hàng "
    #     "có thể lựa chọn số tài khoản trùng số điện thoại, ngày sinh, ngày đặc biệt, hoặc số phong thủy mang lại "
    #     "tài lộc cho khách hàng trong quá trình sử dụng."
    #     "\nHiện nay, SHB đang cung cấp đến khách hàng 3 loại tài khoản số đẹp: 9 số, 10 số và 12 số. Cùng với sự tiện lợi khi "
    #     "giao dịch online mọi lúc mọi nơi qua dịch vụ Ngân hàng số, hạn chế rủi ro khi sử dụng tiền mặt, khách hàng còn được "
    #     "miễn phí chuyển khoản qua mobile App SHB, miễn phí quản lý và số dư tối thiểu khi sử dụng tài khoản số đẹp của SHB."
    #     "\nNgoài kênh giao dịch tại quầy, khách hàng cũng dễ dàng mở tài khoản số đẹp trên ứng dụng SHB "
    #     "Mobile mà không cần hồ sơ thủ tục phức tạp."
    #     "\nHướng mục tiêu trở thành ngân hàng số 1 về hiệu quả tại Việt Nam, ngân hàng bán lẻ hiện đại nhất và là ngân hàng "
    #     "số được yêu thích nhất tại Việt Nam, SHB sẽ tiếp tục nghiên cứu và cho ra mắt nhiều sản phẩm dịch vụ số ưu việt "
    #     "cùng chương trình ưu đãi hấp dẫn, mang đến cho khách hàng lợi ích và trải nghiệm tuyệt vời nhất. "
    #     "\nĐể biết thêm thông tin về chương trình, Quý khách vui lòng liên hệ các điểm giao "
    #     "dịch của SHB trên toàn quốc hoặc Hotline *6688"
    # )
    # # vecto_db.create_db_from_csvs(folder_path="data")
    # # create_db_from_files(folder_path="data")
    # VECTOR_BULDER.create_db_from_text(
    #     text=TEXT,
    #     source="local_bach_test_1"
    # )
    output = VECTOR_DB.similarity_search_with_score(
        query="Quy định về cơ sở vật chất đối với môn đấu kiếm thể thao?",
        k=3,
        post_filter_pipeline=  [
            {
                "$project": {
                    "_id": 0,
                    "text": 1,
                    "score": { "$meta": "vectorSearchScore" }
                }
            }
        ]
    )

    print(output)
