import numpy as np
import tensorflow as tf
import random 
import tqdm
import context2vec
import keras
from keras.layers import TextVectorization
import glob

def txt_eos_bos(text):
    text = tf.strings.join(["[BOS]", text, "[EOS]"], separator=" ")
    return text 

def generate_train_data(sequences, window_size, num_ns, vocab_size, seed):
    targets, contexts, labels = [], [], []
    sampling_table = tf.keras.preprocessing.sequence.make_sampling_table(
        vocab_size)

    # create (context, target) pairs
    def create_ctx_targ_pairs(sequence, window_size):
        ctxt_targs = []
        for i, wi in enumerate(sequence):
            if not wi:
                continue
            if sampling_table[wi] < random.random():
                continue
            window_left = max(0, i-window_size)
            window_right = min(len(sequence), i+window_size+1)
            target = []
            context = []
            target.append(wi)

            for j in range(window_left, window_right):
                if j == i:
                    continue

                context.append(sequence[j])

            ctxt_targs.append([context, target])
        return ctxt_targs
    # for sequence in tqdm.tqdm(sequences):
    for sequence in sequences:
        con_trg = create_ctx_targ_pairs(sequence, window_size=window_size)
        # print(sequence)
        # print("cont", con_trg[0])
        for contxt, targ in con_trg:
            targ_class = tf.expand_dims(tf.constant(targ, dtype="int64"), 1)
            negative_candi, _, _ = tf.random.log_uniform_candidate_sampler(
                true_classes=targ_class,
                num_true=1,
                num_sampled=num_ns,
                range_max=vocab_size,
                unique=True,
                seed=seed,
                name="negative sampling"
            )
            labels.append(np.concatenate(
                (np.ones((1)), np.zeros(num_ns)), axis=-1))
            targets.append(np.concatenate((targ, negative_candi), axis=-1))
            contexts.append(np.array(contxt, np.int64))
    contexts = tf.keras.utils.pad_sequences(contexts, padding="post")       
    # contexts = np.array(contexts, dtype="int64")
    targets = np.array(targets, dtype="int64")
    labels = np.array(labels, dtype="float64")
    return contexts, targets, labels
    

    
# get the data

# define the layer

# define loss
# make the model
