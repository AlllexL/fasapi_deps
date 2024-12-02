from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
)

from utils.helper import GreateHelper
from .dependencies.func_deps import (
    get_x_foo_bar,
    get_header_dependency,
    get_great_helper,
)

router = APIRouter(tags=["Dependencies_Examples"])


@router.get("/single-direct-dependency")
def single_direct_dependency(
    foobar: Annotated[
        str,
        Header(),
    ]
):
    return {"foobar": foobar, "message": "single direct dependency foobar"}


@router.get("/single-via-func")
def single_via_func(
    foobar: Annotated[
        str,
        Depends(get_x_foo_bar),
    ]
):
    return {"x-foobar": foobar, "message": "single via-func dependency foobar"}


@router.get("/multi-direct-and-via-func")
def multi_direct_and_via_func(
    fizzbuzz: Annotated[
        str,
        Header(alias="x-fizz-buzz"),
    ],
    foobar: Annotated[
        str,
        Depends(get_x_foo_bar),
    ],
):
    return {
        "x-fizz-buzz": fizzbuzz,
        "x-foobar": foobar,
        "message": "multi direct and via-func dependency foobar",
    }


@router.get("/multi-indirect")
def multi_indirect(
    foobar: Annotated[
        str,
        Depends(get_header_dependency("x-foobar")),
    ],
    fizzbuzz: Annotated[
        str,
        Depends(get_header_dependency("x-fizzbuzz", default_value="FIZZBUZZ")),
    ],
):
    return {
        "x-fizz-buzz": fizzbuzz,
        "x-foobar": foobar,
        "message": "multi direct",
    }


@router.get("/top-level-helper")
def top_level_helper_creation(
    helper_name: Annotated[
        str, Depends(get_header_dependency("x-helper-name", default_value="HelperOne"))
    ],
    helper_default: Annotated[
        str, Depends(get_header_dependency("x-helper-default-value"))
    ],
):
    helper = GreateHelper(name=helper_name, default=helper_default)
    return {"helper": helper.as_dict(), "message": "Top level helper creation"}


@router.get("/helper-as-dependency")
def helper_as_dependency(helper: Annotated[GreateHelper, Depends(get_great_helper)]):
    return {"helper": helper.as_dict(), "message": "helper_as_dependency"}
