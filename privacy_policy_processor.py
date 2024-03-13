from scanner import (
    WebsiteScanner,
    BaseWebsiteScanner
)
from prepare_vector_db import (
    FAISSVectorSearchBuilder,
    VectorDatabaseBuilder
)
from embeddings import (
    EmbeddingModel
)
from configs import (
    EMBEDDING_MODEL_PATH,
    COOKIE_QUESTION_TEMPLATE,
    DEFAULT_COOKIE_POLICY_QUERY,
)

class PrivacyPolicyProcessor:

    policy_url: str
    website_scannner: BaseWebsiteScanner
    vector_builder: VectorDatabaseBuilder
    question_template: str
    cookie_policy_query: str
    k: int

    def __init__(
            self,
            policy_url: str,
            vector_builder: VectorDatabaseBuilder,
            website_cannner: BaseWebsiteScanner = WebsiteScanner(),
            question_template: str = COOKIE_QUESTION_TEMPLATE,
            cookie_policy_query: str = DEFAULT_COOKIE_POLICY_QUERY,
            k: int = 5,
        ) -> None:
        self.policy_url = policy_url
        self.website_scannner = website_cannner
        self.vector_builder = vector_builder
        self.question_template = question_template
        self.cookie_policy_query = cookie_policy_query
        self.k = k
        self.__save_policy_content()

    def __save_policy_content(self):
        """
        Saves the policy content by exporting content from the website scanner 
        using the policy URL and creating a database from the text using
        the vector builder.
        """
        content = self.website_scannner.export_content(url=self.policy_url)
        self.vector_builder.create_db_from_text(text=content, source=self.policy_url)

    def get_policy_document(self, query: str, k: int = None):

        if k is None:
            k = self.k

        vector_store = self.vector_builder.get_vector_db()
        policy_document = vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

        return policy_document

    def get_policy_content(self, query: str, k: int = None) -> list[str]:

        if k is None:
            k = self.k

        vector_store = self.vector_builder.get_vector_db()
        policy_document = vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

        simularity_text_list= []
        for doc in policy_document:
            simularity_text_list.append(doc[0].page_content)

        return simularity_text_list

    def process(
            self,
            question_template: str = None,
            cookie_policy_query: str = None,
            k: int = None
        ) -> str:
        if question_template is None:
            question_template = self.question_template

        if cookie_policy_query is None:
            cookie_policy_query = self.cookie_policy_query

        if k is None:
            k = self.k

        self.__save_policy_content()
        policy_document = self.get_policy_document(
            query=cookie_policy_query,
            k=k,
        )
        simularity_text = []
        for doc in policy_document:
            simularity_text.append(doc[0].page_content)

        # print(question_template)
        policy_text = "\n\n".join(simularity_text)
        question = question_template.format(content=policy_text)
        return question


if __name__ == "__main__":
    embedding_model = EmbeddingModel(model_file=EMBEDDING_MODEL_PATH).embedding_model
    VECTOR_BULDER = FAISSVectorSearchBuilder(
        embedding_model=embedding_model,
    )

    URL = "https://policies.google.com/privacy?hl=vi"
    privacy_policy_processor = PrivacyPolicyProcessor(
        policy_url=URL,
        vector_builder=VECTOR_BULDER,
        k=10
    )

    QUESTION = privacy_policy_processor.process()
    print(QUESTION)
