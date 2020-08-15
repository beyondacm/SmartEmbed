# SmartEmbed Web Tool

SmartEmbed is a web service tool for clone detection & bug detection for smart contracts. 

Our full research paper: Checking smart contracts with structural code embeddings has been published on TSE (IEEE Transactions on Software Engineering), we describe the details for clone detection and bug detection in smart contracrs using SmartEmbed, for more details please refer to our research paper:   
https://ieeexplore.ieee.org/document/8979435  
https://arxiv.org/abs/2001.07125

SmartEmbed has been published as a tool demo by on [ICSME-2019](https://icsme2019.github.io/), for details of the implementation please refer to our paper:  
https://arxiv.org/abs/1908.08615

Our work: When Deep Learning Meets Smart Contracts has been accepted by ASE-2020 Student Research Competition track, for more details please refer to our paper:  
http://arxiv.org/abs/2008.04093  


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


*When Deep Learning Meets Smart Contracts*
> @article{gao2020deep,  
  title={When Deep Learning Meets Smart Contracts},  
  author={Gao, Zhipeng},   
  journal={arXiv preprint arXiv:2008.04093},  
  year={2020}    
}



## Introduction

This folder contains the code for the SmartEmbed web tool. There are a few important subfolders and files as follows.

- **templates** - contains the frontend html files
- **static** - contains the *css* files and *js* scripts
- **app[dot]py** - main flask file, see below for usage.
- **similarity[dot]py** and **smart_embed[dot]py** - Contains the backend codes for clone detection. 
- **bug[dot]py** and **smart_bug[dot]py** - Contains the backend codes for bug detection. 

## Pretraied Models

We have released the pre-trained model as described in the paper. You can use the following command to download our pretrained model:

```shell
pip install gdown
gdown https://drive.google.com/uc?id=1-LKJTZakqd8ntKzqVNtQZUgdZnFoYtpK
unzip Contract_Embedding.zip
mv Embedding SmartEmbed/contract_level/
```  


```shell
pip install gdown  
gdown https://drive.google.com/uc?id=1lbaQVtZbNuEEjHIWVnwLqGvILxNWwtZW  
unzip Contract_Model.zip  
mv Model SmartEmbed/contract_level/
```

```shell
pip install gdown  
gdown https://drive.google.com/uc?id=18GiDgSwoRjPC25d2Vp15oi_xH2NivyXH  
unzip Statement_Model.zip 
mv Model SmartEmbed/statement_level/  
```


## Usage

1. Install requirements.txt with ```pip install -r requirements.txt```.
2. Clone this project to your local ```git clone https://github.com/beyondacm/SmartEmbed.git```.
3. Please download the pretrained model with the aforementioned shell scripts. 
4. Run the command ```python SmartEmbed/todo/app.py``` . This will initialize the web tool at ```localhost:9000```, as illustrated below.

![image](https://drive.google.com/uc?export=view&id=1k87ZXIMvkGcToYUjAh1Mn0CyBkzmQoC4)

5. Paste the smart contract on to the text area and hit *Submit*.
6. Clone detection results will be displayed as follows.
![image](https://drive.google.com/uc?export=view&id=1iNfJdYrjdByUJqB5DRsCg-IaaYmsL5gK)
7. Bug detection results will be displayed as follows.
![image](https://drive.google.com/uc?export=view&id=1Mg9UOT99lql1XGBI_XQiVDrugbxbNmxn)

## Contact
zhipeng.gao@monash.edu  
vinojmh@smu.edu.sg  
Discussions, suggestions and questions are welcome!


​	
​	
​	

