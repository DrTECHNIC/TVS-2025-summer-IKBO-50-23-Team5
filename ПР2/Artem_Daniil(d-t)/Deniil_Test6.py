from unittest.mock import patch
from Artem_With_Errors1 import BankAccount


class TestBankAccount:

    def setup_method(self):
        with patch.object(BankAccount, 'main_cycle'):
            self.account = BankAccount()

    def test_initial_state(self):
        assert self.account.balance == 0
        assert self.account.operation_history == []
        assert self.account.has_loan == False
        assert self.account.loan_sum == 0
        assert 1000000 <= self.account.id <= 9999999

    @patch('builtins.input')
    def test_deposit_positive_amount(self, mock_input):
        mock_input.return_value = '1000'
        self.account.deposit()
        assert self.account.balance == 1000
        assert self.account.operation_history == [1000]

    @patch('builtins.input')
    @patch('builtins.print')
    def test_deposit_negative_amount(self, mock_print, mock_input):
        mock_input.return_value = '-500'
        self.account.deposit()
        assert self.account.balance == 0
        assert self.account.operation_history == []
        mock_print.assert_any_call("Invalid amount")

    @patch('builtins.input')
    def test_withdraw_valid_amount(self, mock_input):
        self.account.balance = 2000
        mock_input.return_value = '500'
        self.account.withdraw()
        assert self.account.balance == 1500
        assert self.account.operation_history == [-500]

    @patch('builtins.input')
    @patch('builtins.print')
    def test_withdraw_insufficient_funds(self, mock_print, mock_input):
        self.account.balance = 100
        mock_input.return_value = '500'
        self.account.withdraw()
        assert self.account.balance == 100
        assert self.account.operation_history == []
        mock_print.assert_any_call("Invalid amount")

    @patch('builtins.input')
    def test_withdraw_correct_prompt_text(self, mock_input):
        mock_input.return_value = '100'
        self.account.balance = 1000
        self.account.withdraw()
        input_calls = mock_input.call_args_list
        first_call_text = input_calls[0][0][0].lower()
        assert 'withdraw' in first_call_text
        assert 'deposit' not in first_call_text

    @patch('builtins.input')
    @patch('builtins.print')
    def test_view_history_formatting(self, mock_print, mock_input):
        mock_input.return_value = ''
        self.account.operation_history = [1000, -500, 200]
        self.account.view_history()
        calls = [call[0][0] if call[0] else '' for call in mock_print.call_args_list]
        operation_outputs = [call for call in calls if isinstance(call, str) and call.strip() and
                             not call.startswith('Operation history')]
        positive_operations = [op for op in operation_outputs if op.startswith('+')]
        negative_operations = [op for op in operation_outputs if op.startswith('-')]
        assert len(positive_operations) == 2
        assert len(negative_operations) == 1

    @patch('builtins.input')
    def test_pay_loan_negative_amount(self, mock_input):
        self.account.has_loan = True
        self.account.loan_sum = 5000
        self.account.balance = 6000
        initial_balance = self.account.balance
        initial_loan = self.account.loan_sum
        mock_input.return_value = '-1000'
        self.account.pay_loan()
        assert self.account.loan_sum == initial_loan
        assert self.account.balance == initial_balance

    @patch('builtins.input')
    def test_pay_loan_insufficient_funds(self, mock_input):
        self.account.has_loan = True
        self.account.loan_sum = 5000
        self.account.balance = 1000
        initial_balance = self.account.balance
        initial_loan = self.account.loan_sum
        mock_input.return_value = '3000'
        self.account.pay_loan()
        assert self.account.loan_sum == initial_loan
        assert self.account.balance == initial_balance

    @patch('builtins.input')
    def test_pay_loan_more_than_debt(self, mock_input):
        self.account.has_loan = True
        self.account.loan_sum = 1000
        self.account.balance = 5000
        initial_balance = self.account.balance
        mock_input.return_value = '2000'
        self.account.pay_loan()
        assert self.account.loan_sum == 0
        assert self.account.balance == initial_balance - 1000

    @patch('builtins.input')
    def test_pay_loan_exact_amount(self, mock_input):
        self.account.has_loan = True
        self.account.loan_sum = 1000
        self.account.balance = 5000
        mock_input.return_value = '1000'
        self.account.pay_loan()
        assert self.account.loan_sum == 0
        assert self.account.balance == 4000
        assert self.account.has_loan == False

    @patch('builtins.input')
    def test_pay_loan_partial_amount(self, mock_input):
        self.account.has_loan = True
        self.account.loan_sum = 1000
        self.account.balance = 5000
        mock_input.return_value = '500'
        self.account.pay_loan()
        assert self.account.loan_sum == 500
        assert self.account.balance == 4500
        assert self.account.has_loan == True
