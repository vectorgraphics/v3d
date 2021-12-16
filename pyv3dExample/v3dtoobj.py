#!/usr/bin/env python3

from pyv3d import V3DReader
from pyv3d.v3dobjects import V3DTriangleGroups
import gzip


class V3DToObjWriter(V3DReader):
    def __init__(self, fil: gzip.GzipFile):
        super().__init__(fil)

    @classmethod
    def from_file_name(cls, file_name: str):
        with gzip.open(file_name, 'rb') as fil:
            reader_obj = cls(fil)
        return reader_obj

    def write_obj(self, out_name: str, scale=1.0):
        if not self.processed:
            self.process()
        with open(out_name, 'w') as fil:
            base_position_offset = 0
            base_normal_offset = 0
            fil.write('\n')
            k = 0
            for object in self.objects:
                if not isinstance(object, V3DTriangleGroups):
                    break
                fil.write('g triangles_{0}\n'.format(k))
                for x,y,z in object.positions:
                    fil.write('v {0} {1} {2}\n'.format(
                        x*scale, y*scale, z*scale))
                for normal in object.normals:
                    fil.write('vn {0} {1} {2}\n'.format(*normal))

                for i in range(len(object.position_indices)):
                    px, py, pz = object.position_indices[i]
                    nx, ny, nz = object.normals_indices[i]
                    fil.write('f {0}//{3} {1}//{4} {2}//{5}\n'.format(
                        px + base_position_offset+1, py+base_position_offset+1,
                        pz + base_position_offset + 1,
                        nx + base_normal_offset+1, ny+base_normal_offset +
                        1, nz + base_normal_offset + 1
                    ))

                base_position_offset += len(object.positions)
                base_normal_offset += len(object.normals)
                k += 1


def main():
    # produce v3d file with
    # asy -fv3d -prerender 2 -c "import teapot;" -o teapot
    reader = V3DToObjWriter.from_file_name('teapot.v3d')
    reader.write_obj('teapot.obj', 0.01)


if __name__ == '__main__':
    main()
