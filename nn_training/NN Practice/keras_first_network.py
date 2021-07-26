# first neural network with keras tutorial
from keras.layers.core import Dropout
import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from keras.saving.save import load_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import tensorflow as tf
import datetime

def build_model(dataset, nodes, size, ratio):
    random_indicies = np.random.choice(np.size(dataset, 0), size, replace=False)
    X = dataset[random_indicies,:-1]
    y = dataset[random_indicies,-1:]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= ratio, random_state=42)
    # define the keras model
    model = Sequential()
    # Old shape:
    # model.add(Dense(nodes, input_dim=119, activation='relu'))
    model.add(Dropout(0.2, input_shape = (119,), name="DropoutLayer" ))
    model.add(Dense(nodes, name='BrainLayer', kernel_initializer=tf.keras.initializers.Zeros()))
    model.add(Dense(1, name='Output')) # linear activation because regression fitting
    # compile the keras model
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_absolute_error'])
    # fit the keras model on the dataset
    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, write_graph=False,
    write_images=True)
    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), 
                epochs=60, batch_size=20, verbose=0, callbacks=[tensorboard_callback])
    
    return model
    ## OPTIONS: print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['mean_absolute_error'])
    plt.plot(history.history['val_mean_absolute_error'])
    plt.title('Abs Error')
    plt.ylabel('error')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Sqr Error')
    plt.ylabel('error')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    

    pred= model.predict(X_test)
    return np.sqrt(mean_squared_error(y_test,pred))

def read_data():
    # load the dataset
    convert = lambda s : float(int(s, 16))
    dataset = np.genfromtxt('gamedata.nn', delimiter=1, converters = {54: convert,59: convert,64: convert,69: convert, 74: convert})
    return dataset

def DOE():
    for ratio in [0.2, 0.4]:
        for size in [500, 5000]:
            for nodes in [10, 50]:
                pass
    ratio = 0.3
    size = 2750
    nodes = 30
    #build_model(read_data(), nodes, size, ratio)

    #rmse = run_model(X, y, nodes, ratio)
    #print(f"{nodes} Nodes, {size} Size, {ratio} Ratio:".ljust(40) +  "%.2f" % rmse)

ratio = 0.3
size = 2750
nodes = 5
#model = build_model(read_data(), nodes, size, ratio)
#model.save('model.h5')

model:Sequential = load_model('model.h5')

for i, node in enumerate(model.layers[1].get_weights()[0]):
    if node[0] == 0:
        print(i+1)
# for layer in model.layers:
#     print('===== LAYER: ', layer.name,'  =====')
#     if layer.get_weights() != []:
#         weights = layer.get_weights()[0]
#         biases = layer.get_weights()[1]
#         print('weights:')
#         print(weights)
#         print("biases:")
#         print(biases)
#     else:
#         print("weights: ", [])


"""
model.save('model.h5')
del model
model = load_model('model.h5')
"""
