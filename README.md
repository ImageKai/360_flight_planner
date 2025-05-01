
# Flight Plan Generator

This script generates a UAV flight plan using coordinates and flight parameters provided in CSV format.
- Model: DJI Mini 4 Pro, Marvic 3 Pro, Air 3, Any Waypoint Drone. 

## Requirements

- Python 3.8

## Installation

Install the required packages using pip:


pip install pandas utm argparse


## 📄 Input File

### 1. `flight_plan_points.csv`

This file contains the two section:

First section is to provides numeric parameters used to define the flight pattern

#### Format:
| parameter           | value |  unit  |
|---------------------|-------|--------|
| radius              | 24    |  meter |
| executeHeight       | 15    |  meter |

Second section is **geographic coordinates** for:
- Start point
- Center points (used for defining flight groups or paths)
- End point

#### Format:
| type         | latitude   | longitude    |
|--------------|------------|--------------|
| start_point  | 27.760089  | -82.226316   |
| center_point | 27.760034  | -82.226171   |
| ...          | ...        | ...          |
| center_point | 27.759242  | -82.226172   |
| end_point    | 27.760089  | -82.226316   |

- `type` can be `start_point`, `center_point`, or `end_point`.



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

