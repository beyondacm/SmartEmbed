# -*- coding:utf-8 -*-
import re
import os

class Contract_Norm(object): 

    def __init__(self, contract_tokens_path): 
        '''
            initialize Token_Norm for token normalization
            Parameters : contract_tokens_path
        '''
        self.contract_tokens_path = contract_tokens_path
        self.line_span, \
        self.contract_tokens = self.load_contract_tokens()
        self.token_list = self.get_token_list()
        self.token_type = self.get_token_type()
        self.normalized_tokens = self.normalize()
        # print self.normalized_tokens, type(self.normalized_tokens)

        assert len(self.token_list) == len(self.token_type) 

    def load_contract_tokens(self):
        '''
            load contract_tokens into the list
            Parameters : contract_token
            return : token_list 
        '''
        with open(self.contract_tokens_path + 'parse_result', 'r') as ct:
            for line in ct:
                line_span = line.split('\t')[0].strip('[').strip(']').split(', ')
                contract_tokens = line.split('\t')[1]
        return line_span, contract_tokens

    def get_token_list(self, verbose=False):
        '''
            get token list form the contract_tokens 
            Parameters : contract_tokens (string)
            return : token_list, list of tokens 
        '''
        token_list = []
        token_clean_exp = '@[0-9]+,[0-9]+:[0-9]+=' + '|'\
                          ',<[0-9]+>,[0-9]+:[0-9]+' + '|'\
                          ',<[0-9]+>,channel=[0-9],[0-9]+:[0-9]+' + '|'\
                          ',<-1>,[0-9]+:[0-9]+'
        token_clean_reg = re.compile(token_clean_exp)
        token_clean = re.sub(token_clean_reg, '', self.contract_tokens)
        token_list = token_clean.strip().strip('[').strip(']').split('], [')
        token_list = [e.strip("'") for e in token_list]
        if verbose:
            print token_list

        # assert token_list[0] == "pragma" and 
        assert token_list[-1] == "<EOF>"
        return token_list

    def get_token_type(self, verbose=False):
        '''
            get token type from the contract_tokens
            Parameters : contract_tokens (string)
            return : token_list, list of tokens
        '''
        token_type_exp = ',<[0-9]+>,|,<-1>,'
        token_type_reg = re.compile(token_type_exp)
        token_type = token_type_reg.findall(self.contract_tokens)
        
        if verbose:
            print token_type

        # assert token_type[0] == ",<1>," 
        assert token_type[-1] == ",<-1>,"
        return token_type
    
    def normalize(self):
        '''
            remove the comments in the contract code
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
        token_list = self.token_list
        token_type = self.token_type
        token_list_normalized = []
        for i in range(len(self.token_list)):
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
            
        normalized_tokens = []
        for e in token_list_normalized:
            if not e.startswith('%%%%'):
                e = e.lower()
            if len(e) == 1 and ( e >= 'a' and e <= 'z'):
                e = e.replace(e, 'SimpleVar')
            normalized_tokens.append(e)
        assert len(token_list_normalized) == len(normalized_tokens)
        return normalized_tokens

    def store(self):
        with open(self.contract_tokens_path + '/contract_normalized_tokens', 'w') as cnt:
            # print '_'.join(self.line_span)
            cnt.write('_'.join(self.line_span) + '\t')
            cnt.write(' '.join(self.normalized_tokens)) 
        pass


def main():
    # token_norm = Token_Norm('./')
    # token_norm.store()
    base_dir = '/home/zhipeng/work_space/Etherscan_crawl/'
    contract_addrs = os.listdir( base_dir )
    exception_case = open('./exception_case', 'w')
    for addr in contract_addrs:
        if addr.startswith('0xtest'):
            try:
                contract_tokens_path = base_dir + addr + '/'
#                 print contract_tokens_path
                contract_norm = Contract_Norm(contract_tokens_path)
                contract_norm.store()
                break
            except Exception, ex:
#                 print str(ex)
                exception_case.write( str(contract_tokens_path) + '\n')
                # break
                continue
    exception_case.close()
    print "Finished"
    pass

if __name__ == '__main__':
    main()
