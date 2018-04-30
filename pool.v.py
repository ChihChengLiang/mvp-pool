class Casper():
    @constant
    def PURITY_CHECKER()-> address: pass
    
    @public
    @payable
    def deposit(validation_addr: address, withdrawal_addr: address): pass


DEPOSIT_START: public(timestamp)
DEPOSIT_END: public(timestamp)
VALIDATION_START: public(timestamp)
VALIDATION_END: public(timestamp)
CASPER_ADDR: address
VOTER: address
depositors: public({
    withdraw_addr:address,
    shares: int128(wei)
}[int128])
next_depositor_index: public(int128)
depositor_indexes: public(int128[address])
validation_addr: public(address)


@public
def __init__(casper_addr: address, deposit_start:timestamp, deposit_time:timedelta,
             validation_time:timedelta, voter:address):
    self.CASPER_ADDR = casper_addr
    self.DEPOSIT_START = deposit_start
    self.DEPOSIT_END = deposit_start + deposit_time
    self.VALIDATION_START = self.DEPOSIT_END + 86400 # 1 day
    self.VALIDATION_END = self.VALIDATION_START + validation_time
    self.VOTER = voter
    self.next_depositor_index = 1

@public
@payable
def deposit_to_pool(withdraw_addr:address):
    assert not self.depositor_indexes[withdraw_addr]
    assert block.timestamp >= self.DEPOSIT_START and block.timestamp < self.DEPOSIT_END
    self.depositors[self.next_depositor_index] = {
        withdraw_addr:withdraw_addr,
        shares: msg.value
    }
    self.depositor_indexes[withdraw_addr] = self.next_depositor_index
    self.next_depositor_index += 1

@public
def deploy_valcode():
    # TODO: who (delegated voter? pool contract?) when (at init? at deposit ends?) deploy? 
    pass

@public
def deposit_to_casper():
    assert block.timestamp >= self.DEPOSIT_END and block.timestamp < self.VALIDATION_START
    

@public
def logout():
    pass

@public
def withdrawal():
    pass

@public
def assert_voter_useful():
    # verify purity
    assert extract32(raw_call(Casper(self.CASPER_ADDR).PURITY_CHECKER(), concat('\xa1\x90\x3e\xab', convert(self.validation_addr, 'bytes32')), gas=500000, outsize=32), 0) != convert(0, 'bytes32')
    # validate_signature(sighash: bytes32, sig: bytes <= 1024, validator_index: int128) -> bool:
    assert True
    
    