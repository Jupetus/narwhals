from typing import Any

import pyarrow as pa
import pytest

import narwhals.stable.v1 as nw
from narwhals.utils import parse_version
from tests.utils import compare_dicts

data = {
    "i": [0, 1, 2, 3, 4],
    "b": [1, 2, 3, 5, 3],
    "c": [5, 4, 3, 2, 1],
}


def test_diff(constructor: Any, request: Any) -> None:
    if "pyarrow_table_constructor" in str(constructor) and parse_version(
        pa.__version__
    ) < (13,):
        # pc.pairwisediff is available since pyarrow 13.0.0
        request.applymarker(pytest.mark.xfail)
    df = nw.from_native(constructor(data))
    result = df.with_columns(c_diff=nw.col("c").diff()).filter(nw.col("i") > 0)
    expected = {
        "i": [1, 2, 3, 4],
        "b": [2, 3, 5, 3],
        "c": [4, 3, 2, 1],
        "c_diff": [-1, -1, -1, -1],
    }
    compare_dicts(result, expected)


def test_diff_series(constructor_eager: Any, request: Any) -> None:
    if "pyarrow_table_constructor" in str(constructor_eager) and parse_version(
        pa.__version__
    ) < (13,):
        # pc.pairwisediff is available since pyarrow 13.0.0
        request.applymarker(pytest.mark.xfail)
    df = nw.from_native(constructor_eager(data), eager_only=True)
    expected = {
        "i": [1, 2, 3, 4],
        "b": [2, 3, 5, 3],
        "c": [4, 3, 2, 1],
        "c_diff": [-1, -1, -1, -1],
    }
    result = df.with_columns(c_diff=df["c"].diff())[1:]
    compare_dicts(result, expected)
