# V3D Specifications

## Conventions

Here, for each object in V3D, we use the convention `TYPE` or `TYPExN` Object. `TYPExN` means Object of type `TYPE` repeated `N` times. If `N` is zero, then the entry `TYPEx0` does not appear in the file and can be ignored. `TYPE` can be:

1. `UINT`: Unsigned 32-bit integer;
2. `BOOL`: Unsigned 32-bit integer, which denotes False if value is `0`, and True otherwise;
3. `REAL`: Either double or single floating point number, depending on the double precision flag set as described in the subsequent section;
4. `FLOAT`: Single precision 32-bit IEEE 754 Floating point;
5. `TRIPLE`: Triple is `REALx3`;
6. `RGBA`: `FLOATx4`, where each element corresponds, in sequence to red, green, blue and alpha values between `0.0` to `1.0`.


## Basic Information

V3D Files are gzipped XDR Files. Here, "Data" means the uncompressed data stream of the v3d file.

All V3D File Data must start with the following in order:

1. `UINT` Version number, which indicates the version of V3D.
2. `BOOL` Double Precision flag. If this flag is set to true, all `TRIPLE` and `REAL` is treated as double precision IEEE 754 floating point, otherwise single precision.

Then, after that, V3D File contains an arbitrary number of objects in sequence in the format of

1. `UINT` Type Number, which depends on the object type
2. Content of the object, depending on the type.

V3D Types and their corresponding type numbers are available on the `asymptote` repo at <https://github.com/vectorgraphics/asymptote>

## V3D Objects

In this section, the specification of the content described does not include the type number, that is, it is assumed the type number is already processed and known.

### Bezier Patch

Each [Bezier Patch](https://en.wikipedia.org/wiki/B%C3%A9zier_surface]) contains

1. `TRIPLEx16`: Control points of Bezier patches, where each corresponds to the 16 Bezier control points.
2. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`. If Index is zero, denotes there is no center point associated with this object.
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.

### Bezier Triangle

Each [Bezier Triangle](https://en.wikipedia.org/wiki/B%C3%A9zier_surface]) contains

1. `TRIPLEx10`: Control points of Bezier triangles, where each corresponds to the 10 Bezier control points.
2. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`. If Index is zero, denotes there is no center point associated with this object.
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.

### Bezier Patch (Color)

Each Bezier Patch with per-vertex color contains

1. `TRIPLEx16`: Control points of Bezier patches, where each corresponds to the 16 Bezier control points.
2. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`. If Index is zero, denotes there is no center point associated with this object.
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.
4. `RGBAx4`: The colors of each vertex, corresponding to the four corners of the Bezier patch.


### Bezier Triangle (Color)

Each Bezier Triangle with per-vertex color contains

1. `TRIPLEx10`: Control points of Bezier triangles, where each corresponds to the 10 Bezier control points.
2. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`. If Index is zero, denotes there is no center point associated with this object.
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.
4. `RGBAx3`: The colors of each vertex, corresponding to the four corners of the Bezier triangle.

### Triangle groups

This is a collection of triangles specified by a set of vertices, normals and indices constructing each triangle.
Note that the indices of the triangle group always start with `0`, which means programs that read in V3D Files
need to take note of the offset (number of position/normal entries) for formats that does not support segmentation of vertex entries, such as Wavefront `*.obj` file.
Moreover, in certain formats like `*.obj`, indices start with `1` which means programs converting V3D to those formats need to add `1` to all indices written.

Each triangle group contains:

1. `UINT`: Number of position vertex entries. Denote this as `NP`.
2. `TRIPLExNP`: The entries of vertex positions. Denote this array `Triple Positions[NP]`
3. `UINT`: Number of vertex normal entries. Denote this as `NN`.
4. `TRIPLExNN`: The entries of vertex normals.
5. `UINT`: Number of vertex color entries. Denote this as `NC`.
6. `RGBAxNC`: The entries of vertex colors.
7. `UINT`: Number of indices. Denote this number `NI`.

Then, the triangle group contains `NI` number of the following:

1. `UINT`: Type of indices expected.
2. `UINTx3`: Index of the position. These three unsigned integers `i,j,k` correspond to the index of the positions array as `Positions[i]`, `Positions[j]` and `Positions[k]` forming the face of the triangle.

Then, if the index type is `1` or `3`, there is a `UINTx3` normal index denoting the index of normals array such that the normal of each vertex corresponds to. Otherwise, if the index type is `0` or `2`, then the normal index is the same as the position index.

Likewise, if the index type is `2` or `3`, there is a `UINTx3` normal index denoting the index of colors array such that the color of each vertex corresponds to. Otherwise, if the index type is `0` or `1`, then the color index is the same as the position index.

Note that if `NC==0`, then the index type is always `0` or `1`.

Then, the object contains `UINT` Material Index like in the previous objects.
