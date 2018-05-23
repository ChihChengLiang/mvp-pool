import pytest


def test_deposit_to_casper(casper_chain, casper, pool, induct_validators_and_depositors,
                           depositor_privkeys, depositor_deposit_amount, operator, validation_addr, mine_until):

    n_depositor = len(depositor_privkeys)
    induct_validators_and_depositors(depositor_privkeys,
                                     [int(depositor_deposit_amount/n_depositor) + 10**18]*n_depositor)

    operator_valcode_addr = validation_addr(operator["key"])

    mine_until(pool.DEPOSIT_END() + 1)

    assert casper_chain.chain.head.number > pool.DEPOSIT_END()
    assert casper_chain.chain.state.get_balance(pool.address) > casper.MIN_DEPOSIT_SIZE()

    pool.deposit_to_casper(operator_valcode_addr, sender=operator["key"])

    assert casper.validator_indexes(pool.address) == pool.validator_index()


@pytest.mark.parametrize(
    'min_deposit_size,min_total_deposit,depositor_deposit_amount,success',
    [
        (1000*10**18, 1000*10**18, 1000*10**18, True),
        (1000*10**18, 1000*10**18, 500*10**18, False),
        (1000*10**18, 1500*10**18, 1000*10**18, False)
    ]
)
def test_min_total_deposit(min_deposit_size, min_total_deposit, depositor_deposit_amount, success,
                           casper_chain, casper, pool, induct_validators_and_depositors,
                           depositor_privkeys, operator, validation_addr, mine_until, assert_tx_failed):

    n_depositor = len(depositor_privkeys)
    induct_validators_and_depositors(depositor_privkeys,
                                     [int(depositor_deposit_amount/n_depositor)]*n_depositor)

    operator_valcode_addr = validation_addr(operator["key"])
    mine_until(pool.DEPOSIT_END() + 1)

    if success:
        pool.deposit_to_casper(operator_valcode_addr, sender=operator["key"])
    else:
        assert_tx_failed(lambda: pool.deposit_to_casper(
            operator_valcode_addr, sender=operator["key"]))
