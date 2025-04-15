# readme

проверяет конфигурационный файл. валидация параметров и автотесты.

## установка

1. python 3.8+:
   ```bash
   python3 --version
   ```
   нет? ставь: ubuntu (`sudo apt install python3 python3-pip`), macos (`brew install python`), windows ([python.org](https://www.python.org/downloads/)).

2. виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # windows: venv\Scripts\activate
   ```

3. зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## запуск тестов

1. путь к конфигу (если надо):
   ```bash
   export CONFIG_PATH=/path/to/config.ini
   ```

2. тесты:
   ```bash
   pytest tests/ -v --cov=validator --junitxml=test-results/results.xml
   ```

## что где

- `validator.py`: валидация конфига.
- `tests/test_config.py`: автотесты.
- `test-results/`: логи и результаты (`results.xml`, `pytest.log`).