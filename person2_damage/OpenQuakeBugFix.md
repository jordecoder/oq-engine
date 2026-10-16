# OpenQuake Read-Only Array Bug Fix

During the Nepal hazard simulation, OpenQuake encountered a `TypeError` because a read-only NumPy array was passed to a Numba function expecting a writable array.

**File modified:** `openquake/commonlib/calc.py` (inside the installed OpenQuake virtual environment).

**Original code:**
```python
arr = performance.idx_start_stop(eids)
```

**Modified code:**
```python
arr = performance.idx_start_stop(numpy.array(eids, copy=True))
```

This workaround creates a writable copy of the array without changing its values, allowing the hazard simulation to complete successfully.

#### Backup Procedure

Before modifying `calc.py`, create a backup using PowerShell:

```powershell
$path = "$env:USERPROFILE\openquake\Lib\site-packages\openquake\commonlib\calc.py"
Copy-Item $path "$path.bak"
```

Verify the backup exists:

```powershell
Test-Path "$path.bak"
```

The command should return `True`.

#### Rollback Procedure

If the modification causes problems, restore the original file:

```powershell
Copy-Item "$path.bak" $path -Force
```

Restart the Python/OpenQuake process afterward to ensure the restored code is loaded.

**Important Notes:**
- Only apply the patch when encountering the same error.
- Keep the backup until the workaround is no longer needed.
- Stop running OpenQuake calculations before modifying or restoring the file.
- This is a temporary local workaround tested with OpenQuake Engine 3.26.2, not an official fix.
- Teammates may need to apply the same workaround on their own installations.