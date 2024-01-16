# K-NET-LSTM-PGA (Full title ommitted to forestall erroneous plagiarism Detection by crawlers]
Code for Seismological Research Letters Submission SRL-D-23-00427

## Data
Data is sourced from the Japan National Research Institute for Earth Science and Disaster Resilience (NIED) website. Download the data from this website - https://www.kyoshin.bosai.go.jp/. Specifically we utilize Kyoshin Network (K-NET), which constitutes a nationwide network of strong-motion seismographs, comprising approximately 1,000 observation stations that are uniformly distributed across Japan at 20-kilometer intervals. Our data set used the version of the data accessed on May 14, 2023. In compressed format, the size of the data set is 2.8GB.

**The path of the downloaded data set is required for data preprocessing, training and evaluation.**


## Instructions
### Preprocessing
The script used to preprocess seismograms is titled `preprocess.py`. Script includes detailed instructions of defining path to data in comments.

### Training and Evaluation
The script used to train and evaluate experiments is titled `train_eval.py`. Here too, the script includes detailed instructions in comments.
