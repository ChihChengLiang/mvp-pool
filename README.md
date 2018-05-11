# Minimalism Pool for Casper

[![Gitter](https://badges.gitter.im/ethereum/casper.svg)](https://gitter.im/ethereum/casper?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

[![Build Status](https://travis-ci.org/ChihChengLiang/mvp-pool.svg?branch=master)](https://travis-ci.org/ChihChengLiang/mvp-pool)

## Motivation

Since the Casper FFG is implemented with a minimal deposit requirement, an alternative for people who have not enought deposit is to form a staking pool.


## Terms & Definitions

- Validator: who deposit in the Casper FFG contract.
- Depositor: who deposit in the staking pool

## Forms

### Centralized staking pool

A single trusted operater votes and promises some SLA.

This pool is for users who consider staking profitable and are willing to trust a delegated voter. They help the pool meet the minial deposit requirement, and the pool distributes some profit to them.


This will be the first stage mvp pool we are targeting.

> complication: lazy or malcious operator


### Decentralized staking pool

The depositors collectively vote in the pool between every epochs, the pool makes final vote to the main chain.

This pool enables users to participate the network consensus. Their 10 Ether vote now is as important as 1e-5 times of 1M ether, instead of zero. Note that since a pool only represents a Casper contract validator, multiple depositors have only one voice.

The pool votes should be done offline to minimize the risk of not being included in the main chain.

> complication: lazy or malicious depositor.

## The Pool

### States

- stage 1, anyone can deposit and get shares
- stage 2, when there are enough depositors it deposits into the casper contract, then the operator validates
- stage 3, at some point it auto-withdraws, and then share holders get their ETH back


- waiting for deposit
- validator online
- waiting for withdrawal

### Deposit

> Possible design: A pool owner approve deposit of trusted depositors.

depositors deposit Ether in pool, and the pool records shares for each depositor.

- for decentralized pool, this needs signature validation contract deployed

### Validating

Not much to say for centralized staking pool. the operator poke the pool `vote`


### Exit

The pool has a specific duration, say 6 or 12 months. When a specified `exit_time` is reached, the pool automatically logs out the Casper FFG contract.

> we have withdraw delay 4 month, that means the pool might not have too short period like 1 or 3 months.

This minimizes the complexity of design, no dynamic depositor enter or exit scheme.

After the withdrawal delay, any validator can trigger the pool `withdrawal` function. The pool then withdraws from the Casper FFG contract, and distributes the depositors by their shares.


### Contingencies

Red button: Thresholded votes for shutting down the contract. The pool immediately logs out the Casper FFG contract.

> Might suffer 700 dynasties of validator inaction.


## Tentative Implementation

see `pool.v.py`