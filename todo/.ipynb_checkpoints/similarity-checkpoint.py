import os
import pickle
import numpy as np
from smart_embed import Contract_Norm, Contract_Vec, Contract_Detail
from gensim.models.fasttext import FastText
from scipy.spatial.distance import pdist, cdist, squareform

# FASTTEXT_MODEL = FastText.load("/home/vinoj/Deep_code/work_space/Contract_Modeling/FastText/fasttext_model")
# FASTTEXT_MODEL = FastText.load("/media/vinoj/Seagate/vinoj/Deep_code/work_space/Contract_Modeling/FastText/fasttext_model")
FASTTEXT_MODEL = FastText.load("/media/lingxiao/Seagate Data/vinoj/Deep_code/work_space/Contract_Modeling/FastText/fasttext_model")

print("FastText Model loaded")

with open("./Similarity/contract_embedding_matrix.pkl", "r") as handle:
    CONTRACT_EMBEDDING_MATRIX = pickle.load(handle)
print("CONTRACT_EMBEDDING_MATRIX loaded")

# CONTRACT_EMBEDDINGS_PATH = "/home/vinoj/Deep_code/work_space/Contract_Embedding/"
CONTRACT_EMBEDDINGS_PATH = "/media/lingxiao/Seagate Data/vinoj/Deep_code/work_space/Contract_Embedding/"
with open(CONTRACT_EMBEDDINGS_PATH + 'sorted_contract_embeddings.pkl', 'rb') as sce:
    sorted_contract_embeddings = pickle.load(sce)
print("sorted_contract_embeddings loaded")


def save_to_file(messagecontent):
    if not os.path.exists('./Similarity'):
        os.makedirs('./Similarity')
    with open('./Similarity/current.sol', 'w') as handle:
        handle.write(messagecontent)
        
def parser():
    cmd = "java -classpath ./Parse/antlr4.jar:./Parse/target/ Tokenize ./Similarity/current.sol ./Similarity/"
    os.system(cmd) 
    pass

def normalizer():
    print("entering normalizer...")
    cn = Contract_Norm("./Similarity/")    
    return cn.line_span, cn.normalized_tokens
    pass

def vectorizer(norm_result):
    print("entering vectorizer...")
    cv = Contract_Vec(norm_result, FASTTEXT_MODEL)
    return cv.vector
    pass

def similarity_matrix(current_vector, embedding_matrix):
    numerator = cdist(current_vector, embedding_matrix, 'euclidean')
    vec_norm = np.linalg.norm(embedding_matrix, axis=1)
    vec_tile = np.tile(vec_norm, (current_vector.shape[0], 1))
    emb_norm = np.linalg.norm(current_vector, axis=1)
    emb_tile = np.tile(emb_norm, (embedding_matrix.shape[0], 1)).transpose() 
    denominator = np.add(vec_tile, emb_tile)
    similarity_matrix = 1 - np.divide(numerator, denominator)
    return similarity_matrix

def get_top(contract_vector, embedding_matrix=CONTRACT_EMBEDDING_MATRIX, N=5):
    print("entering get_top ...")
    sm = similarity_matrix(contract_vector, embedding_matrix) 
    score = np.copy(sm) 
    index = np.copy(sm)
    score.sort()
    topN_score = score[0][-N:][::-1]
    topN_index = index.argsort()[0][-N:][::-1]
    
    top_result = []
    for score, index in zip(topN_score, topN_index):
        url = sorted_contract_embeddings[index][0].split('@')[0]
        url_full = 'https://etherscan.io/address/' + url + '#code'
        contract_detailer = Contract_Detail(url)
        try:
            print(contract_detailer.get_source_code())
            source_code = str(contract_detailer.get_source_code()[0])
        except Exception as e:
            print(e)
            print(url_full)
            source_code = "Sorry, Source code unavailable here. Please go to the link under contract URL!"
        top_result.append((url_full, score, source_code))
    return top_result

def get_similarity(user_in):
    save_to_file(user_in)
    parser()
    norm_result = normalizer()
    vec_result = vectorizer(norm_result)
    top_result = get_top(vec_result, embedding_matrix=CONTRACT_EMBEDDING_MATRIX, N=5)
    return top_result