# EEG Data Analysis

Analysis is based on a [EEG Database Data Set](https://archive.ics.uci.edu/ml/datasets/eeg+database) originally created for [Kaggle](https://www.kaggle.com/ruslankl/eeg-data-analysis/notebook). It contains [EEG (Electroencephalography)](https://en.wikipedia.org/wiki/Electroencephalography) data for two groups - Alcoholics and Control Group. 

Amount of subjects in each group is 8. The 64 electrodes were placed on subject's scalps to measure theelectrical activity of the brain. The response values were sampled at 256 Hz (3.9-msec epoch) for 1 second. Each subject was exposed to either a single stimulus (S1) or to two stimuli (S1 and S2) which were pictures of objects chosen from the [1980 Snodgrass and Vanderwart picture set](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.294.1979&rep=rep1&type=pdf). When two stimuli were shown, they were presented in either a matched condition where S1 was identical to S2 or in a non-matched condition where S1 differed from S2.

The purpose of my analysis is going to be to find out if there is a difference in response values for different stimuli between control and alcoholic group. And if so, in what brain regions this happens? 
