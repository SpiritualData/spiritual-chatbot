from spiritualchat.prepare_embeddings import prepare_embeddings

def test_prepare_embeddings():
    filepath = 'experiences_sample.csv'
    num_embeddings = prepare_embeddings(filepath, 'experiences')
    assert num_embeddings == 3
