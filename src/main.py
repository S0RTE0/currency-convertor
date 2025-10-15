import TermTk as ttk
from api import Api

root = ttk.TTk()

win = ttk.TTkWindow(parent=root,pos = (1,1), size=(30,10), title="Currency Convertor", border=True)
win.closed.connect(lambda: root.quit())

api = Api()
currencies = api.get_all_currencies()

combo = ttk.TTkComboBox(
    parent=win,
    pos=(2, 2),
    size=(10, 1),
    list=currencies,
    index=0,
    editable=False,
    textAlign=ttk.TTkK.CENTER_ALIGN
)

label = ttk.TTkLabel(parent=win, pos=(2, 5), size=(30, 1), text="Selected: USD")

def on_combo_change(text):
    label.setText(f"Selected: {text}")

combo.currentTextChanged.connect(on_combo_change)

root.mainloop()