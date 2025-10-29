import TermTk as ttk
from TermTk import TTkInput
from api import Api
from TermTk import TTkK


class App:
    def __init__(self):
        self.api = Api()
        self.root = ttk.TTk()

        TTkInput.inputEvent.connect(self.keyCallback)

        currencies = self.api.get_all_currencies() #Fetch currency codes from currency-api

        date = "YYYY-MM-DDD"
        status = "UNDEFINED"
        self.label_status = ttk.TTkLabel(text=f"{date}: {status}")
        self.label_status.setAlignment(ttk.TTkK.RIGHT_ALIGN)

        #From comboBox and button
        self.combo_from = ttk.TTkComboBox(
            size=(20, 1),
            list=currencies,
            index=0,
            editable=False
        )

        #Label to understand the flow of exchange
        label_to = ttk.TTkLabel(text="-->")
        label_to.setAlignment(ttk.TTkK.CENTER_ALIGN)
        
        #To comboBox and button
        self.combo_to = ttk.TTkComboBox(
            size=(10, 1),
            list=currencies,
            index=0,
            editable=False
        )

        #lineEdit and Button "Convert"
        self.line_edit = ttk.TTkLineEdit(size=(20, 1))
        self.line_edit.setInputType(ttk.TTkK.Input_Number)
        self.line_edit.textEdited.connect(self.line_edit_changed)
        self.button_convert = ttk.TTkButton(text="Convert!")
        self.button_convert.setEnabled(False)
        self.button_convert.clicked.connect(self.convert)


        #Exchange layout(combBoxFrom + label_to  + comboBoxTo)
        exchange_layout = ttk.TTkHBoxLayout()
        exchange_layout.addWidget(ttk.TTkSpacer(maxWidth=5))
        exchange_layout.addWidget(self.combo_from)
        exchange_layout.addWidget(ttk.TTkSpacer(maxWidth=1))
        exchange_layout.addWidget(label_to)
        exchange_layout.addWidget(self.combo_to)
        exchange_layout.addWidget(ttk.TTkSpacer(maxWidth=5))
        
        #Exchange frame
        exchange_frame = ttk.TTkFrame(layout=exchange_layout, border=True, title="Exchange")

        #Main layout(label_status + exchange_frame + lineEdit + button_convert)
        main_layout = ttk.TTkVBoxLayout()
        main_layout.addWidget(self.label_status)
        main_layout.addWidget(ttk.TTkSpacer())
        main_layout.addWidget(exchange_frame)
        main_layout.addWidget(ttk.TTkSpacer())

        #Line Edit layout to center it in Main layout
        line_edit_layout = ttk.TTkHBoxLayout()
        line_edit_layout.addWidget(ttk.TTkSpacer())
        line_edit_layout.addWidget(self.line_edit)
        line_edit_layout.addWidget(ttk.TTkSpacer())
        line_edit_frame = ttk.TTkFrame(layout=line_edit_layout, border=False)

        main_layout.addWidget(line_edit_frame)
        main_layout.addWidget(ttk.TTkSpacer())

        #Conver button layout to center it in Main layout
        convert_layout = ttk.TTkHBoxLayout()
        convert_layout.addWidget(ttk.TTkSpacer())
        convert_layout.addWidget(self.button_convert)
        convert_layout.addWidget(ttk.TTkSpacer())
        convert_frame = ttk.TTkFrame(layout=convert_layout, border=False)

        main_layout.addWidget(convert_frame)
        main_layout.addWidget(ttk.TTkSpacer())

        #Main frame
        main_container = ttk.TTkFrame(layout=main_layout, border=True)

        #Root layout(main_container center allignment)
        root_layout = ttk.TTkHBoxLayout()
        root_layout.addWidget(ttk.TTkSpacer(maxWidth=15))
        root_layout.addWidget(main_container)
        root_layout.addWidget(ttk.TTkSpacer(maxWidth=15))
        self.root.setLayout(root_layout)

    #Exit function: if user presses q - exit app
    def keyCallback(self, kevt, mevt):
        if kevt is not None:
            if kevt.key == "q":
                self.root.quit()
            if kevt.key == TTkK.Key_Enter: #本可以做得更好，但它完成了任务，所以算了
                if self.line_edit.text() != "0": 
                    self.convert()
                else:
                    pass
    
    def convert(self):
        user_input = str(self.line_edit.text()).strip()
        if user_input != "":
            user_input = float(user_input)
            code_from = self.combo_from.currentText()
            code_to = self.combo_to.currentText()
            result, date, status_code = self.api.get_currency(code_from, code_to, user_input)
            self.line_edit.setText(f"{result:.1f}")
            self.label_status.setText(f"{date}: {status_code}")
    
    def line_edit_changed(self):
        text = self.line_edit.text()
        if text != "" or text != "0":
            self.button_convert.setEnabled(True)
        else:
            self.button_convert.setDisabled(True)
    
    #Main loop
    def run(self):
        self.root.mainloop()