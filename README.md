# MiceLab swimming kinematics

MiceLab is a desktop application for cleaning DeepLabCut tracking data from dorsal and lateral camera views, processing coordinates, calculating swimming and hindlimb kinematics, and exporting results.

## Run

Use Python 3.10 or newer. From this folder, install the packages and launch the app:

```sh
python -m pip install -r requirements.txt
python main.py
```

The example dorsal and lateral CSVs are in `data/` and are also present in the repository root. They are DeepLabCut exports with the required three-row headers. Import them into the corresponding dorsal and lateral buttons. Either view can be processed on its own; load both for the complete set of measurements.

## Workflow

1. Import a dorsal and/or lateral DeepLabCut CSV.
2. Set frame rate and view-specific calibration in meters per pixel. Defaults are 250 fps, 0.00027257 m/px dorsal, and 0.00026895 m/px lateral. Set the minimum landmark likelihood (default 0.20), detrending order, smoothing window, and tail diameter as appropriate for the recording.
3. Run Filter, Fill Gaps, Convert & Detrend, and Standardize & Smooth in order. A later step runs any missing preceding steps automatically. The inspection controls show the selected coordinate at each completed stage.
   To manually reject detections, select the Raw or Filtered stage, enable manual outlier editing, and click a sample. Red X markers show excluded samples; click a red X to restore it. Undo Point reverts the last change, and Clear Manual Points removes all manual exclusions for the selected view. Manual masks apply to the selected bodypart coordinate and remain in effect when the filtering step is rerun.
4. Calculate kinematics. Results include forward swimming velocity, tail beat frequency and amplitudes, tail lateral velocity and virtual mass, and available hindfoot length, angle amplitude, angular velocity, MTP frequency, and stroke length. A metric is omitted when its landmarks are not present.
5. Save processed data as a combined CSV. Dorsal and lateral columns are prefixed by view. Save the kinematics table as CSV; the matching overview plot is written beside it as PNG.

Filtering masks detections below the selected likelihood and isolated coordinate jumps. Missing x/y detections are interpolated with a shape-preserving cubic spline; edge values without valid bracketing points remain missing. Y coordinates are inverted during unit conversion so upward motion is positive. Detrending is polynomial, and standardization mean-centers each detrended coordinate before Savitzky-Golay smoothing.

## Code layout

- `main.py` starts Qt and loads the application stylesheet.
- `gui.py` owns the window, per-view input data, workflow-stage snapshots, and button actions.
- `data.py` reads DeepLabCut CSV headers and preserves bodypart and coordinate names.
- `processing.py` implements filtering, spline filling, calibration, detrending, and smoothing.
- `kinematics.py` calculates measurements from the processed coordinate table.
- `plotting.py` contains the data preview and overview chart; `layout.py` builds the UI sections.

Python files use four-space indentation and Black formatting (88-character line length). Install the development formatter with `python -m pip install -r requirements-dev.txt`, then run `python -m black *.py` to format the source.
