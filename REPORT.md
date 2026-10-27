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

## Ветки и слияние DVC

| Состояние | Git-коммит | SHA-256 файла data.dvc |
|---|---|---|
| Добавлен Wine | 4debf19aaf494d2a85bc108b0092f7c94cf4ec6e | c42cbceead4c55e97976c576e2bc8dd9ab7037d776a1eff253e8ecde3170ff24 |
| Добавлены признаки Iris | bb3491a5874e9c53cca95e94a592a0450ad331ed | e6ba0d79a80bff8042f21fd623be1788c9babbd1a70a0fcc9293dbf4be1212c9 |
| Слияние веток | 39f78a1128f37e8ad40b1dc6d128c230eaa61e60 | b63003486e5847feba08f387096e7a53191e49eae92790a231dc6c99bbce7692 |

Ветки feature/wine и feature/iris-features созданы от общей базы.
Для объединения настроен DVC merge driver.
Итоговая версия содержит Iris с дополнительными признаками и Wine.
История обеих веток сохранена. Итог перенесён в main.

## Восстановление из чистого клона

Создан отдельный клон mlops-data-kitanin-clean.
Workspace и cache исходного проекта вручную не копировались.
Команда dvc pull получила 3 объекта и восстановила 2 CSV.

| Файл | Строк | Столбцов | Пропусков | SHA-256 |
|---|---:|---:|---:|---|
| data/iris.csv | 150 | 7 | 0 | 3e1ba63f55da2aabc432d00b1670140f5162bf9ef34b837598ec2fc176c9ff26 |
| data/wine.csv | 178 | 14 | 0 | 38860ba04ace4d402242340bcf40be4bd6f4ebde9144a3dc89dc12c20f7f8e60 |

check_data.py merged: все проверки пройдены.
dvc status: Data and pipelines are up to date.
git status --short: пустой вывод.

Локальный remote позволяет восстановить данные в другом клоне на этом
компьютере. Для восстановления на другой машине требуется доступ к этому
хранилищу или перенос remote.