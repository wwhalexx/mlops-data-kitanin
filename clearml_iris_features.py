import hashlib
import tempfile
from pathlib import Path

from clearml import Dataset
from sklearn.datasets import load_iris


BASE_ID = "8665e74fb58643179ccf9d9b4f120d39"


def main():
    with tempfile.TemporaryDirectory(prefix="mlops-iris-features-") as temp_dir:
        frame = load_iris(as_frame=True).frame
        frame = frame.sort_values(
            list(frame.columns),
            kind="mergesort",
        ).reset_index(drop=True)

        frame["sepal_area"] = (
            frame["sepal length (cm)"] * frame["sepal width (cm)"]
        )
        frame["petal_area"] = (
            frame["petal length (cm)"] * frame["petal width (cm)"]
        )

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
            "3e1ba63f55da2aabc432d00b1670140f5"
            "162bf9ef34b837598ec2fc176c9ff26"
        )
        if digest != expected:
            raise ValueError("Хэш Iris не совпадает с версией DVC")

        dataset = Dataset.create(
            dataset_project="MIIT/MLOps/practice_3/kitanin",
            dataset_name="sklearn-tabular-kitanin",
            dataset_version="2.0.0",
            parent_datasets=[BASE_ID],
            dataset_tags=["iris-features"],
            description=(
                "Отдельная ветвь от базы: Iris с признаками "
                "sepal_area и petal_area, без Wine."
            ),
        )

        print("Создан Dataset ID:", dataset.id, flush=True)

        # Заменяем унаследованный iris.csv его изменённой версией.
        dataset.add_files(path=str(path))

        if sorted(dataset.list_files()) != ["iris.csv"]:
            raise ValueError("Неверный состав Dataset")

        if sorted(dataset.list_modified_files()) != ["iris.csv"]:
            raise ValueError("Iris должен быть отмечен как изменённый файл")

        dataset.upload()
        dataset.finalize()

        print("\nBASE_ID:", BASE_ID)
        print("IRIS_FEATURES_ID:", dataset.id)
        print("Файлы:", dataset.list_files())
        print("Добавленные файлы:", dataset.list_added_files())
        print("Изменённые файлы:", dataset.list_modified_files())
        print("Граф зависимостей:", dataset.get_dependency_graph())
        print("SHA-256 iris.csv:", digest)
        print("Версия Iris с признаками загружена и финализирована.")


if __name__ == "__main__":
    main()