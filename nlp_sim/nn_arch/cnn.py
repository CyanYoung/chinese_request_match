from keras.layers import Conv1D, Conv2D, Dense
from keras.layers import MaxPooling1D, GlobalMaxPooling1D, MaxPooling2D, GlobalMaxPooling2D
from keras.layers import BatchNormalization, Dropout, Concatenate, Flatten, Reshape
from keras.layers import Subtract, Multiply, Dot, Lambda

import keras.backend as K


seq_len = 30


def cnn_siam_parallel(embed_input1, embed_input2):
    ca1 = Conv1D(filters=32, kernel_size=2, activation='relu')
    ca2 = Conv1D(filters=32, kernel_size=3, activation='relu')
    ca3 = Conv1D(filters=32, kernel_size=4, activation='relu')
    ca4 = Conv1D(filters=32, kernel_size=5, activation='relu')
    fc1 = Dense(100, activation='relu')
    fc2 = Dense(1, activation='sigmoid')
    x1 = ca1(embed_input1)
    x1 = BatchNormalization()(x1)
    x1 = GlobalMaxPooling1D()(x1)
    x2 = ca2(embed_input1)
    x2 = BatchNormalization()(x2)
    x2 = GlobalMaxPooling1D()(x2)
    x3 = ca3(embed_input1)
    x3 = BatchNormalization()(x3)
    x3 = GlobalMaxPooling1D()(x3)
    x4 = ca4(embed_input1)
    x4 = BatchNormalization()(x4)
    x4 = GlobalMaxPooling1D()(x4)
    x = Concatenate()([x1, x2, x3, x4])
    y1 = ca1(embed_input2)
    y1 = BatchNormalization()(y1)
    y1 = GlobalMaxPooling1D()(y1)
    y2 = ca2(embed_input2)
    y2 = BatchNormalization()(y2)
    y2 = GlobalMaxPooling1D()(y2)
    y3 = ca3(embed_input2)
    y3 = BatchNormalization()(y3)
    y3 = GlobalMaxPooling1D()(y3)
    y4 = ca4(embed_input2)
    y4 = BatchNormalization()(y4)
    y4 = GlobalMaxPooling1D()(y4)
    y = Concatenate()([y1, y2, y3, y4])
    diff = Lambda(lambda a: K.abs(a))(Subtract()([x, y]))
    prod = Multiply()([x, y])
    z = Concatenate()([x, y, diff, prod])
    z = Dropout(0.5)(z)
    z = fc1(z)
    z = Dropout(0.5)(z)
    return fc2(z)


def cnn_siam_serial(embed_input1, embed_input2):
    ca1 = Conv1D(filters=64, kernel_size=2, activation='relu')
    ca2 = Conv1D(filters=64, kernel_size=3, activation='relu')
    fc1 = Dense(100, activation='relu')
    fc2 = Dense(1, activation='sigmoid')
    x = ca1(embed_input1)
    x = BatchNormalization()(x)
    x = MaxPooling1D(3)(x)
    x = ca2(x)
    x = BatchNormalization()(x)
    x = MaxPooling1D(3)(x)
    y = ca1(embed_input2)
    y = BatchNormalization()(y)
    y = MaxPooling1D(3)(y)
    y = ca2(y)
    y = BatchNormalization()(y)
    y = MaxPooling1D(3)(y)
    diff = Lambda(lambda a: K.abs(a))(Subtract()([x, y]))
    prod = Multiply()([x, y])
    z = Concatenate()([x, y, diff, prod])
    z = Flatten()(z)
    z = Dropout(0.5)(z)
    z = fc1(z)
    z = Dropout(0.5)(z)
    return fc2(z)


def cnn_join_parallel(embed_input1, embed_input2):
    ca1 = Conv2D(filters=32, kernel_size=2, activation='relu')
    ca2 = Conv2D(filters=32, kernel_size=3, activation='relu')
    ca3 = Conv2D(filters=32, kernel_size=4, activation='relu')
    ca4 = Conv2D(filters=32, kernel_size=5, activation='relu')
    fc1 = Dense(100, activation='relu')
    fc2 = Dense(1, activation='sigmoid')
    dot_input = Dot(2)([embed_input1, embed_input2])
    dot_input = Reshape((seq_len, seq_len, 1))(dot_input)
    x1 = ca1(dot_input)
    x1 = BatchNormalization()(x1)
    x1 = GlobalMaxPooling2D()(x1)
    x2 = ca2(dot_input)
    x2 = BatchNormalization()(x2)
    x2 = GlobalMaxPooling2D()(x2)
    x3 = ca3(dot_input)
    x3 = BatchNormalization()(x3)
    x3 = GlobalMaxPooling2D()(x3)
    x4 = ca4(dot_input)
    x4 = BatchNormalization()(x4)
    x4 = GlobalMaxPooling2D()(x4)
    x = Concatenate()([x1, x2, x3, x4])
    x = Dropout(0.5)(x)
    x = fc1(x)
    x = Dropout(0.5)(x)
    return fc2(x)


def cnn_join_serial(embed_input1, embed_input2):
    ca1 = Conv2D(filters=64, kernel_size=2, activation='relu')
    ca2 = Conv2D(filters=64, kernel_size=3, activation='relu')
    fc1 = Dense(100, activation='relu')
    fc2 = Dense(1, activation='sigmoid')
    dot_input = Dot(2)([embed_input1, embed_input2])
    dot_input = Reshape((seq_len, seq_len, 1))(dot_input)
    x = ca1(dot_input)
    x = BatchNormalization()(x)
    x = MaxPooling2D(2)(x)
    x = ca2(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D(2)(x)
    x = Flatten()(x)
    x = Dropout(0.5)(x)
    x = fc1(x)
    x = Dropout(0.5)(x)
    return fc2(x)
