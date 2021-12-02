import h5py
from common.src.tokenization import *

# get vocab dictionary
vocab_path = "./common/models/345K/vocab.txt"
vocab = load_vocab(vocab_path)

# get text data file
file_path = './Crawling/textcrawler/use_data/data.txt'
with open(file_path, 'r') as f:
    data = f.read()

# Tokenizing
tokenizer = FullTokenizer(vocab_file=vocab_path, do_lower_case=False)
print("Tokenizing all data...")
tokens = tokenizer.tokenize(data)
data_token_ids = tokenizer.convert_tokens_to_ids(tokens)
print("Done.")

# save as hdf5 file
save_path = './common/data/crawled_data_5.hdf5'
f = h5py.File(save_path, 'w')
g = f.create_group("data")
g.create_dataset("crawled_geulteen", data=data_token_ids)
f.close()
