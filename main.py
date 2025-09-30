from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
import os

# Ensure data folder exists
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
SAVE_FILE = os.path.join(DATA_DIR, "refund_requests.txt")


# -------------------- Form Screen (Logic) --------------------
class FormScreen(Screen):
    # submit_form, clear_form, and go_back are called by the buttons in refundapp.kv
    
    def submit_form(self):
        # Access widgets using their IDs defined in the .kv file
        data = {
            'Full Name': self.ids.full_name.text.strip(),
            'Email': self.ids.email.text.strip(),
            'Phone': self.ids.phone.text.strip(),
            'Amount Charged': self.ids.amount.text.strip(),
            'Date of Charge (YYYY-MM-DD)': self.ids.date.text.strip(),
            'Invoice/Ref No': self.ids.invoice.text.strip(),
            'Reason': self.ids.reason.text.strip(),
        }
        
        # Validation Check
        if not all(data.values()):
            self.show_popup("Error", "All fields are required!")
            return

        result = f"""
        === Refund / Dispute Request ===
        Full Name: {data['Full Name']}
        Email: {data['Email']}
        Phone: {data['Phone']}
        Amount Charged: {data['Amount Charged']}
        Date of Charge: {data['Date of Charge (YYYY-MM-DD)']}
        Invoice/Ref No: {data['Invoice/Ref No']}
        Reason: {data['Reason']}
        """

        with open(SAVE_FILE, "a", encoding="utf-8") as f:
            f.write(result + "\n" + "-" * 50 + "\n")

        self.show_popup("Success", "Your refund/dispute request has been submitted.")
        self.clear_form()

    def clear_form(self):
        # Clear all TextInput widgets using their IDs
        self.ids.full_name.text = ""
        self.ids.email.text = ""
        self.ids.phone.text = ""
        self.ids.amount.text = ""
        self.ids.date.text = ""
        self.ids.invoice.text = ""
        self.ids.reason.text = ""

    def go_back(self):
        self.manager.current = "welcome"

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()


# -------------------- Welcome Screen (Logic) --------------------
class WelcomeScreen(Screen):
    def open_form(self):
        self.manager.current = "form"

    def exit_app(self):
        App.get_running_app().stop()


# -------------------- App --------------------
# Naming the class RefundApp ensures Kivy automatically loads 'refundapp.kv'
class RefundApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(FormScreen(name="form"))
        return sm


if __name__ == "__main__":
    RefundApp().run()