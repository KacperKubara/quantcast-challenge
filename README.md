# quantcast-challenge
## Overview
I scraped the lyrics data from www.lyrics.com for various artists and trained LSTM model on the preprocessed text to fill out the sentences with missing endings.

## Installation
To reproduce the results, you need to install all packages from environment.yml with a following command (using conda): 
`conda env create -f environment.yml `
## Results
First 4 sentences are generated based on the Coldplay lyrics (10 epochs). The last 4 were trained on Taylor Swift Lyrics (20 epochs)
The following figure shows the Loss of the model during the training on Taylor Swift Lyrics

## References
1) Building LSTM - https://keras.io/examples/lstm_text_generation/
2) Theory behind RNNs - http://karpathy.github.io/2015/05/21/rnn-effectiveness/
3) Web Scraping - https://www.crummy.com/software/BeautifulSoup/bs4/doc/
