import os
import cv2
import numpy as np
import tensorflow as tf
from keras import layers, models
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

# Reshape the data to include the channel dimension (28, 28, 1)
# This is done since the convolutional neural network (CNN) requires 3 dimensions where the last dimension is the
# number of channels (colors). It's 1 because it is greyscale.
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

# Data augmentation
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=5,
    zoom_range=0.05,
    width_shift_range=0.05,
    height_shift_range=0.05
)
datagen.fit(x_train)

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),  # first number is the no. of filters
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),  # converts 2D to 1D for the dense layer
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# No need one-hot encoding when using sparse_categorical_crossentropy
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(datagen.flow(x_train, y_train, batch_size=32), epochs=5, validation_data=(x_test, y_test))

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f'\nTest accuracy: {test_acc:.4f}')
print(f'Test loss: {test_loss:.4f}')

model.save('third-new-model.keras')

model = models.load_model('third-new-model.keras')

# Function to load and preprocess image using OpenCV
def PreprocessImage(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read the image as grayscale
    img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)  # Directly resize without padding
    img = np.invert(img)
    img = tf.keras.utils.normalize(img, axis=1)
    img = np.expand_dims(img, axis=-1)  # Add channel dimension
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

def PredictDigit():
    image_number = 1
    while os.path.isfile(f"digits2/digit{image_number}.png"):
        try:
            img = PreprocessImage(f"digits2/digit{image_number}.png")
            prediction = model.predict(img)
            print(f"This digit is probably a {np.argmax(prediction)}")
            plt.imshow(img[0], cmap=plt.cm.binary)
            plt.show()
        except:
            print("Error!")
        finally:
            image_number += 1


PredictDigit()