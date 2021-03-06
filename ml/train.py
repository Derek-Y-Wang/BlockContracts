import json

from ml.AmbiguityDetector import AmbiguityDetector
from ml.Hyperparameters import Hyperparameters
from ml.LayerParameter import LayerParameter

if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from tensorflow.keras import layers

    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences

    # The following lines adjust the granularity of reporting.
    pd.options.display.max_rows = 10
    pd.options.display.float_format = "{:.1f}".format
    # tf.keras.backend.set_floatx('float32')

    print("Ran the import statements.")

    with open("./data/sarcasm.json", 'r') as f:
        datastore = json.load(f)

    sentences = []
    labels = []
    urls = []

    for item in datastore:
        sentences.append(item['headline'])
        labels.append(item['is_sarcastic'])
        urls.append(item['article_link'])

    # updated hypermater values in the final form
    vocab_size = 1000
    embedding_dim = 16
    max_length = 16
    trunc_type = 'post'
    padding_type = 'post'
    oov_token = "<OOV>"
    training_size = 20000

    training_sentences = np.array(sentences[0:training_size])
    testing_sentences = np.array(sentences[training_size:])

    training_labels = np.array(labels[0:training_size])
    testing_labels = np.array(labels[training_size:])

    model = AmbiguityDetector()
    model.setup(0.25, Hyperparameters(0.10, 50, 50), vocab_size,
                embedding_dim, max_length, training_sentences)

    layerParameters = [
        LayerParameter(24, "relu")
    ]

    model.createModel(layerParameters)
    epochs, hist = model.trainModel(training_sentences, training_labels,
                                    testing_sentences,
                                    testing_labels)
    list_of_metrics_to_plot = model.listOfMetrics
    model.plotCurve(epochs, hist, list_of_metrics_to_plot)

    model.export()

    # features = {name: np.array(value) for name, value in test_df_norm.items()}
    # label = np.array(features.pop(labelName))
    #

    words = "former versace store clerk sues over secret 'black code' for minority shoppers"
    print(model.detect([words]))
