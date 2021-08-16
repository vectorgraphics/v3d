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

## V3D Header

A V3D Header is a special type of object.
The header starts with a `UINT` number indicating how many header entires are there, followed by that number of header entry.

Each header entry starts with a `UINT` Header key value, then a `UINT` length of the content in the number of 4-bytes blocks.
For example, a header with a single double-precision number would have the length as `2`.
The content of the header varies by the key.

A more detailed description of header keys and their values is available in the `asymptote` repository.


## V3D Objects

In this section, the specification of the content described does not include the type number, that is, it is assumed the type number is already processed and known.

### Material

V3D Materials are specified by metallic-roughness physical-based rendering format, though the roughness is specified by shininess, which is `1-roughness`, specified by

1. `RGBA` Base color of the material.
2. `RGBA` Emissive color of the material.
3. `RGBA` Specular color. While this number is not used in true PBR, this color is multiplied to the final reflectance (in case of nonmetals).
4. `FLOATx4` Parameters, in `[shininess, metallic, F0, X]` where X is unused. Here, F0 is "Fresnel-0" indicating how much a dielectric surface should reflect the incoming lights when viewed from a perfectly perpendicular angle to the surface (at 0 degrees), which defaults to `0.04`

All `FLOATx4` colors are stored in RGBA format between `0.0` and `1.0`.

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


### Straight Quad

1. `TRIPLEx4`: Corners of the specified rectangle
2. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`. If Index is zero, denotes there is no center point associated with this object.
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.

### Straight Triangle

Each [Bezier Triangle](https://en.wikipedia.org/wiki/B%C3%A9zier_surface]) contains

1. `TRIPLEx3`: Corner of the specified triangle
2. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`. If Index is zero, denotes there is no center point associated with this object.
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.

### Straight Quad (with vertex colors)

Each Bezier Patch with per-vertex color contains

1. `TRIPLEx4`: Corners of the specified rectangle
2. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`. If Index is zero, denotes there is no center point associated with this object.
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.
4. `RGBAx4`: The colors of each vertex, corresponding to the four corners of the Bezier patch.


### Straight Triangle (with vertex colors)

Each Bezier Triangle with per-vertex color contains

1. `TRIPLEx3`: Corner of the specified triangle
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

> 1. `UINTx3`: Index of the position. These three unsigned integers `i,j,k` correspond to the index of the positions array as `Positions[i]`, `Positions[j]` and `Positions[k]` forming the face of the triangle.
> 2. `BOOL` Whether or not normal indices is present. Call this `keepNI`
> 
> if `keepNI==true`, then the file contains `UINTx3` normal indices denoting the index of normals array such that the normal of each vertex corresponds to.
> Otherwise, the normal index is the same as the position index.
> 
> #### The following section only applies if `NC>0`:
> `BOOL` Whether or not color indices is present. Call this `keepCI`
> if `keepCI==true`, then the file contains `UINTx3` normal indices denoting the index of normals array such that the color of each vertex corresponds to.
> Otherwise, the color index is the same as the position index.

#### The following section applies to all triangle groups regardless of `NC` and appears only once after all indices have been processed

Then, the object contains `UINT` Center index and `UINT` Material Index like in the previous objects.

### Sphere

A Sphere is specified by

1. `TRIPLE`: Center of the sphere.
2. `REAL`: Radius of the sphere
3. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`. 
   If Index is zero, denotes there is no center point associated with this object.
4. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.


### Hemisphere

A Hemisphere is the half sphere specified by a base sphere and an angle in polar and azimuth angles
(FIXME: in radians?) specifying the normal vector of the plane which partitions the sphere, with
hemisphere being the side of the sphere normal vector faces.

1. `TRIPLE`: Center of the sphere.
2. `REAL`: Radius of the sphere
3. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`.
   If Index is zero, denotes there is no center point associated with this object.
4. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.
5. `REAL` Polar angle
6. `REAL` Azimuth angle

### Disks

A Disk is a planar filled circle specified by the center point, radius and angle of the surface normal specified by polar and azimuth angles, in the order of

1. `TRIPLE`: Center of the disk.
2. `REAL`: Radius of the disk
3. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`. 
   If Index is zero, denotes there is no center point associated with this object.
4. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.
5. `REAL` Polar angle
6. `REAL` Azimuth angle

### Cylinder

A Cylinder is specific by the center and radius of the bottom disk, alongside the height of the
cylinder indicating how long the cylinder is extruded from the base disk.

1. `TRIPLE`: Center of the disk.
2. `REAL`: Radius of the disk
3. `REAL`: Height of the cylinder
4. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`.
   If Index is zero, denotes there is no center point associated with this object.
5. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.
6. `REAL` Polar angle
7. `REAL` Azimuth angle.

### Tubes

A Tube is a deformed cylinder, without the end faces that follows a bezier curve as its center. It is specified by

1. `TRIPLEx4`: Four Bezier control points indicating the center "core" of the tube.
2. `REAL`: Width of the tube
3. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`.
   If Index is zero, denotes there is no center point associated with this object.
4. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.
5. `BOOL`: Whether or not the center curve should be drawn. This is called the "core" flag in Asymptote.

### Bezier Curve

A Bezier curve is a curve specified by four control points $p, c_0, c_1, q \in \mathbb{R}^3$, producing a curve (which here, is described as a function $C: [0,1] \to \mathbb{R}^3$) by

$$
C: [0,1] \to \mathbb{R}^3, \quad t \mapsto (1-t)^3p + 3t(1-t^2)c_0 + 3t^2(1-t)c_1 + t^3q.
$$

Here, the curve is specified by four points by

1. `TRIPLEx4` The control points p, c_0, c_1 and q respectively.
2. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`.
   If Index is zero, denotes there is no center point associated with this object.
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.

### Line

A line is specified by

1. `TRIPLEx2` The points p, q respectively where the line is specfied as the line from p to q.
2. `UINT`: Center index. This corresponds to the index of an array of center points if index is `> 0`.
   If Index is zero, denotes there is no center point associated with this object.
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.

### Pixel

A "Pixel" here is a single point in a 3D space and a width quantity to specify the drawing size.
In Asymptote, a "pixel" is drawn as a sphere with the radius as width.

1. `TRIPLE`: The point specifying the pixel
2. `REAL`: The drawing width of the pixel
3. `UINT`: Material index. This is the index of the material array `Material` where `Material[i]` is the material of this object.
