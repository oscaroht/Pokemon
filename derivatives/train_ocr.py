

import tensorflow as tf
import os
import cv2
import numpy as np
from sklearn.utils import shuffle
from pokebot.settings import characterlist

char = {}
for i, ch in enumerate(characterlist):
    char[i] = ch
    char[ch] = i


def LoadData(FP = '.'):
    '''
    Loads the OCR dataset. A is matrix of images (NIMG, Height, Width, Channel).
    Y is matrix of characters (NIMG, MAX_CHAR)
    FP:     Path to OCR data folder
    return: Data Matrix, Target Matrix, Target Strings
    '''
    TFP = os.path.join(FP, 'Train.csv')
    A, Y, T, FN = [], [], [], []
    with open(TFP) as F:
        for Li in F:
            try:
                FNi, Yi = Li.strip().split(',')  # filename,string
                T.append( char[Yi] ) # char is a two way dict
                A.append(  cv2.cvtColor(cv2.imread(os.path.join(FP, FNi)), cv2.COLOR_RGB2GRAY ).reshape(32,32,1)/255      )  # cv2.cvtColor(cv2.imread(os.path.join(FP, FNi)), cv2.COLOR_RGB2GRAY )              # np.array( imread(os.path.join(FP, FNi)) ).reshape(8192,32,640, 3)  )
            except:
                pass
    return np.stack(A), np.stack(T)

X, y = LoadData('C:\\Users\\oscar\\PycharmProjects\\Pokemon\\derivatives\\training_data')


# model0 = tf.keras.models.Sequential([
#   tf.keras.layers.Flatten(input_shape=(32, 32)),
#   tf.keras.layers.Dense(1024, activation='relu'),
#   tf.keras.layers.Dropout(0.2),
#   tf.keras.layers.Dense(123) # output is 26+26+10+2
# ])

X, y = shuffle(X, y)

model = tf.keras.Sequential(
    [
    tf.keras.layers.Conv2D(32, (3,3), padding='same', activation="relu",input_shape=(32, 32, 1)),
    tf.keras.layers.MaxPooling2D((3, 3), strides=2),
    tf.keras.layers.Dropout(0.1),

    # tf.keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu'),
    # tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    # tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Conv2D(64, (3,3), padding='same', activation="relu"),
    tf.keras.layers.MaxPooling2D((5, 5), strides=2),
    tf.keras.layers.Dropout(0.1),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(len(characterlist), activation="softmax") # the number of output channels is equal to the number of answer options
]
)

#predictions = model(x_train[:1]).numpy()
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer='adam', #adam
              loss=loss_fn,
              metrics=['accuracy'])

model.fit(X, y, epochs=5)

model.save('ocr_model')





# prediction = model(X[:1341]).numpy()
# probabs = tf.nn.softmax(prediction).numpy()


test=1
