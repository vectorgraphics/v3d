#!/usr/bin/env python3

from .typehints import *
from typing import Optional


class AV3Dobject:
    def __init__(self, material_id: Optional[int] = None, center_index: Optional[int] = None,
                 min_val: Optional[TY_TRIPLE] = None, max_val: Optional[TY_TRIPLE] = None):
        self.material_id = material_id
        self.center_index = center_index
        self.min = min_val
        self.max = max_val


class V3DMaterial(AV3Dobject):
    def __init__(self, diffuse: TY_RGBA, emissive: TY_RGBA, specular: TY_RGBA,
                 metallic: float = 0, shininess: float = 0.8, f0: float = 0.4):
        super().__init__()
        self.diffuse = diffuse
        self.emissive = emissive
        self.specular = specular
        self.metallic = metallic
        self.shininess = shininess
        self.f0 = f0


class V3DSingleLightSource:
    def __init__(self, position: TY_TRIPLE, color: TY_RGBA):
        self.position = position
        self.color = color


class V3DConfigurationValue:
    def __init__(self):
        self.absolute: Optional[bool] = None
        self.zoom_factor: Optional[float] = None
        self.zoom_pinch_factor: Optional[float] = None
        self.zoom_pinch_cap: Optional[float] = None
        self.zoom_step: Optional[float] = None
        self.shift_hold_distance: Optional[float] = None
        self.shift_wait_time: Optional[float] = None
        self.vibrate_time: Optional[float] = None


class V3DHeaderInformation:
    def __init__(self):
        self.canvas_width: Optional[int] = None
        self.canvas_height: Optional[int] = None
        self.b: Optional[TY_TRIPLE] = None
        self.B: Optional[TY_TRIPLE] = None
        self.orthographic: Optional[bool] = None
        self.angle: Optional[float] = None
        self.Zoom0: Optional[float] = None
        self.viewport_margin: Optional[TY_PAIR] = None
        self.viewport_shift: TY_PAIR = (0.0, 0.0)
        self.lights: List[V3DSingleLightSource] = []
        self.background: TY_RGBA = (1.0, 1.0, 1.0, 1.0)
        self.configuration: V3DConfigurationValue = V3DConfigurationValue()


class V3DBezierPatch(AV3Dobject):
    def __init__(
            self, ctrl_points: TY_BEZIER_PATCH, material_id: int = None,
            center_index: int = None, min_val: TY_TRIPLE = None, max_val: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min_val, max_val)
        self.control_pts = ctrl_points


class V3DBezierPatchColor(V3DBezierPatch):
    def __init__(
            self, ctrl_points: TY_BEZIER_PATCH, colors: TY_BEZIER_PATCH_COLOR,
            material_id: int = None, center_index: int = None,
            min_val: TY_TRIPLE = None, max_val: TY_TRIPLE = None):
        super().__init__(ctrl_points, material_id, center_index, min_val, max_val)
        self.colors = colors


class V3DBezierTriangle(AV3Dobject):
    def __init__(
            self, ctrl_points: TY_BEZIER_TRIANGLE, material_id: int = None,
            center_index: int = None, min_val: TY_TRIPLE = None, max_val: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min_val, max_val)
        self.control_pts = ctrl_points


class V3DBezierTriangleColor(V3DBezierPatch):
    def __init__(
            self, ctrl_points: TY_BEZIER_TRIANGLE, colors: TY_BEZIER_TRIANGLE_COLOR,
            material_id: int = None, center_index: int = None,
            min_val: TY_TRIPLE = None, max_val: TY_TRIPLE = None):
        super().__init__(ctrl_points, material_id, center_index, min_val, max_val)
        self.colors = colors


class V3DStraightBezierPatch(AV3Dobject):
    def __init__(
            self, ctrl_points: TY_STRAIGHT_BEZIER_PATCH, material_id: int = None,
            center_index: int = None, min_val: TY_TRIPLE = None, max_val: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min_val, max_val)
        self.control_pts = ctrl_points


class V3DStraightBezierPatchColor(V3DStraightBezierPatch):
    def __init__(
            self, ctrl_points: TY_STRAIGHT_BEZIER_PATCH, colors: TY_BEZIER_PATCH_COLOR,
            material_id: int = None, center_index: int = None,
            min_val: TY_TRIPLE = None, max_val: TY_TRIPLE = None):
        super().__init__(ctrl_points, material_id, center_index, min_val, max_val)
        self.colors = colors


class V3DStraightBezierTriangle(AV3Dobject):
    def __init__(
            self, ctrl_points: TY_STRAIGHT_BEZIER_TRIANGLE, material_id: int = None,
            center_index: int = None, min_val: TY_TRIPLE = None, max_val: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min_val, max_val)
        self.control_pts = ctrl_points


class V3DStraightBezierTriangleColor(V3DBezierPatch):
    def __init__(
            self, ctrl_points: TY_STRAIGHT_BEZIER_TRIANGLE, colors: TY_BEZIER_TRIANGLE_COLOR,
            material_id: int = None, center_index: int = None,
            min_val: TY_TRIPLE = None, max_val: TY_TRIPLE = None):
        super().__init__(ctrl_points, material_id, center_index, min_val, max_val)
        self.colors = colors


class V3DTriangleGroups(AV3Dobject):
    def __init__(
            self, positions: List[TY_TRIPLE], normals: List[TY_TRIPLE],
            position_indices: TY_INDICES, normals_indices: TY_INDICES, material_id: int = None,
            min_value: TY_TRIPLE = None, max_value: TY_TRIPLE = None):
        super().__init__(material_id, None, min_value, max_value)
        self.positions = positions
        self.normals = normals
        self.position_indices = position_indices
        self.normals_indices = normals_indices
        assert len(position_indices) == len(normals_indices)


class V3DTriangleGroupsColor(V3DTriangleGroups):
    def __init__(
            self, positions: List[TY_TRIPLE], normals: List[TY_TRIPLE], colors: List[TY_RGBA],
            position_indices: TY_INDICES, normals_indices: TY_INDICES, color_indices: TY_INDICES,
            material_id: int = None, min_value: TY_TRIPLE = None, max_value: TY_TRIPLE = None):
        super().__init__(positions, normals, position_indices, normals_indices, material_id, min_value, max_value)
        self.colors = colors
        self.color_indices = color_indices
        assert len(color_indices) == len(position_indices)


class V3DSphere(AV3Dobject):
    def __init__(
            self, center: TY_TRIPLE, radius: float, material_id: int = None, center_index: int = None):
        super().__init__(material_id, center_index, None, None)
        self.center = center
        self.radius = radius


class V3DHalfSphere(V3DSphere):
    def __init__(
            self, center: TY_TRIPLE, radius: float, polar: float, azimuth: float,
            material_id: int = None, center_index: int = None):
        super().__init__(center, radius, material_id, center_index)
        self.polar = polar
        self.azimuth = azimuth


class V3DCylinder(AV3Dobject):
    def __init__(
            self, center: TY_TRIPLE, radius: float, height: float, polar: float, azimuth: float, core: bool,
            material_id: int = None, center_index: int = None):
        super().__init__(material_id, center_index, None, None)
        self.center = center
        self.radius = radius
        self.height = height
        self.polar = polar
        self.azimuth = azimuth
        self.core = core


class V3DDisk(AV3Dobject):
    def __init__(
            self, center: TY_TRIPLE, radius: float, polar: float, azimuth: float,
            material_id: int = None, center_index: int = None):
        super().__init__(material_id, center_index)
        self.center = center
        self.radius = radius
        self.polar = polar
        self.azimuth = azimuth


class V3DTube(AV3Dobject):
    def __init__(
            self, c0: TY_TRIPLE, c1: TY_TRIPLE, c2: TY_TRIPLE, c3: TY_TRIPLE, width: float, core: bool,
            material_id: int = None, center_index: int = None,
            min_value: TY_TRIPLE = None, max_value: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min_value, max_value)
        self.path = (c0, c1, c2, c3)
        self.width = width
        self.core = core


class V3DCurve(AV3Dobject):
    def __init__(
            self, z0: TY_TRIPLE, c0: TY_TRIPLE, c1: TY_TRIPLE, z1: TY_TRIPLE,
            material_id: int = None, center_index: int = None,
            min_value: TY_TRIPLE = None, max_value: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min_value, max_value)
        self.z0 = z0
        self.c0 = c0
        self.c1 = c1
        self.z1 = z1


class V3DLine(AV3Dobject):
    def __init__(
            self, z0: TY_TRIPLE, z1: TY_TRIPLE,
            material_id: int = None, center_index: int = None,
            min_value: TY_TRIPLE = None, max_value: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min_value, max_value)
        self.z0 = z0
        self.z1 = z1


class V3DPixel(AV3Dobject):
    def __init__(
            self, point: TY_TRIPLE, width: float,
            material_id: int = None, center_index: int = None,
            min_value: TY_TRIPLE = None, max_value: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min_value, max_value)
        self.point = point
        self.width = width

