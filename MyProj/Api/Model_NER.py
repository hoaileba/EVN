import numpy as np
import tensorflow as tf
import pandas as pd
import os
import json
import re
from tensorflow.keras.layers import Dense, Lambda, dot, Activation, concatenate
from tensorflow.keras.layers import Layer
from transformers import TFAutoModel, PhobertTokenizer
import tensorflow_addons as tfa


TRAINING_MODE = 'training'
PREDICTION_MODE = 'prediction'

class CRFLayer(tf.keras.layers.Layer):

    def __init__(self,
                 units,
                 chain_initializer='orthogonal',
                 use_boundary=True,
                 boundary_initializer='zeros',
                 use_kernel=True,
                 **kwargs):
        super().__init__(**kwargs)
        self.crf = tfa.layers.CRF(
            units,
            chain_initializer=chain_initializer,
            use_boundary=use_boundary,
            boundary_initializer=boundary_initializer,
            use_kernel=use_kernel,
            **kwargs)
        self.units = units
        self.chain_kernel = self.crf.chain_kernel
        # record sequence length to compute loss
        self.sequence_length = None
        self.mask = None
        self.mode = TRAINING_MODE

    def call(self, inputs, training=None, mask=None):
        """Forward pass.
        Args:
            inputs: A [batch_size, max_seq_len, depth] tensor, inputs of CRF layer
            mask: A [batch_size, max_seq_len] boolean tensor, used to compulte sequence length in CRF layer
        Returns:
            potentials: A [batch_size, max_seq_len, units] tensor in train phase.
            sequence: A [batch_size, max_seq_len, units] tensor of decoded sequence in predict phase.
        """
        self.mode = TRAINING_MODE if training is True else PREDICTION_MODE
        sequence, potentials, sequence_length, transitions = self.crf(inputs, mask=mask)
        # sequence_length is computed in both train and predict phase
        self.sequence_length = sequence_length
        # save mask, which is needed to compute accuracy
        self.mask = mask

        sequence = tf.cast(tf.one_hot(sequence, self.units), dtype=self.dtype)
        return tf.keras.backend.in_train_phase(potentials, sequence)

    def accuracy(self, y_true, y_pred):
        if len(tf.keras.backend.int_shape(y_true)) == 3:
            y_true = tf.argmax(y_true, axis=-1)
        if self.mode == PREDICTION_MODE:
            y_pred = tf.argmax(y_pred, axis=-1)
        else:
            y_pred, _ = tfa.text.crf_decode(y_pred, self.chain_kernel, self.sequence_length)
        y_pred = tf.cast(y_pred, dtype=y_true.dtype)
        equals = tf.cast(tf.equal(y_true, y_pred), y_true.dtype)
        if self.mask is not None:
            mask = tf.cast(self.mask, y_true.dtype)
            equals = equals * mask
            return tf.reduce_sum(equals) / tf.reduce_sum(mask)
        return tf.reduce_mean(equals)

    def neg_log_likelihood(self, y_true, y_pred):
        # print(y_true,y_pred)
        # loss = tf.keras.losses.SparseCategoricalCrossentropy(y_true,y_pred)
        log_likelihood, _ = tfa.text.crf_log_likelihood(y_pred, y_true, self.sequence_length, self.chain_kernel)
        return tf.reduce_max(-log_likelihood)

graph = tf.compat.v1.reset_default_graph()

class Attention(Layer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, hidden_states):
        hidden_size = int(hidden_states.shape[2])
        score_first_part = Dense(hidden_size, use_bias=False, name='attention_score_vec')(hidden_states)
        h_t = Lambda(lambda x: x[:, -1, :], output_shape=(hidden_size,), name='last_hidden_state')(hidden_states)
        score = dot([score_first_part, h_t], [2, 1], name='attention_score')
        attention_weights = Activation('softmax', name='attention_weight')(score)
        context_vector = dot([hidden_states, attention_weights], [1, 1], name='context_vector')
        pre_activation = concatenate([context_vector, h_t], name='attention_output')
        attention_vector = Dense(128, use_bias=False, activation='tanh', name='attention_vector')(pre_activation)
        return attention_vector

class Model_NER:
    def __init__(self,batch_size = 64, epochs = 10):
        self.batch_size = batch_size
        self.epochs = epochs
    
    def create_model(self,path_bert = 'vinai/phobert-base', num_class = 6, MAX_LEN = 30):

        phobert = TFAutoModel.from_pretrained(path_bert)
        ids = tf.keras.layers.Input(shape=(MAX_LEN), dtype=tf.int32)
        mask = tf.keras.layers.Input(shape=(MAX_LEN,), name='attention_mask', dtype='int32')
        
        # For transformers v4.x+: 
        embeddings = phobert(ids,attention_mask = mask)[0]
        X =tf.keras.layers.Bidirectional( tf.keras.layers.LSTM(128,return_sequences=True,dropout=0.5))(embeddings)
        X = tf.keras.layers.TimeDistributed(Dense(128,activation='relu'))(X)
        crf = CRFLayer(5)
        Y = crf(X,mask =mask_)

        
        model = tf.keras.models.Model(inputs=[ids,mask_], outputs=[Y])
        model.summary()
        model.layers[2].trainable = False
        self.model = model
      

    def train(self,X_train,X_train_mask,y_true):
        self.model.fit((X_train,X_train_mask),y_true,epochs = self.epochs, batch_size = self.batch_size)
    
    
    def get_summary(self):
        self.model.summary()
    
    
    def predict(self,X_test,X_test_mask):
        pred = self.model.predict((X_test,X_test_mask))
        return np.argmax(pred, axis = 1)

    def save_weight(self,path_save, num_last_lays = 6):
        self.model.save_weights(path_save)
          
    
    def load_weight(self, path_weight):
        self.model.load_weights(path_weight)
    
    def create_model_test(self):
        pass

    def get_predict_test(self,text):
        return [{}]
