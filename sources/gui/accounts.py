from tkinter import ttk


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
