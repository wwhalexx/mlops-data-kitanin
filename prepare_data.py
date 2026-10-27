import argparse
from pathlib import Path

from sklearn.datasets import load_iris, load_wine


DATA_DIR = Path(__file__).resolve().parent / "data"


def prepare_data(mode: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if mode == "wine":
        frame = load_wine(as_frame=True).frame
        filename = "wine.csv"
    else:
        frame = load_iris(as_frame=True).frame
        filename = "iris.csv"

    # Сортируем по всем исходным признакам и target.
    original_columns = list(frame.columns)
    frame = frame.sort_values(
        original_columns,
        kind="mergesort",
    ).reset_index(drop=True)

    if mode == "iris_features":
        frame["sepal_area"] = (
            frame["sepal length (cm)"] * frame["sepal width (cm)"]
        )
        frame["petal_area"] = (
            frame["petal length (cm)"] * frame["petal width (cm)"]
        )

    path = DATA_DIR / filename
    frame.to_csv(
        path,
        index=False,
        encoding="utf-8",
        lineterminator="\n",
        float_format="%.10g",
    )

    print(f"Сохранён файл: data/{filename}")
    print(f"Строк: {frame.shape[0]}, столбцов: {frame.shape[1]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Подготовка данных Iris и Wine")
    parser.add_argument(
        "mode",
        choices=["base", "wine", "iris_features"],
    )
    args = parser.parse_args()
    prepare_data(args.mode)