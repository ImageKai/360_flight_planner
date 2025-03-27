
# Flight Plan Generator

This script generates a UAV flight plan using coordinates and flight parameters provided in CSV format.

---

## 📄 Input Files

### 1. `flight_plan_points.csv`

This file contains the **geographic coordinates** for:
- Start point
- Center points (used for defining flight groups or paths)
- End point

#### Format:
| type         | latitude   | longitude    |
|--------------|------------|--------------|
| start_point  | 27.760089  | -82.226316   |
| center_point | 27.760034  | -82.226171   |
| ...          | ...        | ...          |
| end_point    | 27.760089  | -82.226316   |

- `type` can be `start_point`, `center_point`, or `end_point`.

---

### 2. `flight_plan_parameters.csv`

This file provides numeric parameters used to define the flight pattern.

#### Format:
| parameter           | value |  unit  |
|---------------------|-------|--------|
| radius              | 24    |  meter |
| num_points_per_circle | 20  | points |
| executeHeight       | 15    |  meter |
| waypointSpeed       | 4     |  m/s   |
|gimbalRotateAngel    | -32   | degree |
---

## 🚀 How to Run the Script

### Requirements:
- Python 3.x
- `pandas` library

You can install pandas via pip if needed:
```bash
pip install pandas
```

### Run the script from the command line:

Example:

```bash
python flight_plan_generation_csv_with_output.py \
    --points flight_plan_points.csv \
    --parameter flight_plan_parameters.csv \
    --output ./waylines.wpml
```

---

## ✍️ Notes

- The output path (`--output`) is currently a placeholder. You need to insert your flight path saving logic into the script.
- This setup is ideal for flexible reconfiguration of UAV flight parameters and targets via CSV files.

