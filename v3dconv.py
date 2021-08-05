#!/usr/bin/env python3
import xdrlib
import io
from typing import Union, Tuple, Optional, List
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


class V3DReader:
    def __init__(self, fil: Union[io.FileIO, io.BytesIO]):
        self.objects = []
        self.materials = []

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

    def process_material(self) -> V3DMaterial:
        diffuse = self.unpack_rgba_float()
        emissive = self.unpack_rgba_float()
        specular = self.unpack_rgba_float()
        shininess, metallic, f0, _ = self.unpack_rgba_float()
        return V3DMaterial(diffuse, emissive, specular, shininess, metallic, f0)

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
            elif typ == V3dTypes.V3DTYPES_MATERIAL_:
                self.materials.append(self.process_material())

        self._xdrfile.done()
        self.processed = True


def process_triangles(xdr: xdrlib.Unpacker, objfile: io.FileIO, base_offset: int):
    nP = xdr.unpack_uint()
    positions = xdr.unpack_farray(3 * nP, lambda: xdr.unpack_double())

    for i in range(nP):
        x, y, z = positions[3 * i:3 * i + 3]
        objfile.write('v {0} {1} {2}\n'.format(x / 100, y / 100, z / 100))

    nN = xdr.unpack_uint()
    normals = xdr.unpack_farray(3 * nN, lambda: xdr.unpack_double())

    for i in range(nP):
        x, y, z = normals[3 * i:3 * i + 3]
        objfile.write('vn {0} {1} {2}\n'.format(x, y, z))

    nC = xdr.unpack_uint()
    colors = xdr.unpack_farray(4 * nC, lambda: xdr.unpack_double())

    numIdx = xdr.unpack_uint()
    for _ in range(numIdx):
        numTyp = xdr.unpack_uint()
        posIdx = xdr.unpack_farray(3, lambda: xdr.unpack_uint())
        norIdx = list(posIdx)
        colIdx = list(posIdx)

        if numTyp == 1:
            norIdx = xdr.unpack_farray(3, lambda: xdr.unpack_uint())
        elif numTyp == 2:
            colIdx = xdr.unpack_farray(3, lambda: xdr.unpack_uint())
        elif numTyp == 3:
            norIdx = xdr.unpack_farray(3, lambda: xdr.unpack_uint())
            colIdx = xdr.unpack_farray(3, lambda: xdr.unpack_uint())

        ix, iy, iz = posIdx
        inx, iny, inz = norIdx
        objfile.write('f {0}//{3} {1}//{4} {2}//{5}\n'.format(
            ix + base_offset + 1, iy + base_offset + 1, iz + base_offset + 1,
            inx + base_offset + 1, iny + base_offset + 1, inz + base_offset + 1))
        # print('posIdx=' + str(posIdx))
        # print('norIdx=' + str(norIdx))

    print('materialIndex={0}'.format(xdr.unpack_uint()))
    print('min={0}'.format(xdr.unpack_farray(3, lambda: xdr.unpack_double())))
    print('max={0}'.format(xdr.unpack_farray(3, lambda: xdr.unpack_double())))
    return nP


def main():
    with io.open('teapot.v3d', 'rb') as fil:
        v3d_obj = V3DReader(fil)
    v3d_obj.process()
    pass


if __name__ == '__main__':
    main()
