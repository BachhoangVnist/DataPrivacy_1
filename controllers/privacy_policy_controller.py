# PolicyController.py
from pymongo.collection import Collection
from bson.objectid import ObjectId
from .base_controller import BaseController

class PrivacyPolicyController(BaseController):

    collection: Collection

    def __init__(
            self,
            collection: Collection
        ) -> None:
        """
        Initializes the class with the given collection.

        Args:
            collection (Collection): The collection to be assigned to the class.

        Returns:
            None
        """
        self.collection = collection

    def create_document(self, data) -> str:
        """
        Create a document in the collection using the provided data.

        Args:
            data: The data to be inserted into the collection.

        Returns:
            str: The inserted ID of the document.
        """
        result = self.collection.insert_one(data)
        return result.inserted_id
    
    def create_documents(self, data_list: list) -> list:
        """
        Create documents using the provided data list and return a list of inserted document IDs.
        
        Args:
            data_list (list): The list of data to be inserted as documents.
            
        Returns:
            list: A list of inserted document IDs.
        """
        result = self.collection.insert_many(data_list)
        return result.inserted_ids

    def read_document(self, query):
        return self.collection.find_one(query)

    def read_document_by_name(self, name: str):
        """
        Reads a document from the collection based on the provided platform name.

        Args:
            name (str): The name of the platform.

        Returns:
            dict: The document found in the collection based on the platform name.
        """
        query = {"platform_name": name}
        return self.collection.find_one(query)

    def read_all_documents(self):
        """
        Read all documents from the collection.
        """
        return self.collection.find()

    def read_documents(self, query):
        return list(self.collection.find(query))

    def update_document(self, query, data):
        result = self.collection.update_one(query, {'$set': data})
        return result.modified_count

    def delete_document(self, query):
        result = self.collection.delete_one(query)
        return result.deleted_count

    def read_document_by_id(self, document_id: str):
        """
        Reads a document from the database by its ID.

        Args:
            document_id (str): The ID of the document to be read.

        Returns:
            The document retrieved from the database.
        """
        query = {'_id': ObjectId(document_id)}
        return self.read_document(query)

    def update_document_by_id(self, document_id: str, data):
        """
        Update a document by its ID.

        Args:
            document_id (str): The ID of the document to be updated.
            data: The data with which to update the document.

        Returns:
            The result of the update operation.
        """
        query = {'_id': ObjectId(document_id)}
        return self.update_document(query, data)

    def delete_document_by_id(self, document_id: str):
        """
        Delete a document by its ID.

        Args:
            document_id (str): The ID of the document to be deleted.

        Returns:
            The result of deleting the document.
        """
        query = {'_id': ObjectId(document_id)}
        return self.delete_document(query)

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # pylint: disable=wrong-import-position
    from mongodb_connector import (
        privacy_policy_collection
    )
    privacy_controller = PrivacyPolicyController(
        collection=privacy_policy_collection
    )

    # new_records = [
    #     {
    #         "platform_name": "Shopee",
    #         "home_path": "https://shopee.vn/",
    #         "policy_path": "https://help.shopee.vn/portal/4/article/77244"
    #     },
    #     {
    #         "platform_name": "Lazada",
    #         "home_path": "https://www.lazada.vn/",
    #         "policy_path": "https://pages.lazada.vn/wow/i/vn/corp/privacy?hybrid=1"
    #     },
    #     {
    #         "platform_name": "tiktok",
    #         "home_path": "https://www.tiktok.com/",
    #         "policy_path": "https://www.tiktok.com/legal/page/row/privacy-policy/vi"
    #     }
    # ]

    # privacy_controller.create_documents(
    #     data_list=new_records
    # )

    # documents = privacy_controller.read_all_documents()
    # for doc in documents:
    #     print(doc)

