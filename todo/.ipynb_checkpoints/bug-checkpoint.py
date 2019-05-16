import os
import pickle
import numpy as np
from smart_bug import Statement_Norm, Statement_Vec
from gensim.models.fasttext import FastText
from scipy.spatial.distance import pdist, cdist, squareform
from scipy.spatial import distance

BUG_FASTTEXT_MODEL = FastText.load("./Bug/FastText/fasttext_model")
print("Bug FastText Model loaded")

with open("./Bug/bug_statements_embeddings.pkl", "r") as handle:
    BUG_EMBEDDING_MATRIX = pickle.load(handle)
print("BUG_EMBEDDING_MATRIX loaded")

BUG_EMBEDDINGS_PATH = "./Bug/"
with open(BUG_EMBEDDINGS_PATH + 'sorted_bug_statements_embeddings.pkl', 'rb') as sce:
    sorted_bug_embeddings = pickle.load(sce)
print("sorted_bug_embeddings loaded")


def save_to_file(messagecontent):
    if not os.path.exists('./Bug'):
        os.makedirs('./Bug')
    with open('./Bug/current.sol', 'w') as handle:
        handle.write(messagecontent)
        
def parser():
    cmd = "java -classpath ./State_Parse/antlr4.jar:./State_Parse/target/ Tokenize ./Bug/current.sol ./Bug/"
    os.system(cmd) 
    os.rename('./Bug/parse_result', './Bug/statement_tokens')
    pass

def normalizer():
    print("entering normalizer...")
    sn = Statement_Norm("./Bug/")    
    return sn.linespan_list, sn.statement_tokens_norm
    pass

def vectorizer(norm_result):
    print("entering vectorizer...")
    sv = Statement_Vec(norm_result, BUG_FASTTEXT_MODEL)
    return sv.vector
    pass

def get_similarity(v, e):
    numerator = distance.cdist(v.reshape(1, 150), e, 'euclidean')
    denominator = np.linalg.norm(e, axis=1) + np.linalg.norm(v)
    return 1 - np.divide(numerator, denominator)

def get_vulnerable_matrix(embedding_type):
    vulnerable_statement_list = []
    vulnerable_embedding_list = []
    for statement, embeddings in BUG_EMBEDDING_MATRIX.items():
        vulnerable_embedding_list.append(embeddings[embedding_type])
        vulnerable_statement_list.append(statement)
    vulnerable_embedding_matrix = np.vstack(vulnerable_embedding_list)
    return vulnerable_statement_list, vulnerable_embedding_matrix


def get_bugs(user_in):
    save_to_file(user_in)
    parser()
    norm_result = normalizer()
    vec_result = vectorizer(norm_result)
    embedding_type = 'sum_fasttext'
    vulnerable_fasttext_embedding = np.load("all_bugs.npy")
    
    similarity_list = []
    for v in vulnerable_fasttext_embedding:
        similarity_array = get_similarity(v, vec_result)
        similarity_list.append(similarity_array)
    similarity_matrix = np.vstack(similarity_list)
    top_bug_idx = np.where(similarity_matrix>0.7)
    top_bug = np.empty((0,2))
    if np.max(similarity_matrix)>0.8:
        for ct,k in enumerate(top_bug_idx[1]):
            top_bug = np.append(top_bug,np.array(map(int,norm_result[0][k])).reshape(1,2),axis=0)
            if (ct==6):break
    print(top_bug.shape,top_bug[0])
    return top_bug.tolist()

def get_bugs_cat(user_in,display_these_bugs,bug_types):
    save_to_file(user_in)
    parser()
    norm_result = normalizer()
    vec_result = vectorizer(norm_result)
    embedding_type = 'sum_fasttext'

    top_bug = np.empty((0,3))
    
    for bind,b in enumerate(display_these_bugs):
        vulnerable_fasttext_embedding = np.load(b+'.npy')

        similarity_list = []
        for v in vulnerable_fasttext_embedding:
            similarity_array = get_similarity(v, vec_result)
            similarity_list.append(similarity_array)
        similarity_matrix = np.vstack(similarity_list)
        try:
            top_bug_idx = np.where(similarity_matrix>0.7)
            if np.max(similarity_matrix)>0.8:
                for ct,k in enumerate(top_bug_idx[1]):
                    tmp = map(int,norm_result[0][k])
                    tmp.append(bug_types.index(b))
                    tmp = np.array(tmp)
                    top_bug = np.append(top_bug,tmp.reshape(1,3),axis=0)
                    if (ct==3):break
        except:
            continue
        print(top_bug.shape)
        
    return top_bug.tolist()


def main():
    user_in = open('./test.sol', 'r').read()
    top_result = get_bugs(user_in)
#     print(top_result)
    pass

if __name__ == '__main__':
    main()



