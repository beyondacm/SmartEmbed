import numpy as np

class Statement_Vec(object):
    
    def __init__(self, norm_result, model):
        self.norm_result = norm_result
        self.model = model
        self.vector = self.vectorize()
        pass
    
    def vectorize(self, dimension=150):
        
        # print("entering vectorize...")
        # print(self.norm_result, type(self.norm_result))

        line_span = self.norm_result[0]
        norm_tokens = self.norm_result[1]
        embedding_vector = np.empty((0,dimension), dtype="float64")
        
        for k in range(0,len(norm_tokens)):
            contract_vector = np.zeros((dimension,), dtype="float64")
            ct = 0
            for token in norm_tokens[k]:
                if token in self.model:
                    contract_vector = np.add(contract_vector, self.model[token])
                else: 
                    continue
                ct = ct + 1
            tmp_embedding_vector = np.vstack([contract_vector])
            embedding_vector = np.append(embedding_vector,tmp_embedding_vector,axis=0)
        return embedding_vector


