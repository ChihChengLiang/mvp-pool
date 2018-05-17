def test_withdraw_from_casper(logout_from_casper, new_epoch, casper, pool, mk_suggested_vote, funded_privkeys, withdrawal_delay):
    validator_indexes, depositor_indexes = logout_from_casper()
    for _ in range(7):
        for i, validator_index in enumerate(validator_indexes):
            casper.vote(mk_suggested_vote(validator_index, funded_privkeys[i]))
        new_epoch()
    end_dynasty = casper.validators__end_dynasty(pool.validator_index())
    assert casper.dynasty() > end_dynasty
    for _ in range(withdrawal_delay):
        new_epoch()

    end_epoch = casper.dynasty_start_epoch(end_dynasty + 1)
    withdrawal_epoch = end_epoch + withdrawal_delay
    assert casper.current_epoch() >= withdrawal_epoch
    pool.withdraw_from_casper()
    pool.withdraw_from_pool(depositor_indexes[-1])
