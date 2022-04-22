from tkinter import Tk
from gui import ActionFrame, AccountsFrame, ProxyFrame, LogsFrame


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


if __name__ == '__main__':
    window = MainWindow()
    window.start()
