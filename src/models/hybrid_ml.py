import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class HybridMLModel:
    def __init__(self, config):
        self.config = config
        self.model = self._build_model()
        self.scaler = StandardScaler()

    def _build_model(self):
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Dense(64, activation="relu", input_shape=(10,)),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.Dense(1, activation="linear"),
            ]
        )
        model.compile(
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=self.config["ml_model"]["learning_rate"]
            ),
            loss="mse",
        )
        return model

    def train(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
        self.model.fit(
            X_train,
            y_train,
            epochs=50,
            batch_size=self.config["ml_model"]["batch_size"],
            validation_split=0.2,
        )

    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
