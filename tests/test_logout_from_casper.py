def test_logout_from_casper(deposit_to_casper, pool, mine_until, mk_logout_msg_unsigned, casper, operator):
    deposit_to_casper()
    mine_until(pool.VALIDATION_END() + 1)
    logout_msg = mk_logout_msg_unsigned(pool.validator_index(), casper.current_epoch())
    pool.logout_from_casper(logout_msg, sender=operator["key"])

