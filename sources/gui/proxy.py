from tkinter import ttk, Text, constants


class ProxyFrame(ttk.LabelFrame):
    AVALIABLE_CHARS = [str(i) for i in range(10)] + ['.', ':', '\n', '\r']

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

        self._proxy_view.bind('<KeyPress>', self._input_proxy_mask)
        self._proxy_view.bind('<KeyRelease>', self._input_proxy_mask)

    def _input_proxy_mask(self: 'ProxyFrame', _):
        text = self._proxy_view.get('1.0', constants.END)[:-1]
        changed = ''
        for char in text:
            if char in ProxyFrame.AVALIABLE_CHARS:
                changed += char
        self._proxy_view.delete('1.0', constants.END)
        self._proxy_view.insert('1.0', changed)

    @property
    def proxy_list(self: 'ProxyFrame') -> list:
        proxy_str = self._proxy_view.get(1.0, constants.END)
        try:
            return proxy_str.split('\n')
        except TypeError:
            return list()

    def disable_input(self: 'ProxyFrame') -> None:
        self._proxy_view.configure(state='disabled')

    def enable_input(self: 'ProxyFrame') -> None:
        self._proxy_view.configure(state='normal')
