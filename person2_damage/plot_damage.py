"""Plot OpenQuake scenario-damage results exported by `oq show aggrisk 5`.

Run from the repository root:
    python person2_damage/plot_damage.py person2_damage/results/nepal_demo/aggrisk.txt
"""
from pathlib import Path
import argparse
import csv
import re
import matplotlib.pyplot as plt
import numpy as np

STATES = ["No damage", "Slight", "Moderate", "Extreme", "Complete"]

def read_aggrisk(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        parts = line.split()
        # `oq show aggrisk` prints a pandas-like table with an index column.
        # Accept rows with or without that initial index.
        for offset in (1, 0):
            fields = parts[offset:]
            if len(fields) != 9:
                continue
            try:
                agg, rlz, loss = map(int, fields[:3])
                damages = list(map(float, fields[3:8]))
                losses = float(fields[8])
            except ValueError:
                continue
            if all(np.isfinite(damages)) and min(damages) >= 0:
                rows.append(dict(agg_id=agg, rlz_id=rlz, loss_id=loss,
                                 **{f"dmg_{i}": v for i, v in enumerate(damages)},
                                 losses=losses))
                break
    if not rows:
        raise ValueError("No aggrisk rows detected. Save the output of `oq show aggrisk 5` to a text file.")
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Saved text output from `oq show aggrisk 5`")
    args = parser.parse_args()
    rows = read_aggrisk(args.input)
    output_dir = args.input.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "damage_distribution.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    # Restrict to overall aggregation (agg_id = 0) and available loss categories.
    rows = [r for r in rows if r["agg_id"] == 0]
    loss_ids = sorted(set(r["loss_id"] for r in rows))
    for loss_id in loss_ids:
        selected = sorted((r for r in rows if r["loss_id"] == loss_id), key=lambda r: r["rlz_id"])
        if not selected:
            continue
        ids = [r["rlz_id"] for r in selected]
        values = np.array([[r[f"dmg_{i}"] for i in range(5)] for r in selected])
        fig, ax = plt.subplots(figsize=(10, 5.5))
        x = np.arange(len(STATES))
        width = .8 / len(selected)
        for j, (rlz_id, vals) in enumerate(zip(ids, values)):
            ax.bar(x - .4 + width * (j + .5), vals, width, label=f"Realization {rlz_id}")
        ax.set_xticks(x, STATES)
        ax.set_ylabel("Expected damaged asset units")
        ax.set_title(f"Scenario damage distribution — loss_id {loss_id}")
        ax.legend()
        ax.grid(axis="y", alpha=.25)
        fig.tight_layout()
        fig.savefig(output_dir / f"damage_distribution_loss_{loss_id}.png", dpi=200)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(9, 5))
        percents = values / values.sum(axis=1, keepdims=True) * 100
        bottoms = np.zeros(len(selected))
        for i, state in enumerate(STATES):
            ax.bar([f"Realization {n}" for n in ids], percents[:, i], bottom=bottoms, label=state)
            bottoms += percents[:, i]
        ax.set_ylabel("Share of reported damage-state units (%)")
        ax.set_ylim(0, 100)
        ax.set_title(f"Damage-state shares — loss_id {loss_id}")
        ax.legend(loc="center left", bbox_to_anchor=(1, .5))
        fig.tight_layout()
        fig.savefig(output_dir / f"damage_percentages_loss_{loss_id}.png", dpi=200)
        plt.close(fig)
    print(f"Saved CSV and graphs in: {output_dir.resolve()}")
    print("Note: separate realizations are alternative outcomes; do not add their counts together.")
    print("Verify the exposure inventory and hazard coverage before interpreting the totals.")

if __name__ == "__main__":
    main()
