# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l9ytE_i7FBeZwEE2B2r9cV5oSPufbR5q
"""

import tensorflow as tf
from tensorflow.keras import layers, models

# Define the sub-pixel convolution layer
class SubpixelConv2D(layers.Layer):
    def __init__(self, scale=2, **kwargs):
        super(SubpixelConv2D, self).__init__(**kwargs)
        self.scale = scale

    def call(self, inputs):
        return tf.nn.depth_to_space(inputs, self.scale)

    def get_config(self):
        config = super(SubpixelConv2D, self).get_config()
        config.update({"scale": self.scale})
        return config

# Build the Sub-pixel Convolutional Neural Network
def build_srcnn(input_shape=(24, 24, 3), scale=2):
    inputs = layers.Input(shape=input_shape)

    # Feature extraction layers
    x = layers.Conv2D(64, (5, 5), padding='same', activation='relu')(inputs)
    x = layers.Conv2D(64, (3, 3), padding='same', activation='relu')(x)
    x = layers.Conv2D(32, (3, 3), padding='same', activation='relu')(x)

    # Sub-pixel convolution
    x = layers.Conv2D(3 * (scale ** 2), (3, 3), padding='same')(x)
    x = SubpixelConv2D(scale=scale)(x)

    model = models.Model(inputs, x)
    return model

# Create the model
model = build_srcnn()
model.summary()

# Compile the model
model.compile(optimizer='adam', loss='mse')

# The model is now ready to be trained with training data.