from tkinter import Tk, ttk
from gui import ActionFrame, AccountsFrame, ProxyFrame, LogsFrame

from typing import Union
from twitterbot import TwitterBot
from threading import Thread


class MainWindow():
    """Main GUI windows of the program."""

    def __init__(self: 'MainWindow') -> None:

        self._root = Tk()
        self._root.title('Twitter Bot')
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._action_frame = ActionFrame(
            self._root, text='Панель действий', padding='10 10 10 10')
        self._action_frame.grid(column=0, row=0, sticky='new', padx=15, pady=5)

        self._accounts_frame = AccountsFrame(
            self._root, text='Управление аккаунтами', padding='10 10 10 10')
        self._accounts_frame.grid(
            column=0, row=10, sticky='new', padx=15, pady=5)

        self._accounts_frame.add_account_func = self.add_account
        self._accounts_frame.del_account_func = self.del_account

        self._proxy_frame = ProxyFrame(
            self._root, text='Список прокси', padding='10 10 10 10')
        self._proxy_frame.grid(column=0, row=20, sticky='new', padx=15, pady=5)

        self._logs_frame = LogsFrame(
            self._root, text='Логи работы', padding='10 10 10 10')
        self._logs_frame.grid(column=0, row=100, sticky='new', padx=15, pady=5)

        self._start_btn = ttk.Button(
            self._root, text='Старт', command=self._main_loop)
        self._start_btn.grid(column=0, row=15, sticky='ew', pady=5, padx=15)

    @property
    def logs_frame(self: 'MainWindow') -> 'LogsFrame':
        return self._logs_frame

    @property
    def action_frame(self: 'MainWindow') -> 'ActionFrame':
        return self._action_frame

    def add_account(self: 'MainWindow') -> None:
        userbot = TwitterBot('127.0.0.1:80')
        bot_thread = Thread(target=userbot.login_new_user, args=('new_user',))
        bot_thread.start()
        print('Account added')

    def del_account(self: 'MainWindow') -> None:
        print('Delete account')

    def send_logs(self: 'MainWindow', message: Union[list, str]) -> None:
        self._logs_frame.send_logs(message)

    def _main_loop(self):
        self._start_btn.configure(text='Стоп')
        self._start_btn.configure(command=self._stop_main_loop)

        checkboxes = self._action_frame.get_checkboxes()
        proxy = self._proxy_frame.proxy_list
        count = self._action_frame.count_accounts
        print(checkboxes, proxy, count)

    def _stop_main_loop(self):
        self._start_btn.configure(text='Старт')
        self._start_btn.configure(command=self._main_loop)

        self._proxy_frame.enable_input()

    def _on_close(self: 'MainWindow') -> None:
        """Destroy all threads and close all windows."""
        self._root.destroy()

    def start(self: 'MainWindow') -> None:
        self._root.mainloop()


if __name__ == '__main__':
    window = MainWindow()
    window.start()
