import keras
import matplotlib.pyplot as plt
import matplotlib.image
import numpy as np
import tensorflow as tf
import keras.models as model


img_height = 180
img_width = 180

class_names = ['amusement', 'anger', 'contentment', 'disgust', 'excitement', 'fear', 'sadness']

image = "7f806e9c86510f5c5b8b0c124cfa2134.png"

model = model.load_model("modelNewSamples.h5")

img = tf.keras.utils.load_img(
    image, target_size=(img_height, img_width)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(score)
print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)
img = matplotlib.image.imread(image)
plt.imshow(img)
plt.title(class_names[np.argmax(score)])
plt.show()
