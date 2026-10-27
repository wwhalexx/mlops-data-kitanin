# Практическая работа №3: версионирование данных

Автор: Китанин

## Окружение

- Python: 3.12.15
- DVC: 3.67.1
- ClearML: 2.1.12
- pandas: 3.1.0
- scikit-learn: 1.9.1
- Зависимости зафиксированы в poetry.lock.

## Базовая версия DVC

- Git tag: data-v1
- Состав: только data/iris.csv.
- Размер Iris: 150 строк, 5 столбцов.
- Пропущенных значений: 0.
- SHA-256 iris.csv:
  6d700503c9c2e2c71d187b889a87af8a8d3a6dd5bae1266d46f4ee4db5a6349f
- Хэш директории из data.dvc:
  bf5656de288a783265cb7b85509abc8e.dir
- Повторная генерация base дала одинаковый SHA-256.
- check_data.py base: все проверки пройдены.
- dvc status: Data and pipelines are up to date.

- Базовый Git-коммит: 110f33170a960cacfd1cd1f2ef6b9e7a5a2cc5f9.

## DVC remote

- Имя: localremote.
- Расположение: ../mlops-data-kitanin-remote.
- Хранилище находится вне Git-репозитория.
- Тип: локальная директория.