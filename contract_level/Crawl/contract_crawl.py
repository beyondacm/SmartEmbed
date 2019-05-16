# -*- coding:utf-8 -*-
import re
import os
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
 

