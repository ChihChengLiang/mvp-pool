class Casper():
    @public
    @constant
    def PURITY_CHECKER() -> address: pass
    
    @public
    @constant
    def MIN_DEPOSIT_SIZE() -> wei_value: pass

    @public
    @constant
    def current_epoch() -> int128: pass

    @public
    @constant
    def validator_indexes(validator_address:address) -> int128: pass

    @public
    @payable
    def deposit(validation_addr: address, withdrawal_addr: address): pass

    @public
    def logout(logout_msg: bytes <= 1024): pass

    @public
    def withdraw(validator_index: int128): pass



DEPOSIT_START: public(timestamp)
DEPOSIT_END: public(timestamp)
VALIDATION_START: public(timestamp)
VALIDATION_END: public(timestamp)
CASPER_ADDR: public(address)
VOTER: address
depositors: public({
    withdraw_addr:address,
    shares: int128(wei)
}[int128])
total_shares: public(int128(wei))
next_depositor_index: public(int128)
depositor_indexes: public(int128[address])
validation_addr: public(address)
final_balance: public(int128(wei))


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
    self.total_shares = 0

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
    self.total_shares += msg.value

@public
def register_validation_addr(addr: address):
    # verify purity
    assert extract32(raw_call(Casper(self.CASPER_ADDR).PURITY_CHECKER(), concat('\xa1\x90\x3e\xab', convert(addr, 'bytes32')), gas=500000, outsize=32), 0) != convert(0, 'bytes32')
    self.validation_addr = addr

@public
def deposit_to_casper():
    assert block.timestamp >= self.DEPOSIT_END and block.timestamp < self.VALIDATION_START
    assert not self.validation_addr
    assert self.balance > Casper(self.CASPER_ADDR).MIN_DEPOSIT_SIZE()
    # Vyper has no fallback function at this moment, might use __receive__() in the future
    # https://github.com/ethereum/vyper/issues/781
    Casper(self.CASPER_ADDR).deposit(self.validation_addr, self, value=self.balance)

@public
def logout_from_casper(logout_msg: bytes <= 1024):
    assert block.timestamp >= self.VALIDATION_END
    Casper(self.CASPER_ADDR).logout(logout_msg)

@public
def withdraw_from_casper():
    validator_index: int128 = Casper(self.CASPER_ADDR).validator_indexes(self.validation_addr)
    Casper(self.CASPER_ADDR).withdraw(validator_index)
    self.final_balance = self.balance

@public
def withdraw_from_pool(depositor_index:int128):
    ratio: decimal = self.depositors[depositor_index].shares / self.total_shares
    send(self.depositors[depositor_index].withdraw_addr, floor(ratio * self.final_balance))
