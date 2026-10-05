# MiceLab

MiceLab is a desktop Python application for turning mouse swimming motion-tracking CSV files into cleaned coordinate data, diagnostic plots, and kinematic measurements. The interface is built with PySide6; Pandas and NumPy provide data handling and numerical calculations.

> **Development status:** the current branch contains a working GUI shell, multi-file CSV import, per-dataset variable selection, parameter capture, and a library of kinematic calculation functions. The full analysis workflow is not yet connected. Processing buttons, plots, exports, and final calculations are currently placeholders or test outputs.

## Intended workflow

The application is being developed to match the project manager's workflow:

```text
1. Import dorsal and lateral CSV data
2. Enter calibration specifications
3. Select a dataset and variable
4. Display raw data
5. Filter data and remove invalid points
6. Fill gaps with spline interpolation
7. Convert units and detrend the signal
8. Standardize and smooth the signal
9. Calculate kinematics and plot processed data
                         |
                         +--> Export cleaned variables as CSV
                         +--> Export a table of final kinematic values
```

The top-camera data supplies dorsal measurements such as tail-base movement. The side-camera data supplies lateral measurements, including the metatarsophalangeal joint (MTP/toe joint) and ankle used for hindlimb analysis. These views are complementary and must be processed with the appropriate calibration rather than treated as interchangeable files.

## Current implementation

| Area | Current status |
|---|---|
| GUI and styling | Implemented as a scrollable six-section PySide6 interface |
| Multi-file CSV import | Implemented for CSVs with a three-row DeepLabCut-style header |
| Dataset and variable selectors | Implemented; each imported file is extracted independently |
| Calibration entry | Values are captured and printed, but are not validated, converted to numbers, or applied |
| Data processing | Basic helper functions exist; GUI actions and spline/detrending/smoothing logic are not implemented |
| Plotting | Function stubs exist, but no graph widgets or plots are connected |
| Kinematics | Formula functions exist; the GUI button currently runs only fixed time and virtual-mass tests |
| Export | Buttons exist, but processed-data and results export are not implemented |
| Automated tests | Not present |

The latest refactor separated the original monolithic application into focused modules:

```text
main.py          Application entry point and stylesheet loading
gui.py           Window state, event handlers, and workflow coordination
layout.py        PySide6 widget and section construction
data.py          CSV loading and standardized coordinate extraction
processing.py    Cleaning and signal-processing helpers (partially implemented)
kinematics.py    Tail, swimming, MTP, and hindfoot calculations
plotting.py      Planned visualization API (currently stubs)
styles.qss       GUI stylesheet
```

## Input data

Two example files are included in `data/` and are also currently duplicated in the repository root:

- `mumu7091_dorSwim1.1_2025Aug14.csv` — dorsal/top-camera view
- `mumu7091_latSwim1.1_2025Aug14.csv` — lateral/side-camera view

Each example has 412 frames and a three-level header:

```text
scorer / bodyparts / coords
```

Coordinates use `x`, `y`, and `likelihood` fields. The importer currently standardizes these variables when they exist in a dataset:

```text
frame
tail_tip_x, tail_tip_y
tail_base_x, tail_base_y
snout_x, snout_y
mtp_x, mtp_y
ankle_x, ankle_y
```

Missing body points are stored as `None` and omitted from the variable selector. Unlike the previous implementation, the current code extracts variables from **every** selected CSV; file-selection order no longer determines which dataset is available in the GUI.

## Setup

Python 3.10 or newer is recommended.

1. Clone the repository and enter it:

   ```bash
   git clone <repository-url>
   cd Capstone-CS490
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Resolve the merge-conflict markers currently present in `requirements.txt`, retaining the packages the application needs:

   ```text
   PySide6
   pandas
   numpy
   scipy
   matplotlib
   ```

4. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Start MiceLab:

   ```bash
   python main.py
   ```

The dependency file must be repaired before a clean installation will succeed. This README documents the blocker but intentionally does not silently change application dependencies.

## Using the current prototype

1. Run `python main.py` from the repository root.
2. Select **Import CSV Files** and choose the dorsal and lateral CSVs. Multi-select is supported.
3. Confirm that the file count changes and that both filenames appear in the dataset selector.
4. Enter the research-team-provided values for FPS, lateral calibration, dorsal calibration, polynomial parameters, and tail diameter, then select **Register Parameters**.
5. Select a dataset and inspect the available standardized variables.
6. Select **Calculate Kinematics** only as a connectivity check. It currently displays fixed test calculations; it does not analyze the selected data.

Keep the terminal open while using the prototype. Parameter confirmation and placeholder actions are still reported there.

Do not invent calibration values. FPS, lateral and dorsal meters-per-pixel calibration, polynomial settings, and tail diameter must come from the experimental protocol or project manager.

## Kinematic functions currently available

`kinematics.py` contains functions for:

- elapsed time, swimming velocity, and tail-beat frequency;
- tail wavelength, wave speed, tip/base amplitude, lateral velocity, and relative velocity;
- virtual mass and tail-thrust power;
- MTP frequency, amplitude, wavelength, stroke length, power/recovery duration, and phase ratio;
- hindfoot length, angle, and angular velocity.

These functions are building blocks, not a completed analysis pipeline. Their scientific formulas, units, array alignment, peak/trough definitions, and expected inputs still need validation against the manager's reference analysis before results can be considered reliable.

## Objectives required for manager acceptance

### Priority 0 — make the project reproducible

- Resolve the merge conflict in `requirements.txt`, pin compatible versions, and verify setup on a clean environment.
- Remove committed generated files such as `__pycache__`, and decide whether duplicate/root-level or potentially sensitive research CSVs belong in version control.
- Add a documented command for automated tests and a small non-sensitive fixture dataset.

**Done when:** a new developer can clone the repository, install dependencies, run tests, and open the application without manual file repair.

### Priority 1 — define and validate the data contract

- Identify dorsal and lateral files explicitly instead of relying only on filenames or selection order.
- Validate the three-row CSV schema, required body points, equal/compatible frame ranges, numeric values, and likelihood fields.
- Surface missing columns and malformed inputs as actionable GUI messages.
- Preserve each camera view separately and map it to the correct calibration.

**Done when:** valid paired files load predictably, and invalid or incomplete inputs fail safely with a clear explanation.

### Priority 2 — validate calibration parameters

- Convert inputs to numeric values and reject empty, non-finite, zero, or out-of-range values as appropriate.
- Confirm the units and meaning of FPS, `latcal`, `dorscal`, polynomial coefficients, and tail diameter with the manager.
- Store parameters with the analysis session and apply lateral versus dorsal calibration consistently.

**Done when:** calculations cannot start with invalid parameters and every output has documented units.

### Priority 3 — implement the processing workflow

- Add raw-data plots for the selected variable.
- Use tracking likelihood and/or manager-approved criteria to flag outliers and allow good-region/bad-point selection.
- Implement the required spline gap filling.
- Implement unit conversion, axis orientation, polynomial detrending, mean centering/standardization, and smoothing.
- Keep raw data immutable and store each processed stage so users can review or undo decisions.

**Done when:** the GUI reproduces the manager's raw, filtered, gap-filled, converted/detrended, and standardized/smoothed views for both cameras.

### Priority 4 — connect and verify kinematics

- Build time arrays from frame number and FPS.
- Detect peaks, troughs, strokes, and phase boundaries with documented rules.
- Align MTP data with the shorter hindfoot angular-velocity series before overlaying them.
- Connect processed dorsal and lateral variables to the existing kinematic functions.
- Validate every formula against hand-calculated examples or an approved reference implementation, including edge cases such as missing data, too few cycles, and divide-by-zero conditions.

**Done when:** the same approved input and parameters produce repeatable, scientifically reviewed tail, swimming, MTP, and hindfoot metrics.

### Priority 5 — produce the manager's outputs

- Plot hindfoot angular velocity, the aligned MTP/angular-velocity overlay, detected peaks and valleys, and a final processed-data overview.
- Export cleaned and filtered variables to CSV with frame/time columns and units.
- Export the final kinematic values as a clear summary table with trial identifiers, parameters, units, and quality-control notes.
- Add save dialogs, overwrite confirmation, success/error feedback, and deterministic filenames.

**Done when:** one complete GUI run produces the cleaned-data CSV, final kinematics table, and requested diagnostic figures without relying on terminal output.

### Priority 6 — quality and release readiness

- Add unit tests for extraction, calibration, processing, and every kinematic formula; add an end-to-end test using a small fixture.
- Add application-state rules so steps run only in order and buttons are disabled until prerequisites are satisfied.
- Replace console-only messages with GUI feedback and retain useful logging for diagnosis.
- Profile representative trials, document supported data sizes, and test on the operating systems used by the team.
- Obtain manager sign-off on plots, numerical tolerances, output columns, terminology, and units.

**Done when:** automated tests pass, the full workflow is repeatable, failures are recoverable, and the manager approves the outputs against a reference trial.

## Recommended delivery sequence

Work should proceed in priority order. The critical path is dependency repair → input validation → parameter validation → processing → kinematic integration → plotting/export → scientific acceptance testing. Plot polish should not precede verification of the processed signals and formulas that feed those plots.

## Known limitations

- `requirements.txt` contains unresolved Git conflict markers.
- Parameter fields accept arbitrary text and are not used by the current calculation button.
- Processing button handlers only print placeholder messages.
- Gap filling, detrending, and smoothing functions currently return their inputs unchanged.
- Plotting functions contain only stubs.
- The calculation button uses hard-coded test values rather than imported data.
- Export buttons do not write files.
- There are no automated tests or documented scientific acceptance tolerances.

## Troubleshooting

If Python reports a missing module, activate the virtual environment and reinstall dependencies after repairing `requirements.txt`:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Verify the interpreter and installer refer to the same environment:

```bash
which python
python --version
python -m pip --version
```

If a body point is missing from the variable selector, verify that the selected CSV contains that body part in its second header row. Dorsal and lateral files do not contain identical tracked points.
