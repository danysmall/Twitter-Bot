from tkinter import ttk
from typing import Callable


class AccountsFrame(ttk.LabelFrame):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._count = 15
        self._accounts_count_label = ttk.Label(
            self, text=f'Всего аккаунтов: {self._count}')

        self._del_btn = ttk.Button(
            self, text='Удалить аккаунт', width=24)
        self._add_btn = ttk.Button(
            self, text='Добавить аккаунт', width=24)

        self._accounts_count_label.grid(column=0, row=0, sticky='w', padx=10)
        self._del_btn.grid(column=0, row=1, sticky='new', padx=10)
        self._add_btn.grid(column=1, row=1, sticky='new')

    @property
    def count(self: 'AccountsFrame') -> int:
        return self._count

    @count.setter
    def count(self: 'AccountsFrame', value: int) -> None:
        self._count = value
        self._accounts_count_label.configure(
            text=f'Всего аккаунтов: {self._count}')

    @property
    def add_account_func(self: 'AccountsFrame') -> Callable:
        return self._add_btn.cget('command')

    @add_account_func.setter
    def add_account_func(self: 'AccountsFrame', function: Callable) -> None:
        self._add_btn.configure(command=function)

    @property
    def del_account_func(self: 'AccountsFrame') -> Callable:
        return self._del_btn.cget('command')

    @del_account_func.setter
    def del_account_func(self: 'AccountsFrame', function: Callable) -> None:
        self._del_btn.configure(command=function)
