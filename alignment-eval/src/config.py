"""Read config/models.yaml: which models are under test, which judge them."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "models.yaml"
PLACEHOLDER = "REPLACE_ME"


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class Entry:
    name: str
    model: str
    family: str

    @property
    def is_placeholder(self) -> bool:
        return PLACEHOLDER in self.model

    def as_dict(self) -> dict:
        return {"name": self.name, "model": self.model, "family": self.family}


@dataclass(frozen=True)
class Config:
    under_test: list[Entry]
    judges: list[Entry]

    def family_of(self) -> dict[str, str]:
        """Model string -> family, for every configured model under test."""
        return {e.model: e.family for e in self.under_test if not e.is_placeholder}

    def select(self, names: list[str]) -> list[Entry]:
        known = {e.name: e for e in self.under_test}
        unknown = [n for n in names if n not in known]
        if unknown:
            raise ConfigError(f"unknown model name(s) {unknown}; configured: {sorted(known)}")
        return [known[n] for n in names]


def load_config(path: str | Path = DEFAULT_CONFIG) -> Config:
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}

    def entries(key: str) -> list[Entry]:
        out = []
        for raw in doc.get(key) or []:
            missing = {"name", "model", "family"} - set(raw)
            if missing:
                raise ConfigError(f"{key} entry {raw} is missing {sorted(missing)}")
            out.append(Entry(str(raw["name"]), str(raw["model"]), str(raw["family"])))
        return out

    cfg = Config(entries("under_test"), entries("judges"))
    names = [e.name for e in cfg.under_test + cfg.judges]
    if len(names) != len(set(names)):
        raise ConfigError("model and judge names must be unique")
    if len(cfg.judges) < 2 or len({j.family for j in cfg.judges}) < 2:
        raise ConfigError(
            "at least two judges from at least two families are required; "
            "otherwise some outputs would have no judge outside their own family"
        )
    return cfg
