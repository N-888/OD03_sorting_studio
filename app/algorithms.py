# Импортируем датакласс, чтобы удобно хранить итог работы каждого алгоритма в одной структуре.
from dataclasses import dataclass, field

# Импортируем счетчик высокой точности, чтобы измерять скорость работы алгоритмов.
from time import perf_counter_ns

# Импортируем тип Callable, чтобы описывать словарь с функциями сортировки.
from typing import Callable


# Создаем общий тип для чисел, чтобы алгоритмы работали и с целыми, и с дробными значениями.
Number = int | float


# Создаем структуру результата сортировки, чтобы удобно передавать данные в интерфейс.
@dataclass
class SortResult:
    # Сохраняем название алгоритма, который был использован.
    algorithm_name: str
    # Сохраняем исходные данные, чтобы можно было показать их в интерфейсе.
    source_data: list[Number]
    # Сохраняем отсортированные данные.
    sorted_data: list[Number]
    # Сохраняем список текстовых шагов, чтобы показать подробное объяснение пользователю.
    steps: list[str] = field(default_factory=list)
    # Сохраняем количество сравнений элементов.
    comparisons: int = 0
    # Сохраняем количество перестановок или сдвигов элементов.
    swaps: int = 0
    # Сохраняем длительность работы алгоритма в миллисекундах.
    elapsed_ms: float = 0.0


# Создаем функцию, которая определяет, нужно ли менять элементы местами с учетом выбранного направления сортировки.
def should_move_left(left_value: Number, right_value: Number, reverse: bool) -> bool:
    # Возвращаем истину для сортировки по убыванию, если левый элемент меньше правого.
    if reverse:
        return left_value < right_value

    # Возвращаем истину для сортировки по возрастанию, если левый элемент больше правого.
    return left_value > right_value


# Реализуем пузырьковую сортировку в классическом виде.
def bubble_sort(data: list[Number], reverse: bool = False) -> SortResult:
    # Создаем копию списка, чтобы не портить исходные данные пользователя.
    items = data.copy()
    # Создаем пустой список текстовых шагов.
    steps: list[str] = []
    # Обнуляем счетчик сравнений.
    comparisons = 0
    # Обнуляем счетчик перестановок.
    swaps = 0
    # Сохраняем момент старта, чтобы позже вычислить время работы.
    started_at = perf_counter_ns()

    # Запускаем внешний цикл по количеству проходов.
    for run in range(len(items) - 1):
        # Добавляем заголовок текущего прохода в список шагов.
        steps.append(f"Проход {run + 1}: начинаем обход массива {items}")

        # Запускаем внутренний цикл до последнего неотсортированного элемента.
        for index in range(len(items) - 1 - run):
            # Увеличиваем счетчик сравнений, потому что сейчас будет сравнение двух соседей.
            comparisons += 1
            # Сохраняем левый элемент для удобства чтения кода.
            left_value = items[index]
            # Сохраняем правый элемент для удобства чтения кода.
            right_value = items[index + 1]
            # Добавляем в шаги информацию о текущем сравнении.
            steps.append(f"Сравниваем элементы {left_value} и {right_value}")

            # Проверяем, нужно ли менять эти элементы местами.
            if should_move_left(left_value, right_value, reverse):
                # Меняем местами два соседних элемента.
                items[index], items[index + 1] = items[index + 1], items[index]
                # Увеличиваем счетчик перестановок.
                swaps += 1
                # Добавляем в шаги пояснение после обмена.
                steps.append(f"Меняем местами → получаем {items}")
            else:
                # Добавляем в шаги пояснение, что обмен не потребовался.
                steps.append("Порядок верный, обмен не нужен")

    # Вычисляем длительность работы алгоритма в миллисекундах.
    elapsed_ms = (perf_counter_ns() - started_at) / 1_000_000

    # Возвращаем собранный результат пузырьковой сортировки.
    return SortResult(
        algorithm_name="Пузырьковая сортировка",
        source_data=data.copy(),
        sorted_data=items,
        steps=steps,
        comparisons=comparisons,
        swaps=swaps,
        elapsed_ms=elapsed_ms,
    )


# Реализуем сортировку выбором в классическом виде.
def selection_sort(data: list[Number], reverse: bool = False) -> SortResult:
    # Создаем копию списка, чтобы исходные данные остались без изменений.
    items = data.copy()
    # Создаем пустой список шагов.
    steps: list[str] = []
    # Обнуляем счетчик сравнений.
    comparisons = 0
    # Обнуляем счетчик перестановок.
    swaps = 0
    # Запоминаем время старта.
    started_at = perf_counter_ns()

    # Проходим по каждому индексу списка.
    for index in range(len(items)):
        # Считаем, что первый элемент неотсортированной части пока лучший кандидат.
        selected_index = index
        # Добавляем в шаги пояснение о начале нового этапа.
        steps.append(f"Шаг {index + 1}: ищем подходящий элемент для позиции {index}")

        # Ищем минимальный или максимальный элемент в оставшейся части списка.
        for scan_index in range(index + 1, len(items)):
            # Увеличиваем счетчик сравнений.
            comparisons += 1
            # Добавляем подробность о текущем сравнении.
            steps.append(
                f"Сравниваем кандидата {items[selected_index]} и элемент {items[scan_index]}"
            )

            # Для сортировки по убыванию выбираем больший элемент.
            if reverse and items[scan_index] > items[selected_index]:
                # Обновляем индекс лучшего кандидата.
                selected_index = scan_index
                # Добавляем пояснение о новом кандидате.
                steps.append(f"Новый кандидат для позиции {index} → {items[selected_index]}")
            # Для сортировки по возрастанию выбираем меньший элемент.
            elif not reverse and items[scan_index] < items[selected_index]:
                # Обновляем индекс лучшего кандидата.
                selected_index = scan_index
                # Добавляем пояснение о новом кандидате.
                steps.append(f"Новый кандидат для позиции {index} → {items[selected_index]}")

        # Проверяем, нужно ли реально выполнять обмен.
        if selected_index != index:
            # Меняем местами текущий элемент и найденный лучший элемент.
            items[index], items[selected_index] = items[selected_index], items[index]
            # Увеличиваем счетчик перестановок.
            swaps += 1
            # Добавляем в шаги результат обмена.
            steps.append(f"Ставим элемент на место → получаем {items}")
        else:
            # Добавляем в шаги пояснение, что обмен не потребовался.
            steps.append(f"Элемент {items[index]} уже стоит на правильной позиции")

    # Вычисляем итоговое время работы.
    elapsed_ms = (perf_counter_ns() - started_at) / 1_000_000

    # Возвращаем готовый результат сортировки выбором.
    return SortResult(
        algorithm_name="Сортировка выбором",
        source_data=data.copy(),
        sorted_data=items,
        steps=steps,
        comparisons=comparisons,
        swaps=swaps,
        elapsed_ms=elapsed_ms,
    )


# Реализуем сортировку вставками в классическом виде.
def insertion_sort(data: list[Number], reverse: bool = False) -> SortResult:
    # Создаем копию списка, чтобы не изменять исходные данные пользователя.
    items = data.copy()
    # Создаем пустой список шагов.
    steps: list[str] = []
    # Обнуляем счетчик сравнений.
    comparisons = 0
    # Обнуляем счетчик перестановок и сдвигов.
    swaps = 0
    # Запоминаем время старта.
    started_at = perf_counter_ns()

    # Начинаем со второго элемента, потому что первый уже считается отсортированным.
    for index in range(1, len(items)):
        # Сохраняем текущий элемент, который будем вставлять в нужное место.
        key = items[index]
        # Сохраняем индекс элемента слева для сравнения.
        previous_index = index - 1
        # Добавляем пояснение о начале шага вставки.
        steps.append(f"Берем элемент {key} и ищем для него правильную позицию")

        # Сдвигаем элементы вправо, пока они больше key при обычной сортировке или меньше key при обратной.
        while previous_index >= 0:
            # Увеличиваем счетчик сравнений, потому что сейчас будет проверка условия.
            comparisons += 1
            # Добавляем в шаги информацию о сравнении.
            steps.append(f"Сравниваем {items[previous_index]} и {key}")

            # Проверяем, нужно ли сдвигать элемент вправо.
            if should_move_left(items[previous_index], key, reverse):
                # Сдвигаем элемент на одну позицию вправо.
                items[previous_index + 1] = items[previous_index]
                # Увеличиваем счетчик сдвигов.
                swaps += 1
                # Добавляем в шаги промежуточное состояние списка.
                steps.append(f"Сдвигаем элемент вправо → {items}")
                # Смещаемся еще левее.
                previous_index -= 1
            else:
                # Завершаем цикл, если дальше сдвиг уже не нужен.
                break

        # Вставляем сохраненный элемент на освободившуюся позицию.
        items[previous_index + 1] = key
        # Добавляем в шаги результат вставки.
        steps.append(f"Вставляем {key} на место → {items}")

    # Вычисляем длительность работы алгоритма.
    elapsed_ms = (perf_counter_ns() - started_at) / 1_000_000

    # Возвращаем итог сортировки вставками.
    return SortResult(
        algorithm_name="Сортировка вставками",
        source_data=data.copy(),
        sorted_data=items,
        steps=steps,
        comparisons=comparisons,
        swaps=swaps,
        elapsed_ms=elapsed_ms,
    )


# Реализуем быструю сортировку в учебном рекурсивном стиле.
def quick_sort(data: list[Number], reverse: bool = False) -> SortResult:
    # Создаем список шагов, который будем заполнять по мере рекурсии.
    steps: list[str] = []
    # Создаем словарь-счетчик, чтобы изменять значения внутри вложенной функции.
    counters = {"comparisons": 0, "swaps": 0}
    # Запоминаем время старта сортировки.
    started_at = perf_counter_ns()

    # Создаем вложенную рекурсивную функцию, которая сортирует подсписок.
    def _quick_sort(items: list[Number], depth: int = 0) -> list[Number]:
        # Проверяем базовый случай, когда список пустой или состоит из одного элемента.
        if len(items) <= 1:
            # Добавляем пояснение о завершении рекурсии на этой глубине.
            steps.append(f"Уровень {depth}: список {items} не требует дальнейшей сортировки")
            # Возвращаем список как есть.
            return items.copy()

        # Берем первый элемент как опорный.
        pivot = items[0]
        # Создаем пустой список для элементов меньше опорного.
        left: list[Number] = []
        # Создаем пустой список для элементов, равных опорному.
        center: list[Number] = []
        # Создаем пустой список для элементов больше опорного.
        right: list[Number] = []
        # Добавляем пояснение о выборе опорного элемента.
        steps.append(f"Уровень {depth}: выбираем опорный элемент {pivot} из списка {items}")

        # Проходим по всем элементам текущего списка.
        for item in items:
            # Увеличиваем число сравнений на одну логическую проверку попадания в группу.
            counters["comparisons"] += 1

            # Для обратной сортировки отправляем большие элементы влево.
            if reverse:
                # Проверяем, что элемент больше опорного.
                if item > pivot:
                    # Добавляем элемент в левую часть.
                    left.append(item)
                    # Увеличиваем число операций распределения.
                    counters["swaps"] += 1
                # Проверяем, что элемент меньше опорного.
                elif item < pivot:
                    # Добавляем элемент в правую часть.
                    right.append(item)
                    # Увеличиваем число операций распределения.
                    counters["swaps"] += 1
                # Обрабатываем элементы, равные опорному.
                else:
                    # Добавляем равный элемент в центральную часть.
                    center.append(item)
            # Для обычной сортировки меньшие элементы кладем влево.
            else:
                # Проверяем, что элемент меньше опорного.
                if item < pivot:
                    # Добавляем элемент в левую часть.
                    left.append(item)
                    # Увеличиваем число операций распределения.
                    counters["swaps"] += 1
                # Проверяем, что элемент больше опорного.
                elif item > pivot:
                    # Добавляем элемент в правую часть.
                    right.append(item)
                    # Увеличиваем число операций распределения.
                    counters["swaps"] += 1
                # Обрабатываем элементы, равные опорному.
                else:
                    # Добавляем равный элемент в центральную часть.
                    center.append(item)

        # Добавляем в шаги результат разбиения текущего списка.
        steps.append(
            f"Уровень {depth}: left={left}, center={center}, right={right}"
        )

        # Рекурсивно сортируем левую часть.
        left_sorted = _quick_sort(left, depth + 1)
        # Рекурсивно сортируем правую часть.
        right_sorted = _quick_sort(right, depth + 1)
        # Собираем итог текущего уровня.
        merged = left_sorted + center + right_sorted
        # Добавляем в шаги результат сборки списка на текущем уровне.
        steps.append(f"Уровень {depth}: собираем список обратно → {merged}")
        # Возвращаем отсортированный список выше по рекурсии.
        return merged

    # Запускаем рекурсивную сортировку на копии исходных данных.
    sorted_items = _quick_sort(data.copy())
    # Вычисляем итоговую длительность работы алгоритма.
    elapsed_ms = (perf_counter_ns() - started_at) / 1_000_000

    # Возвращаем итог быстрой сортировки.
    return SortResult(
        algorithm_name="Быстрая сортировка",
        source_data=data.copy(),
        sorted_data=sorted_items,
        steps=steps,
        comparisons=counters["comparisons"],
        swaps=counters["swaps"],
        elapsed_ms=elapsed_ms,
    )


# Создаем словарь всех доступных алгоритмов, чтобы удобно выбирать нужную функцию в интерфейсе.
ALGORITHM_FUNCTIONS: dict[str, Callable[[list[Number], bool], SortResult]] = {
    "Пузырьковая сортировка": bubble_sort,
    "Быстрая сортировка": quick_sort,
    "Сортировка выбором": selection_sort,
    "Сортировка вставками": insertion_sort,
}