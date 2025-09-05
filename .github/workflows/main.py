from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import csv
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

data = {"income": [], "expenses": []}

class BudgetManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.add_widget(Label(text="💰 MyBudgetManager", font_size=24))
        self.input_amount = TextInput(hint_text="Enter amount", multiline=False)
        self.add_widget(self.input_amount)
        self.btn_income = Button(text="Add Income", on_press=self.add_income)
        self.btn_expense = Button(text="Add Expense", on_press=self.add_expense)
        self.btn_summary = Button(text="Show Summary", on_press=self.show_summary)
        self.btn_export_csv = Button(text="Export CSV", on_press=self.export_csv)
        self.btn_export_pdf = Button(text="Export PDF", on_press=self.export_pdf)
        for b in [self.btn_income, self.btn_expense, self.btn_summary, self.btn_export_csv, self.btn_export_pdf]:
            self.add_widget(b)

    def add_income(self, instance):
        try:
            amount = float(self.input_amount.text)
            data["income"].append(amount)
            self.popup("Income added!")
        except:
            self.popup("Invalid input")

    def add_expense(self, instance):
        try:
            amount = float(self.input_amount.text)
            data["expenses"].append(amount)
            self.popup("Expense added!")
        except:
            self.popup("Invalid input")

    def show_summary(self, instance):
        total_income = sum(data["income"])
        total_expenses = sum(data["expenses"])
        balance = total_income - total_expenses
        msg = f"Income: {total_income}\nExpenses: {total_expenses}\nBalance: {balance}"
        self.popup(msg)

    def export_csv(self, instance):
        with open("budget.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Type", "Amount"])
            for i in data["income"]:
                writer.writerow(["Income", i])
            for e in data["expenses"]:
                writer.writerow(["Expense", e])
        self.popup("CSV exported")

    def export_pdf(self, instance):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "MyBudgetManager Report", ln=True, align="C")
        total_income = sum(data["income"])
        total_expenses = sum(data["expenses"])
        balance = total_income - total_expenses
        pdf.multi_cell(0, 10, f"Income: {total_income}\nExpenses: {total_expenses}\nBalance: {balance}")
        pdf.output("budget.pdf")
        self.popup("PDF exported")

    def popup(self, message):
        Popup(title="Info", content=Label(text=message), size_hint=(0.6,0.4)).open()

class MyBudgetApp(App):
    def build(self):
        return BudgetManager()

if __name__ == "__main__":
    MyBudgetApp().run()
