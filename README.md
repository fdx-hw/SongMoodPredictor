# SongMoodPredictor
SmallerDataset.csv consists of the initial and smaller dataset of songs that were used to train and test the models initially and LargerDataset.csv consists of the final and larger dataset of songs used to train and test the same models to observe the changes that occur in the results of these models.
The first section for the script used for generating the datasets can be found in Datasetgeneration.py. After the datasets are generated, we start our implementation process in final.ipynb where-
The first half of the final Jupyter notebook consists of models that were experimented with on the smaller dataset.
The second half of the final Jupyter Notebook consists of models that were trained and tested on the larger dataset.
The final part of the notebook includes using the best models obtained from our experiments on both datasets to predict the mood of the user, which is then used to generate a playlist of songs on that mood
