import os
import logging
import textwrap

from datetime import datetime

from bank.src.modules.persist_data import (
    PersistBankDataJson
)


class BankingSystem():
    def __init__(
        self
    ) -> None:
        base_dir: str = os.path.dirname(__file__)
        file_path: str = os.path.join(
            base_dir,
            'data',
            'bank_account.json'
        )
        self.accounts: object = PersistBankDataJson(
            file_path=file_path
        )

    def _is_holder(
        self,
        account_holder: str,
        operation: str,
        is_creation: bool = False,
        is_reopening: bool = False
    ) -> bool:
        account = self.accounts.get(account_holder)

        def _handle_creation() -> bool:
            logging.info(
                f"\nCreating new account for holder:\n{account_holder}\n"
            )
            return False

        def _handle_existing_account() -> bool:
            logging.warning(
                f"\nAn account already exists for holder:\n{account_holder}!!\n"
            )
            return True

        def _handle_missing_account() -> bool:
            logging.warning(
                f"\nAccount not found for holder:\n{account_holder}\n"
            )
            return False

        def _handle_reopening() -> bool:
            logging.info(
                f"\nReopening closed account for holder:\n{account_holder}\n"
            )
            return False

        def _handle_not_closed() -> bool:
            logging.warning(
                f"\nAccount is not currently closed for holder:\n{account_holder}\n"
            )
            return True

        def _handle_closed_account() -> bool:
            logging.warning(
                f"\nAccount is currently closed for holder:\n{account_holder}\n"
            )
            return False

        def _handle_valid_account() -> bool:
            logging.info(
                f"\nAccount found for holder:\n{account_holder}\nExecuting operation:\n{operation}\n"
            )
            return True

        if is_creation:
            return _handle_creation() if account is None else _handle_existing_account()
        if account is None:
            return _handle_missing_account()
        if is_reopening:
            return _handle_reopening() if account.get("is_closed") else _handle_not_closed()
        if account.get("is_closed"):
            return _handle_closed_account()

        return _handle_valid_account()

    def createAccount(
        self,
        account_holder: str,
        initial_credit: float = 0
    ) -> None:
        operation_time = datetime.now()
        operation: str = 'Account Creation'

        if not self._is_holder(
            account_holder=account_holder,
            operation=operation,
            is_creation=True
        ):
            self.accounts[account_holder] = {
                'credit': initial_credit,
                'account_history': [
                    textwrap.dedent(
                        f'''
                        Initial Account Credit: R${initial_credit}
                        Created At: {operation_time}
                        '''
                    )
                ],
                'created_at': operation_time,
                'last_operation_at': operation_time,
                'is_closed': False
            }

    def closeAccount(
            self,
            account_holder: str
            ) -> None:
        operation_time = datetime.now()
        operation: str = 'Account Closing'

        if self._is_holder(
            account_holder=account_holder,
            operation=operation
        ):
            self.accounts[account_holder]['is_closed'] = True
            self.accounts[account_holder]['closed_at'] = operation_time
            self.accounts[account_holder]['account_history'].append(
                textwrap.dedent(
                    f'''
                    Closing Operation
                    Closed At: {operation_time}
                    '''
                )
            )
            self.accounts.update()

    def reopenAccount(
            self,
            account_holder: str
            ) -> None:
        operation_time = datetime.now()
        operation: str = 'Reopen Account'

        if not self._is_holder(
            account_holder=account_holder,
            operation=operation,
            is_reopening=True
        ):
            was_closed = self.accounts[account_holder]['closed_at']

            self.accounts[account_holder]['is_closed'] = False
            self.accounts[account_holder]['reopened_at'] = operation_time
            self.accounts[account_holder]['closed_at'] = ''
            self.accounts[account_holder]['account_history'].append(
                textwrap.dedent(
                    f'''
                    Reopening Operation
                    Was Closed At: {was_closed}
                    Reopened At: {operation_time}
                    '''
                )
            )
            self.accounts.update()

    def deposit(
            self,
            account_holder: str,
            deposited_amount: float
            ) -> None:
        operation_time = datetime.now()
        operation: str = 'Deposit'

        if self._is_holder(
            account_holder=account_holder,
            operation=operation
        ):
            current_credit: int = self.accounts[account_holder]['credit']
            new_credit: int = current_credit + deposited_amount

            self.accounts[account_holder]['credit'] = new_credit
            self.accounts[account_holder]['account_history'].append(
                textwrap.dedent(
                    f'''
                    Deposit Operation
                    Current Credit: R${current_credit}
                    Amount Deposited: R${deposited_amount}
                    New Credit: R${new_credit}
                    Deposited At: {operation_time}
                    '''
                )
            )
            self.accounts[account_holder]['last_operation_at'] = operation_time
            self.accounts.update()

    def withdrawal(
            self,
            account_holder: str,
            withdrawed_amount: float,
            ) -> None:
        operation_time = datetime.now()
        operation: str = 'Withdrawal'

        if self._is_holder(
            account_holder=account_holder,
            operation=operation
        ):
            current_credit: int = self.accounts[account_holder]['credit']
            new_credit: int = current_credit - withdrawed_amount

            if new_credit < 0:
                logging.warning(
                    '\nHolder does not have enough credit to withdrawal: R${0}\nHolder credit: R${1}\nOperation Aborted'
                    .format(withdrawed_amount, current_credit)
                )
            else:
                self.accounts[account_holder]['credit'] = new_credit
                self.accounts[account_holder]['account_history'].append(
                    textwrap.dedent(
                        f'''
                        Withdrawal Operation
                        Current Credit: R${current_credit}
                        Amount Withdrawed: R${withdrawed_amount}
                        New Credit: R${new_credit}
                        Withdrawed At: {operation_time}
                        '''
                    )
                )
                self.accounts[account_holder]['last_operation_at'] = operation_time
                self.accounts.update()

    def displayBankStatement(
            self,
            account_holder: str
            ) -> None:
        operation: str = 'Bank Statement Display'

        if self._is_holder(
            account_holder=account_holder,
            operation=operation
        ):
            account_history = self.accounts[account_holder]['account_history']
            for operation_history in account_history:
                logging.info(
                    operation_history
                )
