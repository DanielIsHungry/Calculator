import ttkbootstrap as ttk
from tkinter import TclError
from random import choice

class Application:
    def __init__(self, root):
        self.root = root
        self.root.geometry('650x450')

        self.buttons = {}

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky='nsew')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.display_frame = ttk.Frame(self.main_frame)
        self.display_frame.grid(row=0, column=0, columnspan=4, sticky='nsew')

        self.answer_frame = ttk.Frame(self.main_frame)
        self.answer_frame.grid(row=1, column=0, columnspan=4, sticky='nsew')

        display_style = ttk.Style()
        display_style.configure(
            "aaaaa.TLabel",
            background="white",
            foreground="#505050",
            anchor="w",
            justify="right",
            relief="solid",
            borderwidth=1
        )

        self.stroke_style = ttk.Style()
        self.stroke_style.configure(
            "stroke.TButton",
            background="red",
            foreground='blue',
            anchor="center",
            relief="solid",
            borderwidth=0
        )

        self.display = ttk.Label(
            self.display_frame,
            font=('Ariel', 40),
            justify='right',
            text='',
            style="aaaaa.TLabel"
        )
        self.display.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.answer_display = ttk.Label(
            self.answer_frame,
            style="aaaaa.TLabel",
            font=('Ariel', 20)
        )
        self.answer_display.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        self.display_frame.columnconfigure(0, weight=2)
        self.answer_frame.columnconfigure(0, weight=1)

        self.buttons['clickablebackspace'] = ttk.Button(
            self.main_frame,
            text='backspace',
            bootstyle="danger",
            command=lambda: self.display.config(text=self.display.cget('text')[:-1])
        )
        self.buttons['clickablebackspace'].grid(row=2, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

        self.buttons['clickabledeleteall'] = ttk.Button(
            self.main_frame,
            text='C',
            bootstyle="danger",
            command=lambda: (self.display.config(text=''), self.answer_display.config(text=''))
        )
        self.buttons['clickabledeleteall'].grid(row=2, column=2, columnspan=2, sticky='nsew', padx=5, pady=5)

        buttons = [1, 2, 3, "+", 4, 5, 6, "-", 7, 8, 9, "*", ".", 0, "%", "/", "="]
        row = 3
        col = 0

        for i, v in enumerate(buttons):
            if v == "=":
                boot = "success"
                cmd = lambda val=v: self.answer_display.config(text=eval(str(self.display.cget('text'))))
            else:
                boot = "primary"
                cmd = lambda val=v: self.display.config(text=self.display.cget("text") + str(val))

            self.buttons[f'clickable{v}'] = ttk.Button(
                self.main_frame,
                text=v,
                bootstyle=boot,
                command=cmd
            )
            self.buttons[f'clickable{v}'].grid(row=row, column=col, sticky='nsew', padx=5, pady=5, columnspan=4 if v == '=' else 1)

            try:
                self.root.bind(f'{v}', lambda e, val=v: self._handle_keypress(e, val))
            except TclError:
                ...

            if v == "=":
                self.root.bind('<Return>', lambda e: self.answer_display.config(
                    text=eval(str(self.display.cget('text')))
                ))

            col += 1
            if col > 3:
                col = 0
                row += 1

        self.buttons['clickablehavestroke'] = ttk.Button(
            self.main_frame,
            text='Have a silly Andre riding a unicron holding three empty bottles of sting. Aka have a stroke',
            style='stroke.TButton',
            command=self._have_stroke
        )
        self.buttons['clickablehavestroke'].grid(row=row+1, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

        for r in range(row + 2):
            self.main_frame.rowconfigure(r, weight=1)
        for c in range(4):
            self.main_frame.columnconfigure(c, weight=1)

        self._change_stroke_btn()

    def _handle_keypress(self, event, val):
        self.display.config(text=self.display.cget("text") + str(val))

    def _change_stroke_btn(self):
        colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink']
        random_color1 = choice(colors)
        random_color2 = choice(colors)

        self.stroke_style.configure(
            "stroke.TButton",
            background=random_color1,
            foreground=random_color2
        )

        self.buttons['clickablehavestroke'].config(style="stroke.TButton")
        self.root.after(100, self._change_stroke_btn)

    def _have_stroke(self):
        colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'pink']

        def apply_stroke(widget, count=[0]):
            if isinstance(widget, ttk.Button) or isinstance(widget, ttk.Label):
                style_name = f"stroke{count[0]}.TButton"
                count[0] += 1
                random_color1 = choice(colors)
                random_color2 = choice(colors)

                style = ttk.Style()
                style.configure(style_name, background=random_color1, foreground=random_color2)

                try:
                    widget.config(style=style_name)
                except TclError:
                    pass

            for child in widget.winfo_children():
                apply_stroke(child)

        apply_stroke(self.root)
        self.root.after(10, self._have_stroke)


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = Application(root)
    root.mainloop()