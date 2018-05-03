from ethereum.tools import tester
from ethereum import utils


def test_casper_init_first_epoch(casper, new_epoch):
    assert casper.current_epoch() == 0
    assert casper.next_validator_index() == 1

    new_epoch()

    assert casper.dynasty() == 0
    assert casper.next_validator_index() == 1
    assert casper.current_epoch() == 1


def test_deposit_to_pool(casper_chain, casper, new_epoch, pool, funded_privkey, deposit_amount,
                         depositor_privkey, depositor_deposit_amount, induct_validator):

    validator_index = induct_validator(funded_privkey, deposit_amount)

    assert pool.CASPER_ADDR() == '0x' + utils.encode_hex(casper.address)
    assert pool.next_depositor_index() == 1

    new_epoch()

    assert casper_chain.chain.head.number > pool.DEPOSIT_START()
    assert casper_chain.chain.head.number < pool.DEPOSIT_END()

    withdraw_addr = utils.privtoaddr(depositor_privkey)
    pool.deposit_to_pool(withdraw_addr, value=depositor_deposit_amount)

    assert pool.next_depositor_index() == 2


def test_deposit_to_casper(casper_chain, pool, induct_validators_and_depositors, depositor_privkeys, depositor_deposit_amount):

    n_depositor = len(depositor_privkeys)
    induct_validators_and_depositors(depositor_privkeys,
                                     [int(depositor_deposit_amount/n_depositor)]*n_depositor)


def test_logout_from_casper(): pass


def test_withdraw_from_casper(): pass


def withdraw_from_pool(): pass
