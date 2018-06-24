from io import StringIO

import pytest

from cvrp.parser.parser import Reader


@pytest.fixture
def sample_tsplib():
    sample = {}
    sample["input"] = StringIO(
        "NAME : test-E-n2-k4\n"
        "TYPE : CVRP\n"
        "CAPACITY : 2500\n"
        "NODE_COORD_SECTION\n"
        "1 100 200\n"
        "2 200 100\n"
        "DEMAND_SECTION\n"
        "1 0\n"
        "2 1100\n"
        "DEPOT_SECTION\n"
        " 1\n"
        " -1\n"
        "EOF\n"
    )
    sample["output"] = {
        "name": "test-E-n2-k4",
        "type": "CVRP",
        "capacity": 2500,
        "node_coord_section": [(100, 200), (200, 100)],
        "demand_section": [0, 1100],
        "depot_section": [0],
    }
    return sample


def test_parser(sample_tsplib):
    reader = Reader()
    reader.read(sample_tsplib["input"])

    assert reader.instance_data == sample_tsplib["output"]
