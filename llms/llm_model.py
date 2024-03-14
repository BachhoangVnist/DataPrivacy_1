from typing import Optional
from langchain_community.llms.ctransformers import CTransformers
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
import torch
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)
from configs import (
    HF_TOKEN
)
class LLMModel:
    __model_name: str
    __llm_model: Optional[CTransformers]
    __max_new_tokens: int

    def __init__(
            self,
            model_name: str,
            max_new_tokens: int = 1024,
            is_remote_model: bool = False,
        ) -> None:
        self.__model_name = model_name
        self.__max_new_tokens = max_new_tokens
        self.__llm_model = (
            self.__load_hub_model() if is_remote_model else
            self.__load_llm()
        )

    def get_llm_model(self) -> Optional[CTransformers]:
        return self.__llm_model

    def get_model_name(self) -> str:
        return self.__model_name

    def get_max_new_tokens(self) -> int:
        return self.__max_new_tokens

    # Load LLM
    def __load_llm(
            self,
            max_new_tokens: int = None
        ) -> Optional[CTransformers]:
        """
        Load the large language model with the specified maximum number of new tokens. 
        
        Args:
            max_new_tokens (int, optional): The maximum number of new tokens. Defaults to None.
        
        Returns:
            Optional[CTransformers]: The loaded large language model.
        """
        if max_new_tokens is None:
            max_new_tokens = self.__max_new_tokens

        config = {
            "context_length" : 4096,
            "max_new_tokens" : max_new_tokens,
            "temperature" : 0.01
        }

        llm = CTransformers(
            model=self.__model_name,
            model_type="llama",
            config=config
        )
        return llm

    def __load_hub_model(
        self,
        max_new_tokens: int = None
    ):
        """
        Loads a Hugging Face model for text generation and returns a HuggingFacePipeline
        object for interacting with the model. If max_new_tokens is not provided, it
        defaults to the value of self.__max_new_tokens. The function uses a pre-trained
        model and tokenizer from Hugging Face, and sets up a text generation pipeline
        for generating text based on the loaded model. The pipeline is then wrapped
        in a HuggingFacePipeline object and returned.

        Parameters:
        - max_new_tokens (int, optional): The maximum number of new tokens to use.
            Defaults to None.

        Returns:
        - HuggingFacePipeline: A pipeline object for text generation.
        """
        if max_new_tokens is None:
            max_new_tokens = self.__max_new_tokens

        # DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

        model = AutoModelForCausalLM.from_pretrained(
            self.__model_name,
            use_safetensors=True,
            quantization_config=bnb_config,
            trust_remote_code=True,
            device_map="auto",
            token=HF_TOKEN,
        )

        tokenizer = AutoTokenizer.from_pretrained(
            self.__model_name,
            token=HF_TOKEN,
        )

        text_generation_pipeline = pipeline(
            "text-generation",  # LLM task
            model=model,
            tokenizer=tokenizer,
            torch_dtype=torch.float16,
            device_map="auto",
            max_length=2048
        )

        llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

        return llm
