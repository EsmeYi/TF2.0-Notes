import tensorflow as tf
import tensorflow_datasets as tfds
import time

num_batches = 114
batch_size = 32
learning_rate = 0.001

dataset = tfds.load("tf_flowers", split=tfds.Split.TRAIN, as_supervised=True)
dataset = dataset.map(lambda img, label: (tf.image.resize(img, [224, 224]) / 255.0, label)).shuffle(1024).batch(32)
# model = tf.keras.applications.MobileNetV2(weights=None, classes=5)
model = tf.keras.applications.resnet.ResNet50(weights=None, classes=5)

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
start_time = time.time()
for images, labels in dataset:
    with tf.GradientTape() as tape:
        labels_pred = model(images)
        loss = tf.keras.losses.sparse_categorical_crossentropy(y_true=labels, y_pred=labels_pred)
        loss = tf.reduce_mean(loss)
        print("loss %f" % loss.numpy())
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(grads_and_vars=zip(grads, model.trainable_variables))
print("Time cost: ", time.time()-start_time)