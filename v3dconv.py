#!/usr/bin/env python3
import xdrlib
import io
from typing import Union, Tuple, Optional, List, Any
from generated_enums import V3dTypes

TY_TRIPLE = Tuple[float, float, float]
TY_RGBA = Tuple[float, float, float, float]

TY_BEZIER_PATCH = Union[Tuple[
    TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
    TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
    TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
    TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE
], Tuple[TY_TRIPLE, ...]]

TY_BEZIER_PATCH_COLOR = Union[Tuple[TY_RGBA, TY_RGBA, TY_RGBA, TY_RGBA], Tuple[TY_RGBA, ...]]

TY_BEZIER_TRIANGLE = Union[Tuple[
                            TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
                            TY_TRIPLE, TY_TRIPLE, TY_TRIPLE, TY_TRIPLE,
                            TY_TRIPLE, TY_TRIPLE], Tuple[TY_TRIPLE, ...]]

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
            center_index: int = None, min: TY_TRIPLE = None, max: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min, max)
        self.control_pts = ctrl_points


class V3DBezierPatchColor(V3DBezierPatch):
    def __init__(
            self, ctrl_points: TY_BEZIER_PATCH, colors: TY_BEZIER_PATCH_COLOR,
            material_id: int = None, center_index: int = None,
            min: TY_TRIPLE = None, max: TY_TRIPLE = None):
        super().__init__(ctrl_points, material_id, center_index, min, max)
        self.colors = colors


class V3DBezierTriangle(AV3Dobject):
    def __init__(
            self, ctrl_points: TY_BEZIER_TRIANGLE, material_id: int = None,
            center_index: int = None, min: TY_TRIPLE = None, max: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min, max)
        self.control_pts = ctrl_points


class V3DBezierTriangleColor(V3DBezierPatch):
    def __init__(
            self, ctrl_points: TY_BEZIER_TRIANGLE, colors: TY_BEZIER_TRIANGLE_COLOR,
            material_id: int = None, center_index: int = None,
            min: TY_TRIPLE = None, max: TY_TRIPLE = None):
        super().__init__(ctrl_points, material_id, center_index, min, max)
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
    def __init__(self, fil: Union[io.FileIO, io.BytesIO, Any]):
        self.objects = []
        self.materials = []
        self.centers = []

        self.file_ver = None
        self.processed = False

        self._xdrfile = xdrlib.Unpacker(fil.read())

    def get_objtype(self) -> Optional[int]:
        try:
            typ = self._xdrfile.unpack_uint()  # XDR does not support short
            return typ
        except EOFError:
            return None

    def unpack_triple(self) -> TY_TRIPLE:
        x = self._xdrfile.unpack_double()
        y = self._xdrfile.unpack_double()
        z = self._xdrfile.unpack_double()
        return x, y, z

    def unpack_rgba_float(self) -> TY_RGBA:
        r = self._xdrfile.unpack_float()
        g = self._xdrfile.unpack_float()
        b = self._xdrfile.unpack_float()
        a = self._xdrfile.unpack_float()
        return r, g, b, a

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

    def process_sphere(self) -> V3DSphere:
        center = self.unpack_triple()
        radius = self._xdrfile.unpack_float()

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()
        return V3DSphere(center, radius, material_id, center_id)

    def process_half_sphere(self) -> V3DHalfSphere:
        center = self.unpack_triple()
        radius = self._xdrfile.unpack_float()

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        polar = self._xdrfile.unpack_float()
        azimuth = self._xdrfile.unpack_float()
        return V3DHalfSphere(center, radius, polar, azimuth, material_id, center_id)

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
        is_color=False

        nP = self._xdrfile.unpack_uint()
        positions = self.unpack_triple_n(nP)

        nN = self._xdrfile.unpack_uint()
        normals = self.unpack_triple_n(nN)

        nC = self._xdrfile.unpack_uint()
        colors = None

        if nC > 0:
            is_color = True
            colors = self.unpack_rgba_float_n(nC)

        pos_indices = []
        normal_indices = []
        color_indices = None

        if is_color:
            color_indices = []

        numIdx = self._xdrfile.unpack_uint()
        for _ in range(numIdx):
            numTyp = self._xdrfile.unpack_uint()
            posIdx = self._unpack_int_indices()
            norIdx = list(posIdx)
            colIdx = list(posIdx)

            if numTyp == 1:
                norIdx = self._unpack_int_indices()
            elif numTyp == 2:
                colIdx = self._unpack_int_indices()
            elif numTyp == 3:
                norIdx = self._unpack_int_indices()
                colIdx = self._unpack_int_indices()

            pos_indices.append(tuple(posIdx))
            normal_indices.append(tuple(norIdx))
            if is_color:
                color_indices.append(tuple(colIdx))

        material_id = self._xdrfile.unpack_uint()
        min_val = self.unpack_triple()
        max_val = self.unpack_triple()

        if is_color:
            return V3DTriangleGroupsColor(positions, normals, colors, pos_indices,
                                          normal_indices, color_indices, material_id, min_val, max_val)
        else:
            return V3DTriangleGroups(positions, normals, pos_indices, normal_indices, material_id, min_val, max_val)

    def process(self, force: bool = False):
        if self.processed and not force:
            return

        if self.processed and force:
            self._xdrfile.set_position(0)

        self.file_ver = self._xdrfile.unpack_uint()

        while typ := self.get_objtype():
            if typ == V3dTypes.V3DTYPES_BEZIERPATCH:
                self.objects.append(self.process_bezierpatch())
            elif typ == V3dTypes.V3DTYPES_BEZIERPATCHCOLOR:
                self.objects.append(self.process_bezierpatch_color())
            if typ == V3dTypes.V3DTYPES_BEZIERTRIANGLE:
                self.objects.append(self.process_beziertriangle())
            elif typ == V3dTypes.V3DTYPES_BEZIERTRIANGLECOLOR:
                self.objects.append(self.process_beziertriangle_color())
            elif typ == V3dTypes.V3DTYPES_SPHERE:
                self.objects.append(self.process_sphere())
            elif typ == V3dTypes.V3DTYPES_HALFSPHERE:
                self.objects.append(self.process_half_sphere())
            elif typ == V3dTypes.V3DTYPES_TRIANGLES:
                self.objects.append(self.process_triangles())
            elif typ == V3dTypes.V3DTYPES_MATERIAL_:
                self.materials.append(self.process_material())
            elif typ == V3dTypes.V3DTYPES_CENTERS:
                self.centers = self.process_centers()

        self._xdrfile.done()
        self.processed = True


def main():
    with io.open('out_bake.v3d', 'rb') as fil:
        v3d_obj = V3DReader(fil)
    v3d_obj.process()
    pass


if __name__ == '__main__':
    main()
