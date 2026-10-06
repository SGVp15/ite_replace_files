import tkinter as tk


def select_num_folder_gui(file_path, root_path, matches, filename):
    result = {"num": None}

    window = tk.Tk()
    window.title("Выбор папки")

    # Начальный размер окна
    window.geometry("700x500")

    # Окно можно растягивать
    window.minsize(500, 300)

    # ---------------------------------------------------------
    # Верхняя часть
    # ---------------------------------------------------------

    top_frame = tk.Frame(window)
    top_frame.pack(fill="x", padx=15, pady=10)

    file_label = tk.Label(
        top_frame,
        text=f"Файл:\n{filename}",
        font=("Arial", 11),
        justify="left",
        anchor="w"
    )

    file_label.pack(fill="x")

    question_label = tk.Label(
        top_frame,
        text="Выберите папку:",
        font=("Arial", 11, "bold"),
        anchor="w"
    )

    question_label.pack(fill="x", pady=(10, 0))

    # ---------------------------------------------------------
    # Основная область со скроллом
    # ---------------------------------------------------------

    main_frame = tk.Frame(window)
    main_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=5
    )

    canvas = tk.Canvas(main_frame)

    scrollbar = tk.Scrollbar(
        main_frame,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    # Frame внутри Canvas
    list_frame = tk.Frame(canvas)

    canvas_window = canvas.create_window(
        (0, 0),
        window=list_frame,
        anchor="nw"
    )

    # ---------------------------------------------------------
    # Изменение размеров
    # ---------------------------------------------------------

    def configure_list(event):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    def resize_list(event):
        canvas.itemconfig(
            canvas_window,
            width=event.width
        )

    list_frame.bind(
        "<Configure>",
        configure_list
    )

    canvas.bind(
        "<Configure>",
        resize_list
    )

    # ---------------------------------------------------------
    # Обработчики
    # ---------------------------------------------------------

    def select_folder(num):
        print(f"Выбрана папка №{num}")
        result["num"] = int(num)
        window.destroy()

    def skip_file():
        result["num"] = None
        window.destroy()

    # ---------------------------------------------------------
    # Кнопки выбора
    # ---------------------------------------------------------

    for i, folder_name in enumerate(matches, 1):

        row = tk.Frame(list_frame)

        row.pack(
            fill="x",
            pady=3
        )

        # -----------------------------------------------------
        # Кнопка с номером
        # -----------------------------------------------------

        button = tk.Button(
            row,
            text=str(i),
            width=4,
            font=("Arial", 11, "bold"),

            # Передаем именно i
            command=lambda num=i: select_folder(num)
        )

        button.pack(
            side="left",
            padx=(5, 10)
        )

        # -----------------------------------------------------
        # Название папки
        # -----------------------------------------------------

        label = tk.Label(
            row,
            text=folder_name.name,
            font=("Arial", 11),
            anchor="w",
            justify="left"
        )

        label.pack(
            side="left",
            fill="x",
            expand=True
        )

        # При клике на название тоже передаем номер
        label.bind(
            "<Button-1>",
            lambda event, num=i: select_folder(num)
        )

    # ---------------------------------------------------------
    # Нижняя часть
    # ---------------------------------------------------------

    bottom_frame = tk.Frame(window)

    bottom_frame.pack(
        fill="x",
        padx=15,
        pady=10
    )

    skip_button = tk.Button(
        bottom_frame,
        text="Пропустить",
        font=("Arial", 11),
        width=15,
        command=skip_file
    )

    skip_button.pack(
        side="left"
    )

    # ---------------------------------------------------------
    # ESC = пропустить
    # ---------------------------------------------------------

    window.bind(
        "<Escape>",
        lambda event: skip_file()
    )

    window.focus_force()
    window.mainloop()

    # ---------------------------------------------------------
    # Возвращаем именно число
    # ---------------------------------------------------------

    return result["num"]
