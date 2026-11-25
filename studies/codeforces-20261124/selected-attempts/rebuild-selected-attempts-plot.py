"""Rebuild the study figure with API costs from selected attempts only."""
from __future__ import annotations

import argparse
import json
from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

from experiments.analysis import run_key
from experiments.report import Study, accuracy_cost_points, decimal_cost, draw_plot, read_json


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", type=Path, required=True, help="Extracted study archive")
    parser.add_argument("--output", type=Path, required=True, help="Output figure PDF")
    args = parser.parse_args()

    all_attempts = Study.load(args.study)
    selected_costs = {
        run_key(row): decimal_cost(row["model_cost_usd"]) for row in all_attempts.rows
    }
    selected_total = sum(selected_costs.values(), Decimal(0))
    audit = read_json(args.study / "data-audit.json")
    if selected_total != decimal_cost(audit["selected_attempt_cost_usd"]):
        raise ValueError("Selected-attempt costs do not reconcile with the archive audit")
    if any(cost > all_attempts.costs[key] for key, cost in selected_costs.items()):
        raise ValueError("Selected-attempt cost exceeds the corresponding all-attempt cost")

    selected = replace(all_attempts, costs=selected_costs)
    plot_data = accuracy_cost_points(selected)
    settings = read_json(args.study / "report-settings.json")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as staging:
        staging_path = Path(staging)
        draw_plot(plot_data, staging_path, xlim=settings["xlim"], ylim=settings["ylim"])
        copyfile(staging_path / "accuracy-vs-cost.pdf", args.output)

    points = plot_data["points"]
    subtotals = {
        condition: sum(
            (cost for key, cost in selected_costs.items() if key[2] == condition),
            Decimal(0),
        )
        for condition in points
    }
    for condition, point in points.items():
        point["mean_selected_attempt_usd_per_task"] = point.pop(
            "mean_all_attempt_cost_usd_per_task"
        )
        point["total_selected_attempt_usd"] = str(subtotals[condition])
    print(
        json.dumps(
            {
                "total_selected_attempt_usd": str(selected_total),
                "excluded_attempt_usd": str(
                    sum(all_attempts.costs.values(), Decimal(0)) - selected_total
                ),
                "points": points,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
