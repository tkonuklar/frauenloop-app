import unittest
from .account import display_balance

class TestAccount(unittest.TestCase):
    '''
    Testing account.py
    '''
    def test_display_balance_correct_pin_user1(self):
        balance = display_balance(1234, 'user1')
        self.assertEqual(balance, 'This is your current balance: 100 EUR')

    def test_display_balance_correct_pin_user2(self):
        balance = display_balance(5576, 'user2')
        self.assertEqual(balance, 'This is your current balance: 100 EUR')

    def test_display_balance_correct_pin_user3(self):
        balance = display_balance(2293, 'user3')
        self.assertEqual(balance, 'This is your current balance: 100 EUR')

    def test_display_balance_incorrect_pin(self):
        balance = display_balance(2299, 'user1')
        self.assertEqual(balance, 'Access denied: incorrect PIN.')

if __name__ == '__main__':
    unittest.main()