from tkinter import ttk, Listbox, constants
from typing import Callable, Union
import os
from threading import Thread
from time import sleep


class AccountsFrame(ttk.LabelFrame):
    FILES_EXTENSION = '.pkl'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._scan_thread_bool = True
        self._path_to_accounts = '.\\'
        self._count = 0
        self._accounts = list()
        self._accounts_count_label = ttk.Label(
            self, text=f'Всего аккаунтов: {self._count}')

        self.accounts_logged = Listbox(
            self, selectmode=constants.SINGLE,
            width=55, height=8)
        self.accounts_logged.grid(
            column=0, row=1, columnspan=3, padx=3, pady=10)

        self._scrollbar_lgd = ttk.Scrollbar(self)
        self._scrollbar_lgd.grid(column=3, row=1, sticky='nws', pady=10)
        self._scrollbar_lgd.config(command=self.accounts_logged.yview)
        self.accounts_logged.config(yscrollcommand=self._scrollbar_lgd.set)

        self._del_btn = ttk.Button(self, text='Удалить аккаунт', width=17)
        self._add_btn = ttk.Button(self, text='Добавить аккаунт', width=17)
        self._login_btn = ttk.Button(self, text='Войти в аккаунт', width=17)

        self._accounts_count_label.grid(column=0, row=0, sticky='w', padx=3)
        self._del_btn.grid(column=0, row=10, sticky='new', padx=3)
        self._add_btn.grid(column=1, row=10, sticky='new')
        self._login_btn.grid(
            column=2, row=10, sticky='new', padx=3, columnspan=2)

    @property
    def selected_account(self: 'AccountsFrame') -> Union[str, None]:
        try:
            select_id = self.accounts_logged.curselection()[0]
            name = self.accounts_logged.get(select_id)
            return f'{self._path_to_accounts}{name}{AccountsFrame.FILES_EXTENSION}'
        except IndexError:
            return None

    @property
    def all_accounts(self: 'AccountsFrame') -> list:
        return self._accounts

    @property
    def path_to_accounts(self: 'AccountsFrame') -> str:
        return self._path_to_accounts

    @path_to_accounts.setter
    def path_to_accounts(self: 'AccountsFrame', path: str) -> None:
        self._path_to_accounts = path
        self._insert_labels()

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

    @property
    def login_account_func(self: 'AccountsFrame') -> Callable:
        return self._login_btn.cget('command')

    @login_account_func.setter
    def login_account_func(self: 'AccountsFrame', function: Callable) -> None:
        self._login_btn.configure(command=function)

    def delete_account(self: 'AccountsFrame') -> None:
        select = self.accounts_logged.curselection()[0]
        filename = self.accounts_logged.get(select)
        self.accounts_logged.delete(select)
        self._delete_account_file(filename)

    def _delete_account_file(self: 'AccountsFrame', filename: str) -> None:
        try:
            os.remove('{path}{filename}{ext}'.format(
                path=self._path_to_accounts,
                filename=filename,
                ext=AccountsFrame.FILES_EXTENSION))
            self._accounts.remove(f'{filename}{AccountsFrame.FILES_EXTENSION}')
            self._update_count()
        except FileNotFoundError:
            pass

    def _update_count(self: 'AccountsFrame', count=None) -> None:
        if count is not None:
            self._count = count
        else:
            self._count = len(self._accounts)
        self._accounts_count_label.configure(
            text=f'Всего аккаунтов: {self._count}')

    def _find_logged_accounts(self: 'AccountsFrame') -> Union[list, None]:
        if not os.path.isdir(self._path_to_accounts):
            return None
        files = [f.path for f in os.scandir(self._path_to_accounts)
                 if f.is_file() and AccountsFrame.FILES_EXTENSION in f.path]
        return [f[f.rfind('\\') + 1:] for f in files if f.rfind('\\') > -1]

    def _insert_labels(self: 'AccountsFrame'):
        account_files = self._find_logged_accounts()
        listbox = self.accounts_logged.get(0, constants.END)

        # self.accounts_logged.delete(0, constants.END)
        if account_files is not None:
            for i in account_files:
                name = i[:i.rfind(AccountsFrame.FILES_EXTENSION)]
                if name not in listbox:
                    print(name, listbox)
                    self.accounts_logged.insert(
                        0, i[:i.rfind(AccountsFrame.FILES_EXTENSION)])

            self._accounts = account_files
            self._update_count(len(account_files))

    def _scan_thread(self: 'AccountsFrame') -> None:
        while self._scan_thread_bool:
            self._insert_labels()
            sleep(2)

    def start_scan(self: 'AccountsFrame') -> None:
        thread = Thread(target=self._scan_thread)
        thread.start()

    def stop_scan(self: 'AccountsFrame') -> None:
        self._scan_thread_bool = False
