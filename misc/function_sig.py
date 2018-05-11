from vyper import compiler
from eth_utils import function_abi_to_4byte_selector
import binascii


casper_abi = compiler.mk_full_signature(open("../casper/casper/contracts/simple_casper.v.py").read())
for item in casper_abi:
    b = ''.join([ f'\\x{l:02x}' for l in list(function_abi_to_4byte_selector(item))])
    print(item["name"], '\t', b )
