import tensorflow as tf
import keras
from keras.layers import LSTM, Dense, Embedding
import numpy as np


class BiLSTM(keras.layers.Layer):
    def __init__(self,  hidden_units):
        super().__init__()
        self.f_lstm = LSTM(hidden_units)
        self.b_lstm = LSTM(hidden_units, go_backwards=True)

    def call(self, input_seq):
        h1 = self.f_lstm(input_seq)
        h2 = self.b_lstm(input_seq)
        return tf.concat([h1, h2], axis=-1)


class Context2Vec(keras.Model):
    def __init__(self, vocab_size, ns, context_units, bilstm_hidden_units,  input_units, embedding_dim,  seq_length):
        super().__init__()
        self.c_w = Embedding(vocab_size, context_units,
                             input_length=seq_length,
                             name="context_embeddings")
        self.blstm = BiLSTM(hidden_units=bilstm_hidden_units)
        self.l1 = Dense(units=input_units, activation='relu')
        self.l2 = Dense(units=input_units, activation="relu")
        self.scu = Dense(units=embedding_dim, activation='linear')
        self.t_w = Embedding(vocab_size, embedding_dim,
                             input_length=ns+1,
                             name="target_embeddings")

    def call(self,  pair):
        context, target = pair
        c_w = self.c_w(context)
        bl = self.blstm(c_w)

        l1 = self.l1(bl)
        l2 = self.l2(l1)
        scu = self.scu(l2)
        t_w = self.t_w(target)
        return tf.einsum('ik, ijk -> ij ', scu, t_w)


# if __name__ == '__main__':
    # bd = BiLSTM(10)
    # inp = tf.random.normal([1, 3, 1])
    # print(inp)
    # print(bd(inp))
    # print(c2v(inp))
    # x = random.sample(range(10000), 10)
    # con, targ, lab = generate_train_data([x], 3, 3, 10000, 42)
    # print(con)
    # seq_length = con[1].shape[0]
    # print(seq_length)
    # y = [con, targ]

    # print(con)
    # print("targ")
    # print(targ)
    # print(lab)
    # c2v = Context2Vec(10000, 20, 10, 10, 10, 10,
        #   seq_length=seq_length)
    # print(c2v(y))
