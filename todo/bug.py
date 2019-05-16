import os
import pickle
import numpy as np
import sys
# from smart_bug import Statement_Norm, Statement_Vec
# from smart_bug import Statement_Vec
from gensim.models.fasttext import FastText
from scipy.spatial.distance import pdist, cdist, squareform
from scipy.spatial import distance

BUG_FASTTEXT_MODEL = FastText.load("../statement_level/Model/FastText/fasttext_model")
print("Statement FastText Model loaded")

sys.path.append('../statement_level/Normalize')
from statement_normalization import Statement_Norm
sys.path.append('../statement_level/Vectorize/')
from statement_vectorize import Statement_Vec

def save_to_file(messagecontent):
    if not os.path.exists('./USERINPUT'):
        os.makedirs('./USERINPUT')
    with open('./USERINPUT/current.sol', 'w') as handle:
        handle.write(messagecontent)
        
def parser():
    # cmd = "java -classpath ./State_Parse/antlr4.jar:./State_Parse/target/ Tokenize ./Bug/current.sol ./Bug/"
    cmd = "java -classpath ../statement_level/Parse/antlr4.jar:../statement_level/Parse/target/ Tokenize ./USERINPUT/current.sol ./STATEMENT_RESULT/"
    os.system(cmd)
    os.rename('./STATEMENT_RESULT/parse_result', './STATEMENT_RESULT/statement_parse_result')
    pass

def normalizer():
    # print("entering normalizer...")
    sn = Statement_Norm("./STATEMENT_RESULT/")    
    return sn.linespan_list, sn.statement_tokens_norm
    pass

def vectorizer(norm_result):
    # print("entering vectorizer...")
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


def get_bugs_cat(user_in, display_these_bugs, bug_types):

    save_to_file(user_in)
    parser()
    norm_result = normalizer()
    # print("norm result")
    # print(norm_result)
    vec_result = vectorizer(norm_result)
    # print("vec_result")
    # print(type(vec_result), vec_result.shape)
    embedding_type = 'sum_fasttext'

    top_bug = np.empty((0,3))
    
    for bind, b in enumerate(display_these_bugs):

        bug_database_path = "../statement_level/Embedding/"
        vulnerable_fasttext_embedding = np.load(bug_database_path + b+'.npy')

        similarity_list = []
        for v in vulnerable_fasttext_embedding:
            similarity_array = get_similarity(v, vec_result)
            similarity_list.append(similarity_array)

        similarity_matrix = np.vstack(similarity_list)
        # print(b)
        # print("similarity matrix", type(similarity_matrix), similarity_matrix.shape)
        try:
            top_bug_idx = np.where(similarity_matrix>0.85)
            if np.max(similarity_matrix) > 0.85:
                for ct, k in enumerate(top_bug_idx[1]):
                    # get the line index index 
                    tmp = map(int, norm_result[0][k])
                    tmp.append(bug_types.index(b))
                    tmp = np.array(tmp)
                    top_bug = np.append(top_bug,tmp.reshape(1,3),axis=0)
                    # print(top_bug)
                    if (ct==3):break
        except:
            continue
    # print(top_bug.shape)
    return top_bug.tolist()


def main():
    user_in = open('./test.sol', 'r').read()

    bug_types = ['Overflow_bug', 'Honeypot_bug', 'OwnerCVE_bug', 'PRNG_bug', 'blockhash_bug','contract_not_refund','international_scam','public_moves','re_entrancy']
    top_bug = get_bugs_cat(user_in, bug_types, bug_types)
    # top_result = get_bugs(user_in)
    # print("top results:")
    # print(top_result)

    print("top bugs:")
    print(top_bug)
    pass

if __name__ == '__main__':
    main()


