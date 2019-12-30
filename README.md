# quantcast-challenge
## Overview
I scraped the lyrics data from www.lyrics.com for various artists and trained LSTM model on the preprocessed text to fill out the sentences with missing endings. 
### Web scraping
Code available here: https://github.com/KacperKubara/quantcast-challenge/blob/master/data_scraping.py
For webscraping, I used bs4, requests, and urlib.

### Data Preprocessing
Code available here: https://github.com/KacperKubara/quantcast-challenge/blob/master/preprocessor.py
Text had to be preprocessed, i.e. I removed empty lines, and converted the text to lowercase. Before building the model, the text is vectorized.

### LSTM
Code available here: https://github.com/KacperKubara/quantcast-challenge/blob/master/prediction.py
I have reused the Keras tutorial and repurposed the code for the sentence prediction task. I had to change the prediction pipeline as well as part of preprocessing and adjust few parameters of the model.

## Installation
To reproduce the results, you need to install all packages from environment.yml with a following command (using conda): 
`conda env create -f environment.yml `

## Results
First 4 sentences are generated based on the Coldplay lyrics (10 epochs). The last 4 were trained on Taylor Swift Lyrics (20 epochs). Results are available here:
[Text prediction](https://github.com/KacperKubara/quantcast-challenge/blob/master/results/text_prediction.txt)

The following figure shows the Loss of the model during the training on Taylor Swift Lyrics for 20 epochs:
[Loss diagram](https://github.com/KacperKubara/quantcast-challenge/blob/master/loss.png?raw=true)

## What could be improved
1) I have noticed that the lyrics are sometimes duplicated which might be harmful during the training of the model (it can overfit). The duplicated lines should be removed but not necessarily, but on the other hand there might be several exact lines in the whole dataset which are not duplicated (e.g. oh-la-la-la). I didn't have enough time to fix this issue.
2) The datasets were quite small because the artists don't have that much lyrics. Might the dataset would be better if lyrics from different artists would be combined?
3) LSTM with more layers could result in a better accuracy. Maybe adding dropout layers would be helpful to prevent the model from overfitting?
4) Making the code more generic: global parameters, creating a pipeline to accommodate scraping, preprocessing data, training the model, and making predicitons. This, however, is very time consuming and I didn't have time to do that.

## References
1) Building LSTM - https://keras.io/examples/lstm_text_generation/
2) Theory behind RNNs - http://karpathy.github.io/2015/05/21/rnn-effectiveness/
3) Web Scraping - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
