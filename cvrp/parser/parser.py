from abc import ABC, abstractclassmethod
from typing import Any, Dict, TextIO


class ISectionHandler(ABC):
    @abstractclassmethod
    def handle(cls, f):
        raise NotImplementedError

    @staticmethod
    def _has_section_changed(line):
        return line.lower() in SECTION_HANDLERS


class InitialSectionHandler(ISectionHandler):
    @classmethod
    def handle(cls, f):
        data = {}
        while True:
            line = next(f).strip()
            if cls._has_section_changed(line):
                return data, line.lower()

            attr, _colon, value = map(str.strip, line.strip().partition(":"))
            data[attr.lower()] = cls._parse_value(value)

    @staticmethod
    def _parse_value(value):
        if value.isdigit():
            return int(value)
        if value.isdecimal():
            return float(value)
        return value


class NodeCoordSectionHandler(ISectionHandler):
    @classmethod
    def handle(cls, f):
        data = {"node_coord_section": []}
        while True:
            line = next(f).strip()
            if cls._has_section_changed(line):
                return data, line.lower()
            _nr, x, y = line.split()
            data["node_coord_section"].append((int(x), int(y)))


class DemandSectionHandler(ISectionHandler):
    @classmethod
    def handle(cls, f):
        data = {"demand_section": []}
        while True:
            line = next(f).strip()
            if cls._has_section_changed(line):
                return data, line.lower()
            _nr, demand = line.split()
            data["demand_section"].append(int(demand))


class DepotSectionHandler(ISectionHandler):
    @classmethod
    def handle(cls, f):
        data = {"depot_section": []}
        while True:
            line = next(f).strip()
            if cls._has_section_changed(line):
                return data, line.lower()
            nr = line.strip()
            data["depot_section"].append(int(nr))


class EOFSectionHandler(ISectionHandler):
    @classmethod
    def handle(cls, f):
        return {}, "eof"


SECTION_HANDLERS = {
    "initial": InitialSectionHandler,
    "node_coord_section": NodeCoordSectionHandler,
    "demand_section": DemandSectionHandler,
    "depot_section": DepotSectionHandler,
    "eof": EOFSectionHandler,
}


class Reader:
    _data: Dict[str, Any] = dict()

    @property
    def data(self):
        return self._data

    def read(self, f: TextIO) -> None:
        section_handler = SECTION_HANDLERS["initial"]
        section = None
        while section != "eof":
            section_data, section = section_handler.handle(f)  # type: ignore
            self._data.update(section_data)
            section_handler = SECTION_HANDLERS[section]


if __name__ == "__main__":
    _f = open("oldstuff/tests/cvrp1.test", "r")
    r = Reader()
    r.read(_f)
    print(r.data)
