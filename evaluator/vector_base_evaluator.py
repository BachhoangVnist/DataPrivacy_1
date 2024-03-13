import sys
import os
import pandas as pd
from sentence_transformers import util

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=wrong-import-position
from embeddings import EmbeddingModel
from configs import (
    DEFAULT_EVALUATOR_OUTPUT_PATH,
    DEFAULT_EVALUATOR_INPUT_PATH
)

from .base_evaluator import BaseEvaluator

class VectorBaseEvaluator(BaseEvaluator):
    __embedding_model: EmbeddingModel

    def __init__(self, embedding_model: EmbeddingModel) -> None:
        super().__init__()
        self.__embedding_model = embedding_model

    def set_embedding_model(self, embedding_model: EmbeddingModel) -> None:
        self.__embedding_model = embedding_model

    def get_embedding_model(self) -> EmbeddingModel:
        return self.__embedding_model

    def __caculate_sentence_similarity(self, query_1: str, query_2: str) -> float:
        """
        Calculate the similarity between two input sentences using the embedding model.

        Args:
            query_1 (str): The first input sentence.
            query_2 (str): The second input sentence.

        Returns:
            float: The similarity score between the two input sentences.
        """
        embedding_model = self.__embedding_model.embedding_model
        vector_1 = embedding_model.embed_query(query_1)
        vector_2 = embedding_model.embed_query(query_2)
        ouput = util.pytorch_cos_sim(vector_1, vector_2)[0][0].item()
        return ouput

    def evaluate_csv(self, input_path: str = None, output_file: str = None) -> None:
        """
        Evaluate a CSV file and calculate the similarity score for each row, then save the results to a new CSV file.

        :param input_path: The path to the input CSV file. If not provided, a default path is used.
        :param output_file: The path to the output CSV file. If not provided, a default path is used.
        :return: None
        """
        if input_path is None:
            input_path = DEFAULT_EVALUATOR_INPUT_PATH
        if output_file is None:
            output_file = DEFAULT_EVALUATOR_OUTPUT_PATH
        df = pd.read_csv(input_path)
        df["similarity_score"] = df.apply(
            lambda row:
                self.__caculate_sentence_similarity(
                    row["answer_raw"],
                    row["answer_generate"]
                ),
                axis=1
        )
        df.to_csv(output_file)
        print(df)

    def evaluate_json(self, input_path: str, output_file: str) -> None:
        pass
