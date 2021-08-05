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


class V3DColorBezierPatch(V3DBezierPatch):
    def __init__(
            self, ctrl_points: TY_BEZIER_PATCH, colors: Tuple[TY_RGBA, TY_RGBA, TY_RGBA, TY_RGBA],
            material_id: int = None, center_index: int = None,
            min: TY_TRIPLE = None, max: TY_TRIPLE = None):
        super().__init__(ctrl_points, material_id, center_index, min, max)
        self.colors = colors


class V3DBezierPatch(AV3Dobject):
    def __init__(
            self, ctrl_points: TY_BEZIER_PATCH, material_id: int = None,
            center_index: int = None, min: TY_TRIPLE = None, max: TY_TRIPLE = None):
        super().__init__(material_id, center_index, min, max)
        self.control_pts = ctrl_points


def get_objtype(xdr: xdrlib.Unpacker) -> Union[None, int]:
    try:
        typ = xdr.unpack_uint()  # XDR does not support short
        return typ
    except EOFError:
        return None


def unpack_triple(xdr: xdrlib.Unpacker) -> TY_TRIPLE:
    x = xdr.unpack_double()
    y = xdr.unpack_double()
    z = xdr.unpack_double()
    return x, y, z


def unpack_rgba_float(xdr: xdrlib.Unpacker) -> TY_RGBA:
    r = xdr.unpack_float()
    g = xdr.unpack_float()
    b = xdr.unpack_float()
    a = xdr.unpack_float()
    return r, g, b, a


def unpack_triple_n(xdr: xdrlib.Unpacker, n: int = 1) -> List[TY_TRIPLE]:
    final_list = []
    for _ in range(n):
        final_list.append(unpack_triple(xdr))
    return final_list


def process_bezierpatch_no_color(xdr: xdrlib.Unpacker):
    base_ctlpts = unpack_triple_n(xdr, 16)

    center_id = xdr.unpack_uint()
    material_id = xdr.unpack_uint()

    min_val = unpack_triple(xdr)
    max_val = unpack_triple(xdr)

    assert len(base_ctlpts) == 16
    return V3DBezierPatch(tuple(base_ctlpts), material_id, center_id, min_val, max_val)


def process_bezierPatch(xdr: xdrlib.Unpacker):
    base_ctlpts = []
    for _ in range(16):
        base_ctlpts.append(unpack_triple(xdr))

    center_id = xdr.unpack_uint()
    material_id = xdr.unpack_uint()
    assert len(base_ctlpts) == 16
    return V3DBezierPatch(tuple(base_ctlpts), material_id, center_id)


def process_material(xdr: xdrlib.Unpacker):
    diffuse = unpack_rgba_float(xdr)
    emissive = unpack_rgba_float(xdr)
    specular = unpack_rgba_float(xdr)
    shininess, metallic, f0, _ = unpack_rgba_float(xdr)
    return V3DMaterial(diffuse, emissive, specular, shininess, metallic, f0)



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
    filename = 'teapot'
    obj_lists = []
    materials = []
    with io.open(filename + '.v3d', 'rb') as fil:
        unpkg = xdrlib.Unpacker(fil.read())

    print('ver: ' + str(unpkg.unpack_uint()))

    while typ := get_objtype(unpkg):
        if typ == V3dTypes.V3DTYPES_BEZIERPATCH:
            obj_lists.append(process_bezierpatch_no_color(unpkg))
        elif typ == V3dTypes.V3DTYPES_BEZIERPATCHCOLOR:
            process_bezierPatch(unpkg)
        elif typ == V3dTypes.V3DTYPES_MATERIAL_:
            materials.append(process_material(unpkg))

    pass


if __name__ == '__main__':
    main()
