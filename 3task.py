import timeit
from pathlib import Path

def build_shift_table(pattern):
    """Створити таблицю зсувів для алгоритму Боєра-Мура."""
    table = {}
    length = len(pattern)
    # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
    table.setdefault(pattern[-1], length)
    return table



def boyer_moore_search(text, pattern):
    # Створюємо таблицю зсувів для патерну (підрядка)
    shift_table = build_shift_table(pattern)
    i = 0  # Ініціалізуємо початковий індекс для основного тексту

    # Проходимо по основному тексту, порівнюючи з підрядком
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1  # Починаємо з кінця підрядка

        # Порівнюємо символи від кінця підрядка до його початку
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1  # Зсуваємось до початку підрядка

        # Якщо весь підрядок збігається, повертаємо його позицію в тексті
        if j < 0:
            return i  # Підрядок знайдено

        # Зсуваємо індекс i на основі таблиці зсувів
        # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # Якщо підрядок не знайдено, повертаємо -1
    return -1




def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено




def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i : i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(main_string[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base + ord(main_string[i + substring_length])
            ) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

mgs_FileNotFound = """
    ❌ Error type: {}
    ☝️ Для запуску сценарію перейдіть у папку, де знаходиться цей файл.
    """

mgs_WrongEncoding = """
    ❌ Error type: {}
    ☝️ Перевірте кодування файлу
    """


output_head = (
    "| {:^20}|".format("Algorithm types")
    + "{:^10}|\n".format("Speed")
    + "|"
    + "-" * 20
    + "|"
    + "-" * 10
    + "|"
)

fastest_result = "\nFastest algorithm: {} with total time: {}\n"






# Path to test files
path_text1 = Path.cwd().joinpath("text_data/text1.txt")
path_text2 = Path.cwd().joinpath("text_data/text2.txt")

pattern_result = "алгоритм"
pattern_no_result = "пам’яті"

results = {
    "kmp_search": 0,
    "boyer_moore_search": 0,
    "rabin_karp_search": 0,
}


if __name__ == "__main__":
    try:
        # Testing the performance of search algorithms for both approaches
        for approach, text_path in [("APPROACH 1", path_text1), ("APPROACH 2", path_text2)]:
            with open(text_path, "r", encoding="utf-8") as file_path:
                test_text = file_path.read()

            for key in results.keys():
                execution_time = timeit.timeit(
                    f"{key}(test_text, pattern_result)", globals=globals(), number=100
                )
                results[key] = round(execution_time, 5)

            fastest_algorithm, fastest_time = min(results.items(), key=lambda x: x[1])

            benchmark_res = "".join(
                f"\n| {key:<20}| {value:^9}|" for key, value in results.items()
            )

            print(approach, end="\n")
            print(output_head, benchmark_res, end="\n")
            print(fastest_result.format(fastest_algorithm, fastest_time))

            for key in results.keys():
                execution_time = timeit.timeit(
                    f"{key}(test_text, pattern_no_result)", globals=globals(), number=100
                )
                results[key] = round(execution_time, 5)

            fastest_algorithm, fastest_time = min(results.items(), key=lambda x: x[1])

            benchmark_res = "".join(
                f"\n| {key:<20}| {value:^9}|" for key, value in results.items()
            )

            print(output_head, benchmark_res, end="\n")
            print(fastest_result.format(fastest_algorithm, fastest_time))

    except FileNotFoundError as error:
        print(mgs_FileNotFound.format(type(error).__name__))
    except UnicodeDecodeError as error:
        print(mgs_WrongEncoding.format(type(error).__name__))