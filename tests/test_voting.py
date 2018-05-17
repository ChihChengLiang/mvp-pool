def test_operator_can_vote(deposit_to_casper, casper, pool, mk_suggested_vote, operator):
    deposit_to_casper()
    mk_suggested_vote(pool.validator_index(), operator["key"])
