from tkinter import ttk, Text, constants


class ProxyFrame(ttk.LabelFrame):

    def __init__(self: 'ProxyFrame', *args, **kwargs) -> None:
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
