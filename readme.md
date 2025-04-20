# DIO Banking Class Project

*Code developed for the DIO Banking Class.*  
Class example available at:  
[GitHub Link](https://github.com/digitalinnovationone/trilha-python-dio/blob/main/00%20-%20Fundamentos/desafio.py)

---

## Overview

This project demonstrates the use of classes to build a more complete and modular banking system, improving upon the original one-file example.

### Key Features

- Git integration  
- Python OOP principles  
- Best practices (modularity, flake8 linting, type hinting)  
- A more robust and extensible system architecture compared to the initial one-time execution script

---

## Project Structure

*Main executable:* run.py

### Modules

- bank_client:  
  Handles core banking operations—account creation, closing, reopening, deposits, withdrawals, and generating account statements.

- banking_system:  
  Manages user interaction and client operations.

- utils:  
  Currently includes a hash input function (extendable for more utilities).

- persist_data:  
  Manages data persistence via JSON files, organized by account holders.

- __main__:  
  Contains the application execution logic.

---

## TODO

- [ ] Add class and function-level docstrings  
- [ ] Implement input validation and error handling
- [ ] Add unit testing
- [ ] Extend system with more complex class structures and models, adding more features and operations
