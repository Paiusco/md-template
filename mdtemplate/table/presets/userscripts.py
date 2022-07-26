from dataclasses import dataclass
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence

from .. import TableTemplate

try:
    import yaml
except ImportError:
    raise ImportError(
        "Please install `PyYAML` to use the `UserscriptsTableTemplate` preset."
    )


@dataclass
class UserscriptsTableTemplate(TableTemplate):
    """
    This preset expects each Userscript to have its metadata defined in a `meta.yaml` file
    and for bundled userscripts to be in `dist/*.user.js`.
    """

    files: Optional[str] = "src/*/meta.yaml"
    columns: Optional[Sequence[str]] = ("UserScript", "Install")

    def handle_path(self, path: Path) -> Iterable[Iterable[str]]:
        with open(path) as file:
            manifest = yaml.safe_load(file)

        desc = "\n" + manifest["description"] if manifest["description"] else ""
        yield [
            f"[**{manifest['name']}**]({path.parent.as_posix()}){desc}",
            f"[Install](../../raw/{self.repository.branch}/dist/{path.parent.name}.user.js)",
        ]
