import tkinter as tk
from tkinter import messagebox, colorchooser
from tkinter import Menu
import csv
from datetime import datetime

import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.dates as mdates
# Hàm để vẽ biểu đồ số lượng ghi chú theo tháng
def plot_notes_by_month():
    # Lấy số lượng ghi chú theo tháng
    monthly_counts = defaultdict(int)
    for note in notes:
        try:
            note_time = datetime.strptime(note[1], "%H:%M-%d/%m/%Y")
            month = note_time.strftime('%Y-%m')  # Định dạng tháng và năm
            monthly_counts[month] += 1
        except ValueError:
            continue

    months = sorted(monthly_counts.keys())  # Sắp xếp theo thứ tự tháng
    counts = [monthly_counts[month] for month in months]

    # Vẽ biểu đồ cột
    plt.figure(figsize=(10, 6))
    plt.bar(months, counts, color='skyblue')
    plt.xlabel('Tháng-Năm')
    plt.ylabel('Số lượng ghi chú')
    plt.title('Số lượng ghi chú theo tháng')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Hàm để vẽ biểu đồ số lượng ghi chú theo năm
def plot_notes_by_year():
    # Lấy số lượng ghi chú theo năm
    yearly_counts = defaultdict(int)
    for note in notes:
        try:
            note_time = datetime.strptime(note[1], "%H:%M-%d/%m/%Y")
            year = note_time.year
            yearly_counts[year] += 1
        except ValueError:
            continue

    years = sorted(yearly_counts.keys())  # Sắp xếp theo thứ tự năm
    counts = [yearly_counts[year] for year in years]

    # Vẽ biểu đồ cột
    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color='lightgreen')
    plt.xlabel('Năm')
    plt.ylabel('Số lượng ghi chú')
    plt.title('Số lượng ghi chú theo năm')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title('Ứng Dụng Ghi Chú Đơn Giản')
root.geometry('600x700')
root.resizable(False, False)
root.configure(bg="lightblue")

# Dữ liệu ghi chú
notes = []
old_notes = []

# Màu sắc mặc định
re='black'
bg_color = "lightblue"
button_color_add = "black"
button_color_edit = "black"
button_color_delete = "black"
button_color_delete_permanently = "black"
button_color_delete_all_notes = "black"
text_color = "white"

# Hàm đọc dữ liệu từ file CSV
def load_data():
    global notes, old_notes
    try:
        with open('notes.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            notes = list(reader)
    except FileNotFoundError:
        notes = []
    try:
        with open('old_notes.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            old_notes = list(reader)
    except FileNotFoundError:
        old_notes = []
    move_past_notes()  # Kiểm tra ghi chú đã qua và chuyển sang old_notes
    update_listbox()

# Cập nhật Listbox với dữ liệu hiện tại
def update_listbox():
    bo.delete(0, tk.END)
    for index, note in enumerate(notes, 1):
        bo.insert(tk.END, f"{index}. {note[0]} - {note[1]}")
    old.delete(0, tk.END)
    for index, note in enumerate(old_notes, 1):
        old.insert(tk.END, f"{index}. {note[0]} - {note[1]}")

# Hàm thêm ghi chú
def add_item():
    def save_new_note():
        note = note_entry.get()
        date = date_entry.get()
        if note and date:
            try:
                datetime.strptime(date, "%H:%M-%d/%m/%Y")  # Kiểm tra định dạng ngày giờ
                notes.append([note, date])
                update_listbox()
                messagebox.showinfo("Thông Báo", f"Đã thêm ghi chú: {note} vào {date}")
                add_window.destroy()
                save_data()
            except ValueError:
                messagebox.showerror("Lỗi", "Định dạng ngày giờ không hợp lệ! Vui lòng nhập theo kiểu 'HH:MM-DD/MM/YYYY'.")

    add_window = tk.Toplevel(root)
    add_window.title("Thêm Ghi Chú")
    add_window.geometry("300x200")
    add_window.configure(bg=bg_color)

    tk.Label(add_window, text="Ghi chú:", font=('Times New Roman', 12), bg=bg_color).pack(pady=10)
    note_entry = tk.Entry(add_window, font=('Arial', 12))
    note_entry.pack(pady=5)

    tk.Label(add_window, text="Ngày tháng (HH:MM-DD/MM/YYYY):", font=('Times New Roman', 12), bg=bg_color).pack(pady=10)
    date_entry = tk.Entry(add_window, font=('Arial', 12))
    current_datetime = datetime.now().strftime("%H:%M-%d/%m/%Y")  # Đặt thời gian hiện tại làm mặc định
    date_entry.insert(tk.END, current_datetime)
    date_entry.pack(pady=5)

    tk.Button(add_window, text="Lưu", font=('Arial', 12), bg=button_color_add, fg=text_color, command=save_new_note).pack(pady=10)
    tk.Button(add_window, text="Hủy", font=('Arial', 12), bg='red', fg='white', command=add_window.destroy).pack(pady=5)

# Hàm sửa ghi chú
def edit_item():
    selected_index = bo.curselection()
    if selected_index:
        index = selected_index[0]
        old_note = notes[index]

        def save_edited_note():
            new_note = note_entry.get()
            new_date = date_entry.get()
            if new_note and new_date:
                confirm = messagebox.askyesno("Xác nhận sửa", f"Bạn có chắc chắn muốn sửa ghi chú: {old_note[0]}?")
                if confirm:
                    notes[index][0] = new_note
                    notes[index][1] = new_date
                    update_listbox()
                    messagebox.showinfo("Thông Báo", "Ghi chú đã được sửa thành công!")
                    edit_window.destroy()
                    save_data()

        edit_window = tk.Toplevel(root)
        edit_window.title("Sửa Ghi Chú")
        edit_window.geometry("300x200")
        edit_window.configure(bg=bg_color)

        tk.Label(edit_window, text="Ghi chú:", font=('Times New Roman', 12), bg=bg_color).pack(pady=10)
        note_entry = tk.Entry(edit_window, font=('Arial', 12))
        note_entry.insert(tk.END, old_note[0])
        note_entry.pack(pady=5)

        tk.Label(edit_window, text="Ngày tháng:", font=('Times New Roman', 12), bg=bg_color).pack(pady=10)
        date_entry = tk.Entry(edit_window, font=('Arial', 12))
        date_entry.insert(tk.END, old_note[1])
        date_entry.pack(pady=5)

        tk.Button(edit_window, text="Lưu", font=('Arial', 12), bg=button_color_edit, fg=text_color, command=save_edited_note).pack(pady=10)
        tk.Button(edit_window, text="Hủy", font=('Arial', 12), bg='red', fg='white', command=edit_window.destroy).pack(pady=5)
    else:
        messagebox.showwarning("Thông Báo", "Vui lòng chọn ghi chú để sửa!")

# # Hàm khôi phục ghi chú từ ghi chú cũ
def restore_old_note():
    selected_index = old.curselection()
    if selected_index:
        index = selected_index[0]
        note = old_notes[index]
        confirm_restore = messagebox.askyesno("Xác nhận khôi phục", f"Bạn có chắc chắn muốn khôi phục ghi chú: {note[0]}?")
        if confirm_restore:
            old_notes.pop(index)
            notes.append(note)
            update_listbox()
            save_data()
    else:
        messagebox.showwarning("Thông Báo", "Vui lòng chọn ghi chú cũ để khôi phục!")


# Hàm xóa ghi chú (chuyển vào ghi chú cũ)
def delete_item():
    selected_index = bo.curselection()
    if selected_index:
        index = selected_index[0]
        note = notes[index]
        confirm_delete = messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa ghi chú: {note[0]}?")
        if confirm_delete:
            notes.pop(index)
            old_notes.append(note)
            update_listbox()
            save_data()
    else:
        messagebox.showwarning("Thông Báo", "Vui lòng chọn ghi chú để xóa!")

# Hàm xóa ghi chú vĩnh viễn
def delete_permanently():
    selected_index = old.curselection()
    if selected_index:
        index = selected_index[0]
        note = old_notes[index]
        confirm_delete = messagebox.askyesno("Xác nhận xóa vĩnh viễn", f"Bạn có chắc chắn muốn xóa vĩnh viễn ghi chú: {note[0]}?")
        if confirm_delete:
            old_notes.pop(index)
            update_listbox()
            save_data()
    else:
        messagebox.showwarning("Thông Báo", "Vui lòng chọn ghi chú để xóa vĩnh viễn!")

# Hàm xóa tất cả ghi chú (chuyển hết vào ghi chú cũ)
def delete_all_notes():
    confirm_delete = messagebox.askyesno("Xác nhận xóa tất cả ghi chú", "Bạn có chắc chắn muốn xóa tất cả ghi chú và chuyển vào ghi chú cũ?")
    if confirm_delete:
        old_notes.extend(notes)  # Chuyển tất cả ghi chú vào old_notes
        notes.clear()  # Xóa tất cả ghi chú trong notes
        update_listbox()
        save_data()

# Hàm tự động lưu dữ liệu vào file CSV
def save_data():
    try:
        with open('notes.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(notes)
        with open('old_notes.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(old_notes)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi lưu dữ liệu: {e}")

# Hàm kiểm tra và chuyển ghi chú đã qua sang ghi chú cũ
def move_past_notes():
    current_time = datetime.now()
    moved_notes = []
    for note in notes:
        try:
            note_time = datetime.strptime(note[1], "%H:%M-%d/%m/%Y")
            if note_time < current_time:  # Nếu ghi chú đã qua, chuyển vào old_notes
                old_notes.append(note)
                moved_notes.append(note)
        except ValueError:
            continue

    for note in moved_notes:  # Xóa các ghi chú đã qua khỏi danh sách notes
        notes.remove(note)

    if moved_notes:
        update_listbox()
        save_data()

# Hàm Refresh dữ liệu
def refresh_data():
    load_data()  # Tải lại dữ liệu và cập nhật giao diện
    messagebox.showinfo("Thông Báo", "Dữ liệu đã được làm mới!")

# Tạo menu và nút refresh
def create_menu():
    menubar = Menu(root)

    # Menu cài đặt với icon răng cưa
    settings_menu = Menu(menubar, tearoff=0)
    settings_menu.add_command(label="Thay đổi màu nền", command=change_bg_color)
    settings_menu.add_command(label="Thay đổi màu nút Thêm Ghi Chú", command=change_add_button_color)
    settings_menu.add_command(label="Thay đổi màu nút Sửa Ghi Chú", command=change_edit_button_color)
    settings_menu.add_command(label="Thay đổi màu nút Xóa Ghi Chú", command=change_delete_button_color)
    settings_menu.add_command(label="Thay đổi màu nút Xóa Vĩnh Viễn", command=change_delete_permanently_button_color)
    settings_menu.add_command(label="Thay đổi màu nút Xóa Tất Cả", command=change_delete_all_notes_button_color)
    settings_menu.add_command(label="Thay đổi màu nút Khôi Phục Dữ Liệu", command=change_restore_old_note)
    menubar.add_cascade(label="Cài Đặt", menu=settings_menu)

    # Nút refresh
    menubar.add_command(label="Refresh", command=refresh_data)
    root.config(menu=menubar)

# Hàm thay đổi màu nền
def change_bg_color():
    global bg_color
    color_code = colorchooser.askcolor(title="Chọn màu nền")[1]
    if color_code:
        bg_color = color_code
        root.configure(bg=bg_color)
        update_listbox()

# Các hàm thay đổi màu nút
def change_restore_old_note():
    global re
    color_code = colorchooser.askcolor(title="Chọn màu nút Khôi Phục Dữ Liệu")[1]
    if color_code:
        re.config(bg=color_code)


def change_add_button_color():
    global button_color_add
    color_code = colorchooser.askcolor(title="Chọn màu nút Thêm Ghi Chú")[1]
    if color_code:
        button_color_add = color_code
        add_button.config(bg=button_color_add)

def change_edit_button_color():
    global button_color_edit
    color_code = colorchooser.askcolor(title="Chọn màu nút Sửa Ghi Chú")[1]
    if color_code:
        button_color_edit = color_code
        edit_button.config(bg=button_color_edit)

def change_delete_button_color():
    global button_color_delete
    color_code = colorchooser.askcolor(title="Chọn màu nút Xóa Ghi Chú")[1]
    if color_code:
        button_color_delete = color_code
        delete_button.config(bg=button_color_delete)

def change_delete_permanently_button_color():
    global button_color_delete_permanently
    color_code = colorchooser.askcolor(title="Chọn màu nút Xóa Vĩnh Viễn")[1]
    if color_code:
        button_color_delete_permanently = color_code
        delete_permanently_button.config(bg=button_color_delete_permanently)

def change_delete_all_notes_button_color():
    global button_color_delete_all_notes
    color_code = colorchooser.askcolor(title="Chọn màu nút Xóa Tất Cả Ghi Chú")[1]
    if color_code:
        button_color_delete_all_notes = color_code
        delete_all_notes_button.config(bg=button_color_delete_all_notes)

def sort_notes_by_datetime():
    try:
        # Chuyển đổi định dạng ngày giờ và sắp xếp
        notes.sort(key=lambda x: datetime.strptime(x[1], "%H:%M-%d/%m/%Y"))
        update_listbox()
        messagebox.showinfo("Thông Báo", "Ghi chú đã được sắp xếp theo ngày giờ!")
    except ValueError:
        messagebox.showerror("Lỗi", "Định dạng ngày giờ không hợp lệ! Vui lòng nhập theo kiểu 'HH:MM-DD/MM/YYYY'.")
        


# Giao diện chính
tk.Label(root, text="Ghi chú: ", bg='black', fg='white', font=('Times New Roman', 16)).place(x=180, y=5)
tk.Label(root, text="Ghi chú cũ:", bg='white', fg='black', font=('Times New Roman', 16)).place(x=180, y=485)

font_style = ('Arial', 14)
bo = tk.Listbox(root, width=35, height=19, font=font_style, selectmode=tk.SINGLE)
bo.place(x=180, y=35)

old = tk.Listbox(root, width=35, height=6, font=font_style, selectmode=tk.SINGLE)
old.place(x=180, y=515)

re = tk.Button(root, text='Khôi Phục Dữ Liệu', bg='black', fg='white', font=('Times New Roman', 12), command=restore_old_note)
re.place(x=25, y=376)


tk.Button(root, text='Sắp Xếp Ghi Chú', bg='black', fg="white", font=('Times New Roman', 12), command=sort_notes_by_datetime).place(x=30, y=250)

add_button = tk.Button(root, text='Thêm Ghi Chú', bg=button_color_add, fg=text_color, font=('Times New Roman', 12), command=add_item)
add_button.place(x=41, y=120)

edit_button = tk.Button(root, text='Sửa Ghi Chú', bg=button_color_edit, fg=text_color, font=('Times New Roman', 12), command=edit_item)
edit_button.place(x=46, y=164)

delete_button = tk.Button(root, text='Xóa Ghi Chú', bg=button_color_delete, fg=text_color, font=('Times New Roman', 12), command=delete_item)
delete_button.place(x=46, y=208)

delete_permanently_button = tk.Button(root, text='Xóa Vĩnh Viễn', bg=button_color_delete_permanently, fg=text_color, font=('Times New Roman', 12), command=delete_permanently)
delete_permanently_button.place(x=39, y=292)

delete_all_notes_button = tk.Button(root, text='Xóa Tất Cả Ghi Chú', bg=button_color_delete_all_notes, fg=text_color, font=('Times New Roman', 12), command=delete_all_notes)
delete_all_notes_button.place(x=21, y=334)

# Tạo thanh cuộn cho Listbox ghi chú
scrollbar_bo = tk.Scrollbar(root, orient=tk.VERTICAL, command=bo.yview)
scrollbar_bo.place(x=550, y=35, height=440)  # Đặt vị trí cho scrollbar
bo.config(yscrollcommand=scrollbar_bo.set)  # Kết nối scrollbar với Listbox

# Tạo thanh cuộn cho Listbox ghi chú cũ
scrollbar_old = tk.Scrollbar(root, orient=tk.VERTICAL, command=old.yview)
scrollbar_old.place(x=550, y=515, height=140)  # Đặt vị trí cho scrollbar
old.config(yscrollcommand=scrollbar_old.set)  # Kết nối scrollbar với Listbox

# Thêm các nút vào giao diện để gọi các chức năng vẽ biểu đồ
tk.Button(root, text='Biểu Đồ Theo Tháng', bg=button_color_add, fg=text_color, font=('Times New Roman', 12), command=plot_notes_by_month).place(x=18, y=546)
tk.Button(root, text='Biểu Đồ Theo Năm', bg=button_color_add, fg=text_color, font=('Times New Roman', 12), command=plot_notes_by_year).place(x=22, y=504)


tk.Button(root, text='Thoát', bg='red', fg='white', font=(14), command=root.quit).place(x=62, y=588)

create_menu()
load_data()
root.mainloop()  