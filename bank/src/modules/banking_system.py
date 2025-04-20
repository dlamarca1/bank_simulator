import os
import logging
import textwrap

from datetime import datetime

from bank.src.modules.persist_data import (
    PersistBankDataJson
)
from bank.src.modules.utils import (
    hashValue
)


class BankingSystem():
    def __init__(
        self
    ) -> None:
        base_dir: str = os.path.dirname(
            __file__
        )
        dir_path: str = os.path.join(
            base_dir,
            'data'
        )
        self.accounts: object = PersistBankDataJson(
            dir_path=dir_path
        )

    def _is_holder(
        self,
        account_holder: str,
        hashed_holder: str,
        operation: str,
        is_creation: bool = False,
        is_reopening: bool = False
    ) -> bool:
        account: str = self.accounts.get(hashed_holder)

        def _handle_creation() -> bool:
            logging.info(
                f"\nCreating new account for holder: {account_holder}\n"
            )
            return False

        def _handle_existing_account() -> bool:
            logging.warning(
                f"\nAn account already exists for holder: {account_holder}!!\n"
            )
            return True

        def _handle_missing_account() -> bool:
            logging.warning(
                f"\nAccount not found for holder: {account_holder}\n"
            )
            return False

        def _handle_reopening() -> bool:
            logging.info(
                f"\nReopening closed account for holder: {account_holder}\n"
            )
            return False

        def _handle_not_closed() -> bool:
            logging.warning(
                f"\nAccount is not currently closed for holder: {account_holder}\n"
            )
            return True

        def _handle_closed_account() -> bool:
            logging.warning(
                f"\nAccount is currently closed for holder: {account_holder}\n"
            )
            return False

        def _handle_valid_account() -> bool:
            logging.info(
                f"\nAccount found for holder: {account_holder}\nExecuting operation: {operation}\n"
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
        banking_agency: int = 243,
        initial_balance: float = 0
    ) -> None:
        operation_time = datetime.now()
        operation: str = 'Account Creation'
        hashed_holder: str = hashValue(
            value=account_holder
        )

        if not self._is_holder(
            account_holder=account_holder,
            hashed_holder=hashed_holder,
            operation=operation,
            is_creation=True
        ):
            self.accounts[hashed_holder] = {
                'account_holder': account_holder,
                'banking_agency': banking_agency,
                'account': hashValue(
                    value=account_holder + str(operation_time),
                    hash_size=16
                ),
                'balance': initial_balance,
                'account_history': [
                    {
                        'operation': operation,
                        'initial_balance': f'R${initial_balance}',
                        'created_at': operation_time,
                    },
                ],
                'created_at': operation_time,
                'last_operation_at': operation_time,
                'is_closed': False,
            }
            self.accounts.update()

    def closeAccount(
        self,
        account_holder: str
    ) -> None:
        operation_time = datetime.now()
        operation: str = 'Account Closing'
        hashed_holder: str = hashValue(
            value=account_holder
        )

        if self._is_holder(
            account_holder=account_holder,
            hashed_holder=hashed_holder,
            operation=operation
        ):
            self.accounts[hashed_holder]['is_closed'] = True
            self.accounts[hashed_holder]['closed_at'] = operation_time
            self.accounts[hashed_holder]['account_history'].append(
                {
                    'operation': operation,
                    'closed_at': operation_time,
                },
            )
            self.accounts.update()

    def reopenAccount(
        self,
        account_holder: str
    ) -> None:
        operation_time = datetime.now()
        operation: str = 'Reopen Account'
        hashed_holder: str = hashValue(
            value=account_holder
        )

        if not self._is_holder(
            account_holder=account_holder,
            hashed_holder=hashed_holder,
            operation=operation,
            is_reopening=True
        ):
            was_closed = self.accounts[hashed_holder]['closed_at']

            self.accounts[hashed_holder]['is_closed'] = False
            self.accounts[hashed_holder]['reopened_at'] = operation_time
            self.accounts[hashed_holder]['closed_at'] = ''
            self.accounts[hashed_holder]['account_history'].append(
                {
                    'operation': operation,
                    'was_closed_at': was_closed,
                    'reopened_at': operation_time,
                },
            )
            self.accounts.update()

    def deposit(
        self,
        account_holder: str,
        deposited_amount: float
    ) -> None:
        operation_time = datetime.now()
        operation: str = 'Deposit'
        hashed_holder: str = hashValue(
            value=account_holder
        )

        if self._is_holder(
            account_holder=account_holder,
            hashed_holder=hashed_holder,
            operation=operation
        ):
            current_balance: int = self.accounts[hashed_holder]['balance']
            new_balance: int = current_balance + deposited_amount

            self.accounts[hashed_holder]['balance'] = new_balance
            self.accounts[hashed_holder]['account_history'].append(
                {
                    'operation': operation,
                    'current_balance': f'R${current_balance}',
                    'deposited_amount': f'R${deposited_amount}',
                    'new_balance': f'R${new_balance}',
                    'deposited_at': operation_time,
                },
            )
            self.accounts[hashed_holder]['last_operation_at'] = operation_time
            self.accounts.update()

    def withdrawal(
        self,
        account_holder: str,
        withdrawed_amount: float,
    ) -> None:
        operation_time = datetime.now()
        operation: str = 'Withdrawal'
        hashed_holder: str = hashValue(
            value=account_holder
        )

        if self._is_holder(
            account_holder=account_holder,
            hashed_holder=hashed_holder,
            operation=operation
        ):
            current_balance: int = self.accounts[hashed_holder]['balance']
            new_balance: int = current_balance - withdrawed_amount

            if new_balance < 0:
                logging.warning(
                    '\nHolder does not have enough balance for withdrawal!\n'
                )
                logging.info(
                    textwrap.dedent(
                        f'''
                        Holder balance: R${current_balance},
                        Attempted to withdraw: R${withdrawed_amount},
                        Operation Aborted
                        '''
                    )
                )
            else:
                self.accounts[hashed_holder]['balance'] = new_balance
                self.accounts[hashed_holder]['account_history'].append(
                    {
                        'operation': operation,
                        'current_balance': f'R${current_balance}',
                        'withdrawed_amount': f'R${withdrawed_amount}',
                        'new_balance': f'R${new_balance}',
                        'withdrawed_at': operation_time,
                        },
                )
                self.accounts[hashed_holder]['last_operation_at'] = operation_time
                self.accounts.update()

    def displayBankStatement(
        self,
        account_holder: str
    ) -> None:
        operation: str = 'Bank Statement Display'
        hashed_holder: str = hashValue(
            value=account_holder
        )

        if self._is_holder(
            account_holder=account_holder,
            hashed_holder=hashed_holder,
            operation=operation
        ):
            account_history: list[dict[str, any]] = self.accounts[hashed_holder]['account_history']

            for i, operation_history in enumerate(account_history, 1):
                print(f'\nOperation: {i}')
                for key, value in operation_history.items():
                    print(
                        f'  {key}: {value}'
                    )
