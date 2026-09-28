
# CS490 Capstone - MiceLab

MiceLab is a Python application for importing mouse movement CSV data and calculating kinematic measurements. The application uses a PySide6 graphical user interface, Pandas for CSV/data handling, and NumPy for numerical calculations.

## 1. Recommended Folder Layout

Your project folder should look like this:

```text
Capstone-CS490/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── mumu7091_dorSwim1.1_2025Aug14.csv
│   └── mumu7091_latSwim1.1_2025Aug14.csv
└── .venv/
```

### Where do the CSV files go?

Create a folder named:

```text
data
```

inside `Capstone-CS490`.

Then put these two CSV files inside it:

```text
mumu7091_dorSwim1.1_2025Aug14.csv
mumu7091_latSwim1.1_2025Aug14.csv
```

You do **not** need to edit the CSV files.

The application uses the **Import CSV** button to select the files. They do not have to be in a specific folder for the application to work, but keeping project data inside `data/` makes the repository easier for your team to organize.

## 2. What These Two CSV Files Contain

The two files are from the same mouse/trial but contain different camera views/body-point sets.

### Dorsal CSV

```text
mumu7091_dorSwim1.1_2025Aug14.csv
```

This file contains 412 frames and 46 columns. Its tracked body parts include:

- SnoutTip
- TopEye
- BottomEye
- AntBodyMid
- BodyMid
- PostBodyMid
- TailBase
- ProxTail1
- ProxTail2
- ProxTail3
- MidTail
- DistTail1
- DistTail2
- DistTail3
- TailTip

### Lateral CSV

```text
mumu7091_latSwim1.1_2025Aug14.csv
```

This file contains 412 frames and 40 columns. Its tracked body parts include:

- Eye
- SnoutTip
- TailBase
- ProxTail1
- ProxTail2
- ProxTail3
- MidTail
- DistTail1
- DistTail2
- DistTail3
- TailTip
- Ankle
- MTP

Both files use a three-level CSV header:

```text
scorer / bodyparts / coords
```

and contain:

```text
x
y
likelihood
```

for the tracked body parts.

The first column contains frame numbers from 0 through 411.

## 3. Important: How to Import These Files

### Step 1: Start the application

Open Terminal:

```bash
cd ~/Downloads/Capstone-CS490
```

Activate your virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
python main.py
```

### Step 2: Click "Import CSV"

The application opens a file picker.

Navigate to:

```text
Capstone-CS490/data/
```

Select both:

```text
mumu7091_dorSwim1.1_2025Aug14.csv
mumu7091_latSwim1.1_2025Aug14.csv
```

On macOS, you can hold **Command (⌘)** while clicking the second file to select both files.

Then click **Open**.

### Step 3: Confirm the import

The current code prints a message in Terminal:

```text
Loaded 2 CSV file(s).
```

It also prints:

```text
Standardized variables:
```

followed by the variable names.

Keep Terminal open while using the application because the current version reports most processing results there rather than displaying them inside the GUI.

## 4. IMPORTANT CURRENT CODE LIMITATION

Your current `import_csv()` function loads every selected CSV into:

```python
self.data
```

However, it currently extracts variables only from:

```python
self.data[0]
```

That means the **first CSV you select matters**.

For these two files, the safest current order is:

1. `mumu7091_dorSwim1.1_2025Aug14.csv`
2. `mumu7091_latSwim1.1_2025Aug14.csv`

The reason is that the current code extracts:

```text
TailTip
TailBase
SnoutTip
MTP
Ankle
```

The dorsal file has `TailTip`, `TailBase`, and `SnoutTip`, but does not contain `MTP` or `Ankle`.

The lateral file contains all of those required points, including `MTP` and `Ankle`.

Therefore, if your kinematics calculations need MTP and Ankle, the current implementation needs to be changed so that it combines information from the appropriate dorsal and lateral files instead of assuming everything is in `self.data[0]`.

**Do not change the CSV files to solve this. The CSV structure is usable. The code's data-selection logic is what needs to be connected correctly.**

## 5. What the Current Import Code Does

When you click **Import CSV**, the code:

1. Opens the file picker.
2. Allows multiple CSV files to be selected.
3. Stores their paths in `self.file_paths`.
4. Reads each CSV using Pandas.
5. Uses the three-row header:
   ```python
   header=[0, 1, 2]
   ```
6. Stores each DataFrame in:
   ```python
   self.data
   ```
7. Extracts standardized variables from the first DataFrame.
8. Prints the imported variables to Terminal.

The relevant code is:

```python
dataset = pd.read_csv(
    file_path,
    header=[0, 1, 2]
)
```

## 6. Parameters to Enter

The GUI currently has these fields:

| Field | Purpose |
|---|---|
| FPS | Frames per second |
| Latcal (m/pix) | Lateral calibration |
| Dorscal (m/pix) | Dorsal calibration |
| Poly 1 | Calibration polynomial parameter |
| Poly 2 | Calibration polynomial parameter |
| Poly 3 | Calibration polynomial parameter |
| TD | Tail diameter |

Enter the values provided by your project/research team.

**Do not invent values for these fields.** The CSV files provide tracked coordinates, but they do not by themselves establish the correct FPS, calibration values, polynomial coefficients, or tail diameter.

After entering them, click:

```text
Register Parameters
```

The values will be printed in Terminal.

## 7. Current Kinematics Workflow

The intended workflow is:

```text
CSV files
   ↓
Import CSV
   ↓
Extract tracked body points
   ↓
Preprocess/calibrate coordinates
   ↓
Detect peaks/troughs/cycles
   ↓
Calculate kinematic measurements
   ↓
Display/save results
```

Your current code has many of the individual calculation functions already written, but several are still marked TODO and are not yet connected to the imported CSV data.

For example, the code currently has functions for:

- Time
- Tail frequency
- Tail wavelength
- Tail wave speed
- Swimming velocity
- Tail-tip amplitude
- Tail-base amplitude
- Tail lateral velocity
- Relative tail velocity
- Virtual mass
- Tail thrust power
- MTP frequency
- MTP amplitude
- MTP wavelength
- Stroke length
- Power-phase duration
- Recovery-phase duration
- Phase ratio
- Hindfoot length
- Hindfoot angle
- Hindfoot angular velocity

## 8. Current "Calculate Kinematics" Button

The button exists in the GUI, but the complete workflow is **not finished yet**.

The current function contains test calculations such as:

```python
test_time = self.calculate_time(250, 250)
```

and:

```python
test_mass = self.calculate_virtual_mass(0.00225)
```

The code also contains TODO sections for connecting the imported data to the calculations.

Therefore, after importing the CSVs, do not expect the application to automatically produce the final research measurements yet.

## 9. Important Coding Issue Before Using "Calculate Kinematics"

The current button is connected with:

```python
self.calculate_button.clicked.connect(self.calculate_kinematics)
```

but the function is defined as:

```python
def calculate_kinematics(self, variables):
```

The button click does not provide `variables`, so clicking **Calculate Kinematics** in the current version can produce a missing-argument error.

This needs to be changed when the team connects the calculation workflow.

For example, the eventual design could use:

```python
def calculate_kinematics(self):
    variables = self.extract_variables(...)
    ...
```

or another team-approved data pipeline.

Do not simply remove the `variables` parameter without deciding where the dorsal and lateral data should come from.

## 10. First Test: Import Only

Until the calculation pipeline is connected, use this test:

```text
1. Start main.py
2. Click Import CSV
3. Select both CSV files
4. Click Open
5. Look at Terminal
6. Confirm:
   Loaded 2 CSV file(s).
```

You should also see:

```text
Standardized variables:
```

with keys such as:

```text
frame
tail_tip_x
tail_tip_y
tail_base_x
tail_base_y
snout_x
snout_y
mtp_x
mtp_y
ankle_x
ankle_y
```

Because the current code extracts from the first selected file, the MTP and Ankle values may be `None` when the dorsal CSV is first. This is expected from the current implementation and is one reason the two-view data pipeline still needs to be connected.

## 11. Recommended Next Code Change

For these specific CSVs, the next development task should be:

```text
Dorsal CSV
    ↓
Snout / body / tail coordinates
    ↓
Dorsal calibration
    ↓
Dorsal kinematics

Lateral CSV
    ↓
Snout / tail / MTP / Ankle coordinates
    ↓
Lateral calibration
    ↓
Hindfoot/MTP kinematics

          ↓
    Combine results
          ↓
    Final metrics
```

The two files should be treated as **separate datasets from the two camera views**, not as two interchangeable copies of the same data.

## 12. Git

Do not commit the virtual environment:

```text
.venv/
```

Your `.gitignore` should contain:

```text
.venv/
__pycache__/
*.pyc
.DS_Store
```

A recommended repository is:

```text
Capstone-CS490/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
└── data/
    ├── mumu7091_dorSwim1.1_2025Aug14.csv
    └── mumu7091_latSwim1.1_2025Aug14.csv
```

Whether the actual CSV data should be committed to Git depends on your team's project/data-sharing rules. If the data should not be distributed, keep `data/` out of Git and have teammates obtain the CSVs separately.

## 13. Quick Start for Your Current Computer

If your project is in Downloads:

```bash
cd ~/Downloads/Capstone-CS490
```

Create the environment once:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
python main.py
```

Then:

```text
Import CSV
    ↓
Navigate to data/
    ↓
Select:
  mumu7091_dorSwim1.1_2025Aug14.csv
  mumu7091_latSwim1.1_2025Aug14.csv
    ↓
Open
    ↓
Check Terminal for "Loaded 2 CSV file(s)."
```

## 14. Troubleshooting

### `ModuleNotFoundError: No module named 'PySide6'`

Make sure the virtual environment is activated:

```bash
source .venv/bin/activate
```

Then:

```bash
python -m pip install -r requirements.txt
```

Verify:

```bash
python -c "import PySide6; print(PySide6.__version__)"
```

### `ModuleNotFoundError: No module named 'pandas'`

Run:

```bash
python -m pip install -r requirements.txt
```

### `ModuleNotFoundError: No module named 'numpy'`

Run:

```bash
python -m pip install -r requirements.txt
```

### Check which Python is being used

Run:

```bash
which python
python --version
python -m pip --version
```

When the virtual environment is active, `which python` should point inside:

```text
Capstone-CS490/.venv/
```

### Do not use this

Do not run:

```bash
python3 install
```

`install` is not the Python dependency installer.

Use:

```bash
python -m pip install -r requirements.txt
```

## 15. Updating Dependencies

If a new Python package is added:

```bash
python -m pip install package-name
```

Then update the dependency file:

```bash
python -m pip freeze > requirements.txt
```

Review the resulting file before committing it.

