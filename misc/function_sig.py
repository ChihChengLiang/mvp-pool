from vyper import compiler
from eth_utils import function_abi_to_4byte_selector

casper_abi = compiler.mk_full_signature(open("../casper/casper/contracts/simple_casper.v.py").read())
print(function_abi_to_4byte_selector(casper_abi[0]))