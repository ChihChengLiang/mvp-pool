from ethereum import utils

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
