# DeepTalk
A primitive chatbot powered by deep learning and trained on data from Reddit. Built on TensorFlow v1.4.0 and Python v3.5.1.


## Get Started

- **Install [TensorFlow](http://www.tensorflow.org/)** for Python 3. To run a pretrained model, the CPU-only installation should suffice. If you want to train your own models, you'll need the GPU installation of TensorFlow (and a powerful CUDA-compatible GPU).

- Clone this project to your computer.

### Run pre-trained model

- **[Download Data](https://drive.google.com/uc?id=1rRRY-y1KdVk4UB5qhu7BjQHtfadIOmMk&export=download)** (2.3 GB). The zip file extracts into a folder named "reddit". Place that folder into the "models" directory of this project.

- **Run the chatbot**. Open a terminal session and run `python3 chatbot.py`. Warning: this pre-trained model was trained on a diverse set of frequently off-color Reddit comments. It can (and eventually will) say things that are offensive, disturbing, bizarre or sexually explicit. It may insult minorities, it may call you names, it may accuse you of being a pedophile, it may try to seduce you. Please don't use the chatbot if these possibilities would distress you!


### Get training data

If you'd like to train your own model, you'll need training data. There are a few options here.

- **Use pre-formatted Reddit training data.** This is what the pre-trained model was trained on.

  [Download the training data](https://drive.google.com/uc?id=1s77S7COjrb3lOnfqvXYfn7sW_x5U1_l9&export=download) (2.1 GB). Unzip the monolithic zip file. You'll be left with a folder named "reddit" containing 34 files named "output 1.bz2", "output 2.bz2" etc. Do not extract those individual bzip2 files. Instead, place the whole "reddit" folder that contains those files inside the `data` folder of the repo. The first time you run `train.py` on this data, it will convert the raw data into numpy tensors, compress them and save them back to disk, which will create files named "data0.npz" through "data34.npz" (as well as a "sizes.pkl" file and a "vocab.pkl" file). This will fill another ~5 GB of disk space, and will take about half an hour to finish.

Once you have training data in hand (and located in a subdirectory of the `data` directory):

### Train your own model

- **Train.** Use `train.py` to train the model. The default hyperparameters are the best that I've found, and are what I used to train the pre-trained model for a couple of months. These hyperparameters will just about fill the memory of a GTX 1080 Ti GPU (11 GB of VRAM), so if you have a smaller GPU, you will need to adjust them accordingly (for example, set --num_blocks to 2).

  Training can be interrupted with crtl-c at any time, and will immediately save the model when interrupted. Training can be resumed on a saved model and will automatically carry on from where it was interrupted.

## Acknowledgements

The project is based on [Chtbot RNN](https://github.com/pender/chatbot-rnn), Andrej Karpathy's [char-rnn](https://github.com/karpathy/char-rnn) repo, and Sherjil Ozair's [TensorFlow port](https://github.com/sherjilozair/char-rnn-tensorflow).
