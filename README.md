# LeetCode — Python 3 Solutions

Daily problem-solving practice in **Python 3**, as part of my preparation for a career in quantitative finance.

## Why this repository

I solve one LeetCode problem every day. This repository keeps a clean, reviewable record of that work, with three goals:

- **Consistency:** one problem per day, one commit per problem.
- **Understanding over memorisation:** each uploaded solution is the best one I can **explain and defend**, not just one that passes the tests. If I can't reason about why it works and what it costs, it doesn't go in.
- **Interview readiness:** every file records the pattern, the time and space complexity, and how I got from my first idea to the final solution.

## What each file contains

Files are named after the official LeetCode number and title (`0001_two_sum.py`), so they sort in order and are easy to search.

Each file follows the same structure:

1. **Header docstring:** problem number, title, difficulty, link, pattern, complexity and notes. The notes cover my first approach, why I improved it, and the key insights or edge cases.
2. **`Solution` class:** identical to what I submit on LeetCode.
3. **Local tests:** an `if __name__ == "__main__":` block with `assert` checks (official examples plus edge cases).

Problem statements are not copied, since they belong to LeetCode. Each file links to the original problem instead.

## Tooling

- **Python 3.13**, standard library only.
- Written and debugged in **Visual Studio Code**, using breakpoints to trace tricky cases step by step.
- Formatted and linted automatically on save with **[Ruff](https://docs.astral.sh/ruff/)**, which enforces the standard Python style (PEP 8, Black-compatible) and flags common mistakes.

## Running a solution

```bash
python 0001_two_sum.py
```

Prints `OK` if all local tests pass.


## Author

**Diego Estévez Pérez**: BSc in Mathematical Engineering, currently studying for an MSc in Quantitative Finance (AFI, Madrid). Interested in quantitative finance and quantum computing.