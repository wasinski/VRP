from abc import ABC, abstractclassmethod
from collections import defaultdict
from typing import Dict, Iterable, KeysView, Tuple

from cvrp.aliases import SectionName


class SectionHandlerRegister:
    __instance = None
    _register: Dict[SectionName, "ASectionHandler"]

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = object.__new__(cls, *args, **kwargs)
            cls._register = {}
        return cls.__instance

    def dispatch(self, section: SectionName) -> "ASectionHandler":
        return self._register[section]

    def register(self, handler: "ASectionHandler") -> None:
        self._register[handler.section] = handler

    @property
    def section_names(self) -> KeysView[SectionName]:
        return self._register.keys()


class ASectionHandler(ABC):
    """Abstract SectionHandler - TemplateMethod pattern"""

    section: SectionName

    @classmethod
    def handle(cls, f):
        lines, next_section = cls.__read_section(f)
        section_data = cls.process_section(lines)
        return section_data, next_section

    @abstractclassmethod
    def process_section(cls, lines):
        raise NotImplementedError

    @classmethod
    def __read_section(cls, f) -> Tuple[Iterable[str], SectionName]:
        lines = []
        line = f.readline().strip()
        while not cls.__has_section_changed(line):
            lines.append(line)
            line = f.readline().strip()

        next_section = line.lower()
        return lines, next_section

    @staticmethod
    def __has_section_changed(line: str) -> bool:
        return line.lower() in SectionHandlerRegister().section_names


def section_handler(cls):
    """Class decorator for registering handlers"""
    SectionHandlerRegister().register(cls)
    return cls


@section_handler
class InitialSectionHandler(ASectionHandler):
    section = SectionName("initial_section")

    @classmethod
    def process_section(cls, lines):
        data = {}
        for line in lines:
            attr, _colon, value = map(str.strip, line.partition(":"))
            data[attr.lower()] = cls._parse_value(value)
        return data

    @staticmethod
    def _parse_value(value):
        if value.isdigit():
            return int(value)
        if value.isdecimal():
            return float(value)
        return value


@section_handler
class NodeCoordSectionHandler(ASectionHandler):
    section = SectionName("node_coord_section")

    @classmethod
    def process_section(cls, lines):
        data = defaultdict(list)
        for line in lines:
            _nr, x, y = line.split()
            data[cls.section].append((int(x), int(y)))
        return data


@section_handler
class DemandSectionHandler(ASectionHandler):
    section = SectionName("demand_section")

    @classmethod
    def process_section(cls, lines):
        data = defaultdict(list)
        for line in lines:
            _nr, demand = line.split()
            data[cls.section].append(int(demand))
        return data


@section_handler
class DepotSectionHandler(ASectionHandler):
    section = SectionName("depot_section")
    terminator = -1

    @classmethod
    def process_section(cls, lines):
        data = defaultdict(list)
        for line in lines:
            nr = int(line.strip())
            if nr == cls.terminator:
                break
            data[cls.section].append(nr - 1)
        return data


@section_handler
class EOFSectionHandler(ASectionHandler):
    section = SectionName("eof")

    @classmethod
    def process_section(cls, lines):
        return {}, "eof"
