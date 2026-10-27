import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_wine


MODES = {
    "base": {"iris.csv"},
    "wine": {"iris.csv", "wine.csv"},
    "iris_features": {"iris.csv"},
    "merged": {"iris.csv", "wine.csv"},
}


def check_data(directory: Path, mode: str) -> None:
    expected_files = MODES[mode]
    actual_files = {path.name for path in directory.glob("*.csv")}

    if actual_files != expected_files:
        raise ValueError(
            f"Неверный состав CSV: ожидалось {sorted(expected_files)}, "
            f"получено {sorted(actual_files)}"
        )

    for filename in sorted(expected_files):
        path = directory / filename
        frame = pd.read_csv(path)

        if any(str(column).startswith("Unnamed:") for column in frame.columns):
            raise ValueError(f"{filename}: найден столбец индекса")

        source = (
            load_iris(as_frame=True).frame
            if filename == "iris.csv"
            else load_wine(as_frame=True).frame
        )
        original_columns = list(source.columns)
        source = source.sort_values(
            original_columns,
            kind="mergesort",
        ).reset_index(drop=True)

        needs_features = (
            filename == "iris.csv"
            and mode in {"iris_features", "merged"}
        )
        expected_columns = original_columns.copy()
        if needs_features:
            expected_columns += ["sepal_area", "petal_area"]

        if list(frame.columns) != expected_columns:
            raise ValueError(f"{filename}: неверные столбцы или их порядок")

        if len(frame) != len(source):
            raise ValueError(f"{filename}: неверное количество строк")

        if not np.allclose(
            frame[original_columns].to_numpy(dtype=float),
            source.to_numpy(dtype=float),
            rtol=1e-9,
            atol=1e-10,
        ):
            raise ValueError(f"{filename}: исходные данные или порядок строк изменены")

        if needs_features:
            for part in ("sepal", "petal"):
                expected_area = (
                    frame[f"{part} length (cm)"]
                    * frame[f"{part} width (cm)"]
                )
                if not np.allclose(
                    frame[f"{part}_area"],
                    expected_area,
                    rtol=1e-9,
                    atol=1e-10,
                ):
                    raise ValueError(f"{filename}: неверные значения {part}_area")

        missing = int(frame.isna().sum().sum())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()

        print(f"Файл: {directory.name}/{filename}")
        print(f"SHA-256: {digest}")
        print(f"Строк: {frame.shape[0]}, столбцов: {frame.shape[1]}")
        print(f"Столбцы: {list(frame.columns)}")
        print(f"Пропусков: {missing}")
        print()

        if missing:
            raise ValueError(f"{filename}: обнаружены пропущенные значения")

    print("Все проверки пройдены.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Проверка версий данных")
    parser.add_argument("mode", choices=MODES)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "data",
    )
    args = parser.parse_args()

    try:
        check_data(args.data_dir, args.mode)
    except (ValueError, OSError) as error:
        parser.exit(status=1, message=f"Ошибка проверки: {error}\n")