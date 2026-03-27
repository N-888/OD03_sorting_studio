# Импортируем стандартное модальное окно сообщений, чтобы удобно показывать ошибки и подсказки.
from tkinter import messagebox

# Импортируем библиотеку customtkinter для создания современного интерфейса.
import customtkinter as ctk

# Импортируем все доступные функции сортировки из нашего модуля алгоритмов.
from app.algorithms import ALGORITHM_FUNCTIONS, SortResult

# Импортируем настройки приложения, чтобы не хранить их прямо внутри кода окна.
from app.config import (
    ALGORITHM_OPTIONS,
    APP_TITLE,
    INPUT_HINT,
    MIN_WINDOW_SIZE,
    SAMPLE_DATA,
    THEORY_TEXT,
    WINDOW_SIZE,
)

# Импортируем функции разбора и красивого вывода чисел.
from app.parser_utils import InputDataError, format_numbers, parse_numbers


# Создаем главный класс приложения на основе современного окна customtkinter.
class SortingStudioApp(ctk.CTk):
    # Создаем конструктор нашего окна.
    def __init__(self) -> None:
        # Запускаем конструктор родительского класса.
        super().__init__()
        # Устанавливаем заголовок окна.
        self.title(APP_TITLE)
        # Устанавливаем стартовый размер окна.
        self.geometry(WINDOW_SIZE)
        # Устанавливаем минимально допустимый размер окна.
        self.minsize(*MIN_WINDOW_SIZE)

        # Создаем строковую переменную для выбранного алгоритма.
        self.algorithm_var = ctk.StringVar(value=ALGORITHM_OPTIONS[0])
        # Создаем строковую переменную для направления сортировки.
        self.order_var = ctk.StringVar(value="По возрастанию")
        # Создаем строковую переменную для выбранной темы оформления.
        self.theme_var = ctk.StringVar(value="System")

        # Настраиваем адаптивную сетку главного окна по строкам.
        self.grid_rowconfigure(0, weight=1)
        # Настраиваем адаптивную сетку главного окна по столбцу с контентом.
        self.grid_columnconfigure(1, weight=1)

        # Создаем левую боковую панель.
        self._build_sidebar()
        # Создаем основную область приложения.
        self._build_main_area()
        # Заполняем вкладку теории готовым текстом.
        self._load_theory_text()
        # Сразу подставляем пример, чтобы интерфейс не был пустым.
        self.fill_example()

    # Создаем боковую панель с выбором алгоритма и кнопками действий.
    def _build_sidebar(self) -> None:
        # Создаем рамку боковой панели.
        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        # Размещаем боковую панель слева и растягиваем по высоте.
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        # Настраиваем растяжение внутри боковой панели.
        self.sidebar.grid_rowconfigure(99, weight=1)

        # Создаем большой заголовок приложения с иконкой.
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="🧠 Sorting Studio",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        # Размещаем заголовок вверху боковой панели.
        self.logo_label.grid(row=0, column=0, padx=20, pady=(24, 8), sticky="w")

        # Создаем подзаголовок с кратким описанием программы.
        self.subtitle_label = ctk.CTkLabel(
            self.sidebar,
            text="Учебное приложение для изучения алгоритмов сортировки",
            wraplength=220,
            justify="left",
        )
        # Размещаем подзаголовок сразу под логотипом.
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Создаем подпись для выбора алгоритма.
        self.algorithm_label = ctk.CTkLabel(
            self.sidebar,
            text="⚙️ Алгоритм",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        # Размещаем подпись в боковой панели.
        self.algorithm_label.grid(row=2, column=0, padx=20, pady=(0, 8), sticky="w")

        # Создаем выпадающий список алгоритмов.
        self.algorithm_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=ALGORITHM_OPTIONS,
            variable=self.algorithm_var,
            dynamic_resizing=False,
            width=220,
        )
        # Размещаем выпадающий список ниже подписи.
        self.algorithm_menu.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Создаем подпись для выбора порядка сортировки.
        self.order_label = ctk.CTkLabel(
            self.sidebar,
            text="↕️ Порядок сортировки",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        # Размещаем подпись порядка сортировки.
        self.order_label.grid(row=4, column=0, padx=20, pady=(0, 8), sticky="w")

        # Создаем переключатель с двумя вариантами направления сортировки.
        self.order_selector = ctk.CTkSegmentedButton(
            self.sidebar,
            values=["По возрастанию", "По убыванию"],
            variable=self.order_var,
        )
        # Размещаем переключатель направления сортировки.
        self.order_selector.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Создаем подпись для выбора темы оформления.
        self.theme_label = ctk.CTkLabel(
            self.sidebar,
            text="🎨 Тема",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        # Размещаем подпись темы.
        self.theme_label.grid(row=6, column=0, padx=20, pady=(0, 8), sticky="w")

        # Создаем выпадающий список тем оформления окна.
        self.theme_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["System", "Light", "Dark"],
            variable=self.theme_var,
            command=self.change_theme,
            dynamic_resizing=False,
            width=220,
        )
        # Размещаем выпадающий список темы.
        self.theme_menu.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Создаем кнопку для запуска сортировки выбранным алгоритмом.
        self.sort_button = ctk.CTkButton(
            self.sidebar,
            text="▶ Запустить сортировку",
            command=self.run_sort,
            height=40,
        )
        # Размещаем кнопку запуска сортировки.
        self.sort_button.grid(row=8, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Создаем кнопку для сравнения всех алгоритмов сразу.
        self.compare_button = ctk.CTkButton(
            self.sidebar,
            text="📊 Сравнить все алгоритмы",
            command=self.compare_algorithms,
            height=40,
        )
        # Размещаем кнопку сравнения.
        self.compare_button.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Создаем кнопку для подстановки готового примера.
        self.example_button = ctk.CTkButton(
            self.sidebar,
            text="✨ Подставить пример",
            command=self.fill_example,
            fg_color="transparent",
            border_width=1,
        )
        # Размещаем кнопку примера.
        self.example_button.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Создаем кнопку очистки данных.
        self.clear_button = ctk.CTkButton(
            self.sidebar,
            text="🧹 Очистить поля",
            command=self.clear_all,
            fg_color="transparent",
            border_width=1,
        )
        # Размещаем кнопку очистки.
        self.clear_button.grid(row=11, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Создаем нижнюю подсказку в боковой панели.
        self.sidebar_hint = ctk.CTkLabel(
            self.sidebar,
            text="Готово для Windows + PyCharm\nБез сложной настройки",
            justify="left",
        )
        # Размещаем подсказку внизу боковой панели.
        self.sidebar_hint.grid(row=100, column=0, padx=20, pady=(0, 24), sticky="sw")

    # Создаем основную рабочую область справа.
    def _build_main_area(self) -> None:
        # Создаем контейнер для всей правой части окна.
        self.main_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # Размещаем контейнер справа и растягиваем его на все доступное место.
        self.main_area.grid(row=0, column=1, sticky="nsew")
        # Настраиваем растяжение строк правой части.
        self.main_area.grid_rowconfigure(1, weight=1)
        # Настраиваем растяжение столбца правой части.
        self.main_area.grid_columnconfigure(0, weight=1)

        # Создаем верхнюю карточку с вводом данных.
        self.input_card = ctk.CTkFrame(self.main_area, corner_radius=18)
        # Размещаем карточку ввода в верхней части.
        self.input_card.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        # Настраиваем растяжение содержимого карточки ввода.
        self.input_card.grid_columnconfigure(0, weight=1)

        # Создаем заголовок карточки ввода.
        self.input_title = ctk.CTkLabel(
            self.input_card,
            text="📝 Входные данные",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        # Размещаем заголовок карточки ввода.
        self.input_title.grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")

        # Создаем текст-подсказку для поля ввода.
        self.input_hint = ctk.CTkLabel(
            self.input_card,
            text=INPUT_HINT,
            justify="left",
        )
        # Размещаем текст-подсказку под заголовком.
        self.input_hint.grid(row=1, column=0, padx=18, pady=(0, 10), sticky="w")

        # Создаем многострочное поле ввода чисел.
        self.input_text = ctk.CTkTextbox(self.input_card, height=120, corner_radius=14)
        # Размещаем поле ввода и растягиваем его по ширине.
        self.input_text.grid(row=2, column=0, padx=18, pady=(0, 18), sticky="nsew")

        # Создаем нижнюю карточку с вкладками результата.
        self.output_card = ctk.CTkFrame(self.main_area, corner_radius=18)
        # Размещаем карточку результата под карточкой ввода.
        self.output_card.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")
        # Настраиваем растяжение карточки результата.
        self.output_card.grid_rowconfigure(1, weight=1)
        # Настраиваем растяжение карточки результата по ширине.
        self.output_card.grid_columnconfigure(0, weight=1)

        # Создаем заголовок карточки результата.
        self.output_title = ctk.CTkLabel(
            self.output_card,
            text="📦 Результаты и пояснения",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        # Размещаем заголовок результата.
        self.output_title.grid(row=0, column=0, padx=18, pady=(18, 6), sticky="w")

        # Создаем набор вкладок для удобного вывода информации.
        self.tabs = ctk.CTkTabview(self.output_card, corner_radius=14)
        # Размещаем вкладки внутри карточки результата.
        self.tabs.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="nsew")

        # Создаем вкладку для итогового результата.
        self.tabs.add("Результат")
        # Создаем вкладку для пошагового объяснения.
        self.tabs.add("Шаги")
        # Создаем вкладку для сравнения алгоритмов.
        self.tabs.add("Сравнение")
        # Создаем вкладку с теорией.
        self.tabs.add("Теория")

        # Создаем текстовое поле для вывода итогового результата.
        self.result_text = ctk.CTkTextbox(self.tabs.tab("Результат"), corner_radius=12)
        # Размещаем поле результата внутри первой вкладки.
        self.result_text.pack(fill="both", expand=True, padx=12, pady=12)

        # Создаем текстовое поле для пошагового описания.
        self.steps_text = ctk.CTkTextbox(self.tabs.tab("Шаги"), corner_radius=12)
        # Размещаем поле шагов внутри второй вкладки.
        self.steps_text.pack(fill="both", expand=True, padx=12, pady=12)

        # Создаем текстовое поле для сравнения алгоритмов.
        self.compare_text = ctk.CTkTextbox(self.tabs.tab("Сравнение"), corner_radius=12)
        # Размещаем поле сравнения внутри третьей вкладки.
        self.compare_text.pack(fill="both", expand=True, padx=12, pady=12)

        # Создаем текстовое поле для краткой теории.
        self.theory_text = ctk.CTkTextbox(self.tabs.tab("Теория"), corner_radius=12)
        # Размещаем поле теории внутри четвертой вкладки.
        self.theory_text.pack(fill="both", expand=True, padx=12, pady=12)

        # Создаем строку статуса внизу окна.
        self.status_label = ctk.CTkLabel(
            self.main_area,
            text="Готово к работе. Введите числа и выберите алгоритм.",
            anchor="w",
        )
        # Размещаем строку статуса под карточками.
        self.status_label.grid(row=2, column=0, padx=24, pady=(0, 10), sticky="ew")

    # Загружаем теоретический текст в соответствующую вкладку.
    def _load_theory_text(self) -> None:
        # Очищаем поле теории перед записью.
        self.theory_text.delete("1.0", "end")
        # Вставляем готовый учебный текст.
        self.theory_text.insert("1.0", THEORY_TEXT)
        # Переводим поле теории в режим только для чтения.
        self.theory_text.configure(state="disabled")

    # Подставляем пример входных данных в поле ввода.
    def fill_example(self) -> None:
        # Очищаем текущее содержимое поля ввода.
        self.input_text.delete("1.0", "end")
        # Вставляем пример из конфигурации.
        self.input_text.insert("1.0", SAMPLE_DATA)
        # Обновляем строку статуса, чтобы пользователь видел, что пример уже подставлен.
        self.status_label.configure(text="Пример подставлен. Можно сразу запускать сортировку.")

    # Полностью очищаем все текстовые поля приложения.
    def clear_all(self) -> None:
        # Очищаем поле ввода.
        self.input_text.delete("1.0", "end")
        # Очищаем вкладку результата.
        self.result_text.delete("1.0", "end")
        # Очищаем вкладку шагов.
        self.steps_text.delete("1.0", "end")
        # Очищаем вкладку сравнения.
        self.compare_text.delete("1.0", "end")
        # Обновляем строку статуса.
        self.status_label.configure(text="Поля очищены. Введите новые данные.")

    # Меняем тему приложения по выбору пользователя.
    def change_theme(self, selected_theme: str) -> None:
        # Передаем выбранную тему библиотеке customtkinter.
        ctk.set_appearance_mode(selected_theme)
        # Показываем текущую тему в строке статуса.
        self.status_label.configure(text=f"Тема переключена на режим: {selected_theme}")

    # Считываем список чисел из поля ввода и возвращаем его в виде массива.
    def get_numbers_from_input(self) -> list[int | float]:
        # Получаем весь текст из поля ввода.
        raw_text = self.input_text.get("1.0", "end")
        # Преобразуем текст в список чисел и возвращаем результат.
        return parse_numbers(raw_text)

    # Определяем, выбран ли режим сортировки по убыванию.
    def is_reverse_order(self) -> bool:
        # Возвращаем истину, если в переключателе выбран вариант по убыванию.
        return self.order_var.get() == "По убыванию"

    # Запускаем выбранный алгоритм и выводим подробный результат.
    def run_sort(self) -> None:
        # Пытаемся получить данные и выполнить сортировку внутри безопасного блока.
        try:
            # Получаем массив чисел из поля ввода.
            numbers = self.get_numbers_from_input()
            # Получаем название выбранного алгоритма.
            selected_algorithm = self.algorithm_var.get()
            # Находим функцию сортировки по названию алгоритма.
            algorithm_function = ALGORITHM_FUNCTIONS[selected_algorithm]
            # Выполняем сортировку с учетом направления.
            result = algorithm_function(numbers, self.is_reverse_order())
            # Показываем итоговую информацию во вкладках.
            self.show_sort_result(result)
            # Обновляем строку статуса сообщением об успехе.
            self.status_label.configure(text=f"Сортировка завершена: {selected_algorithm}")
        # Обрабатываем ошибки пользовательского ввода.
        except InputDataError as error:
            # Показываем понятное окно с ошибкой.
            messagebox.showerror("Ошибка ввода", str(error))
            # Обновляем строку статуса.
            self.status_label.configure(text="Ошибка ввода. Проверьте числа в поле.")
        # Обрабатываем любые другие неожиданные ошибки.
        except Exception as error:
            # Показываем окно с текстом ошибки.
            messagebox.showerror("Неожиданная ошибка", str(error))
            # Обновляем строку статуса.
            self.status_label.configure(text="Произошла непредвиденная ошибка.")

    # Выводим результат сортировки в нужные вкладки интерфейса.
    def show_sort_result(self, result: SortResult) -> None:
        # Очищаем поле итогового результата.
        self.result_text.delete("1.0", "end")
        # Формируем красивый итоговый текст для первой вкладки.
        summary = (
            f"🏷 Алгоритм: {result.algorithm_name}\n\n"
            f"📥 Исходные данные: {format_numbers(result.source_data)}\n\n"
            f"📤 Отсортированные данные: {format_numbers(result.sorted_data)}\n\n"
            f"🔍 Сравнений: {result.comparisons}\n"
            f"🔁 Перестановок / сдвигов: {result.swaps}\n"
            f"⏱ Время выполнения: {result.elapsed_ms:.6f} мс"
        )
        # Вставляем итоговый текст во вкладку результата.
        self.result_text.insert("1.0", summary)

        # Очищаем поле шагов перед новой записью.
        self.steps_text.delete("1.0", "end")
        # Преобразуем список шагов в многострочный текст.
        steps_output = "\n".join(f"{index + 1}. {step}" for index, step in enumerate(result.steps))
        # Вставляем шаги во вкладку объяснения.
        self.steps_text.insert("1.0", steps_output if steps_output else "Шаги отсутствуют")

        # Делаем активной вкладку результата, чтобы пользователь сразу увидел итог.
        self.tabs.set("Результат")

    # Запускаем все алгоритмы подряд и показываем их мини-сравнение.
    def compare_algorithms(self) -> None:
        # Пытаемся выполнить сравнение внутри безопасного блока.
        try:
            # Получаем список чисел из поля ввода.
            numbers = self.get_numbers_from_input()
            # Создаем пустой список для результатов разных алгоритмов.
            results: list[SortResult] = []

            # Проходим по каждой доступной функции сортировки.
            for algorithm_name, algorithm_function in ALGORITHM_FUNCTIONS.items():
                # Выполняем алгоритм и добавляем результат в общий список.
                results.append(algorithm_function(numbers, self.is_reverse_order()))

            # Сортируем результаты по времени выполнения от меньшего к большему.
            results.sort(key=lambda item: item.elapsed_ms)
            # Очищаем поле сравнения перед новым выводом.
            self.compare_text.delete("1.0", "end")

            # Создаем шапку текста сравнения.
            comparison_output = "🏁 Сравнение алгоритмов\n\n"
            # Добавляем пояснение о входных данных.
            comparison_output += f"Входные данные: {format_numbers(numbers)}\n"
            # Добавляем выбранный порядок сортировки.
            comparison_output += f"Режим: {self.order_var.get()}\n\n"

            # Проходим по уже отсортированным результатам.
            for place, result in enumerate(results, start=1):
                # Добавляем одну строку с показателями очередного алгоритма.
                comparison_output += (
                    f"{place}. {result.algorithm_name}\n"
                    f"   • Время: {result.elapsed_ms:.6f} мс\n"
                    f"   • Сравнений: {result.comparisons}\n"
                    f"   • Перестановок / сдвигов: {result.swaps}\n"
                    f"   • Результат: {format_numbers(result.sorted_data)}\n\n"
                )

            # Вставляем сформированный текст на вкладку сравнения.
            self.compare_text.insert("1.0", comparison_output)
            # Переключаем пользователя на вкладку сравнения.
            self.tabs.set("Сравнение")
            # Обновляем строку статуса после успешного сравнения.
            self.status_label.configure(text="Сравнение алгоритмов успешно выполнено.")
        # Обрабатываем ошибки пользовательского ввода.
        except InputDataError as error:
            # Показываем окно с объяснением ошибки.
            messagebox.showerror("Ошибка ввода", str(error))
            # Обновляем строку статуса после ошибки.
            self.status_label.configure(text="Сравнение не выполнено из-за ошибки ввода.")
        # Обрабатываем любые другие неожиданные ошибки.
        except Exception as error:
            # Показываем окно с текстом неожиданной ошибки.
            messagebox.showerror("Неожиданная ошибка", str(error))
            # Обновляем строку статуса.
            self.status_label.configure(text="Произошла ошибка при сравнении алгоритмов.")