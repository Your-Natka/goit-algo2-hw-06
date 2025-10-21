from datasketch import HyperLogLog
import random
import os

def load_ips_from_log(file_path):
    """Завантаження IP-адрес із лог-файлу"""
    ips = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                parts = line.split()
                for part in parts:
                    if part.count('.') == 3:  # Проста перевірка формату IPv4
                        ips.append(part)
        print(f"✅ Завантажено {len(ips)} IP-адрес із лог-файлу.")
    except FileNotFoundError:
        print("⚠️  Лог-файл не знайдено. Генеруємо тестові дані...")
        ips = [f"192.168.{random.randint(0, 50)}.{random.randint(1, 255)}"
               for _ in range(10000)]
        print(f"✅ Згенеровано {len(ips)} випадкових IP-адрес.")
    return ips


def estimate_unique_ips(ips):
    """Оцінка кількості унікальних IP-адрес за допомогою HyperLogLog"""
    hll = HyperLogLog(p=14)  # точність ~1%
    for ip in ips:
        hll.update(ip.encode('utf-8'))
    return len(ips), hll.count()


if __name__ == "__main__":
    print("🔹 Завантаження IP-адрес із лог-файлу...")
    log_file = "lms-stage-access.log"

    ips = load_ips_from_log(log_file)
    total, estimated = estimate_unique_ips(ips)

    print("\n📊 Результати аналізу:")
    print(f"🔸 Усього записів у логу: {total}")
    print(f"🔸 Приблизна кількість унікальних IP: {int(estimated)}")
    print(f"🔹 Похибка: {abs(total - estimated) / total * 100:.2f}%")
