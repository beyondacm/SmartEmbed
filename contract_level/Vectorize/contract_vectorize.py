import numpy as np

class Contract_Vec(object):
    
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
        contract_vector = np.zeros((dimension,), dtype="float64")

        for token in norm_tokens:
            if token in self.model:
                contract_vector = np.add(contract_vector, self.model[token])
            else: 
                continue
#                 print(token)
        embedding_vector = np.vstack([contract_vector])
        return embedding_vector


