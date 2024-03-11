import os
from abc import abstractmethod, ABC

class BasePathUtils(ABC):

    @staticmethod
    @abstractmethod
    def get_csv_files_in_directory(folder_path: str) -> list[str]:
        pass

    @staticmethod
    @abstractmethod
    def create_file_path_in_current_directory(foler_name: str, file_name: str) -> str:
        pass

class PathUtils(BasePathUtils):

    @staticmethod
    def get_csv_files_in_directory(folder_path: str) -> list[str]:
        """
        Returns a list of CSV files in the specified directory.

        Args:
            folder_path (str): The path to the directory to search for CSV files.

        Returns:
            list[str]: A list of file paths to the CSV files found in the directory.
        """
        csv_files = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                csv_files.append(filename)
        return csv_files

    @staticmethod
    def create_file_path_in_current_directory(foler_name: str, file_name: str) -> str:
        """
        Create a file path in the current directory using the provided folder name and file name.
        
        Args:
            folder_name (str): The name of the folder in which the file will be created.
            file_name (str): The name of the file to be created.
        
        Returns:
            str: The file path in the current working directory.
        """
        # Use the current_directory variable to create the path to the file in the current working directory
        current_directory = os.getcwd()

        # Create file_path by joining the current_directory and file_name
        folder_path = os.path.join(current_directory, foler_name)
        # If folder name not exit create folder
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, file_name)
        return file_path

if __name__ == "__main__":
    path_util = PathUtils()
    paths = path_util.get_csv_files_in_directory("data")
    print(paths)
