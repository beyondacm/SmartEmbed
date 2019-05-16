# -*- coding:utf-8 -*-
import pickle
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import cdist
from scipy.spatial.distance import squareform

class Embeddings():

    def __init__(self):
        # self.CONTRACT_EMBEDDINGS_PATH = "/home/zhipeng/work_space/Contract_Embedding/"
        self.contract_embeddings = self.load_contract_embeddings()
        self.contract_embedding_matrix = self.get_contract_embedding_matrix()
        # self.contract_embedding_matrix = self.load_contract_embedding_matrix()
        pass
    
    def load_contract_embeddings(self):
        print("loading contract embeddings...")
        with open('./sorted_contract_embeddings.pkl', 'rb') as sce:
            contract_embeddings = pickle.load(sce)

        return contract_embeddings
        pass
    

    def get_contract_embedding_matrix(self):
        embedding_list = []
        for e in self.contract_embeddings:
            embedding_array = e[1]['sum_fasttext']
            embedding_list.append(embedding_array)
        embedding_matrix = np.vstack(embedding_list)

        with open('./contract_embedding_matrix.pkl', 'wb') as handle:
            pickle.dump(embedding_matrix, handle)
        return embedding_matrix


def main():
    eb = Embeddings()
    # print(type(eb.contract_embeddings))
    # print(type(eb.contract_embedding_matrix))
    print(eb.contract_embedding_matrix.shape)
    pass

if __name__ == '__main__':
    main()



