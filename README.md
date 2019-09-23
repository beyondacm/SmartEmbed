# SmartEmbed Web Tool

SmartEmbed is a web service tool for clone detection & bug detection for smart contracts. 
SmartEmbed has been published as a tool demo by on [ICSME-2019](https://icsme2019.github.io/), for details of the implementation please refer to our paper:
https://arxiv.org/abs/1908.08615

We have published our tool through the following url : 

[http://www.smartembed.net/](http://www.smartembed.net/) 

There is a tutorial video introducing how to use SmartEmbed on Youtube: 

https://youtu.be/o9ylyOpYFq8

Source data can be downloaded from : 

https://drive.google.com/file/d/13iTTpt7gFd9wEW35C2fX4pVT7cVlHgxi/view?usp=sharing

## Introduction

This folder contains the code for the SmartEmbed web tool. There are a few important subfolders and files as follows.

- **templates** - contains the frontend html files
- **static** - contains the *css* files and *js* scripts
- **app[dot]py** - main flask file, see below for usage.
- **similarity[dot]py** and **smart_embed[dot]py** - Contains the backend codes for clone detection. 
- **bug[dot]py** and **smart_bug[dot]py** - Contains the backend codes for bug detection. 

## Usage

1. Install requirements.txt with ```pip install -r requirements.txt```.
2. Please update the ```FASTTEXT_MODEL``` and ```CONTRACT_EMBEDDINGS_PATH``` to the corresponding ```work_space``` directory in the ```similarity.py``` lines ```10``` and ```19``` respectively.
3. Run the command ```python app.py``` . This will initialize the web tool at ```localhost:9700```, as illustrated below.

![image](https://drive.google.com/uc?export=view&id=1k87ZXIMvkGcToYUjAh1Mn0CyBkzmQoC4)

4. Paste the smart contract on to the text area and hit *Submit*.
5. Clone detection results will be displayed as follows.
![image](https://drive.google.com/uc?export=view&id=1iNfJdYrjdByUJqB5DRsCg-IaaYmsL5gK)
6. Bug detection results will be displayed as follows.
![image](https://drive.google.com/uc?export=view&id=1Mg9UOT99lql1XGBI_XQiVDrugbxbNmxn)

## Contact

vinojmh@smu.edu.sg  
Discussions, suggestions and questions are welcome!


​	
​	
​	






