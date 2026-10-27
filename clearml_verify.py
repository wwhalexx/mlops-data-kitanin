import json
from pathlib import Path

from clearml import Dataset

from check_data import check_data


VERSIONS = [
    ("1.0.0", "8665e74fb58643179ccf9d9b4f120d39", "base"),
    ("1.1.0", "51057cea8c1d40c8a42390b038f624aa", "wine"),
    ("2.0.0", "ecdd27025172462586774221b78baba1", "iris_features"),
]

PROJECT_DIR = Path(__file__).resolve().parent
DOWNLOAD_ROOT = PROJECT_DIR.parent / "mlops-data-kitanin-clearml-downloads"


def main():
    # До скачивания проверяем все пути, чтобы избежать перезаписи.
    for version, _, _ in VERSIONS:
        target = DOWNLOAD_ROOT / version
        if target.exists() and any(target.iterdir()):
            raise ValueError(f"Папка не пустая: {target}")

    for version, dataset_id, mode in VERSIONS:
        dataset = Dataset.get(dataset_id=dataset_id)
        target = DOWNLOAD_ROOT / version

        print(f"\n{'=' * 60}", flush=True)
        print(f"Версия: {version}", flush=True)
        print(f"Dataset ID: {dataset.id}", flush=True)
        print("Файлы:", dataset.list_files(), flush=True)
        print("Добавленные:", dataset.list_added_files(), flush=True)
        print("Изменённые:", dataset.list_modified_files(), flush=True)
        print("Удалённые:", dataset.list_removed_files(), flush=True)
        print(
            "Граф зависимостей:",
            json.dumps(dataset.get_dependency_graph(), ensure_ascii=False),
            flush=True,
        )

        target.parent.mkdir(parents=True, exist_ok=True)
        dataset.get_mutable_local_copy(
            target_folder=str(target),
            overwrite=False,
        )

        print(f"Скачано в: {target}", flush=True)
        check_data(target, mode)

    print("\nВсе три версии скачаны и проверены.")


if __name__ == "__main__":
    main()