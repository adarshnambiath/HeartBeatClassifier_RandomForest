# Heart Beat Classifier using RandomForest

There is not much work here while training the forest, this is mainly just an experiment on the utility of Random Forest.

The features this forest uses are the amplitudes of the raw ecg waveform, so by the end when feature importance is plotted, it shows what part of the waveform is most crucial while splitting nodes.

There is a very high accuracy reported by the model, which is attributed to the convenience of the mitbih dataset used.

Another assumption taken to use the raw waveforms in this model is that all the waveformed are "centered" around the R peak of the previous PQRST complex.

Datasets used: mitbih ecg dataset, I found on kaggle, with 187 amplitude values and one label in each record, already split into training and testing sets.

