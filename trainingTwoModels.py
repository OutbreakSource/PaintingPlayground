import tensorflow as tf


IMG_SIZE = 480
img_data_shape = (IMG_SIZE, IMG_SIZE, 3)
csv_data_shape = (480, 640)
num_classes = 2

# define two inputs layers
img_input = tf.keras.layers.Input(shape=img_data_shape, name="image")
csv_input = tf.keras.layers.Input(shape=csv_data_shape, name="csv")

# define layers for image data
x1 = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)(img_input)
x1 = tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu', name="conv1_img")(x1)
x1 = tf.keras.layers.MaxPooling2D(name="mxp1_img")(x1)
x1 = tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu', name="conv2_img")(x1)
x1 = tf.keras.layers.MaxPooling2D(name="mxp2_img")(x1)
x1 = tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu', name="conv3_img")(x1)
x1 = tf.keras.layers.MaxPooling2D(name="mxp3_img")(x1)
x1 = tf.keras.layers.Flatten(name="flatten_img")(x1)

# define layers for csv data
x2 = tf.keras.layers.Flatten(name="flatten_csv")(csv_input)
x2 = tf.keras.layers.Dense(16, activation='relu', name="dense1_csv")(x2)
x2 = tf.keras.layers.Dense(32, activation='relu', name="dense2_csv")(x2)
x2 = tf.keras.layers.Dense(64, activation='relu', name="dense3_csv")(x2)

# merge layers
x = tf.keras.layers.concatenate([x1,x2], name="concat_csv_img")
x = tf.keras.layers.Dense(128, activation='relu', name="dense1_csv_img")(x)
output = tf.keras.layers.Dense(num_classes, name="classify")(x)

# make model with 2 inputs and 1 output
model = tf.keras.models.Model(inputs=[img_input, csv_input], outputs=output)

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

BATCH_SIZE = 8
train_image_data = tf.keras.utils.image_dataset_from_directory("TestImages",
                                       validation_split=0.2, subset="training",
                                       seed=123, label_mode=None,
                                       image_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH_SIZE)
test_image_data = tf.keras.utils.image_dataset_from_directory("TestImages/anger",
                                       validation_split=0.2, subset="validation",
                                       seed=123, label_mode=None,
                                       image_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH_SIZE)
'''
Found 327 files belonging to 2 classes.
Using 262 files for training.
Found 327 files belonging to 2 classes.
Using 65 files for validation.
'''
# generate random csv data
# number of samples should be equal to images
# in other words for each image you should have 1 corresponding csv entry
train_num_data = tf.random.uniform((262,480,640))
test_num_data = tf.random.uniform((65,480,640))

# create csv dataset
train_num_data = tf.data.Dataset.from_tensor_slices(train_num_data).batch(BATCH_SIZE)
test_num_data = tf.data.Dataset.from_tensor_slices(test_num_data).batch(BATCH_SIZE)

# generate random labels
y_train = tf.data.Dataset.from_tensor_slices(tf.random.uniform((262,1))).batch(BATCH_SIZE)
y_test = tf.data.Dataset.from_tensor_slices(tf.random.uniform((65,1))).batch(BATCH_SIZE)

def my_gen(subset):
    while True:
        if subset == "training":
            for i in train_image_data.take(1):
                img_batch = i
            for j in train_num_data.take(1):
                csv_batch = j
            for k in y_test.take(1):
                labels_batch = k
        else:
            for i in test_image_data.take(1):
                img_batch = i
            for j in test_num_data.take(1):
                csv_batch = j
            for k in y_test.take(1):
                labels_batch = k

        yield ((img_batch, csv_batch), labels_batch)

gen_train = my_gen("training")
gen_valid = my_gen("validation")

model.fit(gen_train, epochs=2, steps_per_epoch=3, validation_data=gen_valid, validation_steps=1)
