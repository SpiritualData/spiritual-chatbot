import json
import pandas as pd

def prepare_arxiv(filepath, output_csv='arxiv_embedding_data.csv', chunk_size=1000, categories_filepath='prioritized_arxiv_categories.txt'):
    """
    Prepare arXiv data for embedding.

    Args:
        - filepath (str): Filepath containing arXiv data in JSON lines format.
        - output_csv (str): Filepath for output CSV file (default: 'arxiv_embedding_data.csv').
        - chunk_size (int): Number of lines to read into memory at one time (default: 1000).
        - categories_filepath (str): Filepath containing prioritized arXiv categories (default: 'prioritized_arxiv_categories.txt').
    """
    # Initialize DataFrame with desired columns
    df = pd.DataFrame(columns=['Name', 'Description', 'URL'])
    
    # Open output CSV file for writing
    with open(output_csv, 'w', newline='') as csvfile:
        # Write header to CSV
        df.to_csv(csvfile, header=True, index=False)
    
    # Read and process JSON lines from the file
    chunk = []
    total = 0
    with open(filepath, 'r') as f:
        for line in f:
            article = json.loads(line)
            
            # Get the title, abstract, and id for generating the URL
            title = article.get('title', '')
            abstract = article.get('abstract', '')
            arxiv_id = article.get('id', '')
            
            # Create URL based on arXiv ID
            url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""
            
            # Create a dictionary and append to chunk list
            chunk.append({
                'Name': title,
                'Description': abstract,
                'URL': url
            })
            
            # If chunk size reached, append to CSV and clear chunk
            if len(chunk) >= chunk_size:
                df = pd.DataFrame(chunk)
                total += len(df)
                with open(output_csv, 'a', newline='') as csvfile:
                    df.to_csv(csvfile, header=False, index=False)
                chunk.clear()
            print(f'total: {total}')
        # Write any remaining records to CSV
        if chunk:
            df = pd.DataFrame(chunk)
            with open(output_csv, 'a', newline='') as csvfile:
                df.to_csv(csvfile, header=False, index=False)
        print(f'total: {total}')

from fire import Fire
Fire(prepare_arxiv)