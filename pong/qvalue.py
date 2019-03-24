import numpy as np
import pyoneer as pynr
import tensorflow as tf

from gym.spaces import Box


class QValue(tf.keras.Model):
    def __init__(self, **kwargs):
        super(QValue, self).__init__(**kwargs)

        self.observation_space = Box(
            np.array([-1, -1, -1, 0, 0, 0]), np.array([1, 1, 1, 1, 1, 1])
        )

        kernel_initializer = tf.keras.initializers.VarianceScaling(scale=2.0)

        self.dense = tf.keras.layers.Dense(
            units=64,
            activation=pynr.nn.swish,
            kernel_initializer=kernel_initializer
        )

        self.dense_value = tf.keras.layers.Dense(
            units=1, activation=None, kernel_initializer=kernel_initializer
        )

    def call(self, inputs, training=False):
        loc, var = pynr.nn.moments_from_range(self.observation_space.low, self.observation_space.high)
        inputs = pynr.math.normalize(inputs, loc=loc, scale=tf.sqrt(var))

        hidden = self.dense(inputs)
        value = self.dense_value(hidden)

        return value[..., 0]
