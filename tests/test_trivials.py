from ethereum.tools import tester

def test_init_first_epoch(casper, new_epoch):
    assert casper.current_epoch() == 0
    assert casper.next_validator_index() == 1

    new_epoch()

    assert casper.dynasty() == 0
    assert casper.next_validator_index() == 1
    assert casper.current_epoch() == 1


def test_deposit_to_pool(casper, new_epoch, pool, funded_privkey, deposit_amount,
                                 induct_validator):
    validator_index = induct_validator(funded_privkey, deposit_amount)

    new_epoch()

    pool.deposit_to_pool(tester.a1, value=5000)