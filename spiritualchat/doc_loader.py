from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.csv_loader import CSVLoader

def document_loader(file_path, encoding="utf-8", csv_args={'delimiter': ','}):
    """
    Args:
        file_path (str): Path to CSV file.
        encoding (str): Encoding of CSV file (default: utf-8).
        csv_args (dict): Arguments to be passed to csv.reader (default: {'delimiter': ','}).

    Returns:
        - documents (list of str): Each document is a row from the CSV file.
    """
    loader = CSVLoader(file_path=file_path, encoding=encoding, csv_args=csv_args)
    documents = loader.load()
    return documents
