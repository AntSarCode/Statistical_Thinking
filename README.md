# Statistical Thinking for Data Science

This project demonstrates applied statistical reasoning in the context of data analysis, experiment design, and business decision-making. It includes hypothesis testing, A/B testing methodology, sample sizing, and dashboard reporting using real-world datasets.

## Project Overview

The goal of this project is to simulate common decision-making scenarios using sound statistical techniques. The pipeline takes the user from data ingestion to hypothesis evaluation and ends with a visual dashboard summarizing the outcome.

## Components

- Data import from SQL databases or `.csv` files
- Sample size estimation for A/B testing
- Hypothesis testing using z-tests and t-tests
- Confidence interval visualization
- Dashboard with conversion metrics and test results

## Technologies Used

| Purpose              | Tools / Libraries           |
|----------------------|-----------------------------|
| Language             | Python 3.10+                |
| Statistics & Testing | scipy, statsmodels, numpy   |
| Data Handling        | pandas                      |
| Visualization        | matplotlib, seaborn, Plotly |
| Database             | SQLite                      |

## Directory Structure

Statistical_Thinking/
├── A-B_Testing/
│   ├── 00_Database_Import.py
│   ├── 01_Stats_Hyp_Test.py
│   ├── 02_Minimum_Sample_Size.py
│   ├── 03_AB_Visuals.py
│   ├── 04_Dashboard.py
│   └── LendingClub.db (excluded from repo)
├── README.md
└── requirements.txt

## Instructions

1. Set up the environment
  - pip install -r requirements.txt

2. Run modules in order for complete A/B analysis:
  - python A-B_Testing/00_Database_Import.py
  - python A-B_Testing/01_Stats_Hyp_Test.py
  - python A-B_Testing/02_Minimum_Sample_Size.py
  - python A-B_Testing/03_AB_Visuals.py
  - python A-B_Testing/04_Dashboard.py

3. View final results in the generated HTML or live Dash dashboard

## Notes

  - The LendingClub.db file is too large for GitHub and is excluded via .gitignore
  - All scripts are modular and can be run independently

## Future Improvements
  - Add support for Bayesian testing methods

  - Integrate with real-time experiment logs

  - Expand dashboard to multi-test analysis

  - Support export to PDF report

Author
AntSarCode
Statistical Thinking Project
GitHub: https://github.com/AntSarCode
