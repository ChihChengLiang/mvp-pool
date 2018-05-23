from ethereum import utils
import pytest


def test_deposit_to_pool(casper_chain, casper, new_epoch, pool, funded_privkey, deposit_amount,
                         depositor_privkey, depositor_deposit_amount, induct_validator):

    induct_validator(funded_privkey, deposit_amount)

    assert pool.CASPER_ADDR() == '0x' + utils.encode_hex(casper.address)
    assert pool.next_depositor_index() == 1

    new_epoch()

    assert casper_chain.chain.head.number > pool.DEPOSIT_START()
    assert casper_chain.chain.head.number < pool.DEPOSIT_END()

    withdraw_addr = utils.privtoaddr(depositor_privkey)
    pool.deposit_to_pool(withdraw_addr, value=depositor_deposit_amount)

    assert pool.next_depositor_index() == 2


@pytest.mark.parametrize(
    'min_individual_deposit,depositor_deposit_amount,success',
    [
        (10*10**18, 15*10**18, True),
        (10*10**18, 5*10**18, False)
    ]
)
def test_min_individual_deposit(min_individual_deposit, depositor_deposit_amount, success,
                                new_epoch, pool, funded_privkey, deposit_amount,
                                depositor_privkey, induct_validator, assert_tx_failed):

    induct_validator(funded_privkey, deposit_amount)
    new_epoch()
    withdraw_addr = utils.privtoaddr(depositor_privkey)

    def deposit(): return pool.deposit_to_pool(
        withdraw_addr, value=depositor_deposit_amount)

    if success:
        deposit()
    else:
        assert_tx_failed(deposit)
