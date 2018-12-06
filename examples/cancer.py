from keras2pmml import keras2pmml
from sklearn.datasets import load_breast_cancer
import numpy as np
import theano
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense
from sklearn.preprocessing import MinMaxScaler

cancer = load_breast_cancer()
X = cancer.data
y = cancer.target

theano.config.floatX = 'float32'
X = X.astype(theano.config.floatX)
y = y.astype(np.int32)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, stratify=y, random_state=42)

y_train_ohe = np_utils.to_categorical(y_train)
y_test_ohe = np_utils.to_categorical(y_test)

mms = MinMaxScaler()
X_train_scaled = mms.fit_transform(X_train)
X_test_scaled = mms.transform(X_test)

model = Sequential()
model.add(Dense(input_dim=X_train_scaled.shape[1], output_dim=20, activation='tanh'))
model.add(Dense(input_dim=20, output_dim=5, activation='tanh'))
model.add(Dense(input_dim=5, output_dim=y_train_ohe.shape[1], activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='sgd')
model.fit(X_train_scaled, y_train_ohe, nb_epoch=100, batch_size=1, verbose=3, validation_data=None)

params = {
    'copyright': 'Václav Čadek',
    'description': 'Simple Keras model for Iris dataset.',
    'model_name': 'Iris Model'
}
file_name = 'cancer.pmml'
keras2pmml(model, transformer=mms, file=file_name, **params)
