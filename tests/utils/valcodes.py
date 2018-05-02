from vyper import optimizer, compile_lll
from vyper.parser.parser_utils import LLLnode
from ethereum.utils import bytes_to_int


def generate_validation_code(address):
    valcode = generate_pure_ecrecover_LLL_source(address)
    lll_node = LLLnode.from_list(valcode)
    optimized = optimizer.optimize(lll_node)
    assembly = compile_lll.compile_to_assembly(optimized)
    evm = compile_lll.assembly_to_evm(assembly)
    return evm


def generate_pure_ecrecover_LLL_source(address):
    return [
        'seq',
        ['return', [0],
            ['lll',
                ['seq',
                    ['calldatacopy', 0, 0, 128],
                    ['call', 3000, 1, 0, 0, 128, 0, 32],
                    ['mstore',
                        0,
                        ['eq',
                            ['mload', 0],
                            bytes_to_int(address)]],
                    ['return', 0, 32]],
                [0]]]
    ]
