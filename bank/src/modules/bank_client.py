import logging

from bank.src.modules.banking_system import (
    BankingSystem
)


class BankCLI:
    def __init__(
        self
    ) -> None:
        self.bank: object = BankingSystem()
        self.operations: dict[str, object] = {
            'create': self._createAccount,
            'close': self._closeAccount,
            'reopen': self._reopenAccount,
            'deposit': self._deposit,
            'withdrawal': self._withdrawal,
            'statement': self._displayBankStatement,
            'exit': self._exit
        }

    def run(
        self
    ) -> None:
        logging.info(
            '\nWelcome to our bank!\n'
        )

        while True:
            logging.info(
                '\nHere is a list of available operations:\n'
            )

            for operation in self.operations:
                logging.info(
                    operation
                )

            op: str = input(
                "\nWhat operation do you wish to do now?\n"
            ) \
                .strip() \
                .lower()

            try:
                self.operations[op]()
            except SystemExit:
                break

    def _createAccount(
        self
    ) -> None:
        name: str = input(
            "\nProvide holder's name:\n"
        ) \
            .strip() \
            .lower()
        credit: float = float(
            input(
                "\nProvide the amount you are starting with:\n"
            )
        )

        self.bank.createAccount(
            account_holder=name,
            initial_credit=credit
        )

    def _closeAccount(
        self
    ) -> None:
        name: str = input(
            "\nProvide holder's name:\n"
        ) \
            .strip() \
            .lower()

        self.bank.closeAccount(
            account_holder=name
        )

    def _reopenAccount(
        self
    ) -> None:
        name: str = input(
            "\nProvide holder's name:\n"
        ) \
            .strip() \
            .lower()

        self.bank.reopenAccount(
            account_holder=name
        )

    def _deposit(
        self
    ) -> None:
        name: str = input(
            "\nProvide holder's name:\n"
        ) \
            .strip() \
            .lower()

        amount = float(
            input(
                "\nProvide the amount you want to deposit:\n"
            )
        )

        self.bank.deposit(
            account_holder=name,
            deposited_amount=amount
        )

    def _withdrawal(
        self
    ) -> None:
        name: str = input(
            "\nProvide holder's name:\n"
        ) \
            .strip() \
            .lower()
        amount = float(
            input(
                "\nProvide the amount you want to withdraw:\n"
            )
        )

        self.bank.withdrawal(
            account_holder=name,
            withdrawed_amount=amount
        )

    def _displayBankStatement(
        self
    ) -> None:
        name: str = input(
            "\nProvide holder's name:\n"
        ) \
            .strip() \
            .lower()

        self.bank.displayBankStatement(
            account_holder=name
        )

    def _exit(
        self
    ) -> None:
        is_exit: str = input("\nAre you sure you want to exit? (y/n)\n").strip().lower()
        if is_exit == 'y':
            logging.info('\nEnding session on user request\n')
            logging.info('\nThanks for visiting our bank!')
            raise SystemExit
        elif is_exit == 'n':
            logging.info('\nReturning to menu..\n')
        else:
            logging.warning(f'\nThe command {is_exit} is not a valid command!\n')
            logging.info('\nReturning to menu..\n')
