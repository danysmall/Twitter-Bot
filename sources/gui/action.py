from tkinter import ttk, BooleanVar


class ActionFrame(ttk.LabelFrame):
    """Action pannel with checkboxes and buttons."""

    def __init__(self: 'ActionFrame', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._like_bool = BooleanVar(value=False)
        self._retweet_bool = BooleanVar(value=False)
        self._subscribe_bool = BooleanVar(value=False)
        self._comment_bool = BooleanVar(value=False)

        self._like_check = ttk.Checkbutton(
            self, text='Лайк', variable=self._like_bool)
        self._retweet_check = ttk.Checkbutton(
            self, text='Ретвит', variable=self._retweet_bool)
        self._subscribe_check = ttk.Checkbutton(
            self, text='Подписка', variable=self._subscribe_bool)
        self._comment_check = ttk.Checkbutton(
            self, text='Комментарий', variable=self._comment_bool)

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

    @property
    def is_like(self: 'ActionFrame') -> bool:
        return self._like_bool.get()

    @property
    def is_retweet(self: 'ActionFrame') -> bool:
        return self._retweet_bool.get()

    @property
    def is_subscribe(self: 'ActionFrame') -> bool:
        return self._subscribe_bool.get()

    @property
    def is_comment(self: 'ActionFrame') -> bool:
        return self._comment_bool.get()

    @property
    def count_accounts(self: 'ActionFrame') -> int:
        try:
            return int(self._account_count.get())
        except ValueError:
            return 0

    def get_checkboxes(self: 'ActionFrame') -> dict[str, bool]:
        return {
            'like': self._like_bool.get(),
            'retweet': self._retweet_bool.get(),
            'subscribe': self._subscribe_bool.get(),
            'comment': self._comment_bool.get()
        }
