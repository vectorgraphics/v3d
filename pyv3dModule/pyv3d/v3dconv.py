#!/usr/bin/env python3

import xdrlib, gzip
from typing import Callable
from .v3dtypes import v3dtypes
from .v3dheadertypes import v3dheadertypes
from .v3dobjects import *


class V3DReader:
    def __init__(self, fil: gzip.GzipFile):
        self._objects: List[AV3Dobject] = []
        self._materials: List[V3DMaterial] = []
        self._centers: List[TY_TRIPLE] = []
        self._header: V3DHeaderInformation = V3DHeaderInformation()

        self._file_ver: Optional[int] = None
        self._processed: bool = False

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
            v3dtypes.v3dtypes_pixel: self.process_pixel,
            v3dtypes.v3dtypes_triangles: self.process_triangles
        }

        self._xdrfile = xdrlib.Unpacker(fil.read())
        self.unpack_double: Callable[[], float] = self._xdrfile.unpack_double
        self._allow_double_precision: bool = True

    @classmethod
    def from_file_name(cls, file_name: str):
        with gzip.open(file_name, 'rb') as fil:
            reader_obj = cls(fil)
        return reader_obj

    @property
    def processed(self) -> bool:
        return self._processed

    @property
    def header(self) -> V3DHeaderInformation:
        self.process()
        return self._header

    @property
    def objects(self) -> List[AV3Dobject]:
        self.process()
        return self._objects

    @property
    def materials(self) -> List[V3DMaterial]:
        self.process()
        return self._materials

    @property
    def centers(self) -> List[TY_TRIPLE]:
        self.process()
        return self._centers

    @property
    def file_version(self) -> Optional[bool]:
        self.process()
        return self._file_ver

    @property
    def allow_double_precision(self) -> Optional[float]:
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

    def unpack_pair(self) -> TY_PAIR:
        x = self.unpack_double()
        y = self.unpack_double()
        return x, y

    def unpack_rgb_float(self) -> TY_RGB:
        r = self._xdrfile.unpack_float()
        g = self._xdrfile.unpack_float()
        b = self._xdrfile.unpack_float()
        return r, g, b

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

    def process_header(self) -> V3DHeaderInformation:
        header = V3DHeaderInformation()
        num_headers = self._xdrfile.unpack_uint()
        for _ in range(num_headers):
            header_type = self._xdrfile.unpack_uint()
            block_count = self._xdrfile.unpack_uint()

            if header_type == v3dheadertypes.v3dheadertypes_canvasWidth:
                header.canvasWidth = self._xdrfile.unpack_uint()
            elif header_type == v3dheadertypes.v3dheadertypes_canvasHeight:
                header.canvasHeight = self._xdrfile.unpack_uint()
            elif header_type == v3dheadertypes.v3dheadertypes_minBound:
                header.minBound = self.unpack_triple()
            elif header_type == v3dheadertypes.v3dheadertypes_maxBound:
                header.maxBound = self.unpack_triple()
            elif header_type == v3dheadertypes.v3dheadertypes_orthographic:
                header.orthographic = self.unpack_bool()
            elif header_type == v3dheadertypes.v3dheadertypes_angleOfView:
                header.angleOfView = self.unpack_double()
            elif header_type == v3dheadertypes.v3dheadertypes_initialZoom:
                header.initialZoom = self.unpack_double()
            elif header_type == v3dheadertypes.v3dheadertypes_viewportShift:
                header.viewportShift = self.unpack_pair()
            elif header_type == v3dheadertypes.v3dheadertypes_viewportMargin:
                header.viewportMargin = self.unpack_pair()
            elif header_type == v3dheadertypes.v3dheadertypes_light:
                position = self.unpack_triple()
                color = self.unpack_rgb_float()
                header.lights.append(V3DSingleLightSource(position, color))
            elif header_type == v3dheadertypes.v3dheadertypes_background:
                header.background = self.unpack_rgba_float()
            elif header_type == v3dheadertypes.v3dheadertypes_absolute:
                # Configuration from now on
                header.configuration.absolute = self.unpack_bool()
            elif header_type == v3dheadertypes.v3dheadertypes_zoomFactor:
                header.configuration.zoomFactor = self.unpack_double()
            elif header_type == v3dheadertypes.v3dheadertypes_zoomPinchFactor:
                header.configuration.zoomPinch_factor = self.unpack_double()
            elif header_type == v3dheadertypes.v3dheadertypes_zoomStep:
                header.configuration.zoomStep = self.unpack_double()
            elif header_type == v3dheadertypes.v3dheadertypes_shiftHoldDistance:
                header.configuration.shiftHoldDistance = self.unpack_double()
            elif header_type == v3dheadertypes.v3dheadertypes_shiftWaitTime:
                header.configuration.shiftWaitTime = self.unpack_double()
            elif header_type == v3dheadertypes.v3dheadertypes_vibrateTime:
                header.configuration.vibrateTime = self.unpack_double()
            else:
                for _ in range(block_count):
                    self._xdrfile.unpack_uint()
        return header

    def process_bezierpatch(self) -> V3DBezierPatch:
        base_ctlpts = self.unpack_triple_n(16)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        assert len(base_ctlpts) == 16
        return V3DBezierPatch(tuple(base_ctlpts), material_id, center_id)

    def process_bezierpatch_color(self) -> V3DBezierPatchColor:
        base_ctlpts = self.unpack_triple_n(16)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        colors = self.unpack_rgba_float_n(4)

        assert len(base_ctlpts) == 16
        return V3DBezierPatchColor(tuple(base_ctlpts), tuple(colors), material_id, center_id)

    def process_beziertriangle(self) -> V3DBezierTriangle:
        base_ctlpts = self.unpack_triple_n(10)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        assert len(base_ctlpts) == 10
        return V3DBezierTriangle(tuple(base_ctlpts), material_id, center_id)

    def process_beziertriangle_color(self) -> V3DBezierTriangleColor:
        base_ctlpts = self.unpack_triple_n(10)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        colors = self.unpack_rgba_float_n(3)

        assert len(base_ctlpts) == 10
        return V3DBezierTriangleColor(tuple(base_ctlpts), tuple(colors), material_id, center_id)

    def process_straight_bezierpatch(self) -> V3DStraightBezierPatch:
        base_ctlpts = self.unpack_triple_n(4)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        assert len(base_ctlpts) == 4
        return V3DStraightBezierPatch(tuple(base_ctlpts), material_id, center_id)

    def process_straight_bezierpatch_color(self) -> V3DStraightBezierPatchColor:
        base_ctlpts = self.unpack_triple_n(4)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        colors = self.unpack_rgba_float_n(4)

        assert len(base_ctlpts) == 4
        return V3DStraightBezierPatchColor(tuple(base_ctlpts), tuple(colors), material_id, center_id)

    def process_straight_beziertriangle(self) -> V3DStraightBezierTriangle:
        base_ctlpts = self.unpack_triple_n(3)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        assert len(base_ctlpts) == 3
        return V3DStraightBezierTriangle(tuple(base_ctlpts), material_id, center_id)

    def process_straight_beziertriangle_color(self) -> V3DStraightBezierTriangleColor:
        base_ctlpts = self.unpack_triple_n(3)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        colors = self.unpack_rgba_float_n(3)

        assert len(base_ctlpts) == 3
        return V3DStraightBezierTriangleColor(tuple(base_ctlpts), tuple(colors), material_id, center_id)

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

        core_base = self.unpack_bool()

        return V3DTube(points[0], points[1], points[2], points[3], width, core_base, material_id, center_id)

    def process_curve(self) -> V3DCurve:
        points = self.unpack_triple_n(4)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        return V3DCurve(points[0], points[1], points[2], points[3], material_id, center_id)

    def process_line(self) -> V3DLine:
        points = self.unpack_triple_n(2)

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        return V3DLine(points[0], points[1], material_id, center_id)

    def process_pixel(self) -> V3DPixel:
        point = self.unpack_triple()
        width = self.unpack_double()

        material_id = self._xdrfile.unpack_uint()

        return V3DPixel(point, width, material_id, None)

    def process_material(self) -> V3DMaterial:
        diffuse = self.unpack_rgba_float()
        emissive = self.unpack_rgba_float()
        specular = self.unpack_rgba_float()
        shininess, metallic, f0 = self.unpack_rgb_float()
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

        num_idx = self._xdrfile.unpack_uint()

        num_pos = self._xdrfile.unpack_uint()
        positions = self.unpack_triple_n(num_pos)

        num_normal = self._xdrfile.unpack_uint()
        normals = self.unpack_triple_n(num_normal)

        explicitNI = self.unpack_bool()

        num_color = self._xdrfile.unpack_uint()

        if num_color > 0:
            is_color = True
            colors = self.unpack_rgba_float_n(num_color)
            explicitCi = self.unpack_bool()

        pos_indices = []
        normal_indices = []
        color_indices = None

        if is_color:
            color_indices = []

        for _ in range(num_idx):
            pos_idx = self._unpack_int_indices()
            nor_idx = self._unpack_int_indices() if explicitNI else list(pos_idx)

            col_idx = None
            if is_color:
                col_idx = self._unpack_int_indices() if explicitCi else list(pos_idx)

            pos_indices.append(tuple(pos_idx))
            normal_indices.append(tuple(nor_idx))
            if is_color:
                color_indices.append(tuple(col_idx))

        center_id = self._xdrfile.unpack_uint()
        material_id = self._xdrfile.unpack_uint()

        if is_color:
            return V3DTriangleGroupsColor(positions, normals, colors, pos_indices, normal_indices, color_indices,
                                          material_id, center_id)
        else:
            return V3DTriangleGroups(positions, normals, pos_indices, normal_indices, material_id, center_id)

    def get_fn_process_type(self, typ: int) -> Optional[Callable[[], AV3Dobject]]:
        return self._object_process_fns.get(typ, None)

    def process(self, force: bool = False):
        if self._processed and not force:
            return

        if self._processed and force:
            self._xdrfile.set_position(0)

        self._processed = True
        self._file_ver = self._xdrfile.unpack_uint()

        self._allow_double_precision = self.unpack_bool()
        if not self._allow_double_precision:
            self.unpack_double = self._xdrfile.unpack_float

        while typ := self.get_obj_type():
            if typ == v3dtypes.v3dtypes_material:
                self._materials.append(self.process_material())
            elif typ == v3dtypes.v3dtypes_centers:
                self._centers = self.process_centers()
            elif typ == v3dtypes.v3dtypes_header:
                self._header = self.process_header()
            else:
                fn = self.get_fn_process_type(typ)
                if fn is not None:
                    obj = fn()
                    self._objects.append(obj)
                else:
                    raise RuntimeError('Unknown Object type. Received type {0}'.format(typ))

        self._xdrfile.done()


def main():
    # asy -fv3d 2 -c "import teapot;" -o teapot
    v3d_obj = V3DReader.from_file_name('teapot.v3d')
    print(v3d_obj.objects)
    pass


if __name__ == '__main__':
    main()
