# V3D File Format Specification and Reference Toolset: Version 1

This repository contains the specification for the V3D file format, a compact 3D graphics file format for Bezier curves, Bezier patches, Bezier triangles, and triangle groups, all with optional vertex-dependent colors.

A reference Python module `pyv3d` for reading in V3D is included in the `module`directory, along with an example of its usage in the `example`directory.

To build and install `pyv3d`:

```
pip3 install build
cd module
python3 -m build
pip3 install --user dist/pyv3d-1.0-py3-none-any.whl
```

## Authors
The authors of the V3D file format are John C. Bowman <bowman@ualberta.ca> and
Supakorn "Jamie" Rassameemasmuang <jamievlin@outlook.com>

# V3D Specification

## Conventions

`TYPExN` means an object of type `TYPE` repeated `N` times, where `TYPE` can be:

1. `UINT`: Unsigned 32-bit integer;
2. `BOOL`: Unsigned 32-bit integer, denoting False if the value is `0` and True otherwise;
3. `REAL`: A double or single floating point value, depending on the double precision flag, as described in the next section;
4. `FLOAT`: A single precision 32-bit IEEE 754 Floating point value;
5. `PAIR`: An alias for `REALx2`;
6. `TRIPLE`: An alias for `REALx3`;
7. `RGB`: `An alias for FLOATx3`, where the elements respectively correspond to red, green, and blue channels between `0.0` to `1.0`;
8. `RGBA`: `An alias for FLOATx4`, where the elements respectively correspond to red, green, blue, and alpha channels between `0.0` to `1.0`;
9. `WORD`: A 4-byte word.

## Basic information

V3D files are gzipped [XDR](https://en.wikipedia.org/wiki/External_Data_Representation) files. The uncompressed data stream of a V3D file must begin with the following entries, in order:

1. `UINT`: V3D version number;
2. `BOOL`: Double precision flag. If this flag is set to True (False), all `TRIPLE` and `REAL` values are treated as double (single) precision IEEE 754 floating point values.

After that, a V3D File contains an arbitrary sequence of objects in the format:

1. `UINT`: Type number of the object;
2. Content of the object, depending on the type.

See [V3D types](https://raw.githubusercontent.com/vectorgraphics/asymptote/HEAD/v3dtypes.csv) for the list of V3D objects and their corresponding type numbers.

The `center index` is used for implementing billboard labels that always face the viewer. If the index is positive, it points into an array of center positions; if it is zero, there is no associated center position and the labels are embedded into the 3D scene.

The `material index` points into an array `Material` of materials.

## V3D header

A V3D Header is a special type of object that starts with a `UINT` number indicating the number of header entries, followed by a sequence of header entries.

Each header entry consists of
1. `UINT`: Header key;
2. `UINT`: Length `n` of the content measured in units of 4-byte words. For example, `n=2` for a header containing one double-precision number;
3. `WORDxn`: The header content of length `n` words of types that depend on the header key.

See [V3D header types](https://raw.githubusercontent.com/vectorgraphics/asymptote/HEAD/v3dheadertypes.csv) for the list of V3D headers and their corresponding keys.

## V3D objects

The content following the type number is described for each of the following types.

### Centers

Each center position is a point in 3D space about which a billboard surface should rotate so as to always face the camera.

1. `UINT`: Number `n` of center positions;
2. `TRIPLExn`: Center positions.

### Material

V3D materials are specified by their metallic-roughness physical-based rendering properties, where `shininess=1-roughness`:

1. `RGBA`: Diffuse (base) color of the material;
2. `RGBA`: Emissive color of the material;
3. `RGBA`: Specular color (used to weight the reflectance of nonmetals);
4. `FLOATx3`: Parameters `shininess, metallic, fresnel0`. Here, `fresnel0` measures how much a dielectric surface reflects incoming light when viewed perpendicular to the surface.

### Bezier patch

Each [Bezier patch](https://en.wikipedia.org/wiki/Bézier_surface) contains a set of 16 control points $P_{i,j} \in \mathbb{R}^3$, where $i,j\in \{0,1,2,3\}$, producing a surface $\Phi$ parametrized by $u,v \in [0,1]$:

$$
\Phi: [0,1]^2 \to \mathbb{R}^3, \quad (u,v) \mapsto \sum_{i=0}^3 B_i(u) \sum_{j=0}^3 B_j(v)P_{i,j},
$$

where $B_i(t)$ are the cubic Bernstein basis polynomials
$B_0(t) = t^3$, $B_1(t)=3t^2(1-t)$, $B_2(t)=3t(1-t)^2$, and $B_3(t)=(1-t)^3$.

1. `TRIPLEx16`: Control points $p_{i,j}$ stored in entry $4i+j$;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Bezier triangle

Each [Bezier triangle](https://en.wikipedia.org/wiki/B%C3%A9zier_triangle) contains

1. `TRIPLEx10`: Control points $p_{i,j,3-i-j}$ stored in entry $(i+j)(i+j+1)/2+j$;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Bezier patch (per-vertex color)

Each Bezier patch with per-vertex color contains

1. `TRIPLEx16`: Control points;
2. `UINT`: Center index;
3. `UINT`: Material index;
4. `RGBAx4`: The colors assigned to the four vertices, bilinearly interpolated over the surface.

### Bezier triangle (per-vertex color)

Each Bezier triangle with per-vertex color contains

1. `TRIPLEx10`: Control points;
2. `UINT`: Center index;
3. `UINT`: Material index;
4. `RGBAx3`: The colors assigned to the three vertices, bilinearly interpolated over the surface.

### Straight planar quad

Each rectangle contains

1. `TRIPLEx4`: Vertices;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Straight triangle

Each triangle contains

1. `TRIPLEx3`: Vertices;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Straight planar quad (per-vertex color)

Each rectangle with per-vertex color contains

1. `TRIPLEx4`: Vertices;
2. `UINT`: Center index;
3. `UINT`: Material index;
4. `RGBAx4`: The colors assigned to the four vertices, bilinearly interpolated over the surface.

### Straight triangle (per-vertex color)

Each triangle with per-vertex color contains

1. `TRIPLEx3`: Vertices of the specified triangle;
2. `UINT`: Center index;
3. `UINT`: Material index;
4. `RGBAx3`: The colors assigned to the three vertices, bilinearly interpolated over the surface.

### Triangle group

A triangle group is a collection of triangles specified by arrays of positions, normals, and index triplets identifying the entries in the position and normal arrays assigned to the three vertices of each triangle in the group.

The indices of every triangle group begins with `0`, which means programs that read in V3D Files need to take note of the offset (number of position/normal entries) for formats that does not support segmentation of vertex entries, such as Wavefront `*.obj` file. Moreover, in certain formats like `*.obj` where indices start with `1`, programs converting V3D to those formats need to add `1` to the output indices.

Each triangle group contains:

1. `UINT`: Number of indices. Denote this as `nI`;
2. `UINT`: Number of position vertex array entries. Denote this as `nP`;
3. `TRIPLExnP`: Vertex position array;
4. `UINT`: Number of vertex normal array entries. Denote this as `nN`;
5. `TRIPLExnN`: Vertex normal array;
6. `BOOL` Whether or not explicit normal indices are present. Call this `explicitNI`;
7. `UINT`: Number of vertex color array entries. Denote this as `nC`.

> ##### The next two entries only appear if `nC > 0`:
8. `RGBAxnC`: Vertex color array;
9. `BOOL` Whether or not explicit color indices are present. Call this `explicitCI`.

Then, the triangle group contains `nI` entries of the form:

> 1. `UINTx3`: Vertex position array indices specifying the position of each of the three vertices.
>
> ##### The next entry only appears if `explicitNI=true` (if `explicitNI=false`, the normal indices are assumed to be identical to the position indices):
> 2. `UINTx3`: Vertex normal array index triplets specifying the normal of each of the three vertices.
>
> ##### The next entry only appears if `nC > 0` and `explicitCI=true` (if `explicitCI=false`, the color indices are assumed to be identical to the position indices):
> 3. `UINTx3`: Vertex color array index triplets specifying the color of each of the three vertices.

Like the previous objects, a triangle group ends with

8. `UINT`: Center index;
9. `UINT`: Material index.

### Sphere

A sphere is specified by:

1. `TRIPLE`: Center of the sphere;
2. `REAL`: Radius of the sphere;
3. `UINT`: Center index;
4. `UINT`: Material index.


### Hemisphere

A hemisphere is the half sphere specified by a base sphere and (polar, azimuthal) direction in radians specifying the normal vector of the plane that partitions the sphere, with the hemisphere chosen on the same side as the normal vector:

1. `TRIPLE`: Center of the sphere;
2. `REAL`: Radius of the sphere;
3. `UINT`: Center index;
4. `UINT`: Material index;
5. `REAL`: Polar angle;
6. `REAL`: Azimuthal angle.

### Disk

A disk is a planar filled circle specified by the center point, radius, and (polar, azimuthal) direction in radians of the surface normal:

1. `TRIPLE`: Center of the disk;
2. `REAL`: Radius of the disk;
3. `UINT`: Center index;
4. `UINT`: Material index;
5. `REAL`: Polar angle;
6. `REAL`: Azimuthal angle.

### Cylinder

A cylinder is specified by the center and radius of a bottom disk, with normal vector aligned in the (polar, azimuthal) direction in radians, and the extrusion height of the cylinder along the normal vector to the disk:

1. `TRIPLE`: Center of the disk;
2. `REAL`: Radius of the disk;
3. `REAL`: Height of the cylinder;
4. `UINT`: Center index;
5. `UINT`: Material index;
6. `REAL` Polar angle;
7. `REAL` Azimuthal angle.

### Tube

A tube is a deformed cylinder, without end faces, whose center line follows a Bezier curve:

1. `TRIPLEx4`: Four control points specifying the Bezier curve that forms the central "core" of the tube;
2. `REAL`: Width of the tube;
3. `UINT`: Center index;
4. `UINT`: Material index;
5. `BOOL`: Whether or not the center curve should be drawn. This is called the "core" flag in Asymptote.

### Bezier curve

A Bezier curve is specified by four control points $z_0, c_0, c_1, z_1 \in \mathbb{R}^3$ that generate a curve $C$ on $[0,1]$:

$$
C: [0,1] \to \mathbb{R}^3, \quad t \mapsto (1-t)^3z_0 + 3t(1-t^2)c_0 + 3t^2(1-t)c_1 + t^3z_1.
$$

A Bezier curve is specified by:

1. `TRIPLEx4` The control points $z_0, c_0, c_1, z_1$;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Line segment

A line segment is specified by:

1. `TRIPLEx2` The endpoints $z_0, z_1$;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Pixel

A `pixel` is a single point in 3D space drawn with a specified width measured in screen pixels:

1. `TRIPLE`: The position of the pixel;
2. `REAL`: The width of the pixel;
3. `UINT`: Material index.

# License
This specification is released under Version 2.0 of the Apache License, see the LICENSE file for details.
