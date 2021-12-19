#!/usr/bin/env python3

from typing import Union, Tuple, List

TY_PAIR = Tuple[float, float]
TY_TRIPLE = Tuple[float, float, float]
TY_RGB = Tuple[float, float, float]
TY_RGBA = Tuple[float, float, float, float]

TY_BEZIER_PATCH = Union[Tuple[
                            TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
                            TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
                            TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
                            TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE
                        ], Tuple[TY_TRIPLE, ...]]

TY_STRAIGHT_BEZIER_PATCH = Union[Tuple[TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE], Tuple[TY_TRIPLE, ...]]

TY_BEZIER_PATCH_COLOR = Union[Tuple[TY_RGBA, TY_RGBA, TY_RGBA, TY_RGBA], Tuple[TY_RGBA, ...]]

TY_BEZIER_TRIANGLE = Union[Tuple[
                               TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
                               TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
                               TY_TRIPLE, TY_TRIPLE], Tuple[TY_TRIPLE, ...]]

TY_STRAIGHT_BEZIER_TRIANGLE = Union[Tuple[TY_TRIPLE, TY_TRIPLE], Tuple[TY_TRIPLE, ...]]

TY_BEZIER_TRIANGLE_COLOR = Union[Tuple[TY_RGBA, TY_RGBA, TY_RGBA], Tuple[TY_RGBA, ...]]

TY_TRIANGLE_INDEX = Tuple[int, int, int]
TY_INDICES = List[TY_TRIANGLE_INDEX]
