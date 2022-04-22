from tkinter import ttk, Tk, Text, constants
from datetime import datetime
import typing


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
        self._accounts_frame.grid(column=0, row=10, sticky='new', padx=15, pady=5)

        self._proxy_frame = ProxyFrame(
            self._root, text='Список прокси', padding='10 10 10 10')
        self._proxy_frame.grid(column=0, row=20, sticky='new', padx=15, pady=5)

        self._logs_frame = LogsFrame(
            self._root, text='Логи работы', padding='10 10 10 10')
        self._logs_frame.grid(column=0, row=100, sticky='new', padx=15, pady=5)

    @property
    def logs_frame(self: 'MainWindow') -> 'LogsFrame':
        return self._logs_frame

    @property
    def action_frame(self: 'MainWindow') -> 'ActionFrame':
        return self._action_frame

    def _on_close(self: 'MainWindow') -> None:
        """Destroy all threads and close all windows."""
        self._root.destroy()

    def start(self: 'MainWindow') -> None:
        self._root.mainloop()


class LogsFrame(ttk.LabelFrame):
    """Frame with elements and actions to log panel."""

    def __init__(self: 'LogsFrame', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._logs_view = Text(
            self,
            width=40,
            height=5,
            wrap=constants.WORD,
            state='disabled')
        self._logs_view.grid(column=0, row=0)

        self._logs_scroll = ttk.Scrollbar(self)
        self._logs_scroll.grid(column=1, row=0, sticky='ns')
        self._logs_scroll.config(command=self._logs_view.yview)
        self._logs_view.config(yscrollcommand=self._logs_scroll.set)

        self._clear_btn = ttk.Button(
            self,
            text='Очистить логи',
            command=self._clear_logs)
        self._clear_btn.grid(column=0, row=1, sticky='ew')

    def _clear_logs(self: 'LogsFrame') -> None:
        self._logs_view.config(state='normal')
        self._logs_view.delete('1.0', constants.END)
        self._logs_view.config(state='disabled')

    def send_logs(
        self: 'LogsFrame',
        message: typing.Union[list, str]
    ) -> None:
        """Send logs to frame in special format."""
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        if isinstance(message, list):
            message = '\n'.join(
                [f'[{now}]: {i}' for i in message]) + '\n'

        elif isinstance(message, str):
            message = f'[{now}]: {message}\n'

        else:
            raise TypeError('Argument message must be str or list')

        self._logs_view.configure(state='normal')
        self._logs_view.insert('1.0', message)
        self._logs_view.configure(state='disabled')


class ActionFrame(ttk.LabelFrame):
    """Action pannel with checkboxes and buttons."""

    def __init__(self: 'ActionFrame', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._like_check = ttk.Checkbutton(self, text='Лайк')
        self._retweet_check = ttk.Checkbutton(self, text='Ретвит')
        self._subscribe_check = ttk.Checkbutton(self, text='Подписка')
        self._comment_check = ttk.Checkbutton(self, text='Комментарий')

        self._like_check.grid(column=0, row=0)
        self._retweet_check.grid(column=1, row=0)
        self._subscribe_check.grid(column=2, row=0)
        self._comment_check.grid(column=3, row=0)

        self._account_count_label = ttk.Label(
            self, text='Количество аккаунтов')
        self._account_count = ttk.Entry(self)

        self._account_count_label.grid(
            column=0, row=1, columnspan=2, padx=10, pady=(15, 0))
        self._account_count.grid(
            column=2, row=1, columnspan=2, sticky='ew', pady=(15, 0))


class ProxyFrame(ttk.LabelFrame):

    def __init__(self: 'LogsFrame', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._proxy_view = Text(
            self,
            width=40,
            height=10,
            wrap=constants.WORD,
            state='normal')
        self._proxy_view.grid(column=0, row=0)

        self._proxy_scroll = ttk.Scrollbar(self)
        self._proxy_scroll.grid(column=1, row=0, sticky='ns')
        self._proxy_scroll.config(command=self._proxy_view.yview)
        self._proxy_view.config(yscrollcommand=self._proxy_scroll.set)

    @property
    def proxy_list(self):
        return self._proxy_view.get()


class AccountsFrame(ttk.LabelFrame):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._count = 15
        self._accounts_count_label = ttk.Label(
            self, text=f'Всего аккаунтов: {self._count}')

        self._del_btn = ttk.Button(
            self, text='Удалить аккаунт', command=self._del_account, width=24)
        self._add_btn = ttk.Button(
            self, text='Добавить аккаунт', command=self._add_account, width=24)

        self._accounts_count_label.grid(column=0, row=0, sticky='w', padx=10)
        self._del_btn.grid(column=0, row=1, sticky='new', padx=10)
        self._add_btn.grid(column=1, row=1, sticky='new')

    @property
    def count(self: 'AccountsFrame') -> int:
        return self._count

    @count.setter
    def count(self: 'AccountsFrame', value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f'Argument must be int, not {type(value)}')
        self._count = value
        self._accounts_count_label.configure(
            'text', f'Всего аккаунтов: {self._count}')

    def _add_account(self) -> None:
        pass

    def _del_account(self) -> None:
        pass


if __name__ == '__main__':
    window = MainWindow()
    window.start()
