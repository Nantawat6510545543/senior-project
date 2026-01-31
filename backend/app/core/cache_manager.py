PIPELINE_VERSION = "v3"

import hashlib
import json
import logging
from pathlib import Path

from pydantic import BaseModel

def _repo_root(start: Path) -> Path:
    for p in [*start.parents, start]:
        if (p / ".git").exists() or (p / "pyproject.toml").exists():
            return p
    return start


def _hash_of_dict(d):
    s = json.dumps(d, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(s.encode()).hexdigest()[:16]

# TODO refactor
class CacheKey(BaseModel):
    subject: str
    task: str
    run: str | None
    stage: str
    params: dict
    pipeline_ver: str

    class Config:
        frozen = True

    def subdir(self):
        r = f"run-{self.run}" if self.run else "run-none"
        return f"{self.subject}/{self.task}/{r}/{self.stage}"

    def filename_stem(self):
        return f"{_hash_of_dict(self.params)}-{self.pipeline_ver}"

class LocalCache:
    pass