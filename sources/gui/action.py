from tkinter import ttk, BooleanVar, StringVar


class ActionFrame(ttk.LabelFrame):
    """Action pannel with checkboxes and buttons."""
    MASK_MAX_INT_LEN = 4
    CYFRALS_STR = [str(i) for i in range(10)]

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
            self, text='Количество аккаунтов: ')

        self._account_count_var = StringVar()
        self._account_count = ttk.Entry(
            self, name='account_count', textvariable=self._account_count_var)
        self._bind_int_mask(
            self._account_count,
            self._account_count_var)

        self._account_count_label.grid(
            column=0, row=1, columnspan=2, sticky='w', padx=10, pady=(15, 5))
        self._account_count.grid(
            column=2, row=1, columnspan=2, sticky='ew', pady=(15, 5))

        self._max_accounts_alive_label = ttk.Label(
            self, text='Одновременных аккаунтов: ')

        self._max_accounts_alive_var = StringVar()
        self._max_accounts_alive = ttk.Entry(
            self, name='max_account',
            textvariable=self._max_accounts_alive_var)
        self._bind_int_mask(
            self._max_accounts_alive,
            self._max_accounts_alive_var)

        self._max_accounts_alive_label.grid(
            column=0, row=10, columnspan=2, sticky='w')
        self._max_accounts_alive.grid(
            column=2, row=10, columnspan=2, sticky='ew')

    def _bind_int_mask(
        self: 'ActionFrame',
        entity: ttk.Entry,
        variable: StringVar
    ) -> None:
        def bind_function(_):
            self._input_int_mask(_, variable)
        entity.bind('<KeyPress>', bind_function)
        entity.bind('<KeyRelease>', bind_function)

    def _input_int_mask(self: 'ActionFrame', _, entity) -> None:
        temp = entity.get()
        changed = ''
        for index, char in enumerate(temp):
            if index > ActionFrame.MASK_MAX_INT_LEN:
                break
            if char in ActionFrame.CYFRALS_STR:
                changed += char
        entity.set(changed)

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

    @property
    def max_count_accounts(self: 'ActionFrame') -> int:
        return int(self._max_accounts_alive_var.get())

    def get_checkboxes(self: 'ActionFrame') -> dict[str, bool]:
        return {
            'like': self._like_bool.get(),
            'retweet': self._retweet_bool.get(),
            'subscribe': self._subscribe_bool.get(),
            'comment': self._comment_bool.get()
        }
