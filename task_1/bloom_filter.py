import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size: int = 1000, num_hashes: int = 3):
        """Ініціалізуємо фільтр Блума з заданим розміром і кількістю хешів."""
        if size <= 0 or num_hashes <= 0:
            raise ValueError("Size and num_hashes must be positive integers.")
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item: str):
        """Генерує num_hashes позицій для елемента"""
        for i in range(self.num_hashes):
            yield mmh3.hash(item, i) % self.size

    def add(self, item: str):
        """Додає елемент до фільтра"""
        if not isinstance(item, str):
            item = str(item)
        for position in self._hashes(item):
            self.bit_array[position] = 1

    def __contains__(self, item: str) -> bool:
        """Перевіряє, чи може елемент бути у фільтрі"""
        if not isinstance(item, str):
            item = str(item)
        return all(self.bit_array[position] for position in self._hashes(item))
