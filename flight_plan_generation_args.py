# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 10:13:59 2024

@author: sunga
"""
import math
import pandas as pd
import argparse
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom 
import io
import utm

# Define the wpml namespace

kml_ns = "http://www.opengis.net/kml/2.2"
wpml_ns = "http://www.dji.com/wpmz/1.0.2"
    
    # Register namespaces
ET.register_namespace("", kml_ns)  # Default KML namespace
ET.register_namespace("wpml", wpml_ns)  # DJI wpml namespace
    
    # Create the root KML element with namespaces
placemark = ET.Element(f"{{{kml_ns}}}kml")

# Create the Document element
document = ET.SubElement(placemark, "Document")

def create_wpml_element(parent, tag, text=None):
    elem = ET.SubElement(parent, tag)
    if text is not None:
        elem.text = str(text)
    return elem

def create_action_groups_text(placemark, num_groups, start_point):
    # Create the first action group with full details
    row = start_point
    placemark = create_wpml_element(placemark, 'Placemark')
    point = create_wpml_element(placemark, "Point")
    create_wpml_element(point, "coordinates", f"{row['Longitude']},{row['Latitude']}")
    
    # Create waypoint elements
    create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}index", row['PointID'])
    create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}executeHeight", row['executeHeight'])
    create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}waypointSpeed", row['waypointSpeed'])

    # Waypoint heading params
    wp_heading_param = create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingParam")
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingMode", row['waypointHeadingMode'])
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingAngle", row['waypointHeadingAngle'])
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointPoiPoint", row['waypointPoiPoint'])
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingAngleEnable", "1")
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingPathMode", row['waypointHeadingPathMode'])
    
    # Waypoint turn params
    wp_turn_param = create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}waypointTurnParam")
    create_wpml_element(wp_turn_param, "{http://www.dji.com/wpmz/1.0.2}waypointTurnMode", row['waypointTurnMode'])
    create_wpml_element(wp_turn_param, "{http://www.dji.com/wpmz/1.0.2}waypointTurnDampingDist", row['waypointTurnDampingDist'])
    create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}useStraightLine", row['useStraightLine'])
    
    action_group_1 = ET.SubElement(placemark, "{http://www.dji.com/wpmz/1.0.2}actionGroup")
    group_id_1 = ET.SubElement(action_group_1, "{http://www.dji.com/wpmz/1.0.2}actionGroupId")
    group_id_1.text = "1"

    start_index_1 = ET.SubElement(action_group_1, "{http://www.dji.com/wpmz/1.0.2}actionGroupStartIndex")
    start_index_1.text = "0"

    end_index_1 = ET.SubElement(action_group_1, "{http://www.dji.com/wpmz/1.0.2}actionGroupEndIndex")
    end_index_1.text = "0"

    group_mode_1 = ET.SubElement(action_group_1, "{http://www.dji.com/wpmz/1.0.2}actionGroupMode")
    group_mode_1.text = "parallel"

    action_trigger_1 = ET.SubElement(action_group_1, "{http://www.dji.com/wpmz/1.0.2}actionTrigger")
    trigger_type_1 = ET.SubElement(action_trigger_1, "{http://www.dji.com/wpmz/1.0.2}actionTriggerType")
    trigger_type_1.text = "reachPoint"

    # First action in action group 1
    action_1 = ET.SubElement(action_group_1, "{http://www.dji.com/wpmz/1.0.2}action")
    action_id_1 = ET.SubElement(action_1, "{http://www.dji.com/wpmz/1.0.2}actionId")
    action_id_1.text = "1"

    action_func_1 = ET.SubElement(action_1, "{http://www.dji.com/wpmz/1.0.2}actionActuatorFunc")
    action_func_1.text = "gimbalRotate"

    actuator_func_param_1 = ET.SubElement(action_1, "{http://www.dji.com/wpmz/1.0.2}actionActuatorFuncParam")

    gimbal_yaw_base_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalHeadingYawBase")
    gimbal_yaw_base_1.text = "aircraft"

    rotate_mode_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalRotateMode")
    rotate_mode_1.text = "absoluteAngle"

    gimbal_pitch_enable_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalPitchRotateEnable")
    gimbal_pitch_enable_1.text = "1"

    gimbal_pitch_angle_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalPitchRotateAngle")
    gimbal_pitch_angle_1.text = "-45"

    gimbal_roll_enable_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalRollRotateEnable")
    gimbal_roll_enable_1.text = "0"

    gimbal_roll_angle_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalRollRotateAngle")
    gimbal_roll_angle_1.text = "0"

    gimbal_yaw_enable_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalYawRotateEnable")
    gimbal_yaw_enable_1.text = "0"

    gimbal_yaw_angle_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalYawRotateAngle")
    gimbal_yaw_angle_1.text = "0"

    gimbal_rotate_time_enable_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalRotateTimeEnable")
    gimbal_rotate_time_enable_1.text = "0"

    gimbal_rotate_time_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}gimbalRotateTime")
    gimbal_rotate_time_1.text = "0"

    payload_position_index_1 = ET.SubElement(actuator_func_param_1, "{http://www.dji.com/wpmz/1.0.2}payloadPositionIndex")
    payload_position_index_1.text = "0"
    
    # Create additional action groups with reduced information

    action_group = ET.SubElement(placemark, "{http://www.dji.com/wpmz/1.0.2}actionGroup")

    group_id_2 = ET.SubElement(action_group, "{http://www.dji.com/wpmz/1.0.2}actionGroupId")
    group_id_2.text = "2"

    start_index = ET.SubElement(action_group, "{http://www.dji.com/wpmz/1.0.2}actionGroupStartIndex")
    start_index.text = "0"

    end_index = ET.SubElement(action_group, "{http://www.dji.com/wpmz/1.0.2}actionGroupEndIndex")
    end_index.text = "1"

    group_mode = ET.SubElement(action_group, "{http://www.dji.com/wpmz/1.0.2}actionGroupMode")
    group_mode.text = "parallel"

    action_trigger = ET.SubElement(action_group, "{http://www.dji.com/wpmz/1.0.2}actionTrigger")
    trigger_type = ET.SubElement(action_trigger, "{http://www.dji.com/wpmz/1.0.2}actionTriggerType")
    trigger_type.text = "reachPoint"

            # Action for the current group
    action = ET.SubElement(action_group, "{http://www.dji.com/wpmz/1.0.2}action")
    action_id = ET.SubElement(action, "{http://www.dji.com/wpmz/1.0.2}actionId")
    action_id.text = "2"

    action_func = ET.SubElement(action, "{http://www.dji.com/wpmz/1.0.2}actionActuatorFunc")
    action_func.text = "gimbalEvenlyRotate"

    actuator_func_param = ET.SubElement(action, "{http://www.dji.com/wpmz/1.0.2}actionActuatorFuncParam")
    gimbal_pitch_angle = ET.SubElement(actuator_func_param, "{http://www.dji.com/wpmz/1.0.2}gimbalPitchRotateAngle")
    gimbal_pitch_angle.text = "-45"

    payload_position_index = ET.SubElement(actuator_func_param, "{http://www.dji.com/wpmz/1.0.2}payloadPositionIndex")
    payload_position_index.text = "0"
            

def create_action_group(placemark, group_id, point_id, action_id, func, pitch_angle=None):
    action_group = create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}actionGroup")
    
    create_wpml_element(action_group, "{http://www.dji.com/wpmz/1.0.2}actionGroupId", group_id)
    create_wpml_element(action_group, "{http://www.dji.com/wpmz/1.0.2}actionGroupStartIndex", point_id)
    create_wpml_element(action_group, "{http://www.dji.com/wpmz/1.0.2}actionGroupEndIndex", point_id)
    create_wpml_element(action_group, "{http://www.dji.com/wpmz/1.0.2}actionGroupMode", "parallel")
    
    # Action trigger
    action_trigger = create_wpml_element(action_group, "{http://www.dji.com/wpmz/1.0.2}actionTrigger")
    create_wpml_element(action_trigger, "{http://www.dji.com/wpmz/1.0.2}actionTriggerType", "reachPoint")
    
    # Action
    action = create_wpml_element(action_group, "{http://www.dji.com/wpmz/1.0.2}action")
    create_wpml_element(action, "{http://www.dji.com/wpmz/1.0.2}actionId", action_id)
    create_wpml_element(action, "{http://www.dji.com/wpmz/1.0.2}actionActuatorFunc", func)
    
    # Action actuator function parameters
    actuator_func_param = create_wpml_element(action, "{http://www.dji.com/wpmz/1.0.2}actionActuatorFuncParam")
    
    if pitch_angle:
        create_wpml_element(actuator_func_param, "{http://www.dji.com/wpmz/1.0.2}gimbalPitchRotateAngle", pitch_angle)
    
    create_wpml_element(actuator_func_param, "{http://www.dji.com/wpmz/1.0.2}payloadPositionIndex", "0")
    
def create_document_generation(placemark):
    mission_config = ET.SubElement(document, f"{{{wpml_ns}}}missionConfig")
    ET.SubElement(mission_config, f"{{{wpml_ns}}}flyToWaylineMode").text = "safely"
    ET.SubElement(mission_config, f"{{{wpml_ns}}}finishAction").text = "noAction"
    ET.SubElement(mission_config, f"{{{wpml_ns}}}exitOnRCLost").text = "executeLostAction"
    ET.SubElement(mission_config, f"{{{wpml_ns}}}executeRCLostAction").text = "hover"
    ET.SubElement(mission_config, f"{{{wpml_ns}}}globalTransitionalSpeed").text = "2.5"

    # Add droneInfo inside missionConfig
    drone_info = ET.SubElement(mission_config, f"{{{wpml_ns}}}droneInfo")
    ET.SubElement(drone_info, f"{{{wpml_ns}}}droneEnumValue").text = "68"
    ET.SubElement(drone_info, f"{{{wpml_ns}}}droneSubEnumValue").text = "0"
    
    # Add Folder element inside Document
    folder = ET.SubElement(document, "Folder")
    ET.SubElement(folder, f"{{{wpml_ns}}}templateId").text = "0"
    ET.SubElement(folder, f"{{{wpml_ns}}}executeHeightMode").text = "relativeToStartPoint"
    ET.SubElement(folder, f"{{{wpml_ns}}}waylineId").text = "0"
    ET.SubElement(folder, f"{{{wpml_ns}}}distance").text = "0"
    ET.SubElement(folder, f"{{{wpml_ns}}}duration").text = "0"
    ET.SubElement(folder, f"{{{wpml_ns}}}autoFlightSpeed").text = "2.5"
    return folder

def create_point_text(placemark, df_row, actions=None):
    row = df_row
    print(row)
    # Create the Point element
    placemark = create_wpml_element(placemark, 'Placemark')
    point = create_wpml_element(placemark, "Point")
    create_wpml_element(point, "coordinates", f"{row['Longitude']},{row['Latitude']}")
    
    # Create waypoint elements
    create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}index", row['PointID'])
    create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}executeHeight", row['executeHeight'])
    create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}waypointSpeed", row['waypointSpeed'])

    # Waypoint heading params
    wp_heading_param = create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingParam")
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingMode", row['waypointHeadingMode'])
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingAngle", row['waypointHeadingAngle'])
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointPoiPoint", row['waypointPoiPoint'])
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingAngleEnable", "1")
    create_wpml_element(wp_heading_param, "{http://www.dji.com/wpmz/1.0.2}waypointHeadingPathMode", row['waypointHeadingPathMode'])
    
    # Waypoint turn params
    wp_turn_param = create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}waypointTurnParam")
    create_wpml_element(wp_turn_param, "{http://www.dji.com/wpmz/1.0.2}waypointTurnMode", row['waypointTurnMode'])
    create_wpml_element(wp_turn_param, "{http://www.dji.com/wpmz/1.0.2}waypointTurnDampingDist", row['waypointTurnDampingDist'])
    create_wpml_element(placemark, "{http://www.dji.com/wpmz/1.0.2}useStraightLine", row['useStraightLine'])
    
    # Handle actions based on the action type
    if row['action'] == 1:
        create_action_group(placemark, '1', row['PointID'], row['actionID']-1, "startRecord")
        create_action_group(placemark, "2", row['PointID'], row['actionID'], "gimbalEvenlyRotate", row['gimbalRotateAngel'])
    
    elif row['action'] == 2:
        print(1)
        create_action_group(placemark, '1', row['PointID'], row['actionID']-1, "stopRecord")
        create_action_group(placemark, "2", row['PointID'], row['actionID'], "gimbalEvenlyRotate", row['gimbalRotateAngel'])
    elif row['action'] == 0:
        create_action_group(placemark, "2", row['PointID'], row['actionID'], "gimbalEvenlyRotate", row['gimbalRotateAngel'])



def actionID_generation(action_input,num_groups):
    actionNum = num_groups
    actionID = [1]
    for i in action_input[1:]:
        if i == 0:  # Compare each element 'i', not the entire list
            actionNum += 1
        else:   
            actionNum += 2
        actionID.append(actionNum)
    return actionID

def generate_circle_points(center, radius, num_points=10):
    circle_points = []
    
    # Convert center from lat/lon to UTM
    utm_center_x, utm_center_y, zone_number, zone_letter = utm.from_latlon(center[0], center[1])
    
    # Calculate points around the circle in UTM
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        delta_utmx = radius * math.cos(angle)
        delta_utmy = radius * math.sin(angle)
        
        # Compute new UTM coordinates
        new_utm_x = utm_center_x + delta_utmx
        new_utm_y = utm_center_y + delta_utmy
        
        # Convert back from UTM to lat/lon
        new_lat, new_lon = utm.to_latlon(new_utm_x, new_utm_y, zone_number, zone_letter)
        circle_points.append((new_lat, new_lon))
    
    return circle_points

def action_generation(group_numbers, num_points_per_circle):
    actions = [0]  # Start point action is 0 (no action)
    unique_groups = sorted(set(group_numbers) - {0})  # Ignore group 0 (start and end points)

    for group in unique_groups:
        group_indices = [i for i, g in enumerate(group_numbers) if g == group]
        # Set first point to 1 (startRecord), last point to 2 (stopRecord), others to 0
        for i, idx in enumerate(group_indices):
            if i == 0:
                actions.append(1)
            elif i == len(group_indices)-1:
                actions.append(2)
            else:
                actions.append(0)

    actions.append(0)  # End point action is 0 (no action)
    return actions

def actionActuatorFunc_generation(action_input): 
    if action_input == 1:
        return 'startRec'
    elif action_input == 2:
        return 'stopRec'
    elif action_input == 0:
        return 'gimbalEvenlyRotate'
def actionID_generation(action_input,num_groups = 2):
    actionNum = 2
    actionID = [0]
    for i in action_input[1:]:
        if i == 0:  # Compare each element 'i', not the entire list
            actionNum += 1
        else:  
            actionNum += 2
        actionID.append(actionNum)
    return actionID

def waypoint_heading_angle_generation(waypoints, center):
    """
    Calculate heading angles from each waypoint aiming toward the center point.
    
    Args:
        waypoints (list): List of waypoints [(lat, lon), ...].
        center (tuple): Center point (lat, lon).
        
    Returns:
        list: Heading angles in degrees ranging from -180 to 180, aiming toward the center.
    """
    heading_angles = []
    center_lat, center_lon = center
    for lat, lon in waypoints:
        # Calculate deltas (waypoint to center)
        delta_lat = center_lat - lat
        delta_lon = center_lon - lon
        # Calculate heading in radians and convert to degrees
        angle_rad = math.atan2(delta_lon, delta_lat)
        angle_deg = math.degrees(angle_rad)
        # Normalize to [-180, 180]
        if angle_deg > 180:
            angle_deg -= 360
        elif angle_deg < -180:
            angle_deg += 360
        heading_angles.append(angle_deg)
    return heading_angles

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate flight plan from CSV inputs.")
parser.add_argument('--csv', type=str, required=True, help='Path to the parameters CSV file')
parser.add_argument('--output', type=str, required=True, help='Path to the output WPML file')

args = parser.parse_args()
csv_path = args.csv

output_path = args.output

with open(csv_path, "r") as f:
    lines = f.readlines()

split_index = lines.index('\n')  # Find blank line separating sections

# Parse parameters
param_lines = lines[:split_index]
param_df = pd.read_csv(io.StringIO(''.join(param_lines)))
param_dict = dict(zip(param_df['parameter'], param_df['value']))

# Parse points
point_lines = lines[split_index + 1:]
df = pd.read_csv(io.StringIO(''.join(point_lines)))

# Extract points
start_point = tuple(df[df['type'] == 'start_point'][['latitude', 'longitude']].iloc[0])
end_point = tuple(df[df['type'] == 'end_point'][['latitude', 'longitude']].iloc[0])
center_points = [tuple(x) for x in df[df['type'] == 'center_point'][['latitude', 'longitude']].values]

# Extract parameters
radius = float(param_dict['radius'])
num_points_per_circle = int(radius)
executeHeight = float(param_dict['executeHeight'])
waypointSpeed = 2.5
gimbalRotateAngel = -int(90 - math.degrees(math.atan(radius / executeHeight)))

# === Your original script continues here ===

# Placeholder for actual flight plan logic (keep your logic below)
num_groups = len(center_points)
latitudes = [start_point[0]]
longitudes = [start_point[1]]
group_numbers = [0]  # Start point's group number is 0
waypoint_headings = [0]  # Initial heading
waypoint_heading_mode = ['smoothTransition']
poi_points = ['0.000000, 0.000000, 0.000000']
waypoint_heading_path_mode = ['followBadArc']
turn_mode = ['toPointAndPassWithContinuityCurvature']
turn_damping_dist = [0]
use_straight_line = [0]
actions = [0]  # Start point has no action

# Loop over each center point
for group_id, center in enumerate(center_points, start=1):
    print(center)
    print(group_id)
    # Generate circle points and heading angles for the current center
# Generate circle points for the current center
    circle_points = generate_circle_points(center, radius, num_points_per_circle)
    print(circle_points)
    # Calculate dynamic headings
    heading_angles = waypoint_heading_angle_generation(circle_points, center)
    # Append the generated points and angles to the lists
    latitudes.extend([pt[0] for pt in circle_points])
    longitudes.extend([pt[1] for pt in circle_points])
    group_numbers.extend([group_id] * num_points_per_circle)
    waypoint_headings.extend(heading_angles)
    waypoint_heading_mode.extend(['smoothTransition'] * num_points_per_circle)
    poi_points.extend(['0.000000, 0.000000, 0.000000'] * num_points_per_circle)
    waypoint_heading_path_mode.extend(['followBadArc'] * num_points_per_circle)
    turn_mode.extend(['toPointAndPassWithContinuityCurvature'] * num_points_per_circle)
    turn_damping_dist.extend([0] * num_points_per_circle)
    use_straight_line.extend([0] * num_points_per_circle)

# Add the end point data
latitudes.append(end_point[0])
longitudes.append(end_point[1])
group_numbers.append(0)  # End point's group number is 0
waypoint_headings.append(0)
waypoint_heading_mode.append('smoothTransition')
poi_points.append('0.000000, 0.000000, 0.000000')
waypoint_heading_path_mode.append('followBadArc')
turn_mode.append('toPointAndPassWithContinuityCurvature')
turn_damping_dist.append(0)
use_straight_line.append(0)
actions.append(0)  # End point has no action

# Generate the action column based on the group numbers
actions = action_generation(group_numbers, num_points_per_circle)

# Prepare the DataFrame
data_points = {
    'PointID': range(0, len(latitudes)),
    'Latitude': latitudes,
    'Longitude': longitudes,
    'groupNumber': group_numbers,
    'executeHeight': [executeHeight] * len(latitudes),
    'waypointSpeed': [waypointSpeed] * len(latitudes),
    'waypointHeadingMode': waypoint_heading_mode,
    'waypointHeadingAngle': waypoint_headings,
    'waypointPoiPoint': poi_points,
    'waypointHeadingPathMode': waypoint_heading_path_mode,
    'waypointTurnMode': turn_mode,
    'waypointTurnDampingDist': turn_damping_dist,
    'useStraightLine': use_straight_line,
    'action': actions,
    'actionID': actionID_generation(actions, num_groups),
    'gimbalRotateAngel': gimbalRotateAngel
}
# print(data_points)
df = pd.DataFrame(data_points)

folder = create_document_generation(document) 

create_action_groups_text(folder, 2, df.iloc[0,:])

for i in range(1, len(df)):
    create_point_text(folder, df.iloc[i,:], actions)
    

# Prettify the XML
def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    # Suppress the default declaration by retrieving only the document body
    xml_body = reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")
    xml_body = '\n'.join(xml_body.split('\n')[1:])  # Remove the first line (default declaration)
    # Add the correct XML declaration
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_body


pretty_xml = prettify_xml(placemark)
with open(output_path, "w", encoding="utf-8") as files:
    files.write(pretty_xml)
    


