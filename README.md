# SmartEmbed Web Tool

SmartEmbed is a web service tool for clone detection & bug detection for smart contracts. 

Our full research paper: Checking smart contracts with structural code embeddings has been published on TSE (IEEE Transactions on Software Engineering), we describe the details for clone detection and bug detection in smart contracrs using SmartEmbed, for more details please refer to our research paper:   
https://ieeexplore.ieee.org/document/8979435  
https://arxiv.org/abs/2001.07125

SmartEmbed has been published as a tool demo by on [ICSME-2019](https://icsme2019.github.io/), for details of the implementation please refer to our paper:  
https://arxiv.org/abs/1908.08615

We have published our tool through the following url:   
[http://www.smartembed.tools/](http://www.smartembed.tools/)   


There is a tutorial video introducing how to use SmartEmbed on Youtube:  
https://youtu.be/o9ylyOpYFq8

Source data can be downloaded from:  
https://drive.google.com/file/d/13iTTpt7gFd9wEW35C2fX4pVT7cVlHgxi/view?usp=sharing

Please cite our work if you found our work is helpful:  
*Checking smart contracts with structural code embeddings:*  
> @article{gao2020checking,    
  title={Checking Smart Contracts with Structural Code Embedding},  
  author={Gao, Zhipeng and Jiang, Lingxiao and Xia, Xin and Lo, David and Grundy, John},  
  journal={IEEE Transactions on Software Engineering},
  year={2020},  
  publisher={IEEE}  
}  


*Smartembed: A tool for clone and bug detection in smart contracts through structural code embedding:*  
> @inproceedings{gao2019smartembed,  
  title={Smartembed: A tool for clone and bug detection in smart contracts through structural code embedding},  
  author={Gao, Zhipeng and Jayasundara, Vinoj and Jiang, Lingxiao and Xia, Xin and Lo, David and Grundy, John},  
  booktitle={2019 IEEE International Conference on Software Maintenance and Evolution (ICSME)},  
  pages={394--397},  
  year={2019},  
  organization={IEEE}  
}




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
zhipeng.gao@monash.edu  
vinojmh@smu.edu.sg  
Discussions, suggestions and questions are welcome!


​	
​	
​	






