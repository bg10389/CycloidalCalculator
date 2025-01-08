import csv
import os
import tkinter as tk
from tkinter import ttk

def load_bearings(csv_filename):
    """
    Loads bearing data from the specified CSV file.
    Returns a list of dictionaries, each representing one bearing entry.
    """
    bearings_data = []
    if not os.path.isfile(csv_filename):
        return bearings_data

    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Convert ID, OD, and Thickness to floats or ints as appropriate
            # PartNumber stays as a string
            bearings_data.append({
                'PartNumber': row['PartNumber'],
                'ID': float(row['ID']),
                'OD': float(row['OD']),
                'Thickness': float(row['Thickness'])
            })
    return bearings_data

def find_bearing_by_ID(bearings_data, inner_diameter):
    """
    Searches the list of bearings for an entry with matching inner diameter.
    Returns the bearing dictionary if found, else None.
    """
    for bearing in bearings_data:
        if abs(bearing['ID'] - inner_diameter) < 1e-6:
            return bearing
    return None

def on_shaft_diameter_change(*args):
    """
    Event handler for when the shaft diameter changes.
    Looks up bearing data and auto-populates fields if found.
    """
    try:
        sd = float(entry_shaft_diameter.get())
    except ValueError:
        return

    found_bearing = find_bearing_by_ID(bearings_list, sd)
    if found_bearing:
        bearing_thickness_var.set(str(found_bearing['Thickness']))
        bearing_od_var.set(str(found_bearing['OD']))
        part_number_shaft_var.set(found_bearing['PartNumber'])
        # The cycloidal disc ID is set to the bearing OD
        cycloidal_disc_id_var.set(str(found_bearing['OD']))

def on_roller_base_diameter_change(*args):
    """
    Event handler for the roller base diameter.
    Looks up bearing data and auto-populates fields if found.
    """
    try:
        rbd = float(entry_roller_base_diameter.get())
    except ValueError:
        return

    found_bearing = find_bearing_by_ID(bearings_list, rbd)
    if found_bearing:
        roller_base_bearing_thickness_var.set(str(found_bearing['Thickness']))
        roller_base_bearing_od_var.set(str(found_bearing['OD']))
        part_number_roller_base_var.set(found_bearing['PartNumber'])

def calculate_cycloidal_params():
    """
    Main calculation routine.
    Pulls all relevant inputs, computes derived parameters,
    and updates fields accordingly.
    """
    try:
        shaft_diam = float(entry_shaft_diameter.get())
        num_drive_rollers = int(entry_num_drive_rollers.get())
        drive_roller_diam = float(entry_drive_roller_diameter.get())
        drive_roller_base_thickness = float(entry_drive_roller_base_thickness.get())
        roller_base_diam = float(entry_roller_base_diameter.get())
        ring_pin_diam = float(entry_ring_pin_diameter.get())
        cycloidal_pin_diam = float(entry_cycloidal_pin_diameter.get())
        cycloidal_pin_height = float(entry_cycloidal_pin_height.get())
        tolerance_val = float(entry_tolerance.get())
        cycloidal_disc_id = float(cycloidal_disc_id_var.get())
        cycloidal_disc_thickness = float(entry_cycloidal_disc_thickness.get())
    except ValueError:
        return

    # Example: auto-calculate hole diameters
    # For drive rollers: hole_diameter = drive_roller_diam + a bit of clearance
    # Use tolerance_val if you want to reduce the hole by that margin or add clearance
    drive_roller_hole_diam = drive_roller_diam + 0.2 - tolerance_val
    # For cycloidal pins, similarly:
    cycloidal_pin_hole_diam = cycloidal_pin_diam + 0.2 - tolerance_val

    hole_drive_roller_var.set(f"{drive_roller_hole_diam:.3f}")
    hole_cycloidal_pin_var.set(f"{cycloidal_pin_hole_diam:.3f}")

    # Additional logic for eccentricity, gear ratio, etc., could be placed here
    # For demonstration, let's just do a placeholder eccentricity
    # A typical approach: eccentricity = (ring_pin_diam - cycloidal_pin_diam) / 2
    eccentricity_value = (ring_pin_diam - cycloidal_pin_diam) / 2.0
    eccentricity_var.set(f"{eccentricity_value:.3f}")

    # Possibly compute a gear ratio if the user enters the number of lobes
    # For demonstration, assume gear ratio = (number of ring pins) / (number of lobes)
    # or something similar. We’ll skip the specifics unless needed.

# ------------------- MAIN GUI -------------------
root = tk.Tk()
root.title("Cycloidal Drive Calculator")

# Load bearing data from CSV
csv_filename = "bearing.csv"
bearings_list = load_bearings(csv_filename)

# StringVar variables for real-time updates
shaft_diameter_var = tk.StringVar()
shaft_diameter_var.trace_add("write", on_shaft_diameter_change)

roller_base_diameter_var = tk.StringVar()
roller_base_diameter_var.trace_add("write", on_roller_base_diameter_change)

bearing_thickness_var = tk.StringVar()
bearing_od_var = tk.StringVar()
part_number_shaft_var = tk.StringVar()

roller_base_bearing_thickness_var = tk.StringVar()
roller_base_bearing_od_var = tk.StringVar()
part_number_roller_base_var = tk.StringVar()

cycloidal_disc_id_var = tk.StringVar()

hole_drive_roller_var = tk.StringVar()
hole_cycloidal_pin_var = tk.StringVar()
eccentricity_var = tk.StringVar()

# ------------- ROW 0: Shaft Diameter -------------
label_shaft_diameter = tk.Label(root, text="Shaft Diameter (mm)")
label_shaft_diameter.grid(row=0, column=0, sticky="e")
entry_shaft_diameter = tk.Entry(root, textvariable=shaft_diameter_var)
entry_shaft_diameter.grid(row=0, column=1, padx=5, pady=5)

label_shaft_part = tk.Label(root, text="Shaft Bearing Part #")
label_shaft_part.grid(row=0, column=2, sticky="e")
label_shaft_partnumber = tk.Label(root, textvariable=part_number_shaft_var, fg="blue")
label_shaft_partnumber.grid(row=0, column=3, padx=5, pady=5)

# ------------- ROW 1: Bearing Dimensions (Shaft) -------------
label_bearing_thickness = tk.Label(root, text="Shaft Bearing Thickness (mm)")
label_bearing_thickness.grid(row=1, column=0, sticky="e")
entry_bearing_thickness = tk.Label(root, textvariable=bearing_thickness_var, bg="lightgray")
entry_bearing_thickness.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

label_bearing_od = tk.Label(root, text="Shaft Bearing OD (mm)")
label_bearing_od.grid(row=1, column=2, sticky="e")
entry_bearing_od = tk.Label(root, textvariable=bearing_od_var, bg="lightgray")
entry_bearing_od.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

# ------------- ROW 2: Number of Drive Rollers -------------
label_num_drive_rollers = tk.Label(root, text="Number of Drive Rollers")
label_num_drive_rollers.grid(row=2, column=0, sticky="e")
entry_num_drive_rollers = tk.Entry(root)
entry_num_drive_rollers.grid(row=2, column=1, padx=5, pady=5)

# ------------- ROW 3: Drive Roller Diameter -------------
label_drive_roller_diameter = tk.Label(root, text="Drive Roller Diameter (mm)")
label_drive_roller_diameter.grid(row=3, column=0, sticky="e")
entry_drive_roller_diameter = tk.Entry(root)
entry_drive_roller_diameter.grid(row=3, column=1, padx=5, pady=5)

label_drive_roller_base_thickness = tk.Label(root, text="Drive Roller Base Thickness (mm)")
label_drive_roller_base_thickness.grid(row=3, column=2, sticky="e")
entry_drive_roller_base_thickness = tk.Entry(root)
entry_drive_roller_base_thickness.grid(row=3, column=3, padx=5, pady=5)

# ------------- ROW 4: Roller Base Diameter -------------
label_roller_base_diameter = tk.Label(root, text="Roller Base Diameter (mm)")
label_roller_base_diameter.grid(row=4, column=0, sticky="e")
entry_roller_base_diameter = tk.Entry(root, textvariable=roller_base_diameter_var)
entry_roller_base_diameter.grid(row=4, column=1, padx=5, pady=5)

label_roller_base_part = tk.Label(root, text="Roller Base Bearing Part #")
label_roller_base_part.grid(row=4, column=2, sticky="e")
label_roller_base_partnumber = tk.Label(root, textvariable=part_number_roller_base_var, fg="blue")
label_roller_base_partnumber.grid(row=4, column=3, padx=5, pady=5)

# ------------- ROW 5: Roller Base Bearing Dimensions -------------
label_roller_base_bearing_thickness = tk.Label(root, text="Roller Base Bearing Thickness (mm)")
label_roller_base_bearing_thickness.grid(row=5, column=0, sticky="e")
entry_roller_base_bearing_thickness = tk.Label(root, textvariable=roller_base_bearing_thickness_var, bg="lightgray")
entry_roller_base_bearing_thickness.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

label_roller_base_bearing_od = tk.Label(root, text="Roller Base Bearing OD (mm)")
label_roller_base_bearing_od.grid(row=5, column=2, sticky="e")
entry_roller_base_bearing_od = tk.Label(root, textvariable=roller_base_bearing_od_var, bg="lightgray")
entry_roller_base_bearing_od.grid(row=5, column=3, padx=5, pady=5, sticky="ew")

# ------------- ROW 6: Pin Diameters -------------
label_ring_pin_diameter = tk.Label(root, text="Ring Pin Diameter (mm)")
label_ring_pin_diameter.grid(row=6, column=0, sticky="e")
entry_ring_pin_diameter = tk.Entry(root)
entry_ring_pin_diameter.grid(row=6, column=1, padx=5, pady=5)

label_cycloidal_pin_diameter = tk.Label(root, text="Cycloidal Pin Diameter (mm)")
label_cycloidal_pin_diameter.grid(row=6, column=2, sticky="e")
entry_cycloidal_pin_diameter = tk.Entry(root)
entry_cycloidal_pin_diameter.grid(row=6, column=3, padx=5, pady=5)

# ------------- ROW 7: Cycloidal Pin Height & Tolerance -------------
label_cycloidal_pin_height = tk.Label(root, text="Cycloidal Pin Height (mm)")
label_cycloidal_pin_height.grid(row=7, column=0, sticky="e")
entry_cycloidal_pin_height = tk.Entry(root)
entry_cycloidal_pin_height.grid(row=7, column=1, padx=5, pady=5)

label_tolerance = tk.Label(root, text="Tolerance (mm)")
label_tolerance.grid(row=7, column=2, sticky="e")
entry_tolerance = tk.Entry(root)
entry_tolerance.grid(row=7, column=3, padx=5, pady=5)

# ------------- ROW 8: Cycloidal Disc Parameters -------------
label_cycloidal_disc_id = tk.Label(root, text="Cycloidal Disc ID (mm)")
label_cycloidal_disc_id.grid(row=8, column=0, sticky="e")
entry_cycloidal_disc_id = tk.Label(root, textvariable=cycloidal_disc_id_var, bg="lightgray")
entry_cycloidal_disc_id.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

label_cycloidal_disc_thickness = tk.Label(root, text="Cycloidal Disc Thickness (mm)")
label_cycloidal_disc_thickness.grid(row=8, column=2, sticky="e")
entry_cycloidal_disc_thickness = tk.Entry(root)
entry_cycloidal_disc_thickness.grid(row=8, column=3, padx=5, pady=5)

# ------------- ROW 9: Calculated Hole Diameters (Results) -------------
label_hole_drive_roller = tk.Label(root, text="Hole Diameter for Drive Rollers (mm)")
label_hole_drive_roller.grid(row=9, column=0, sticky="e")
entry_hole_drive_roller = tk.Label(root, textvariable=hole_drive_roller_var, bg="lightgray")
entry_hole_drive_roller.grid(row=9, column=1, padx=5, pady=5, sticky="ew")

label_hole_cycloidal_pin = tk.Label(root, text="Hole Diameter for Cycloidal Pins (mm)")
label_hole_cycloidal_pin.grid(row=9, column=2, sticky="e")
entry_hole_cycloidal_pin = tk.Label(root, textvariable=hole_cycloidal_pin_var, bg="lightgray")
entry_hole_cycloidal_pin.grid(row=9, column=3, padx=5, pady=5, sticky="ew")

# ------------- ROW 10: Eccentricity (Result) -------------
label_eccentricity = tk.Label(root, text="Eccentricity (mm)")
label_eccentricity.grid(row=10, column=0, sticky="e")
entry_eccentricity = tk.Label(root, textvariable=eccentricity_var, bg="lightgray")
entry_eccentricity.grid(row=10, column=1, padx=5, pady=5, sticky="ew")

# ------------- ROW 11: Calculate Button -------------
calculate_button = tk.Button(root, text="Calculate", command=calculate_cycloidal_params)
calculate_button.grid(row=11, column=0, columnspan=4, pady=10)

# Just some spacing adjustments
for i in range(12):
    root.grid_rowconfigure(i, pad=3)

root.mainloop()
