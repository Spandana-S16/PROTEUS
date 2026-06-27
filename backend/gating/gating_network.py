import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout


class GatingNetwork:

    def __init__(self):

        self.model = Sequential([

            Dense(
                32,
                activation="relu",
                input_shape=(12,)
            ),

            Dropout(0.2),

            Dense(
                16,
                activation="relu"
            ),

            Dense(
                3,
                activation="softmax"
            )

        ])

        self.model.compile(

            optimizer="adam",

            loss=tf.keras.losses.KLDivergence(),

            metrics=["mae"]

        )

    def train(self, X, y):

        self.model.fit(

            X,

            y,

            epochs=50,

            batch_size=32,

            validation_split=0.2,

            verbose=1

        )

    def predict_weights(self, X):

        return self.model.predict(
            X,
            verbose=0
        )