import calendar
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk


prices = {"Базовый": 1500, "Стандарт": 2200, "Премиум": 3000}
max_date = date(2099, 12, 31)
today = date.today()
year = today.year
month = today.month


def choose_day(day):
    selected = date(year, month, day)
    date_entry.delete(0, tk.END)
    date_entry.insert(0, selected.strftime("%d.%m.%Y"))


def show_month():
    for widget in days_frame.winfo_children():
        widget.destroy()

    month_label.config(text=f"{month:02d}.{year}")
    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    for column, name in enumerate(weekdays):
        tk.Label(days_frame, text=name).grid(row=0, column=column)

    today = date.today()
    weeks = calendar.monthcalendar(year, month)
    for row, week in enumerate(weeks, start=1):
        for column, day in enumerate(week):
            if day == 0:
                continue
            button = tk.Button(days_frame, text=day, width=4,
                               command=lambda day=day: choose_day(day))
            if date(year, month, day) < today:
                button.config(state="disabled")
            button.grid(row=row, column=column, padx=2, pady=2)


def change_month(step):
    global year, month
    new_year = year
    new_month = month + step
    if new_month == 0:
        new_year -= 1
        new_month = 12
    elif new_month == 13:
        new_year += 1
        new_month = 1

    if 1900 <= new_year <= max_date.year:
        year = new_year
        month = new_month
        show_month()
    return login != "" and "." in domain[1:-1]


def calculate(buy=False):
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    if len(name) < 2:
        messagebox.showerror("Ошибка", "Введите имя: минимум 2 символа.")
        return
    if not email_is_valid(email):
        messagebox.showerror("Ошибка", "Проверьте email. Пример: user@mail.ru")
        return

    try:
        start = datetime.strptime(date_entry.get(), "%d.%m.%Y").date()
    except ValueError:
        messagebox.showerror("Ошибка", "Введите существующую дату: ДД.ММ.ГГГГ.")
        return
    if start < date.today() or start > max_date:
        messagebox.showerror("Ошибка", "Дата должна быть от сегодня до 31.12.2099.")
        return
    if buy and not agreement.get():
        messagebox.showerror("Ошибка", "Подтвердите согласие с условиями.")
        return

    tariff_name = tariff.get()
    months = int(duration.get())
    total = prices[tariff_name] * months

    end_year = start.year
    end_month = start.month + months
    if end_month > 12:
        end_year += 1
        end_month -= 12
    days_in_month = calendar.monthrange(end_year, end_month)[1]
    end_day = min(start.day, days_in_month)
    last_day = date(end_year, end_month, end_day) - timedelta(days=1)

    status = "Предварительный расчёт"
    if buy:
        status = "Абонемент оформлен (демо)"

    result.config(text=(
        f"{status}\n"
        f"Клиент: {name} | {email}\n"
        f"Тариф: {tariff_name} | Срок: {months} мес.\n"
        f"Период: {start:%d.%m.%Y} — {last_day:%d.%m.%Y}\n"
        f"Итого: {total} руб. за весь срок. Деньги не списываются."
    ))


root = tk.Tk()
root.title("Тренажёрный зал — Tkinter")
root.geometry("800x590")
root.minsize(800, 590)

tk.Label(root, text="Абонемент в тренажёрный зал", font=("Arial", 20)).pack(pady=15)

body = tk.Frame(root)
body.pack(padx=15, fill="x")
left = tk.LabelFrame(body, text="Выберите дату начала", padx=10, pady=10)
left.pack(side="left", anchor="n")

navigation = tk.Frame(left)
navigation.pack(fill="x")
tk.Button(navigation, text="<", command=lambda: change_month(-1)).pack(side="left")
tk.Button(navigation, text=">", command=lambda: change_month(1)).pack(side="right")
month_label = tk.Label(navigation)
month_label.pack()
days_frame = tk.Frame(left)
days_frame.pack(pady=10)

form = tk.Frame(body)
form.pack(side="right", anchor="n", padx=15)

tk.Label(form, text="Имя").grid(row=0, column=0, sticky="w", pady=4)
name_entry = ttk.Entry(form, width=25)
name_entry.grid(row=0, column=1)

tk.Label(form, text="Email").grid(row=1, column=0, sticky="w", pady=4)
email_entry = ttk.Entry(form, width=25)
email_entry.grid(row=1, column=1)

tk.Label(form, text="Дата (ДД.ММ.ГГГГ)").grid(row=2, column=0, sticky="w", pady=4)
date_entry = ttk.Entry(form, width=25)
date_entry.insert(0, today.strftime("%d.%m.%Y"))
date_entry.grid(row=2, column=1)

tk.Label(form, text="Тариф").grid(row=3, column=0, sticky="w", pady=4)
tariff = ttk.Combobox(form, values=list(prices), state="readonly", width=22)
tariff.current(0)
tariff.grid(row=3, column=1)
tk.Label(form, justify="left", text="Базовый — 1500 руб./мес.\nСтандарт — 2200 руб./мес.\n"
         "Премиум — 3000 руб./мес.").grid(row=4, column=1, sticky="w")

tk.Label(form, text="Срок, мес.").grid(row=5, column=0, sticky="w", pady=4)
duration = ttk.Combobox(form, values=[1, 3, 6, 12], state="readonly", width=22)
duration.current(0)
duration.grid(row=5, column=1)

agreement = tk.BooleanVar()
tk.Checkbutton(form, text="Согласен с условиями", variable=agreement).grid(
    row=6, column=0, columnspan=2, sticky="w", pady=4
)

calculate_button = tk.Button(form, text="Рассчитать", command=calculate)
calculate_button.grid(row=7, column=0, sticky="w", pady=4)
buy_button = tk.Button(form, text="Оформить", command=lambda: calculate(True))
buy_button.grid(row=7, column=1, sticky="w", pady=4)

result = tk.Label(root, text="Заполните форму и нажмите «Рассчитать».",
                  justify="left", wraplength=750, font=("Arial", 11))
result.pack(padx=15, pady=15, anchor="w")

show_month()
root.mainloop()
