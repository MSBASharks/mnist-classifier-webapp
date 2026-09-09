"""
Loads the trained MNIST CNN and classifies uploaded digit images.

Preprocessing here matches exactly what Group_1_Project_1.ipynb did before
training (see cells 3-4 and 39):
    x_train, x_test = x_train / 255.0, x_test / 255.0          # scale to 0-1
    x_train = x_train.reshape((n, 28, 28, 1))                  # add channel dim
    NModelFinal.fit(x_train, y_train, ...)                     # no batch dim needed for fit,
                                                                # but predict() needs one

The model is loaded ONCE here, at module import time — not inside
classify_image() — per the A6 hand-off requirement. Django imports this
module once per worker process, so the model stays resident in memory
across every request instead of reloading (slowly) on each upload.
"""
import numpy as np
import tensorflow as tf

# The notebook built the final layer with activation=tf.nn.softmax (a direct
# function reference, not the string 'softmax'). Whatever Keras version
# Colab used at training time serialized that as TensorFlow's internal name
# for it, 'softmax_v2'. Keras 3 (bundled with this tensorflow-cpu version)
# uses a different, stricter deserializer that doesn't recognize that
# internal name on its own -- custom_objects tells it explicitly what
# 'softmax_v2' actually refers to, so the saved model can load correctly
# without needing to retrain or re-save it.
model = tf.keras.models.load_model(
    'ml/mnistmodel.keras',
    custom_objects={'softmax_v2': tf.nn.softmax},
)


def classify_image(img_array):
    """
    Args:
        img_array: a 28x28 numpy array, pixel values already scaled to 0-1
                   (views.py's _parse_pixel_csv already does this scaling —
                   this function just adds the channel and batch dimensions
                   the model itself expects).

    Returns:
        (digit, confidence): digit is an int 0-9, confidence is a float 0-1
        representing the softmax probability assigned to that digit.
    """
    # (28, 28) -> (1, 28, 28, 1): batch dimension of 1, single grayscale channel.
    model_input = img_array.reshape(1, 28, 28, 1).astype('float32')

    probs = model.predict(model_input, verbose=0)  # shape (1, 10)
    digit = int(probs.argmax(axis=1)[0])
    confidence = float(probs.max(axis=1)[0])

    return digit, confidence

