import keras
import matplotlib.pyplot as plt
import matplotlib.image
import numpy as np
import pathlib
import tensorflow as tf
import keras.models as model


img_height = 180
img_width = 180

data_dir = pathlib.Path("C:\\Users\\danie\\PycharmProjects\\PaintingPlayground\\ArtSamples")

image_count = len(list(data_dir.glob('*/*.jpg')))
print(image_count)

batch_size = 32
img_height = 180
img_width = 180

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

class_names = train_ds.class_names

img_height = 180
img_width = 180

sunflower_path = "03e58fc1af619e267802f56b6dafc142.png"

model = model.load_model("checkpoints/model.h5")

img = tf.keras.utils.load_img(
    sunflower_path, target_size=(img_height, img_width)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)
img = matplotlib.image.imread(sunflower_path)
plt.imshow(img)
plt.title(class_names[np.argmax(score)])
plt.show()
