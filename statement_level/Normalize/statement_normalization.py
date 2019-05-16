# -*- coding:utf-8 -*-
import re
import os

class Statement_Norm(object):

    def __init__(self, statement_tokens_path):
         
        self.statement_tokens_path = statement_tokens_path
        # self.header_list = self.get_header_list()
        # self.statement_list = self.get_statement_list()
        self.linespan_list, \
        self.ancestor_list, \
        self.statement_list = self.load_statement_tokens()
        self.statement_tokens = self.get_statement_tokens()
        self.statement_tokens_type = self.get_statement_tokens_type()
        self.statement_tokens_norm = self.get_statement_tokens_norm()
        # print self.statement_tokens_norm
        assert len(self.linespan_list) == len(self.ancestor_list)
        assert len(self.ancestor_list) == len(self.statement_list)
        assert len(self.statement_list) == len(self.statement_tokens_norm)
        assert len(self.statement_tokens) == len(self.statement_tokens_type)
    
    def load_statement_tokens(self):
        '''
        '''
        linespan_list = []
        ancestor_list = []
        statement_list = []
        with open(self.statement_tokens_path + "statement_parse_result") as st:
            for i, line in enumerate(st):
                linespan = line.split('\t')[0].strip('[').strip(']').split(', ')
                ancestor = line.split('\t')[1].strip('[').strip(']').split(', ')
                statement = line.split('\t')[2]
                if statement.startswith('[['):
                    linespan_list.append(linespan)
                    ancestor_list.append(ancestor)
                    statement_list.append(statement.strip())
                else:
                    continue
        return linespan_list, ancestor_list, statement_list 
        pass
    
    def get_statement_tokens(self):
        '''
        '''
        statement_tokens = []
        for statement_str in self.statement_list:
            tokens = self.get_tokens( statement_str )
            statement_tokens.append( tokens )
        return statement_tokens
        pass

    def get_statement_tokens_type(self):
        '''
        '''
        statement_tokens_type = []  
        for statement_str in self.statement_list:
            tokens_type = self.get_token_type( statement_str )
            statement_tokens_type.append( tokens_type )
        return statement_tokens_type
        pass
        
    def get_statement_tokens_norm(self):
        statement_tokens_norm = [] 
        for i in range(len(self.statement_list)):
            token = self.statement_tokens[i]
            token_type = self.statement_tokens_type[i]
            assert len(token) == len(token_type)
            tokens_norm = self.get_token_normalize(token, token_type) 
            statement_tokens_norm.append(tokens_norm)
        return statement_tokens_norm
        pass

    def store(self):
        with open(self.statement_tokens_path + 'statement_normalized_tokens', 'w') as snt:
            for e in zip(self.linespan_list, self.ancestor_list, self.statement_tokens_norm):
                # snt.write( str(self.statement_tokens_path) )
                snt.write( '_'.join(e[0]) + '\t')
                snt.write( ' '.join(e[1]) + ' ')
                snt.write( ' '.join(e[2]) + '\n')
        pass

    def get_tokens(self, statement_str, verbose=False):
        '''
            get token list form the statement_tokens 
            Parameters : statement_tokens (string)
            return : list of tokens str
        '''
        tokens = []
        token_clean_exp = '@[0-9]+,[0-9]+:[0-9]+=' + '|'\
                          ',<[0-9]+>,[0-9]+:[0-9]+' + '|'\
                          ',<[0-9]+>,channel=[0-9],[0-9]+:[0-9]+' + '|'\
                          ',<-1>,[0-9]+:[0-9]+'
        token_clean_reg = re.compile(token_clean_exp)
        token_clean = re.sub(token_clean_reg, '', statement_str)
        tokens = token_clean.strip().strip('[').strip(']').split('], [')
        tokens = [e.strip("'") for e in tokens]
        if verbose:
            print tokens

        return tokens
    
    def get_token_type(self, statement_str, verbose=False):
        '''
            get token type from the statement_tokens
            Parameters : statement_tokens (string)
            return : token_type, list of token types
        '''
        token_type_exp = ',<[0-9]+>,|,<-1>,'
        token_type_reg = re.compile(token_type_exp)
        token_type = token_type_reg.findall(statement_str)
        
        if verbose:
            print token_type

        # assert token_type[0] == ",<1>," 
        # assert token_type[-1] == ",<-1>,"
        return token_type

    def get_token_normalize(self, token_list, token_type):
        '''
            remove the comments in the source code
            Parameters : token_list & token_type
                         token_type == 117 -> COMMENT 
                         token_type == 118 -> LINE_COMMENT
                         token_type == 2 --> ;
                         token_type == 15 --> , 
                         token_type == 34 --> .
                         token_type == 115 --> StringLiteral
                         token_type == 97 --> DecimalNumber
                         token_type == 98 --> HexNumber
                         token_type == 100 --> HexLiteral
                         token_type == 95 --> VersionLiteral 
                         token_type == 114 --> Identifier
            return : normalized tokens 
        '''
        # token_list = self.token_list
        # token_type = self.token_type
        assert len(token_list) == len(token_type)
        # print str(token_list) + str(len(token_list)) + str(type(token_list))
        # print str(token_type) + str(len(token_type)) + str(type(token_type))

        token_list_normalized = []
        for i in range(len(token_list)):
            # handle the comment 
            if token_type[i] == ",<117>," or token_type[i] == ",<118>,":
                pass
            # handle the punctuations 
            elif token_type[i] == ",<2>," or token_type[i] == ",<15>," or token_type == ',<34>,':
                pass        
            # handle the version
            elif token_type[i] == ',<95>,':
                token_list[i] = "VersionLiteral"
                token_list_normalized.append(token_list[i])
            # handle the string constant 
            elif token_type[i] == ",<115>," :
                token_list[i] = "StringLiteral"
                token_list_normalized.append(token_list[i])
            # handle the DecimalNumber 
            elif token_type[i] == ",<97>," :
                token_list[i] = "DecimalNumber"
                token_list_normalized.append(token_list[i])
            # handle the HexNumber
            elif token_type[i] == ",<98>,":
                token_list[i] = "HexNumber"
                token_list_normalized.append(token_list[i])
            # handle the HexLiteral
            elif token_type[i] == ",<100>,":
                token_list[i] = "HexLiteral"
                token_list_normalized.append(token_list[i])
            # handle the identifier
            elif token_type[i] == ",<114>,":
                # token_list_normalized.append('%%%%' +token_list[i])
            
                identifier_candidates = []
                camel_case_candidates = []

                camel_case_exp = '([A-Z][a-z]+)'
                camel_case_reg = re.compile(camel_case_exp)
                camel_case_cut = camel_case_reg.findall(token_list[i])
                
                # print '113 Case:' + token_list[i]
                if not camel_case_cut:
                    camel_case_candidates.append(token_list[i])
                else :
                    token_list_normalized.append('%%%%' +token_list[i])
                    remain = token_list[i]
                    for e in camel_case_cut:
                        remain = remain.replace(e, '')
                    if remain:
                        camel_case_candidates.append(remain)
                    for e in camel_case_cut:
                        camel_case_candidates.append(e)
                
                for candidate in camel_case_candidates:
                    if '_' not in candidate:
                        identifier_candidates.append(candidate)
                    else :
                        under_line_cut = candidate.split('_')
                        for e in under_line_cut:
                            if e:
                                identifier_candidates.append(e)
        
                token_list_normalized.extend(identifier_candidates)
            # other situations : normal tokens
            else :
                token_list_normalized.append(token_list[i])
        
        # print token_list_normalized
        normalized_tokens = []
        for e in token_list_normalized:
            if not e.startswith('%%%%'):
                e = e.lower()
            if len(e) == 1 and ( e >= 'a' and e <= 'z'):
                e = e.replace(e, 'SimpleVar')
            normalized_tokens.append(e)
        
        # print normalized_tokens
        assert len(token_list_normalized) == len(normalized_tokens)
        return normalized_tokens


def main():
    
    # base_dir = '/home/zhipeng/work_space/Etherscan_crawl/'
    base_dir = '../stp01_crawl/'
    contract_addrs = os.listdir( base_dir )
    exception_case = open('./exception_case', 'w')
    for addr in contract_addrs:
        if addr.startswith('0x'):
            try:
                statement_tokens_path = base_dir + addr + '/'  
                print addr
                statement_norm = Statement_Norm(statement_tokens_path) 
                statement_norm.store()
                # break
            except Exception, ex:
                # print ex
                # break
                exception_case.write( str(statement_tokens_path) + '\n')
                continue
                
    exception_case.close()
    print "Finished"
    pass

if __name__ == '__main__':
    main()
