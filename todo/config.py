class Config():

    def __init__(self):

        self.contract_model = "../contract_level/Model/FastText/fasttext_model"          
        self.contract_embedding_matrix = "../contract_level/Embedding/contract_embedding_matrix.pkl" 
        self.sorted_contract_embeddings = "../contract_level/Embedding/sorted_contract_embeddings.pkl"

        self.statement_model = "../statement_level/Model/FastText/fasttext_model"       
        self.bug_database = "../statement_level/Bug_Database/sorted_bug_statements_embeddings.pkl"
        self.bug_info = "../statement_level/Bug_Database/bug_info.pickle"
    

