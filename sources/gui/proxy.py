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
    def proxy_list(self: 'ProxyFrame') -> list:
        proxy_str = self._proxy_view.get(1.0, constants.END)
        try:
            return proxy_str.split('\n')
        except TypeError:
            print('Error of getting list of proxy')
            return list()

    def disable_input(self: 'ProxyFrame') -> None:
        self._proxy_view.configure(state='disabled')

    def enable_input(self: 'ProxyFrame') -> None:
        self._proxy_view.configure(state='normal')
