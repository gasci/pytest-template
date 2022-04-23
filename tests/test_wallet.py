import repackage

repackage.up()

import pytest
from wallet import Wallet, InsufficientAmount


@pytest.fixture
def empty_wallet():
    """Returns a Wallet instance with a zero balance"""
    return Wallet()


@pytest.fixture
def wallet_20():
    """Returns a Wallet instance with a balance of 20"""
    return Wallet(20)


def test_default_initial_amount(empty_wallet):
    assert empty_wallet.balance == 0


def test_setting_initial_amount(wallet_20):
    assert wallet_20.balance == 20


def test_wallet_spend_cash(wallet_20):
    wallet_20.spend_cash(10)
    assert wallet_20.balance == 10


# multiple fixtures
def test_wallet_add_cash(wallet_20, empty_wallet):
    wallet_20.add_cash(80)
    empty_wallet.add_cash(80)
    assert empty_wallet.balance == 80 and wallet_20.balance == 100


def test_wallet_spend_cash_raises_exception_on_insufficient_amount(empty_wallet):
    with pytest.raises(InsufficientAmount):
        empty_wallet.spend_cash(100)


@pytest.mark.parametrize(
    "earned,spent,expected",
    [
        (30, 10, 20),
        (20, 2, 18),
    ],
)
def test_transactions(empty_wallet, earned, spent, expected):
    empty_wallet.add_cash(earned)
    empty_wallet.spend_cash(spent)
    assert empty_wallet.balance == expected
