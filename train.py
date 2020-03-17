from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.callbacks import ModelCheckpoint

def get_model(X, encoding_size):
    print("gettig model")
    model = Sequential()
    model.add(LSTM(
        256,
        input_shape=(X.shape[1], X.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.3))
    model.add(LSTM(256, return_sequences=True))
    model.add(Dropout(0.3))

    
    # model.add(LSTM(256, return_sequences=True))
    # model.add(Dropout(0.3))
    

    model.add(LSTM(256))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(encoding_size))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train(X, y, encoding_size):
    #5 epoc
    #another LSTM
    model = get_model(X, encoding_size)
    print("load weights start")
    model.load_weights('weights.49-0.8625.hdf5')
    print("load weights done")
    filepath = "seq50CONT.{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(
        filepath, monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]
    model.fit(X, y, epochs=10000, batch_size=64, callbacks=callbacks_list)