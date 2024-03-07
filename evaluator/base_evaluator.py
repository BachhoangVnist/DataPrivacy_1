from abc import ABC, abstractmethod

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate_csv(self, input_path: str = None, output_file: str = None) -> None:
        pass

    @abstractmethod
    def evaluate_json(self, input_path: str, output_file: str) -> None:
        pass
