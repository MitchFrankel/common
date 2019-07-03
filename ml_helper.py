"""
Helper functions for use with machine learning
"""

# Base Imports
import matplotlib.pyplot as plt
import numpy as np

# Keras imports
from keras.datasets import imdb


def plot_train_val_loss(model_history, ax=None, figsize=None):
    """
    Plot the training and validation loss for deep learning model across epochs

    Parameters
    ----------
    model_history: keras.callbacks.History object dictionary
        The history output dictionary of a trained model from keras

    ax: matplotlib axes, default=None
        Specific axes to plot to

    figsize: tuple, default=None
        Plot figure size if no axes passed

    Returns
    -------
    ax: matplotlib axes object
        Plot axes
    """

    # Create figure or use axes
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)

    # Plot loss
    epochs = range(1, len(model_history['loss']) + 1)
    ax.plot(epochs, model_history['loss'], 'rx', label="Training Loss")
    ax.plot(epochs, model_history['val_loss'], 'bo', label="Validation Loss")

    # Add title/labels
    ax.set_title("Training and Validation Loss")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Loss")
    ax.legend()

    return ax


def plot_train_val_accuracy(model_history, ax=None, figsize=None):
    """
    Plot the training and validation accuracy for deep learning model across epochs

    Parameters
    ----------
    model_history: keras.callbacks.History object dictionary
        The history output of a trained model from keras

    ax: matplotlib axes, default=None
        Specific axes to plot to

    figsize: tuple, default=None
        Plot figure size if no axes passed

    Returns
    -------
    ax: matplotlib axes object
        Plot axes
    """

    # Create figure or use axes
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)

    # Create Epoch numbers
    epochs = range(1, len(model_history['acc']) + 1)

    # Plot losses
    ax.plot(epochs, model_history['acc'], 'rx', label="Training Accuracy")
    ax.plot(epochs, model_history['val_acc'], 'bo', label="Validation Accuracy")

    # Add title/labels
    ax.set_title("Training and Validation Accuracy")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Accuracy")
    ax.legend()

    return ax


def vectorize_sequences(sequences, dim=10000):
    res = np.zeros((len(sequences), dim))
    for i, seq in enumerate(sequences):
        res[i, seq] = 1.
    return res


def decode_keras_word_lists(word_list_data, dataset):
    word_index = dataset.get_word_index()
    reverse_word_index = dict((value, key) for (key, value) in word_index.items())
    decoded_words = " ".join(reverse_word_index.get(i-3, '?') for i in word_list_data)
    return decoded_words


def plot_val_and_acc(model_history, ax=None, figsize=None):
    """
    Plot both accuracy and validation in a single plot. Additionally, display min loss and max accuracy
    Plot the training and validation accuracy for deep learning model across epochs

    Parameters
    ----------
    model_history: keras.callbacks.History object dictionary
        The history output of a trained model from keras

    ax: matplotlib axes, default=None
        Specific axes to plot to

    figsize: tuple, default=None
        Plot figure size if no axes passed

    Returns
    -------
    ax: matplotlib axes object
        Plot axes
    """

    # Create figure or use axes
    if ax is None:
        fig, ax = plt.subplots(1, 2, figsize=figsize)

    # Plot
    plot_train_val_loss(model_history, ax=ax[0])
    plot_train_val_accuracy(model_history, ax=ax[1])

    # Print
    print("Min Validation Loss of {:.2f} at Epoch {}".format(min(model_history['val_loss']),
                                                             np.argmin(model_history['val_loss']) + 1))
    print("Max Validation Accuracy of {:.2f} at Epoch {}".format(max(model_history['val_acc']),
                                                                 np.argmax(model_history['val_acc']) + 1))

    return ax
