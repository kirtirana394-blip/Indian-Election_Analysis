# Indian National Level Election Data — Cleaning Summary

## Files
| File | Description |
|---|---|
| `indian-national-level-election.csv` | Raw input data (Lok Sabha election results, 1977–2014) |
| `data.py` | Python (pandas) script that cleans the raw data |
| `clean_election_data.csv` | Cleaned dataset, comma-separated |
| `clean_election_data.txt` | Cleaned dataset, tab-separated (same content as the CSV) |
| `readme.md` | This file |

## Source Data
- **Rows:** 73,081
- **Columns:** 11 — `st_name, year, pc_no, pc_name, pc_type, cand_name, cand_sex, partyname, partyabbre, totvotpoll, electors`
- **Coverage:** Indian general (Lok Sabha) elections, 1977–2014

## Issues Found in Raw Data
1. **Inconsistent state names** — same state spelled multiple ways, e.g.:
   - `Chattisgarh` / `Chhattisgarh`
   - `Orissa` / `Odisha`
   - `Pondicherry` / `Puducherry`
   - `Uttaranchal` / `Uttarakhand`
   - `Goa Daman & Diu` / `Goa, Daman & Diu`
   - `Nct Of Delhi` / `National Capital Territory Of Delhi`
2. **Missing values**
   - `pc_type`: 8,070 missing
   - `cand_sex`: 542 missing
3. **Inconsistent casing/whitespace**
   - `pc_type` had mixed case and trailing spaces (e.g. `"SC "`)
   - `pc_name` had 807 rows with leading/trailing whitespace
   - Candidate and constituency names had inconsistent capitalization
4. **Duplicate rows** — 1 exact duplicate row
5. **Logically invalid rows** — checked for votes exceeding electors or zero/negative electors (none found, but the check is built into the pipeline for safety)

## Cleaning Steps (`data.py`)
1. **Trim whitespace** from all text columns
2. **Standardize state names** to one canonical spelling per state
3. **Normalize `pc_type`** — uppercase, trimmed, missing values filled with `"UNKNOWN"`
4. **Normalize `cand_sex`** — uppercase, trimmed, missing values filled with `"UNKNOWN"`
5. **Title-case** candidate names (`cand_name`) and constituency names (`pc_name`)
6. **Enforce correct data types** for `year`, `pc_no`, `totvotpoll`, `electors` (all integers)
7. **Remove duplicates and invalid rows** (negative votes, zero electors, or votes exceeding electors)
8. **Add a derived column** — `vote_share_pct`: each candidate's vote share (%) of total electors in their constituency

## Output Schema
| Column | Type | Description |
|---|---|---|
| `st_name` | string | State/UT name (standardized) |
| `year` | int | Election year |
| `pc_no` | int | Parliamentary constituency number |
| `pc_name` | string | Constituency name |
| `pc_type` | string | Constituency category (`GEN`, `SC`, `ST`, `UNKNOWN`) |
| `cand_name` | string | Candidate name |
| `cand_sex` | string | Candidate sex (`M`, `F`, `O`, `UNKNOWN`) |
| `partyname` | string | Full party name |
| `partyabbre` | string | Party abbreviation |
| `totvotpoll` | int | Total votes polled for the candidate |
| `electors` | int | Total registered electors in the constituency |
| `vote_share_pct` | float | `totvotpoll / electors * 100`, rounded to 2 decimals |

## Result
- **73,080 clean rows** (1 duplicate removed from the original 73,081)
- **0 missing values** across all columns
- **12 columns** (added `vote_share_pct`)

## How to Reproduce
```bash
pip install pandas --break-system-packages
python data.py
```
This reads `indian-national-level-election.csv` from the same folder and writes `clean_election_data.csv` and `clean_election_data.txt`.
