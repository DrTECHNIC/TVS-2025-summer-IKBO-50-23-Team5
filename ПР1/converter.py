import tkinter as tk
from tkinter import ttk


def currency_convert():
    try:
        val = float(entry_currency_value.get())
        cur1 = combo_currency_from.get()
        cur2 = combo_currency_to.get()
        currency = {
            "USD": 0.012,
            "EUR": 0.01,
            "RUB": 1, # конвертация относительно рубля
            "IDR": 202.06,
            "KZT": 6.63,
            "GBP": 0.0091
        } # на момент 13:45 05.09.2025
        result = val / currency[cur2] * currency[cur1] # cur1 и cur2 перепутаны местами
        label_currency_result.config(text=f"{val} {cur1} = {result} {cur2}") # результат не ограничен в длине
    except ValueError:
        label_currency_result.config(text="Ошибка: Введите число")


def length_convert():
    try:
        val = float(entry_length_value.get())
        len1 = combo_length_from.get()
        len2 = combo_length_to.get()
        lengths = {
            "Метр": 1,
            "Километр": 1000,
            "Сантиметр": 0.01,
            "Миля": 1609.34,
            "Фут": 0.3048,
            "Дюйм": 0.0254,
            "Ярд": 0.9144,
            "Морская миля": 1852
        }
        result = val * lengths[len1] / lengths[len2]
        label_length_result.config(text=f"{val} {len1} = {result} {len2}")
    except ValueError:
        label_length_result.config(text="Ошибка: Введите число")


def mass_convert():
    try:
        val = float(entry_mass_value.get())
        mass1 = combo_mass_from.get()
        mass2 = combo_mass_to.get()
        masses = {
            "Килограмм": 1,
            "Грамм": 0.001,
            "Фунт": 0.453592,
            "Унция": 0.0283495,
            "Тонна": 1000,
            "Карат": 0.0002,
            "Стоун": 6.35029
        }
        result = val * masses[mass1] / masses[mass2]
        label_mass_result.config(text=f"{val} {mass1} = {result} {mass2}")
    except ValueError:
        label_mass_result.config(text="Ошибка: Введите число")

root = tk.Tk()
root.title("Универсальный конвертер")

notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill='both', expand=True)

currency_frame = ttk.Frame(notebook)
length_frame = ttk.Frame(notebook)
mass_frame = ttk.Frame(notebook)

notebook.add(currency_frame, text="Валюты")
notebook.add(length_frame, text="Длины")
notebook.add(mass_frame, text="Массы")

tk.Label(currency_frame, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
entry_currency_value = tk.Entry(currency_frame)
entry_currency_value.grid(row=0, column=1, padx=5, pady=5)

tk.Label(currency_frame, text="Из:").grid(row=1, column=0, padx=5, pady=5)
combo_currency_from = ttk.Combobox(currency_frame, values=["USD", "EUR", "RUB", "IDR", "KZT", "GBP"])
combo_currency_from.current(2)
combo_currency_from.grid(row=1, column=1, padx=5, pady=5)

tk.Label(currency_frame, text="В:").grid(row=2, column=0, padx=5, pady=5)
combo_currency_to = ttk.Combobox(currency_frame, values=["USD", "EUR", "RUB", "IDR", "KZT", "GBP"])
combo_currency_to.current(0)
combo_currency_to.grid(row=2, column=1, padx=5, pady=5)

button_currency_convert = tk.Button(currency_frame, text="Конвертировать", command=currency_convert)
button_currency_convert.grid(row=3, column=0, columnspan=2, pady=10)

label_currency_result = tk.Label(currency_frame, text="")
label_currency_result.grid(row=4, column=0, columnspan=2)

tk.Label(length_frame, text="Значение:").grid(row=0, column=0, padx=5, pady=5)
entry_length_value = tk.Entry(length_frame)
entry_length_value.grid(row=0, column=1, padx=5, pady=5)

tk.Label(length_frame, text="Из:").grid(row=1, column=0, padx=5, pady=5)
combo_length_from = ttk.Combobox(length_frame, values=["Метр", "Километр", "Сантиметр", "Миля", "Фут", "Дюйм", "Ярд", "Морская миля"])
combo_length_from.current(0)
combo_length_from.grid(row=1, column=1, padx=5, pady=5)

tk.Label(length_frame, text="В:").grid(row=2, column=0, padx=5, pady=5)
combo_length_to = ttk.Combobox(length_frame, values=["Метр", "Километр", "Сантиметр", "Миля", "Фут", "Дюйм", "Ярд", "Морская миля"])
combo_length_to.current(1)
combo_length_to.grid(row=2, column=1, padx=5, pady=5)

button_length_convert = tk.Button(length_frame, text="Конвертировать", command=length_convert)
button_length_convert.grid(row=3, column=0, columnspan=2, pady=10)

label_length_result = tk.Label(length_frame, text="")
label_length_result.grid(row=4, column=0, columnspan=2)

tk.Label(mass_frame, text="Значение:").grid(row=0, column=0, padx=5, pady=5)
entry_mass_value = tk.Entry(mass_frame)
entry_mass_value.grid(row=0, column=1, padx=5, pady=5)

tk.Label(mass_frame, text="Из:").grid(row=1, column=0, padx=5, pady=5)
combo_mass_from = ttk.Combobox(mass_frame, values=["Килограмм", "Грамм", "Фунт", "Унция", "Тонна", "Карат", "Стоун"])
combo_mass_from.current(0)
combo_mass_from.grid(row=1, column=1, padx=5, pady=5)

tk.Label(mass_frame, text="В:").grid(row=2, column=0, padx=5, pady=5)
combo_mass_to = ttk.Combobox(mass_frame, values=["Килограмм", "Грамм", "Фунт", "Унция", "Тонна", "Карат", "Стоун"])
combo_mass_to.current(1)
combo_mass_to.grid(row=2, column=1, padx=5, pady=5)

button_mass_convert = tk.Button(mass_frame, text="Конвертировать", command=mass_convert)
button_mass_convert.grid(row=3, column=0, columnspan=2, pady=10)

label_mass_result = tk.Label(mass_frame, text="")
label_mass_result.grid(row=4, column=0, columnspan=2)

root.eval('tk::PlaceWindow . center')
root.mainloop()