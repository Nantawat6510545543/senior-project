from pathlib import Path
import os, re
from typing import List, Tuple, Optional
from dotenv import load_dotenv

load_dotenv() 
DATA_ROOT = Path(os.getenv("DATA_ROOT"))

_TASK_RX = re.compile(
    r"^(sub-[^_]+)_task-([^_]+)(?:_run-(\d+))?_eeg\.set$",
    re.IGNORECASE,
)

# Check file on startup
if not DATA_ROOT.exists():
    raise FileNotFoundError(f"DATA_ROOT does not exist: {DATA_ROOT}")

if not DATA_ROOT.is_dir():
    raise NotADirectoryError(f"DATA_ROOT is not a directory: {DATA_ROOT}")


def list_subjects() -> List[str]:
    """
    Return all subject IDs found under cmi_bids_R*/*/eeg folders.
    """
    subjects = set()

    for rdir in DATA_ROOT.glob("cmi_bids_R*"):
        if not rdir.is_dir():
            continue

        for subj_dir in rdir.glob("sub-*"):
            eeg_dir = subj_dir / "eeg"
            if eeg_dir.exists():
                subjects.add(subj_dir.name)

    return sorted(subjects)


def list_tasks(subject_id: str) -> List[Tuple[str, Optional[str]]]:
    """
    Return (task, run) pairs for a given subject across all releases.
    """
    tasks = set()

    for rdir in DATA_ROOT.glob("cmi_bids_R*"):
        eeg_dir = rdir / subject_id / "eeg"
        if not eeg_dir.exists():
            continue

        for f in eeg_dir.glob("sub-*_task-*_eeg.set"):
            m = _TASK_RX.match(f.name)
            if not m:
                continue

            task = m.group(2)
            run = m.group(3)  # may be None
            tasks.add((task, run))

    return sorted(tasks)
