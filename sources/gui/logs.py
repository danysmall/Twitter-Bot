from tkinter import ttk, constants, Text
import typing
from datetime import datetime


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
