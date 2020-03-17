import train

import numpy as np
import matplotlib.pyplot as plt
from mido import MidiFile
from collections import defaultdict
from sklearn.metrics import confusion_matrix
import random
import os

def evaluate(X_train, y_train, X_dev, y_dev, X_test, y_test, encoding_size, weights_name):
    model = train.get_model(X_dev, encoding_size)
    model.load_weights(weights_name)

    print("TRAIN STATS:")
    print(model.evaluate(X_train, y_train))

    print("DEV STATS:")
    print(model.evaluate(X_dev, y_dev))

    print("TEST STATS:")
    print(model.evaluate(X_test, y_test))

import matplotlib.pyplot as plt

def plot_confusion_matrix(save_name, y_true, y_pred, normalize=False, title=None, cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels = np.arange(1,281))
    # Only use the labels that appear in the data
    # classes = ['0 (C)', '1 (C#)', '2 (D)', '3 (D#)', '4 (E)', '5 (F)', '6 (F#)','7 (G)', '8 (G#)', '9 (A)', '10 (A#)', '11 (B)']
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots(figsize = (60, 60))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=np.arange(1,281), yticklabels=np.arange(1,281),
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    if save_name != None:
        plt.savefig(save_name)
    return ax