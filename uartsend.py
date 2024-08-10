import tkinter as tk
from tkinter import ttk
import serial

def show_frame(frame):
    frame.tkraise()

def configure_styles():
    style = ttk.Style()
    style.configure("TButton", font=("Segoe UI", 14), padding=10, relief="flat")
    style.configure("TLabel", font=("Segoe UI", 16), foreground="#ecf0f1", background="#2c3e50")
    style.configure("TFrame", background="#000")
    style.configure("Large.TButton", font=("Segoe UI", 18), padding=15)
    style.configure("Small.TButton", font=("Segoe UI", 20), padding=10)

def create_frame(root):
    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky='nsew')
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    return frame

def create_main_frame(root):
    main_frame = create_frame(root)

    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=20, padx=20, expand=True)

    ttk.Button(btn_frame, text="수동 제어", style="Large.TButton", command=lambda: show_frame(manual_frame)).pack(
        pady=40, padx=20, side='left', expand=True)
    ttk.Button(btn_frame, text="자동 제어", style="Large.TButton", command=lambda: show_frame(auto_frame)).pack(
        pady=40, padx=20, side='right', expand=True)

    return main_frame

def create_manual_frame(root):
    manual_frame = create_frame(root)

    controller_frame = ttk.Frame(manual_frame)
    controller_frame.pack(pady=20, padx=20, fill='both', expand=True)

    for i in range(7):
        controller_frame.grid_rowconfigure(i, weight=1)
        controller_frame.grid_columnconfigure(i, weight=1)

    control_buttons = {
        "↑": (2, 3, "forward", '1'),
        "←": (3, 2, "left", '2'),
        "→": (3, 4, "right", '3'),
        "↓": (4, 3, "backward", '4')
    }

    for text, (row, col, command, count) in control_buttons.items():
        ttk.Button(controller_frame, text=text, style="Small.TButton",
                   command=lambda cmd=command, cnt=count: send_uart(cnt)).grid(
            row=row, column=col, padx=0, pady=0, sticky='s')

    ttk.Button(manual_frame, text="홈으로", style="Large.TButton", command=lambda: show_frame(main_frame)).pack(
        pady=60, padx=20, anchor='s', side='bottom')

    return manual_frame

def create_auto_frame(root):
    auto_frame = create_frame(root)

    action_frame = ttk.Frame(auto_frame)
    action_frame.pack(pady=20, padx=20, expand=True)

    ttk.Button(action_frame, text="맵핑", style="Large.TButton", command=lambda: send_uart('5')).pack(
        pady=40, padx=20, side='left', expand=True)
    ttk.Button(action_frame, text="자율주행", style="Large.TButton", command=lambda: show_frame(autodrive_frame)).pack(
        pady=40, padx=20, side='right', expand=True)

    ttk.Button(auto_frame, text="홈으로", style="Large.TButton", command=lambda: show_frame(main_frame)).pack(
        pady=60, padx=20, anchor='s', side='bottom')

    return auto_frame

def create_autodrive_frame(root):
    autodrive_frame = create_frame(root)

    ttk.Button(autodrive_frame, text="홈으로", style="Large.TButton", command=lambda: show_frame(main_frame)).pack(
        pady=60, padx=20, anchor='s', side='bottom')

    return autodrive_frame

def send_uart(data):
    print(data)
    uart.write(str(data).encode())

def main():
    global uart
    uart = serial.Serial('/dev/ttyTHS1', baudrate=9600, timeout=10)

    root = tk.Tk()
    root.title("PECO")
    root.geometry("1366x768")
    root.configure(bg="#2c3e50")

    configure_styles()

    global main_frame, manual_frame, auto_frame, autodrive_frame
    main_frame = create_main_frame(root)
    manual_frame = create_manual_frame(root)
    auto_frame = create_auto_frame(root)
    autodrive_frame = create_autodrive_frame(root)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    show_frame(main_frame)

    root.mainloop()

if __name__ == "__main__":
    main()
