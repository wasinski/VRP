from typing import Any, Dict, TextIO

import attr

from cvrp.aliases import SectionName
from cvrp.parser.handlers import SectionHandlerRegister


@attr.s
class Reader:
    _data: Dict[str, Any] = attr.ib(default=attr.Factory(dict))

    @property
    def instance_data(self) -> Dict[str, Any]:
        return self._data

    def read(self, f: TextIO) -> None:
        section = SectionName("initial_section")
        while section != "eof":
            section_data, section = (
                SectionHandlerRegister().dispatch(section).handle(f)
            )
            self._data.update(section_data)


if __name__ == "__main__":
    _f = open("oldstuff/tests/cvrp1.test", "r")
    r = Reader()
    r.read(_f)
    print(r.instance_data)
