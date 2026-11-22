"""Compare sequential funnels across disjoint cohorts."""

TITLE = "Funnel Friction Map"
DESCRIPTION = "See where people leave a sequential funnel and which cohorts account for the loss."
PROMPT = ("Explain the biggest losses with their stage and cohort denominators. "
          "Separate absolute losses from percentages, flag small cohorts, and avoid causal claims.")


def analyze(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Input must be an object.")
    stages, cohorts = data.get("stages"), data.get("cohorts")
    if (not isinstance(stages, list) or len(stages) < 2
            or any(not isinstance(s, str) or not s.strip() for s in stages)
            or len(set(stages)) != len(stages)):
        raise ValueError("Provide at least two distinct, nonempty stage names.")
    if not isinstance(cohorts, dict) or not cohorts:
        raise ValueError("Provide a nonempty mapping of cohort names to counts.")
    rows = []
    totals = [0] * len(stages)
    for cohort, counts in cohorts.items():
        if not isinstance(cohort, str) or not cohort.strip():
            raise ValueError("Cohort names must be nonempty strings.")
        if (not isinstance(counts, list) or len(counts) != len(stages)
                or any(type(n) is not int or n < 0 for n in counts)):
            raise ValueError(f"{cohort}: provide one nonnegative integer per stage.")
        if any(after > before for before, after in zip(counts, counts[1:])):
            raise ValueError(f"{cohort}: counts must not increase between stages.")
        totals = [total + value for total, value in zip(totals, counts)]
        for i, (before, after) in enumerate(zip(counts, counts[1:])):
            rows.append({"Cohort": cohort, "From stage": stages[i], "To stage": stages[i + 1],
                         "Entered": before, "Reached next": after, "Lost": before - after,
                         "Loss (%)": round(100 * (before - after) / before, 2) if before else None})
    losses = [a - b for a, b in zip(totals, totals[1:])]
    peak = losses.index(max(losses))
    summary = (f"The largest pooled loss was {losses[peak]} of {totals[peak]} people "
               f"from {stages[peak]} to {stages[peak + 1]}.") if max(losses) else "No entrants were lost between stages."
    return {"summary": summary, "metrics": {"Entrants": totals[0], "Finishers": totals[-1],
            "Completion (%)": round(100 * totals[-1] / totals[0], 2) if totals[0] else None},
            "rows": rows}
