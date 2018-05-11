from ethereum.tools import tester
from ethereum import utils


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

def test_operator_can_vote(deposit_to_casper, casper, pool, mk_suggested_vote, operator):
    deposit_to_casper()
    mk_suggested_vote(pool.validator_index(), operator["key"])


def test_logout_from_casper(deposit_to_casper, pool, mine_until, mk_logout_msg_unsigned, casper, operator):
    deposit_to_casper()
    mine_until(pool.VALIDATION_END() + 1)
    logout_msg = mk_logout_msg_unsigned(pool.validator_index(), casper.current_epoch())
    pool.logout_from_casper(logout_msg, sender=operator["key"])


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
