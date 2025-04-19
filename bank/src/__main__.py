import logging

from bank.src.modules import (
    BankCLI
)


def main():
    logging.basicConfig(level=logging.INFO)

    client: object = BankCLI()
    client.run()
