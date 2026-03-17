from pathlib import Path
import pandas as pd


def save_rows_to_csv(rows:list[dict],output_file:Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False,encoding='utf-8')