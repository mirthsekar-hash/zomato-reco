from __future__ import annotations

import json
from pathlib import Path

from datasets import load_dataset
import pandas as pd

from .config import FoundationConfig
from .preprocess import preprocess_restaurants
from .quality import build_quality_report


def _load_raw_dataframe(config: FoundationConfig) -> pd.DataFrame:
    dataset = load_dataset(config.dataset_name, split=config.split)
    return dataset.to_pandas()


def run_foundation_pipeline(config: FoundationConfig | None = None) -> dict:
    cfg = config or FoundationConfig()
    cfg.output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = _load_raw_dataframe(cfg)
    cleaned_df = preprocess_restaurants(raw_df)
    report = build_quality_report(cleaned_df)

    cleaned_df.to_csv(cfg.output_csv_path, index=False)
    cfg.quality_report_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")

    return {
        "output_csv": str(cfg.output_csv_path),
        "quality_report": str(cfg.quality_report_path),
        "rows_written": len(cleaned_df),
        "quality_gate_passed": report.quality_gate_passed,
    }


if __name__ == "__main__":
    result = run_foundation_pipeline()
    print(json.dumps(result, indent=2))

