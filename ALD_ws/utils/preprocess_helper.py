import json
import re
import string
import pickle
import numpy as np
import pandas as pd
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from sklearn.base import BaseEstimator, TransformerMixin

class SeparateEmoji(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.emoji_set = pickle.load(open('./data/emoji_set.pkl','rb'))

    def fit(self, X, y=None):
        return self

    @staticmethod
    def seperate_emoji(self, text):
        for c in text:
            if c in self.emoji_set:
                text=text.replace(c,' '+c+' ')
        return text

    def transform(self, X):
        return X.apply(lambda x: self.seperate_emoji(self, x))


class RemovePunct(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    @staticmethod
    def remove_punct(text):
        table = str.maketrans(dict.fromkeys(string.punctuation + "\'\""))
        return text.translate(table)

    def transform(self, X):
        return X.apply(lambda x: self.remove_punct(x))


class RemoveUrl(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    @staticmethod
    def remove_url( text):
        return re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE).strip()

    def transform(self, X):
        return X.apply(lambda x: self.remove_url(x))


class Convert2Zemberek(BaseEstimator, TransformerMixin):
    def __init__(self, zemb, src_path="/tmp/before_zem.json", tgt_path="/tmp/after_zem.json"):
        self.zemb = zemb
        self.src_path = src_path
        self.tgt_path = tgt_path

    def fit(self, X, y=None):
        return self

    def set_zemberek_file(self, X):
        thedic = {"texts": []}
        for z in X:
            thedic["texts"].append(z)
        json.dump(thedic, open(self.src_path, "w"))
        self.zemb.text2zemb(self.src_path, self.tgt_path)
        X = pd.read_json(self.tgt_path)["text"]
        return X

    def transform(self, X):
        return self.set_zemberek_file(X)


class TweetTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.tokenizer = Tokenizer(oov_token='<UNK>')

    def fit(self, X, y=None):
        self.tokenizer.fit_on_texts(X.tolist())
        return self

    def transform(self, X):
        return X.apply(lambda sent: self.tokenizer.texts_to_sequences([sent])[0])


class FixSequenceLength(BaseEstimator, TransformerMixin):
    def __init__(self, z=5, pad_value=0):
        self.z = z
        self.pad_value = pad_value

    def fit(self, X, y=None):
        self.sentences_lengths = [len(x) for x in X]
        self.seq_length = int(np.mean(self.sentences_lengths) + (self.z * np.std(self.sentences_lengths)))
        return self

    def transform(self, X):
        return pad_sequences(X, self.seq_length, value=self.pad_value)
