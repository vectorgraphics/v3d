#!/usr/bin/env python3
import xdrlib
import gzip
from typing import Union, Tuple, Optional, List, Callable
from enums.v3dtypes import v3dtypes

TY_TRIPLE = Tuple[float, float, float]
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


class V3DReader:
    def __init__(self, fil: gzip.GzipFile):
        self._objects = []
        self._materials = []
        self._centers = []

        self._file_ver = None
        self._processed = False

        self._object_process_fns: dict[int, Callable[[], AV3Dobject]] = {
            v3dtypes.v3dtypes_bezierPatch: self.process_bezierpatch,
            v3dtypes.v3dtypes_bezierPatchColor: self.process_bezierpatch_color,
            v3dtypes.v3dtypes_bezierTriangle: self.process_beziertriangle,
            v3dtypes.v3dtypes_bezierTriangleColor: self.process_beziertriangle_color,
            v3dtypes.v3dtypes_quad: self.process_straight_bezierpatch,
            v3dtypes.v3dtypes_quadColor: self.process_straight_bezierpatch_color,
            v3dtypes.v3dtypes_triangle: self.process_straight_beziertriangle,
            v3dtypes.v3dtypes_triangleColor: self.process_straight_beziertriangle_color,
            v3dtypes.v3dtypes_sphere: self.process_sphere,
            v3dtypes.v3dtypes_halfSphere: self.process_half_sphere,
            v3dtypes.v3dtypes_cylinder: self.process_cylinder,
            v3dtypes.v3dtypes_disk: self.process_disk,
            v3dtypes.v3dtypes_tube: self.process_tube,
            v3dtypes.v3dtypes_curve: self.process_curve,
            v3dtypes.v3dtypes_line: self.process_line,
            v3dtypes.v3dtypes_pixel_: self.process_pixel,
            v3dtypes.v3dtypes_triangles: self.process_triangles
        }

        self._xdrfile = xdrlib.Unpacker(fil.read())
        self.unpack_double = self._xdrfile.unpack_double
        self._allow_double_precision = True

    @classmethod
    def from_file_name(cls, file_name: str):
        with gzip.open(file_name, 'rb') as fil:
            reader_obj = cls(fil)
        return reader_obj

    @property
    def processed(self):
        return self._processed

    @property
    def objects(self):
        self.process()
        return self._objects

    @property
    def materials(self):
        self.process()
        return self._materials

    @property
    def centers(self):
        self.process()
        return self._centers

    @property
    def file_version(self):
        self.process()
        return self._file_ver

    @property
    def allow_double_precision(self):
        self.process()
        return self._allow_double_precision

    def get_obj_type(self) -> Optional[int]:
        try:
            typ = self._xdrfile.unpack_uint()  # XDR does not support short
            return typ
        except EOFError:
            return None

    def unpack_triple(self) -> TY_TRIPLE:
        x = self.unpack_double()
        y = self.unpack_double()
        z = self.unpack_double()
        return x, y, z

    def unpack_rgba_float(self) -> TY_RGBA:
        r = self._xdrfile.unpack_float()
        g = self._xdrfile.unpack_float()
        b = self._xdrfile.unpack_float()
        a = self._xdrfile.unpack_float()
        return r, g, b, a

    def unpack_bool(self) -> bool:
        base = self._xdrfile.unpack_uint()
        return base != 0

    def unpack_triple_n(self, n: int) -> List[TY_TRIPLE]:
        final_list = []
        for _ in range(n):
            final_list.append(self.unpack_triple())
        return final_list

    def unpack_rgba_float_n(self, n: int) -> List[TY_RGBA]:
        final_list = []
        for _ in range(n):
            final_list.append(self.unpack_rgba_float())
        return final_list

    def process_header(self):
        num_headers = self._xdrfile.unpack_uint()
        for _ in range(num_headers):
            header_type = self._xdrfile.unpack_uint()
            block_count = self._xdrfile.unpack_uint()
            for _ in range(block_count):
                dummy = self._xdrfile.unpack_uint()

    def process_bezierpatch(self) -> V3DBezierPatch:
        base_ctlpts = self.unpack_triple_n(16)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()

        assert len(base_ctlpts) == 16
        return V3DBezierPatch(tuple(base_ctlpts), material_id, center_id, min_val, max_val)

    def process_bezierpatch_color(self) -> V3DBezierPatchColor:
        base_ctlpts = self.unpack_triple_n(16)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        colors = self.unpack_rgba_float_n(4)

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()
        assert len(base_ctlpts) == 16
        return V3DBezierPatchColor(tuple(base_ctlpts), tuple(colors), material_id, center_id, min_val, max_val)

    def process_beziertriangle(self) -> V3DBezierTriangle:
        base_ctlpts = self.unpack_triple_n(10)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()

        assert len(base_ctlpts) == 10
        return V3DBezierTriangle(tuple(base_ctlpts), material_id, center_id, min_val, max_val)

    def process_beziertriangle_color(self) -> V3DBezierTriangleColor:
        base_ctlpts = self.unpack_triple_n(10)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        colors = self.unpack_rgba_float_n(3)

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()
        assert len(base_ctlpts) == 10
        return V3DBezierTriangleColor(tuple(base_ctlpts), tuple(colors), material_id, center_id, min_val, max_val)

    def process_straight_bezierpatch(self) -> V3DStraightBezierPatch:
        base_ctlpts = self.unpack_triple_n(4)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()

        assert len(base_ctlpts) == 4
        return V3DStraightBezierPatch(tuple(base_ctlpts), material_id, center_id, min_val, max_val)

    def process_straight_bezierpatch_color(self) -> V3DStraightBezierPatchColor:
        base_ctlpts = self.unpack_triple_n(4)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        colors = self.unpack_rgba_float_n(4)

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()
        assert len(base_ctlpts) == 4
        return V3DStraightBezierPatchColor(tuple(base_ctlpts), tuple(colors), material_id, center_id, min_val, max_val)

    def process_straight_beziertriangle(self) -> V3DStraightBezierTriangle:
        base_ctlpts = self.unpack_triple_n(3)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()

        assert len(base_ctlpts) == 3
        return V3DStraightBezierTriangle(
            tuple(base_ctlpts), material_id, center_id, min_val, max_val)

    def process_straight_beziertriangle_color(self) -> V3DStraightBezierTriangleColor:
        base_ctlpts = self.unpack_triple_n(3)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        colors = self.unpack_rgba_float_n(3)

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()
        assert len(base_ctlpts) == 3
        return V3DStraightBezierTriangleColor(
            tuple(base_ctlpts), tuple(colors), material_id, center_id, min_val, max_val)

    def process_sphere(self) -> V3DSphere:
        center = self.unpack_triple()
        radius = self.unpack_double()

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()
        return V3DSphere(center, radius, material_id, center_id)

    def process_half_sphere(self) -> V3DHalfSphere:
        center = self.unpack_triple()
        radius = self.unpack_double()

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        polar = self.unpack_double()
        azimuth = self.unpack_double()
        return V3DHalfSphere(center, radius, polar, azimuth, material_id, center_id)

    def process_cylinder(self) -> V3DCylinder:
        center = self.unpack_triple()
        radius = self.unpack_double()
        height = self.unpack_double()

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        polar = self.unpack_double()
        azimuth = self.unpack_double()
        core_base = self.unpack_bool()

        return V3DCylinder(center, radius, height, polar, azimuth, core_base, material_id, center_id)

    def process_disk(self) -> V3DDisk:
        center = self.unpack_triple()
        radius = self.unpack_double()

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        polar = self.unpack_double()
        azimuth = self.unpack_double()

        return V3DDisk(center, radius, polar, azimuth, material_id, center_id)

    def process_tube(self) -> V3DTube:
        points = self.unpack_triple_n(4)
        width = self.unpack_double()

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()
        core_base = self.unpack_bool()

        return V3DTube(points[0], points[1], points[2], points[3],
                       width, core_base, material_id, center_id, min_val, max_val)

    def process_curve(self) -> V3DCurve:
        points = self.unpack_triple_n(4)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()

        return V3DCurve(points[0], points[1], points[2], points[3],
                        material_id, center_id, min_val, max_val)

    def process_line(self) -> V3DLine:
        points = self.unpack_triple_n(2)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()

        return V3DLine(points[0], points[1], material_id, center_id, min_val, max_val)

    def process_pixel(self) -> V3DPixel:
        point = self.unpack_triple()
        width = self.unpack_double()

        material_id = self._xdrfile.unpack_uint()

        min_val = self.unpack_triple()
        max_val = self.unpack_triple()

        return V3DPixel(point, width, material_id, None, min_val, max_val)

    def process_material(self) -> V3DMaterial:
        diffuse = self.unpack_rgba_float()
        emissive = self.unpack_rgba_float()
        specular = self.unpack_rgba_float()
        shininess, metallic, f0, _ = self.unpack_rgba_float()
        return V3DMaterial(diffuse, emissive, specular, shininess, metallic, f0)

    def process_centers(self) -> List[TY_TRIPLE]:
        number_centers = self._xdrfile.unpack_uint()
        return self.unpack_triple_n(number_centers)

    def _unpack_int_indices(self):
        x = self._xdrfile.unpack_uint()
        y = self._xdrfile.unpack_uint()
        z = self._xdrfile.unpack_uint()
        return x, y, z

    def process_triangles(self) -> Union[V3DTriangleGroups, V3DTriangleGroupsColor]:
        is_color = False

        num_pos = self._xdrfile.unpack_uint()
        positions = self.unpack_triple_n(num_pos)

        num_normal = self._xdrfile.unpack_uint()
        normals = self.unpack_triple_n(num_normal)

        num_color = self._xdrfile.unpack_uint()
        colors = None

        if num_color > 0:
            is_color = True
            colors = self.unpack_rgba_float_n(num_color)

        pos_indices = []
        normal_indices = []
        color_indices = None

        if is_color:
            color_indices = []

        num_idx = self._xdrfile.unpack_uint()
        for _ in range(num_idx):
            num_typ = self._xdrfile.unpack_uint()
            pos_idx = self._unpack_int_indices()
            nor_idx = list(pos_idx)
            col_idx = list(pos_idx)

            if num_typ == 1:
                nor_idx = self._unpack_int_indices()
            elif num_typ == 2:
                col_idx = self._unpack_int_indices()
            elif num_typ == 3:
                nor_idx = self._unpack_int_indices()
                col_idx = self._unpack_int_indices()

            pos_indices.append(tuple(pos_idx))
            normal_indices.append(tuple(nor_idx))
            if is_color:
                color_indices.append(tuple(col_idx))

        material_id = self._xdrfile.unpack_uint()
        min_val = self.unpack_triple()
        max_val = self.unpack_triple()

        if is_color:
            return V3DTriangleGroupsColor(positions, normals, colors, pos_indices,
                                          normal_indices, color_indices, material_id, min_val, max_val)
        else:
            return V3DTriangleGroups(positions, normals, pos_indices,
                                     normal_indices, material_id, min_val, max_val)

    def get_fn_process_type(self, typ: int) -> Optional[Callable[[], AV3Dobject]]:
        return self._object_process_fns.get(typ, None)

    def process(self, force: bool = False):
        if self._processed and not force:
            return

        if self._processed and force:
            self._xdrfile.set_position(0)

        self._file_ver = self._xdrfile.unpack_uint()

        self._allow_double_precision = self.unpack_bool()
        if not self._allow_double_precision:
            self.unpack_double = self._xdrfile.unpack_float

        while typ := self.get_obj_type():
            if typ == v3dtypes.v3dtypes_material_:
                self._materials.append(self.process_material())
            elif typ == v3dtypes.v3dtypes_centers:
                self._centers = self.process_centers()
            elif typ == v3dtypes.v3dtypes_header:
                self.process_header()
            else:
                fn = self.get_fn_process_type(typ)
                if fn is not None:
                    obj = fn()
                    self._objects.append(obj)
                else:
                    raise RuntimeError('Unknown Object type. Received type {0}'.format(typ))

        self._xdrfile.done()
        self._processed = True


def main():
    v3d_obj = V3DReader.from_file_name('teapot.v3d')
    print(v3d_obj.objects)
    pass


if __name__ == '__main__':
    main()
