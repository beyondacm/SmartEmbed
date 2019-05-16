import os
import pickle
import numpy as np
from config import Config
from gensim.models.fasttext import FastText
from scipy.spatial.distance import pdist, cdist, squareform
from scipy.spatial import distance

import sys 
import os.path 

sys.path.append('../statement_level/Normalize')
from statement_normalization import Statement_Norm
sys.path.append('../statement_level/Vectorizer/')
from statement_vectorize import Statement_Vec

class Contract_Validate(object):

    def __init__(self):

        self.config = Config()
        self.USERINPUT = "./USERINPUT/"
        self.STATEMENT_RESULT = "./STATEMENT_RESULT/"
        if not os.path.exists( self.USERINPUT ):
            os.makedirs(self.USERINPUT)
        if not os.path.exists( self.STATEMENT_RESULT ):
            os.makedirs(self.STATEMENT_RESULT)
        
        self.fasttext_model = self.get_fasttext_model()
        self.bug_database_statement_embeddings = self.get_bug_database_statement_embeddings()
        self.bug_embedding_matrix = self.get_bug_embedding_matrix()
        self.bug_info = self.get_bug_info()

    def get_bug_info(self):
        '''
        '''
        with open(self.config.bug_info) as bi:
            bug_info = pickle.load(bi)
        return bug_info

    def get_bug_database_statement_embeddings(self):
        '''
        '''
        with open(self.config.bug_database) as sbse: 
            bug_database_statement_embeddings = pickle.load(sbse)
            print("Bug Database loaded")
        return bug_database_statement_embeddings 
        pass
    
    def get_bug_embedding_matrix(self, embedding_type='sum_fasttext'):
        '''
        '''
        bug_embedding_lst = []
        for e in self.bug_database_statement_embeddings:
            bug_embedding_array = e[1][embedding_type]
            bug_embedding_lst.append(bug_embedding_array)
        bug_embedding_matrix = np.vstack(bug_embedding_lst)
        print("Bug Embedding Matrix loaded")
        return bug_embedding_matrix
        pass

    def get_fasttext_model(self):
        '''
        '''
        FASTTEXT_MODEL = FastText.load(self.config.statement_model)
        print("fasttext_model loaded")
        return FASTTEXT_MODEL
        
    def save_to_file(self, user_in):

        if not os.path.exists( self.USERINPUT ):
            os.makedirs(self.USERINPUT)
        with open( self.USERINPUT + 'user_input.sol', 'w') as handle:
            handle.write(user_in)

    def parser(self):
        '''
            parse the user_input.sol into AST 
        '''
        # cmd = "java -classpath ./Parse/antlr4.jar:./Parse/target/ Tokenize ./Similarity/current.sol ./Similarity/"
        cmd = "java -classpath ../statement_level/Parse/antlr4.jar:../statement_level/Parse/target/ \
                    Tokenize ./USERINPUT/user_input.sol ./STATEMENT_RESULT/"
        os.system(cmd) 

    def normalizer(self):
        '''
            normalize 
        '''
        # print("entering normalizer...")
        # result = []
        sn = Statement_Norm( self.STATEMENT_RESULT )    
        sn.store()
        print("normalized statement tokens saved")

    def indexer(self):
        '''
        '''
        linespan2statementtokens = {}
        statementtokens_path = self.STATEMENT_RESULT + "statement_normalized_tokens"
        if os.path.exists(statementtokens_path):
            with open(statementtokens_path, 'r') as st:
                for line in st:
                    linespan = line.split('\t')[0]
                    statementtokens = line.split('\t')[1]
                    linespan2statementtokens[linespan] = statementtokens
        return linespan2statementtokens

    def get_user_statement_embeddings(self, norm_result):
        '''
        '''
        sv = Statement_Vec(norm_result, self.fasttext_model)  
        return sv.sorted_statement_embeddings
        pass
    
    def get_user_embedding_matrix(self, user_statement_embeddings, embedding_type="sum_fasttext"):
        user_embedding_lst = []
        for e in user_statement_embeddings:
            user_embedding_array = e[1][embedding_type]
            user_embedding_lst.append( user_embedding_array )
        user_embedding_matrix = np.stack(user_embedding_lst)
        return user_embedding_matrix
    
    def get_similarity(self, v, e):
        numerator = distance.cdist(v.reshape(1, 150), e, 'euclidean')
        denominator = np.linalg.norm(e, axis=1) + np.linalg.norm(v)
        return 1 - np.divide(numerator, denominator)
    
    def get_similarity_matrix(self, user_embedding_matrix):
        similarity_lst = []
        for v in user_embedding_matrix:
            similarity_array = self.get_similarity(v, self.bug_embedding_matrix)
            similarity_lst.append(similarity_array)
        similarity_matrix = np.vstack(similarity_lst)
        return similarity_matrix

    
    def get_similar_bugs(self, similarity_matrix, threshold=0.90):
        '''
        return similar_bugs - list 
        [
            user_index helps to locate bug lines in user input
            bug_index helps to locate bug type in bug database
            score is the similarity socre 
            (user_index, bug_index, score)
            ...
        ]
        '''
        similar_bugs = []
        score_sorted = np.sort(similarity_matrix)
        index_sorted = np.argsort(similarity_matrix)
        
        for i in range(similarity_matrix.shape[0]): 
            for score, bug_index in zip(score_sorted[i][::-1], index_sorted[i][::-1]):
                if score < threshold:
                    break
                user_index = i
                similar_bugs.append( (user_index, bug_index, score) )
        
        return similar_bugs
    
    def transform_result(self, similar_bugs, user_statement_embeddings):
        '''
           transform 
           [(user_index, bug_index, score)] --> [(line_start, line_end, bug_type, bug_addr, score)]
        '''
        final_result = []
        for e in similar_bugs:
            user_index, bug_index, score = e[0], e[1], e[2]
            user_linespan = user_statement_embeddings[user_index][0]
            candidate_start_line = int(user_linespan.split('_')[0])
            candidate_end_line = int(user_linespan.split('_')[1])

            bug_addr = self.bug_database_statement_embeddings[bug_index][0].split('@')[0]
            bug_type = self.bug_info[bug_addr]["type"].strip()
            final_result.append( (candidate_start_line, candidate_end_line, bug_type, bug_addr, score) )
        return final_result
    
    def validate(self, user_in):
        self.save_to_file(user_in)
        self.parser()
        self.normalizer()
        norm_result = self.indexer()
        user_statement_embeddings = self.get_user_statement_embeddings(norm_result)
        user_embedding_matrix = self.get_user_embedding_matrix(user_statement_embeddings)
        similarity_matrix = self.get_similarity_matrix(user_embedding_matrix)
        similar_bugs = self.get_similar_bugs(similarity_matrix)
        validate_result = self.transform_result(similar_bugs, user_statement_embeddings)
        return validate_result

def main():
    # Test Clone_Detect()
    cv = Contract_Validate()
    user_in = open('./test.sol', 'r').read()
    validate_result = cv.validate(user_in)
    print(validate_result)
    pass

if __name__ == '__main__':
    main()

