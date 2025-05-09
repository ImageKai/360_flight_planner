
# Flight Plan Generator

This script generates a UAV flight plan using coordinates and flight parameters provided in CSV format.
- Model: DJI Mini 4 Pro, Marvic 3 Pro, Air 3, Any Waypoint Drone. 

## Requirements

- Python 3.8

## Installation

Install the required packages using pip:


pip install pandas utm argparse


## 📄 Input Files

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
| `X`  | longitude |
| `Y`  | latitude |
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

|X|Y|id|
|--------------------|----------------------|---|
|-82.2262211436591| 27.7611716629339| 1 |
|-82.226185015564| 27.7611200087153| 2 |
|-82.2261847169847| 27.7610683544967| 3 |
|-82.2261844184054| 27.7610143116436| 4 |
|-82.226142020145| 27.7611710657753| 999 |


### Run the script from the command line:

Example:

```bash
python flight_plan_generation_args.py \
    --points waypoints.csv \
    --parameters parameters.csv \  
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

