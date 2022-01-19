import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    print("print empty bank account")
    return BankAccount()

@pytest.fixture

def bank_account():
    return BankAccount(50)



@pytest.mark.parametrize("num1, num2, expected", [

    (3, 2, 5),
    (7, 1, 8),
    (12,4, 16)

])



def test_add(num1, num2, expected):
    #print("testing add function")
    #sum = add(5,3)
    assert add(num1, num2) == expected

def test_subtract():

    assert subtract(9,4) == 5

def test_multiply():
    assert multiply(5,4) == 20

def test_divide():
    assert divide(10,2)  == 5

def test_bank_initial_Balance(bank_account):
    #bank_account = BankAccount(50)

    assert bank_account.balance == 50

def test_bank_default_balance(zero_bank_account):
    #bank_account = BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    #bank_account = BankAccount(50)
    #if amount > self.balance:
        #raise Exception("insufficent funds in amount")
    #self.balance = amount
    bank_account.withdraw(30)
    assert bank_account.balance == 20

def test_deposit(bank_account):
    #bank_account = BankAccount(50)
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest(bank_account):
    #bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [

    (200, 100, 100),
    (30, 10, 20),
    (1000,200,800)




])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):

    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)

    assert zero_bank_account.balance == expected


def test_insufficent_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)




    
