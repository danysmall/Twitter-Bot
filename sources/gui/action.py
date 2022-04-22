from tkinter import ttk


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
