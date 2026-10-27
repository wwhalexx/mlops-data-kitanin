import hashlib
import tempfile
from pathlib import Path

from clearml import Dataset
from sklearn.datasets import load_wine


BASE_ID = "8665e74fb58643179ccf9d9b4f120d39"


def main():
    with tempfile.TemporaryDirectory(prefix="mlops-wine-") as temp_dir:
        frame = load_wine(as_frame=True).frame
        frame = frame.sort_values(
            list(frame.columns),
            kind="mergesort",
        ).reset_index(drop=True)

        path = Path(temp_dir) / "wine.csv"
        frame.to_csv(
            path,
            index=False,
            encoding="utf-8",
            lineterminator="\n",
            float_format="%.10g",
        )

        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = (
            "38860ba04ace4d402242340bcf40be4bd"
            "6f4ebde9144a3dc89dc12c20f7f8e60"
        )
        if digest != expected:
            raise ValueError("Хэш Wine не совпадает с версией DVC")

        dataset = Dataset.create(
            dataset_project="MIIT/MLOps/practice_3/kitanin",
            dataset_name="sklearn-tabular-kitanin",
            dataset_version="1.1.0",
            parent_datasets=[BASE_ID],
            dataset_tags=["wine"],
            description="Наследует исходный Iris от базы и добавляет Wine.",
        )

        print("Создан Dataset ID:", dataset.id, flush=True)

        # Iris наследуется: повторно его не добавляем.
        dataset.add_files(path=str(path))

        if sorted(dataset.list_files()) != ["iris.csv", "wine.csv"]:
            raise ValueError("Неверный состав Dataset")

        dataset.upload()
        dataset.finalize()

        print("\nBASE_ID:", BASE_ID)
        print("WINE_ID:", dataset.id)
        print("Файлы:", dataset.list_files())
        print("Добавленные файлы:", dataset.list_added_files())
        print("Граф зависимостей:", dataset.get_dependency_graph())
        print("SHA-256 wine.csv:", digest)
        print("Версия Wine загружена и финализирована.")


if __name__ == "__main__":
    main()