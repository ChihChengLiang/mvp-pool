def test_casper_init_first_epoch(casper, new_epoch):
    """
    This is a sanity test to make sure Casper contract work here.
    """
    assert casper.current_epoch() == 0
    assert casper.next_validator_index() == 1

    new_epoch()

    assert casper.dynasty() == 0
    assert casper.next_validator_index() == 1
    assert casper.current_epoch() == 1
