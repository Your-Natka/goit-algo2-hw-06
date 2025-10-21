import re
import time
from datasketch import HyperLogLog


def load_ips_from_log(file_path: str) -> list[str]:
    """Завантажує IP-адреси з лог-файлу"""
    ips = []
    pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                ips.append(match.group())
    return ips


def count_unique_ips_set(ips: list[str]) -> tuple[int, float]:
    """Точний підрахунок через set"""
    start = time.time()
    unique_ips = len(set(ips))
    end = time.time()
    return unique_ips, end - start


def count_unique_ips_hll(ips: list[str], precision: int = 12) -> tuple[int, float]:
    """Наближений підрахунок через HyperLogLog"""
    start = time.time()
    hll = HyperLogLog(p=precision)
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    end = time.time()
    return int(hll.count()), end - start


if __name__ == "__main__":
    log_file = "lms-stage-access.log"

    print("🔹 Завантаження IP-адрес із лог-файлу...")
    ips = load_ips_from_log(log_file)
    print(f"Знайдено {len(ips)} записів у лог-файлі.")

    print("\n🔹 Порівняння підрахунків...")
    exact_count, exact_time = count_unique_ips_set(ips)
    hll_count, hll_time = count_unique_ips_hll(ips)

    print("\nРезультати порівняння:")
    print(f"{'Метод':<25}{'Унікальні елементи':<25}{'Час виконання (сек.)'}")
    print(f"{'-'*70}")
    print(f"{'Точний підрахунок (set)':<25}{exact_count:<25}{exact_time:.4f}")
    print(f"{'HyperLogLog':<25}{hll_count:<25}{hll_time:.4f}")
