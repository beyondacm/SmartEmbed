import os
import pickle
import numpy as np
from config import Config
from gensim.models.fasttext import FastText
from scipy.spatial.distance import pdist, cdist, squareform

import sys
import os.path
sys.path.append('../contract_level/Normalize/')
from contract_normalization import Contract_Norm
sys.path.append('../contract_level/Vectorize/')
from contract_vectorize import Contract_Vec
sys.path.append('../contract_level/Crawl')
from contract_crawl import Contract_Detail

class Clone_Detect(object):

    def __init__(self):
        self.config = Config()
        self.USERINPUT = "./USERINPUT/"
        self.fasttext_model = self.get_fasttext_model()
        self.contract_embedding_matrix = self.get_contract_embedding_matrix()
        self.sorted_contract_embeddings = self.get_sorted_contract_embeddings()
    
    def get_fasttext_model(self):
        '''
            load fasttext model
        '''        
        FASTTEXT_MODEL = FastText.load(self.config.contract_model)
        print("contract fasttext_model loaded")
        return FASTTEXT_MODEL
    
    def get_contract_embedding_matrix(self):
        '''    
            load contract_embedding_matrix
        '''
        with open(self.config.contract_embedding_matrix, "r") as handle:
            CONTRACT_EMBEDDING_MATRIX = pickle.load(handle)
            print("CONTRACT_EMBEDDING_MATRIX loaded")
        return CONTRACT_EMBEDDING_MATRIX

    def get_sorted_contract_embeddings(self):
        '''
            load sorted_contract_embeddings
        '''
        with open(self.config.sorted_contract_embeddings, 'rb') as sce:
            sorted_contract_embeddings = pickle.load(sce)
            print("sorted_contract_embeddings loaded")
        return sorted_contract_embeddings

    def save_to_file(self, user_in):
        '''
            save user input into file
        '''
        if not os.path.exists( self.USERINPUT ):
            os.makedirs(self.USERINPUT)
        with open( self.USERINPUT + 'user_input.sol', 'w') as handle:
            handle.write(user_in)
    
    def parser(self):
        '''
            parse the user_input.sol into AST 
        '''
        # cmd = "java -classpath ./Parse/antlr4.jar:./Parse/target/ Tokenize ./Similarity/current.sol ./Similarity/"
        cmd = "java -classpath ../contract_level/Parse/antlr4.jar:../contract_level/Parse/target/ \
                    Tokenize ./USERINPUT/user_input.sol ./CONTRACT_RESULT/"
        os.system(cmd) 

    def normalizer(self):
        '''
            normalize 
        '''
        # print("entering normalizer...")
        cn = Contract_Norm("./CONTRACT_RESULT/")    
        return cn.line_span, cn.normalized_tokens

    def vectorizer(self, norm_result):
        # print("entering vectorizer...")
        cv = Contract_Vec(norm_result, self.fasttext_model)
        return cv.vector

    def similarity_matrix(self, current_vector, embedding_matrix):
        numerator = cdist(current_vector, embedding_matrix, 'euclidean')
        vec_norm = np.linalg.norm(embedding_matrix, axis=1)
        vec_tile = np.tile(vec_norm, (current_vector.shape[0], 1))
        emb_norm = np.linalg.norm(current_vector, axis=1)
        emb_tile = np.tile(emb_norm, (embedding_matrix.shape[0], 1)).transpose() 
        denominator = np.add(vec_tile, emb_tile)
        similarity_matrix = 1 - np.divide(numerator, denominator)
        return similarity_matrix

    def get_top(self, contract_vector, N=5):
        # print("entering get_top ...")
        sm = self.similarity_matrix(contract_vector, self.contract_embedding_matrix)
        score = np.copy(sm) 
        index = np.copy(sm)
        score.sort()
        topN_score = score[0][-N:][::-1]
        topN_index = index.argsort()[0][-N:][::-1]
        
        top_result = []
        for score, index in zip(topN_score, topN_index):
            url = self.sorted_contract_embeddings[index][0].split('@')[0]
            url_full = 'https://etherscan.io/address/' + url + '#code'
            contract_detailer = Contract_Detail(url)
            try:
                source_code = str(contract_detailer.get_source_code()[0])
            except Exception as e:
                source_code = "Sorry, Source code unavailable here. Please go to the link under contract URL!"
            top_result.append((url_full, score, source_code))
        return top_result


    def get_similarity(self, user_in):
        self.save_to_file(user_in)
        self.parser()
        norm_result = self.normalizer()
        vec_result = self.vectorizer(norm_result)
        top_result = self.get_top(vec_result, N=5)
        return top_result   
    

def main():
    # Test Clone_Detect()
    cd = Clone_Detect()
    user_in = open('./test.sol', 'r').read()
    top_result = cd.get_similarity(user_in)
    print(top_result)
    pass

if __name__ == '__main__':
    main()



