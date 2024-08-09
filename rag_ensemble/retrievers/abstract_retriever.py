from abc import ABC, abstractmethod

class Retriever(ABC):
    @abstractmethod
    def add_document(self, vectors, metadata=None):
        """
        Add vectors to the store.
        
        Args:
            vectors (list or np.ndarray): A list or array of vectors to add.
            metadata (list, optional): A list of metadata corresponding to the vectors.
        
        Returns:
            None
        """
        pass

    @abstractmethod
    def remove_document(self, vectors, metadata=None):
        """
        Add vectors to the store.
        
        Args:
            vectors (list or np.ndarray): A list or array of vectors to add.
            metadata (list, optional): A list of metadata corresponding to the vectors.
        
        Returns:
            None
        """
        pass

    @abstractmethod
    def search_vectors(self, query_vector, k=5):
        """
        Search for the top-k most similar vectors to the query_vector.
        
        Args:
            query_vector (np.ndarray): The vector to search for.
            k (int): The number of top similar vectors to return.
        
        Returns:
            list: A list of the top-k similar vectors and their metadata.
        """
        pass

    @abstractmethod
    def save(self, file_path):
        """
        Save the vector store to a file.
        
        Args:
            file_path (str): The path to save the vector store.
        
        Returns:
            None
        """
        pass

    @abstractmethod
    def load(self, file_path):
        """
        Load the vector store from a file.
        
        Args:
            file_path (str): The path to load the vector store from.
        
        Returns:
            None
        """
        pass

