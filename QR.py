import qrcode
import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
from PIL import ImageTk

def generate_qr_code(data, fill_color, back_color, box_size, border):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill_color, back_color=back_color)

def choose_fill_color():
    color = colorchooser.askcolor(title="Выберите цвет заполнения")
    if color[1]:
        fill_color_var.set(color[1])

def choose_back_color():
    color = colorchooser.askcolor(title="Выберите цвет фона")
    if color[1]:
        back_color_var.set(color[1])

def on_generate():
    data = data_entry.get()
    fill_color = fill_color_var.get()
    back_color = back_color_var.get()
    box_size = int(box_size_entry.get())
    border = int(border_entry.get())
    if not data:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите текст или URL.")
        return
    img = generate_qr_code(data, fill_color, back_color, box_size, border)
    qr_window = tk.Toplevel(root)
    qr_window.title("Предварительный просмотр QR-кода")
    qr_window.configure(bg="white")
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(qr_window, image=img_tk, bg="white")
    label.image = img_tk
    label.pack(pady=10)
    create_rounded_button(qr_window, "Закрыть", qr_window.destroy)

def on_save():
    data = data_entry.get()
    fill_color = fill_color_var.get()
    back_color = back_color_var.get()
    box_size = int(box_size_entry.get())
    border = int(border_entry.get())
    if not data:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите текст или URL.")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not filename:
        return
    img = generate_qr_code(data, fill_color, back_color, box_size, border)
    img.save(filename)
    messagebox.showinfo("Успех", f"QR-код сохранен как {filename}")

def create_rounded_button(parent, text, command):
    button_width = 550
    button_height = 40
    padding = 10
    button = tk.Canvas(parent, width=button_width, height=button_height, bg="white", highlightthickness=0)
    button.pack(pady=10)
    button.create_oval(0, 0, padding * 2, button_height, fill="black", outline="black")
    button.create_oval(button_width - padding * 2, 0, button_width, button_height, fill="black", outline="black")
    button.create_rectangle(padding, 0, button_width - padding, button_height, fill="black", outline="black")
    button.create_text(button_width / 2, button_height / 2, text=text, fill="white", font=("Arial", 10))
    button.bind("<Button-1>", lambda e: command())

root = tk.Tk()
root.title("Генератор QR-кодов")
root.configure(bg="#302e2e")
fill_color_var = tk.StringVar(value="black")
back_color_var = tk.StringVar(value="white")

tk.Label(root, text="Введите текст или URL:", bg="white", font=("Arial", 6)).pack(pady=5)
data_entry = tk.Entry(root, width=50, font=("Arial", 6), bd=2, relief="solid", highlightthickness=1, highlightbackground="black")
data_entry.pack(pady=5)
data_entry.insert(0, "https://darateria.com")

tk.Label(root, text="Цвет заполнения:", bg="white", font=("Arial", 6)).pack(pady=5)
create_rounded_button(root, "Выбрать цвет", choose_fill_color)

tk.Label(root, text="Цвет фона:", bg="white", font=("Arial", 6)).pack(pady=5)
create_rounded_button(root, "Выбрать цвет", choose_back_color)

tk.Label(root, text="Размер блока (box size):", bg="white", font=("Arial", 6)).pack(pady=5)
box_size_entry = tk.Entry(root, font=("Arial", 6), bd=2, relief="solid", highlightthickness=1, highlightbackground="black")
box_size_entry.insert(0, "10")
box_size_entry.pack(pady=5)

tk.Label(root, text="Толщина границы (border):", bg="white", font=("Arial", 6)).pack(pady=5)
border_entry = tk.Entry(root, font=("Arial", 6), bd=2, relief="solid", highlightthickness=1, highlightbackground="black")
border_entry.insert(0, "4")
border_entry.pack(pady=5)

create_rounded_button(root, "Предварительный просмотр QR-кода", on_generate)
create_rounded_button(root, "Сохранить QR-код", on_save)

root.mainloop()
