from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100

    transaction = fund_me.fund({"from": account, "value": entrance_fee})
    transaction.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    transaction2 = fund_me.withdraw({"from": account})
    transaction2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    # We want to test if the tx effectively revert
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})


def main():
    test_fund_and_withdraw()
    test_only_owner_can_withdraw()
