import numpy as np

from transformers import BertTokenizer
import onnxruntime as ort

from rahti_utils import download_file

bert_model_url = 'https://a3s.fi/mldata/distilbert-imdb.onnx'

print('Using ONNX Runtime version: {}.'.format(ort.__version__))


class DetectSentiment:
    def __init__(self):
        bert_model_fname = download_file(bert_model_url)
        self.ort_session = ort.InferenceSession(bert_model_fname)
        print('Loaded BERT model from', bert_model_url)

        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased',
                                                       do_lower_case=True)
        print('Initialized BERT tokenizer')

    def predict(self, text):
        tokenized = self.tokenizer.tokenize("[CLS] " + text + " [SEP]")
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized)

        x = np.pad(indexed_tokens, (0, 128-len(indexed_tokens)),
                   mode='constant')

        X = np.zeros((32, 128), dtype=np.long)
        X[0, :] = x
        logits = self.ort_session.run(None, {'input': X})

        p = logits[0][0]
        p = np.exp(p[1])/sum(np.exp(p))  # softmax

        return float(p)
