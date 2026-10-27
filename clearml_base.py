import hashlib
import tempfile
from pathlib import Path

from clearml import Dataset
from sklearn.datasets import load_iris


def main():
    # Готовим исходный Iris отдельно от рабочей папки DVC.
    with tempfile.TemporaryDirectory(prefix="mlops-iris-base-") as temp_dir:
        frame = load_iris(as_frame=True).frame
        frame = frame.sort_values(
            list(frame.columns),
            kind="mergesort",
        ).reset_index(drop=True)

        path = Path(temp_dir) / "iris.csv"
        frame.to_csv(
            path,
            index=False,
            encoding="utf-8",
            lineterminator="\n",
            float_format="%.10g",
        )

        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = (
            "6d700503c9c2e2c71d187b889a87af8a8"
            "d3a6dd5bae1266d46f4ee4db5a6349f"
        )
        if digest != expected:
            raise ValueError("Хэш Iris не совпадает с базовой версией DVC")

        dataset = Dataset.create(
            dataset_project="MIIT/MLOps/practice_3/kitanin",
            dataset_name="sklearn-tabular-kitanin",
            dataset_version="1.0.0",
            dataset_tags=["base"],
            description="Базовая версия: исходный Iris из scikit-learn.",
        )

        print("Создан Dataset ID:", dataset.id, flush=True)

        dataset.add_files(path=str(path))

        if sorted(dataset.list_files()) != ["iris.csv"]:
            raise ValueError("Неверный состав базового Dataset")

        dataset.upload()
        dataset.finalize()

        print("\nBASE_ID:", dataset.id)
        print("Файлы:", dataset.list_files())
        print("SHA-256 iris.csv:", digest)
        print("Базовая версия загружена и финализирована.")


if __name__ == "__main__":
    main()