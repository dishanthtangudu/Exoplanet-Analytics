# 🪐 Exoplanet Analytics

### A Data-Driven Analysis of Exoplanets and Astronomical Events

## 1. Project Overview

Exoplanet Analytics is a Python-based data analytics web application developed using Streamlit. It allows users to explore astronomical datasets, manage records, analyze scientific measurements, and visualize patterns through interactive charts.

The application uses CSV files for data storage and Pandas and NumPy for data processing and statistical analysis.

## 2. Project Objectives

- Explore and analyze astronomical datasets.
- Perform Create, Read, Update, and Delete (CRUD) operations on records.
- Search, filter, and sort dataset records.
- Calculate useful summary statistics.
- Display interactive charts and visualizations.
- Store and manage data using CSV files.
- Export filtered datasets for further analysis.

## 3. Project Modules

### Module 1: Exoplanet Discoveries

Explores exoplanet candidates and their characteristics using Kepler Objects of Interest (KOI) data.

**Main features:**
- Exoplanet disposition analysis.
- Kepler score distribution.
- Orbital period and planet radius comparison.
- Summary statistics for exoplanet records.

### Module 2: Exoplanet Characteristics

Analyzes Kepler time-series data using training and testing datasets.

**Main features:**
- Training and testing dataset selection.
- Exoplanet and non-exoplanet signal counts.
- Exoplanet signal distribution.
- Flux signal visualization.

### Module 3: Meteorite Landings

Analyzes meteorite landing records and their physical characteristics.

**Main features:**
- Meteorite classification.
- Meteorite fall status analysis.
- Landing year distribution.
- Meteorite mass distribution.

### Module 4: Solar and Lunar Eclipses

Explores solar and lunar eclipse records using astronomical measurements.

**Main features:**
- Solar and lunar eclipse dataset selection.
- Eclipse type distribution.
- Eclipse magnitude analysis.
- Gamma, duration, and magnitude comparisons.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Interactive web application |
| Pandas | Data loading, cleaning, and manipulation |
| NumPy | Numerical calculations and statistics |
| Plotly Express | Interactive charts |
| CSV | Data storage format |

## 5. Project Folder Structure

```text
python term project/
│
├── app.py
├── utils.py
├── csv_manager.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── exoplanet_discoveries.csv
│   ├── exoTrain.csv
│   ├── exoTest.csv
│   ├── meteorite_landings.csv
│   ├── solar_eclipses.csv
│   └── lunar_eclipses.csv
│
├── pages/
│   ├── page1.py
│   ├── page2.py
│   ├── page3.py
│   └── page4.py
│
└── venv/
```

*Note: The filenames inside `pages/` should match the filenames used in your actual project. The `venv/` directory is created locally and generally should not be included in the submitted ZIP or GitHub repository.*

## 6. Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip package manager
- Visual Studio Code or another Python editor

### Step 1: Open the project folder

Open the project folder in Visual Studio Code and open its terminal.

### Step 2: Activate the virtual environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If the virtual environment has not been created, run:

```powershell
python -m venv venv
```

Then activate it using the command above.

### Step 3: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Run the application

```powershell
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open that address in your browser to use the application.

## 7. Data Management

The application uses CSV files to store records.

The shared `CSVManager` class provides the main data management operations:

- **Create:** Add new records.
- **Read:** Load and display existing records.
- **Update:** Modify selected records.
- **Delete:** Remove selected records.

The shared utility functions provide common page styling, form inputs, search, filtering, sorting, chart display, and CSV export.

## 8. Data Analysis and Visualization

Each module provides summary statistics and visualizations relevant to its dataset.

Examples include:

- Pie charts for category distributions.
- Bar charts for comparing counts.
- Histograms for examining numerical distributions.
- Scatter plots for exploring relationships between variables.
- Line charts for examining flux signal patterns.

The charts help users identify patterns and understand the datasets more easily.

## 9. Error Handling

The project includes basic error handling to improve reliability.

Examples include:

- Detecting missing CSV files.
- Handling empty CSV files.
- Checking for required columns.
- Preventing duplicate record identifiers.
- Displaying user-friendly messages when CRUD operations fail.
- Using temporary files when writing updated CSV data.

## 10. Team Contributions.

The project is divided into four modules so each team member can develop and explain one part of the application.

| Team Member | Responsibility |
|---|---|
| Student 1 | Exoplanet Discoveries |
| Student 2 | Exoplanet Characteristics |
| Student 3 | Meteorite Landings |
| Student 4 | Solar and Lunar Eclipses |

Replace the placeholders with the actual team members' names before submission.

## 11. How to Use the Application

1. Run the application using Streamlit.
2. Select a module from the sidebar.
3. View the dataset records.
4. Search for specific records or filter and sort the data.
5. Add, update, or delete records using the available forms.
6. Explore the summary statistics and interactive charts.
7. Download the filtered dataset as a CSV file.

## 12. Learning Outcomes

Through this project, we gain practical experience in:

- Python programming and object-oriented programming.
- CSV file handling and data management.
- Pandas and NumPy operations.
- CRUD application development.
- Interactive visualization using Plotly.
- Building multi-page applications using Streamlit.
- Error handling and collaborative software development.

## 13. Conclusion

Exoplanet Analytics demonstrates how Python can be used to build an interactive data analytics application for astronomical datasets. By combining CSV-based data management, CRUD operations, statistical analysis, and interactive visualizations, the project provides a practical way to explore exoplanets, meteorites, and eclipse events.

## 14. Future Enhancements

- Add more astronomical datasets.
- Improve data validation and missing-value handling.
- Generate downloadable summary reports.
- Add additional statistical analysis and visualizations.
- Improve the user interface and data exploration features.

---

**Course:** 22AIE205 – Introduction to Python  
**Semester:** 3  
**Project:** Exoplanet Analytics
