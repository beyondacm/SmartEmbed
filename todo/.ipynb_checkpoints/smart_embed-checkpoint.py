# -*- coding:utf-8 -*-
import re
import os
import numpy as np
from crawler_utils import crawl_url_by_get
from lxml import etree
import json
import sys

class Contract_Detail(object):
    
    def __init__(self, contract_addr):
        self.contract_addr = contract_addr
        self.base_dir = './' + str(contract_addr)
        self.api_key = 'NXR4MP72TG297DXPDSUGZMVXJTBGNN2BX2'
        self.parse_html = self.get_parse_html()
        pass

    def get_parse_html(self, write2file=False):
        '''
            get details of a given smart contract
            Parameters : contract_addr, smart contract address 
            return : parse_html
        '''

        '''
        if os.path.exists(self.base_dir + '/parse.html'):
            with open(self.base_dir + '/parse.html', 'r') as pt:
                raw_html = pt.read() 
                parse_html = etree.HTML(raw_html)
                return parse_html
        '''
        base_url = 'https://etherscan.io/address/'
        target_url = str(base_url) + str(self.contract_addr) + str('#code') 
        raw_html = crawl_url_by_get(target_url, proxy=None)
        parse_html = etree.HTML(raw_html)
        if write2file:
            with open(self.base_dir + '/parse.html', 'w') as parse:
                parse.write( etree.tostring(parse_html) )
        return parse_html
    
    def get_basic_info(self):
        '''
            extract basic info from a given html
            Parameters : 
            return : basic_info, dict, 
                     {
                        'contract_name' : ..., 
                        'eth_balance' : ...,
                        'eth_usd_value' : ...,
                        'no_of_trans' : ...,
                     }
        '''
        basic_info = {}
        cleanr = re.compile('<.*?>')
        
        table_2_key = self.parse_html.xpath("//div[@id='ContentPlaceHolder1_contractCodeDiv']//table//td[1]")
        table_2_value = self.parse_html.xpath("//div[@id='ContentPlaceHolder1_contractCodeDiv']//table//td[2]")
        table_2_dict = {}
        for i in range(len(table_2_key)):
            key = str( re.sub(cleanr, '', etree.tostring(table_2_key[i])) ).strip().replace(" ", "")
            value = str( re.sub(cleanr, '', etree.tostring(table_2_value[i])) ).strip()
            table_2_dict[key] = value

        table_1_key = self.parse_html.xpath("//div[@id='ContentPlaceHolder1_divSummary']//table//td[1]")
        table_1_value = self.parse_html.xpath("//div[@id='ContentPlaceHolder1_divSummary']//table//td[2]")
        table_1_dict = {}
        for i in range(len(table_1_key)):
            key = str( re.sub(cleanr, '', etree.tostring(table_1_key[i])) ).strip().replace(" ", "")
            value = str( re.sub(cleanr, '', etree.tostring(table_1_value[i])) ).strip()
            table_1_dict[key] = value
        # print table_1_dict

        basic_info['contract_addr'] = self.contract_addr
        if 'ContractName:' in table_2_dict:
            basic_info['contract_name'] = table_2_dict['ContractName:']

        if 'Balance:' in table_1_dict:
            basic_info['eth_balance'] = table_1_dict['Balance:'] 
        elif 'ETHBalance:' in table_2_dict:
            basic_info['eth_balance'] = table_1_dict['ETHBalance:'] 

        if 'EtherValue:' in table_1_dict:
            basic_info['eth_usd_value'] = table_1_dict['EtherValue:'] 
        elif 'ETHUSDValue:' in table_1_dict:
            basic_info['eth_usd_value'] = table_1_dict['ETHUSDValue:'] 

        if 'Transactions:' in table_1_dict:
            basic_info['no_of_trans'] = table_1_dict['Transactions:'] 
        elif 'NoOfTransactions:' in table_1_dict:
            basic_info['no_of_trans'] = table_1_dict['NoOfTransactions:'] 

        if 'TokenContract:' in table_1_dict:
            basic_info['token_contract'] = table_1_dict['TokenContract:']
        elif 'TokenContract(ERC20):' in table_1_dict:
            basic_info['token_contract'] = table_1_dict['TokenContract(ERC20):']
        
        if 'ContractCreator:' in table_1_dict:
            basic_info['creator_address'] = table_1_dict['ContractCreator:'].split(' txn ')[0]
            basic_info['creator_transaction'] = table_1_dict['ContractCreator:'].split(' txn ')[1]
        elif 'ContractCreator' in table_1_dict:
            basic_info['creator_address'] = table_1_dict['ContractCreator'].split(' txn ')[0]
            basic_info['creator_transaction'] = table_1_dict['ContractCreator'].split(' txn ')[1]
        # print basic_info
        json.dump(basic_info, open(self.base_dir + '/basic_info','w'))
        # with open(self.base_dir + '/basic_info', 'w') as bi:
        #     bi.write( str(basic_info) )
        return basic_info
        

    def get_source_code(self):
        '''
            extract source code from a given html and write into a file
            Parameters : contract_addr
            return : file of source code
        '''
        # parse_html = self.get_parse_html()
#         source_code = self.parse_html.xpath('//pre[@class = "js-sourcecopyarea"]/text()')
        source_code = self.parse_html.xpath('//pre[@class = "js-sourcecopyarea editor"]/text()')
#         with open(self.base_dir + '/source_code', 'w') as sc:
#             for e in source_code:
#                 sc.write(e)
        return source_code

    def get_contract_abi(self):
        '''
            get contract ABI from api call 'https://api.etherscan.io/api?module=contract&action=getabi&address='
            Parameters : contract_addr 
            return : file of contract abi
        '''
        target_url = 'https://api.etherscan.io/api?module=contract&action=getabi'\
                        + '&address=' + str(self.contract_addr)\
                        + '&apikey=' + str(self.api_key)
        result = crawl_url_by_get(target_url, proxy=None, enable_proxy=True)
        # print result, type(result)
        with open(self.base_dir + '/contract_abi', 'w') as ca:
            ca.write(result)

    def get_byte_code(self):
        '''
            get byte code from api call 'https://api.etherscan.io/api?module=proxy&action=eth_getCode&address=0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c&tag=latest&apikey=YourApiKeyToken'
            Parameters : contract_addr
            return : file of byte code
        '''
        target_url = 'https://api.etherscan.io/api?module=proxy&action=eth_getCode&address=' + str(self.contract_addr)
        result = crawl_url_by_get(target_url, proxy=None, enable_proxy=True)
        # print result, type(result)
        with open(self.base_dir + '/byte_code', 'w') as bc:
            bc.write(result)

    def get_op_code(self):
        '''
            get op codes from api call 'https://etherscan.io/api?module=opcode&action=getopcode&address=0xDa65eed883A48301D0EcF37465f135A7a0C9d978'
            Parameters : contract_addr
            return : file of op code
        '''
        target_url = 'https://etherscan.io/api?module=opcode&action=getopcode&address=' + str(self.contract_addr)
        result = crawl_url_by_get(target_url, proxy=None, enable_proxy=True)
        # print result, type(result)
        with open(self.base_dir + '/op_code', 'w') as oc:
            oc.write(result)

        parse_op_code = json.loads(result)['result'].split('<br>')
        # print parse_op_code, type(parse_op_code)
        with open(self.base_dir + '/parse_op_code', 'w') as poc:
            for e in parse_op_code:
                poc.write(e + '\n')

    def get_contract_detail(self):
        try:
            # self.get_parse_html(write2file=True )
            self.get_source_code()
            # self.get_contract_abi()
            # self.get_byte_code()
            # self.get_op_code()
            self.get_basic_info()
            # return basic_info, True
            return True
        except Exception, ex:
#             print 'get_contract_detail（） -------- ', str(ex) 
            # return None, False
            return False
        
class Contract_Vec(object):
    
    def __init__(self, norm_result, model):
        self.norm_result = norm_result
        self.model = model
        self.vector = self.vectorize()
        pass
    
    def vectorize(self, dimension=150):
        
        print("entering vectorize...")
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
    pass

if __name__ == '__main__':
    main()
