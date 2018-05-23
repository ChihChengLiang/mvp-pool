class Casper():
    @public
    @constant
    def PURITY_CHECKER() -> address: pass

    @public
    @constant
    def MIN_DEPOSIT_SIZE() -> int128(wei): pass

    @public
    @constant
    def current_epoch() -> int128: pass

    @public
    @constant
    def validator_indexes(validator_address: address) -> int128: pass

    @public
    @payable
    def deposit(validation_addr: address, withdrawal_addr: address): pass

    @public
    def logout(logout_msg: bytes <= 1024): pass

    @public
    def withdraw(validator_index: int128): pass


DEPOSIT_START: public(int128)
DEPOSIT_END: public(int128)
VALIDATION_START: public(int128)
VALIDATION_END: public(int128)
CASPER_ADDR: public(address)
OPERATOR: address
MIN_TOTAL_DEPOSIT: public(int128(wei))
MIN_INDIVIDUAL_DEPOSIT: public(int128(wei))
depositors: public({
    withdraw_addr: address,
    shares: int128(wei)
}[int128])
total_shares: public(int128(wei))
next_depositor_index: public(int128)
depositor_indexes: public(int128[address])
final_balance: public(int128(wei))
# The index recorded in Casper contract, meaning which validator the pool represents.
validator_index: public(int128)
can_withdraw_from_pool: public(bool)


@public
def __init__(
    casper_addr: address, deposit_start: int128,
    deposit_to_pool_time: int128, deposit_to_casper_time: int128,
    validation_time: int128, operator: address,
    min_total_deposit: int128(wei), min_individual_deposit: int128(wei)):
    self.CASPER_ADDR = casper_addr
    self.DEPOSIT_START = deposit_start
    self.DEPOSIT_END = deposit_start + deposit_to_pool_time
    self.VALIDATION_START = self.DEPOSIT_END + deposit_to_casper_time
    self.VALIDATION_END = self.VALIDATION_START + validation_time
    self.OPERATOR = operator

    assert min_total_deposit >= Casper(self.CASPER_ADDR).MIN_DEPOSIT_SIZE()
    self.MIN_TOTAL_DEPOSIT = min_total_deposit
    self.MIN_INDIVIDUAL_DEPOSIT = min_individual_deposit

    self.next_depositor_index = 1
    self.total_shares = 0


@public
@payable
def deposit_to_pool(withdraw_addr: address):
    assert msg.value >= self.MIN_INDIVIDUAL_DEPOSIT
    assert not self.depositor_indexes[withdraw_addr]
    assert block.number >= self.DEPOSIT_START and block.number < self.DEPOSIT_END
    self.depositors[self.next_depositor_index] = {
        withdraw_addr: withdraw_addr,
        shares: msg.value
    }
    self.depositor_indexes[withdraw_addr] = self.next_depositor_index
    self.next_depositor_index += 1
    self.total_shares += msg.value


@public
def deposit_to_casper(validation_addr: address):
    assert msg.sender == self.OPERATOR  # Only the operator can do this
    assert block.number >= self.DEPOSIT_END and block.number < self.VALIDATION_START
    assert self.balance >= self.MIN_TOTAL_DEPOSIT
    # Use the following when `value` is supported in Vyper
    # Casper(self.CASPER_ADDR).deposit(validation_addr, self, value=self.balance)
    raw_call(
        self.CASPER_ADDR,
        concat('\xf9\x60\x9f\x08', convert(validation_addr, 'bytes32'), convert(self, 'bytes32')),
        gas=500000,
        outsize=0,
        value=self.balance
        )
    self.validator_index = Casper(self.CASPER_ADDR).validator_indexes(self)


@public
def logout_from_casper(logout_msg:bytes <= 1024):
    # Any depositor or the operator can logout, when validation ends
    assert msg.sender == self.OPERATOR or self.depositor_indexes[msg.sender] > 0
    assert block.number >= self.VALIDATION_END
    Casper(self.CASPER_ADDR).logout(logout_msg)


@public
def withdraw_from_casper():
    # Anyone, after withdraw dynasty in Casper
    Casper(self.CASPER_ADDR).withdraw(self.validator_index)
    self.final_balance = self.balance
    self.can_withdraw_from_pool = True


@private
def delete_depositor(index: int128):
    self.depositor_indexes[self.depositors[index].withdraw_addr] = 0
    self.depositors[index] = {
        withdraw_addr: None,
        shares: 0
    }


@public
def withdraw_from_pool(depositor_index: int128):
    assert self.can_withdraw_from_pool
    ratio: decimal = self.depositors[depositor_index].shares / \
        self.total_shares
    send(self.depositors[depositor_index].withdraw_addr,
         floor(ratio * self.final_balance))
    # depositors already withdrawn can't withdraw again
    self.delete_depositor(depositor_index)
