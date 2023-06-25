from spiritualchat.prepare_embeddings import prepare_embeddings

def test_prepare_embeddings():
    filepath = 'experiences_sample.csv'
    assert not prepare_embeddings(filepath, 'experiences')
