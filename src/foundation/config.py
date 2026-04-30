from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FoundationConfig:
    dataset_name: str = "ManikaSaini/zomato-restaurant-recommendation"
    split: str = "train"
    output_dir: Path = Path("data/processed")
    output_file_name: str = "restaurants_cleaned.csv"
    quality_report_file_name: str = "quality_report.json"
    min_required_columns: tuple[str, ...] = ("name", "location", "cuisines", "average_cost_for_two", "aggregate_rating")

    @property
    def output_csv_path(self) -> Path:
        return self.output_dir / self.output_file_name

    @property
    def quality_report_path(self) -> Path:
        return self.output_dir / self.quality_report_file_name

