<div align="center">

# 🚗 Virtual Car Showroom & Recommendation Engine

An interactive Command-Line Interface (CLI) application built with Python and Pandas that processes multi-brand vehicle datasets, performs interactive feature lookups, compares vehicles side-by-side, and ranks top models across budget categories using a weighted recommendation engine.

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## 🌟 Application Screenshots & CLI Capabilities

### 1. Interactive Menu System
Upon launch, the application dynamically indexes the raw manufacturer datasets and renders a styled ASCII menu interface.

```text
==================================================
              VIRTUAL CAR SHOWROOM
==================================================

Hi Sir/Ma'am, Welcome to our Virtual Car Showroom
Loading Data...

Total manufacturers loaded: 9

+----------------------------------+
|           Menu System            |
+----------------------------------+
| 1. Search                        |
| 2. Car Comparison                |
| 3. Best Car in Manufacturer      |
| 4. Exit                          |
+----------------------------------+=

Available Manufacturers:

Audi, BMW, Ford, Hyundai, Mercedes, Skoda, Toyota, Vauxhall, Volkswagen

Allows users to compare two vehicles or more cars across core raw specifications (Year, Price, MPG, Engine Size, Horsepower) alongside calculated sub-scores and overall recommendation ratings

Sample:

CAR COMPARISON
--------------------------------------------------
Specification       Bmw 7 Series      Hyundi I30
--------------------------------------------------
Year                2013              2010
Price (£)           13950.00          3095.00
MPG                 50.40             50.42
Engine (L)          3.00              1.45
Horsepower          225               109
--------------------------------------------------
Power Score         10.00             4.84
Economy Score       10.00             10.00
Value Score         4.58              10.00
Overall Score       8.37              7.94
--------------------------------------------------

RECOMMENDATION
Bmw 7 Series (2013)
Overall Score: 8.37/10
--------------------------------------------------

Automatically filters and ranks vehicles within a specific brand into Budget, Mid-Range, and Top-Tier tiers based on custom weighted scoring:'

Sample:

================================================================================
                                 BEST BMW CARS
================================================================================

BUDGET
  Bmw 3 Series (1999) | £1200 | 31.0 MPG | 210 HP | 5.44/10

MID-RANGE
  Bmw M5 (2015) | £27052 | 28.5 MPG | 330 HP | 3.91/10

TOP
  Bmw 8 Series (2018) | £63980 | 26.9 MPG | 330 HP | 3.78/10

================================================================================


📂 Project Directory Structure

car-recommendation-cli/
├── Cars_Dataset/        # CSV files (Audi, BMW, Ford, Hyundai, etc.)
├── car_recomd.py        # Core application logic & recommendation engine
├── requirements.txt     # Python dependencies
├── .gitignore          # File exclusions
└── README.md            # Project documentation