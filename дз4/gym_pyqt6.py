import sys

from PyQt6.QtCore import QDate, QLocale, Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QCheckBox,
    QPushButton, QCalendarWidget, QMessageBox, QVBoxLayout, QHBoxLayout,
    QFormLayout
)


prices = {"Базовый": 1500, "Стандарт": 2200, "Премиум": 3000}


def email_is_valid(email):
    parts = email.split("@")
    if len(parts) != 2 or len(email.split()) != 1:
        return False

    login, domain = parts
    return login != "" and "." in domain[1:-1]


def calculate(buy=False):
    name = name_entry.text().strip()
    email = email_entry.text().strip()

    if len(name) < 2:
        QMessageBox.warning(window, "Ошибка", "Введите имя: минимум 2 символа.")
        return
    if not email_is_valid(email):
        QMessageBox.warning(window, "Ошибка", "Проверьте email. Пример: user@mail.ru")
        return
    if buy and not agreement.isChecked():
        QMessageBox.warning(window, "Ошибка", "Подтвердите согласие с условиями.")
        return

    start = calendar_widget.selectedDate()
    tariff_name = tariff.currentText()
    months = int(duration.currentText())
    total = prices[tariff_name] * months
    last_day = start.addMonths(months).addDays(-1)

    status = "Предварительный расчёт"
    if buy:
        status = "Абонемент оформлен (демо)"

    result.setText(
        f"{status}\n"
        f"Клиент: {name} | {email}\n"
        f"Тариф: {tariff_name} | Срок: {months} мес.\n"
        f"Период: {start.toString('dd.MM.yyyy')} — {last_day.toString('dd.MM.yyyy')}\n"
        f"Итого: {total} руб. за весь срок. Деньги не списываются."
    )


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Тренажёрный зал — PyQt6")
window.resize(800, 520)

main = QVBoxLayout(window)
title = QLabel("Абонемент в тренажёрный зал")
title.setStyleSheet("font-size: 24px")
main.addWidget(title)

body = QHBoxLayout()
main.addLayout(body)

calendar_widget = QCalendarWidget()
calendar_widget.setLocale(QLocale("ru_RU"))
calendar_widget.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
calendar_widget.setMinimumDate(QDate.currentDate())
calendar_widget.setMaximumDate(QDate(2099, 12, 31))
body.addWidget(calendar_widget)

form = QFormLayout()
body.addLayout(form)

name_entry = QLineEdit()
email_entry = QLineEdit()
form.addRow("Имя:", name_entry)
form.addRow("Email:", email_entry)

tariff = QComboBox()
tariff.addItems(list(prices))
form.addRow("Тариф:", tariff)
form.addRow(QLabel(
    "Базовый — 1500 руб./мес.\nСтандарт — 2200 руб./мес.\nПремиум — 3000 руб./мес."
))

duration = QComboBox()
duration.addItems(["1", "3", "6", "12"])
form.addRow("Срок, мес.:", duration)

agreement = QCheckBox("Согласен с условиями")
form.addRow(agreement)

calculate_button = QPushButton("Рассчитать")
buy_button = QPushButton("Оформить")
calculate_button.clicked.connect(calculate)
buy_button.clicked.connect(lambda: calculate(True))
form.addRow(calculate_button, buy_button)

result = QLabel("Заполните форму и нажмите «Рассчитать».")
result.setTextFormat(Qt.TextFormat.PlainText)
result.setWordWrap(True)
main.addWidget(result)

window.show()
sys.exit(app.exec())
