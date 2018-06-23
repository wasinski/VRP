from typing import Any, Dict, TextIO

from cvrp.parser.handlers import SectionHandlerRegister


class Reader:
    _data: Dict[str, Any] = dict()

    @property
    def data(self):
        return self._data

    def read(self, f: TextIO) -> None:
        section = "initial_section"
        while section != "eof":
            section_data, section = (
                SectionHandlerRegister().dispatch(section).handle(f)
            )
            self._data.update(section_data)


if __name__ == "__main__":
    _f = open("oldstuff/tests/cvrp1.test", "r")
    r = Reader()
    r.read(_f)
    print(r.data)
