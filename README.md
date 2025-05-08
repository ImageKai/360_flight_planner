
# Flight Plan Generator

This script generates a UAV flight plan using coordinates and flight parameters provided in CSV format.
- Model: DJI Mini 4 Pro, Marvic 3 Pro, Air 3, Any Waypoint Drone. 

## Requirements

- Python 3.8

## Installation

Install the required packages using pip:


pip install pandas utm argparse


## 📄 Input File

### 1. points csv file

This file contains the two section:

First section is to provides numeric parameters used to define the flight pattern

#### Format:
| parameter           | value |  unit  |
|---------------------|-------|--------|
| radius              | 24    |  meter |
| executeHeight       | 15    |  meter |

## Points csv file

This CSV file defines key geographic points for UAV flight planning using Well-Known Text (WKT) format. The file includes the start point, center points for circular orbits, and an optional end point.


| Column | Description |
|--------|-------------|
| `WKT`  | Coordinates in WKT `POINT (longitude latitude)` format |
| `id`   | Unique identifier for each point. Special IDs are used to define flight roles (see below) |

## Point Roles

- **Start Point**:  
  - `id = 1`  
  - Specifies the UAV's starting location.

- **Center Points**:  
  - `id ≥ 2` and sequential  
  - Used to define circular orbit centers for the flight path.

- **End Point**:  
  - `id = 999`  
  - (Optional) Specifies the UAV's return or landing location. If not provided, it can default to the start point.

## Example

```csv
|WKT|id|
|------------------------------------------|---|
|POINT (-82.2263457448251 27.7600793304701)| 1 |
|POINT (-82.2262361416445 27.7599842473691)| 2 |
|POINT (-82.2262342680859 27.7599439658583)| 3 |
|POINT (-82.2262319261376 27.7598886958783)| 4 |
|POINT (-82.2262300525789 27.7598563769918)| 5 |
|POINT (-82.2261700987024 27.760087761484)|999|


### Run the script from the command line:

Example:

```bash
python flight_plan_generation_args.py \
    --csv flight_plan_points.csv \
    --output wpmz/waylines.wpml
```
## 📦 How to Upload to UAV

1. After generating the `.wpmz` flight plan file:
   - Zip the file using your operating system or a compression tool.
   - Change the file extension from `.zip` to `.kmz`.
   - rename

2. Upload the `.kmz` file to your UAV system.

link: https://www.waypointmap.com/Home/Tutorial

---

## ✍️ Notes

- The output path (`--output`) is currently a placeholder. You need to insert your flight path saving logic into the script.
- This setup is ideal for flexible reconfiguration of UAV flight parameters and targets via CSV files.

