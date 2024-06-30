# 💠 BLU - Polish Chatbot

![GitHub last commit](https://img.shields.io/github/last-commit/adpaczek/chatbot)

### Description

BLU is a chatbot that generates text in Polish based on the Transformer model and trained using data from movie subtitles collected through web scraping.

<img src="https://github.com/adpaczek/chatbot/assets/83600967/6788659c-6167-4213-b0ab-254e093155a2" width="390" height="400">

### Dataset
Polish is one of the most complicated languages ​​in the world. Hence, there are not many training datasets for language models. Therefore, it was decided to create such a dataset, from files with movie subtitles in Polish, which were collected using the [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) script. Conversation pairs were created from SRT files.

| Version | Number of conversation pairs |
| ----------- | ----------- |
| I| 197 212 |
| II | 283 389 |
| III | 1 008 839 (*) |

(*) In version III, some conversation pairs are duplicated.
  
Based on the self-created language corpus, several versions of models were trained, which were later used to build a chatbot. 

### Model
The Transformer model was used, its implementation is based on tutorials linked in the bibliography. 

Different versions of hyperparameters were tested and finally 3 versions of models were trained - based on 3 versions of data sets.

### Results
For logical correctness testing, 384 different messages were prepared and delivered to the chatbot with different versions of the model loaded. The test set included both questions and declarative sentences. The topics of the test set were diverse and included a range of statements that could be used during a classic, everyday conversation.

Results of testing the logical correctness of the BLU response:

| Model | Number of correct, logical answers | Level of logical correctness |
| ----------- | ----------- | ----------- |
| I | 156 | 40,63% |
| II | 158 | 41,15% |
| III | 187 | 48,7% |

### Installation

### Bibliography
* [Vaswani A. i in., Attention Is All You Need, 12.06.2017](https://arxiv.org/abs/1706.03762)
* [Li B. M., A Transformer Chatbot Tutorial with TensorFlow 2.0, 23.05.2019](https://blog.tensorflow.org/2019/05/transformer-chatbot-tutorial-with-tensorflow-2.html)
* [Neural Machine translation with a Transformer and Keras](https://www.tensorflow.org/text/tutorials/transformer)
