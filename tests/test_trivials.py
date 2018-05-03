from ethereum.tools import tester
from ethereum import utils


def test_init_first_epoch(casper, new_epoch):
    assert casper.current_epoch() == 0
    assert casper.next_validator_index() == 1

    new_epoch()

    assert casper.dynasty() == 0
    assert casper.next_validator_index() == 1
    assert casper.current_epoch() == 1


def test_deposit_to_pool(casper, new_epoch, pool, funded_privkey, deposit_amount,
                         depositor_privkey, depositor_deposit_amount, induct_validator):
    validator_index = induct_validator(funded_privkey, deposit_amount)

    new_epoch()
    withdraw_addr = utils.privtoaddr(depositor_privkey)

    pool.deposit_to_pool(withdraw_addr, value=depositor_deposit_amount)


def test_register_validation_addr(): pass


def test_deposit_to_casper(): pass


def test_logout_from_casper(): pass


def test_withdraw_from_casper(): pass


def withdraw_from_pool(): pass
