# V3D Specifications

## Conventions

`TYPExN` means an object of type `TYPE` repeated `N` times, where `TYPE` can be:

1. `UINT`: Unsigned 32-bit integer;
2. `BOOL`: Unsigned 32-bit integer, denoting False if the value is `0` and True otherwise;
3. `REAL`: A double or single floating point value, depending on the double precision flag, as described in the next section;
4. `FLOAT`: A single precision 32-bit IEEE 754 Floating point value;
5. `TRIPLE`: An alias for `REALx3`;
6. `RGBA`: `An alias for FLOATx4`, where the elements respectively correspond to the red, green, blue, and alpha channels between `0.0` to `1.0`;
7. `WORD`: A 4-byte word.

## Basic information

V3D files are gzipped XDR Files. The uncompressed data stream of a V3D file must begin with the following entries, in order:

1. `UINT`: Version number, indicating the version of V3D;
2. `BOOL`: Double Precision flag. If this flag is set to True (False), all `TRIPLE` and `REAL` values are treated as double (single) precision IEEE 754 floating point values.

After that, a V3D File contains an arbitrary sequence of objects in the format:

1. `UINT`: Type number of the object;
2. Content of the object, depending on the type.

See [V3D types](https://raw.githubusercontent.com/vectorgraphics/asymptote/HEAD/v3dtypes.csv) for the list of V3D objects and their corresponding type numbers.

The `center index` is used for implementing billboard labels that always face the viewer. If the index is positive, it points into an array of center positions; if it is zero, there is no associated center point.

The `material index` points into an array `Material` of materials.

## V3D header

A V3D Header is a special type of object that starts with a `UINT` number indicating the number of header entries, followed by a sequence of header entries.

Each header entry consists of
1. `UINT` Header key;
2. `UINT` length of the content measured in units of 4-byte words. Call this length `n`. For example, `n=2` for a header with one double-precision number.
3. `WORDxn`. The header content of length `n` words of types dependent on the header key.

See [V3D header types](https://raw.githubusercontent.com/vectorgraphics/asymptote/HEAD/v3dheadertypes.csv) for the list of V3D headers and their corresponding keys.

A description of the headers is available at (https://raw.githubusercontent.com/vectorgraphics/asymptote/HEAD/webgl/gl.js)

## V3D objects

The content following the type number is described for each of the following types.

### Material

V3D materials are specified by their metallic-roughness physical-based rendering properties, where `shininess=1-roughness`:

1. `RGBA` Diffuse (base) color of the material.
2. `RGBA` Emissive color of the material.
3. `RGBA` Specular color (used to weight the reflectance of nonmetals).
4. `FLOATx3` Parameters `shininess, metallic, fresnel0`. Here, fresnel0 measures how much a dielectric surface reflects incoming light when viewed perpendicular to the surface.

### Bezier patch

Each [Bezier Patch](https://en.wikipedia.org/wiki/Bézier_surface) is a set of 16 control points $P_{i,j} \in \mathbb{R}^3$ where $i,j\in \{0,1,2,3\}$, producing a surface $\Phi$ parameterized by $u,v \in [0,1]$ as a function

$$
\Phi: [0,1]^2 \to \mathbb{R}^3, \quad (u,v) \mapsto \sum_{i=0}^3 B_i(u) \sum_{i=0}^3 B_j(v)P_{i,j}
$$

where $B_n(t)$ are the cubic Bernstein basis polynomials
$$
  B_0(t) = t^3, \; B_1(t)=3t^2(1-t), \; B_2(t)=3t(1-t)^2, \; B_3(t)=(1-t)^3.
$$

1. `TRIPLEx16`: Control points: the $n$th entry is mapped to $p_{i,j}$ by `i=n/4` and `j=n%4`;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Bezier triangle

Each [Bezier triangle](https://en.wikipedia.org/wiki/B%C3%A9zier_triangle) contains

1. `TRIPLEx10`: Control points;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Bezier patch (color)

Each Bezier Patch with per-vertex color contains

1. `TRIPLEx16`: Control points;
2. `UINT`: Center index;
3. `UINT`: Material index;
4. `RGBAx4`: The colors to use for the four vertices, bilinearly interpolated over the surface.

### Bezier triangle (color)

Each Bezier Triangle with per-vertex color contains

1. `TRIPLEx10`: Control points of Bezier triangles, where each corresponds to the 10 Bezier control points;
2. `UINT`: Center index;
3. `UINT`: Material index;
4. `RGBAx3`: The colors to use for the three vertices, bilinearly interpolated over the surface.

### Straight planar quad

1. `TRIPLEx4`: Vertices of the specified rectangle;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Straight triangle

Each triangle contains

1. `TRIPLEx3`: Corner of the specified triangle;
2. `UINT`: Center index;
3. `UINT`: Material index.

### Straight planar quad (with vertex colors)

Each Bezier Patch with per-vertex color contains

1. `TRIPLEx4`: Corners of the specified rectangle;
2. `UINT`: Center index;
3. `UINT`: Material index;
4. `RGBAx4`: The colors to use for the four vertices, bilinearly interpolated over the surface.

### Straight triangle (with vertex colors)

Each Bezier Triangle with per-vertex color contains

1. `TRIPLEx3`: Corner of the specified triangle;
2. `UINT`: Center index;
3. `UINT`: Material index;
4. `RGBAx3`: The colors to use for the three vertices, bilinearly interpolated over the surface.

### Triangle groups

This is a collection of triangles specified by a set of vertices, normals and indices constructing each triangle.
Note that the indices of the triangle group always start with `0`, which means programs that read in V3D Files
need to take note of the offset (number of position/normal entries) for formats that does not support segmentation of vertex entries, such as Wavefront `*.obj` file.
Moreover, in certain formats like `*.obj` where indices start with `1`, programs converting V3D to those formats need to add `1` to the output indices.

Each triangle group contains:

1. `UINT`: Number of indices. Denote this as`nI`;
2. `UINT`: Number of position vertex array entries. Denote this as `nP`;
3. `TRIPLExnP`: Vertex position array;
4. `UINT`: Number of vertex normal array entries. Denote this as `nN`;
5. `TRIPLExnN`: Vertex normal array;
6. `BOOL` Whether or not explict normal indices are present. Call this `explicitNI`;
7. `UINT`: Number of vertex color array entries. Denote this as `nC`.

> #### The next two entries only appear if `nC > 0`:
8. `RGBAxnC`: Vertex color array;
9. `BOOL` Whether or not explict color indices are present. Call this `explicitCI`.

Then, the triangle group contains `nI` entries of the form

> 1. `UINTx3`: Vertex position array indices specifying the position of each of the three vertices.
>
> #### The next entry only appears if `explicitNI=true`:
> #### Otherwise, the normal indices are assumed to be identical to the position indices;
> 2. `UINTx3`: Vertex normal array indices specifying the normal of each of the three vertices.
>
> #### The remainder of this section only applies if `nC > 0`:
> #### The next entry only appears if `explicitCI=true`:
> #### Otherwise, the color indices are assumed to be identical to the position indices;
> 3. `UINTx3`: Vertex color array indices specifying the color of each of the three vertices.

Like the previous objects, a triangle group ends with
8. `UINT` Center index
9. `UINT` Material index.

### Sphere

A Sphere is specified by

1. `TRIPLE`: Center of the sphere.
2. `REAL`: Radius of the sphere
3. `UINT`: Center index.
4. `UINT`: Material index.


### Hemisphere

A Hemisphere is the half sphere specified by a base sphere and an angle in polar and azimuth angles in radians specifying the normal vector of the plane which partitions the sphere, with hemisphere being the side of the sphere normal vector faces.

1. `TRIPLE`: Center of the sphere.
2. `REAL`: Radius of the sphere
3. `UINT`: Center index.
4. `UINT`: Material index.
5. `REAL` Polar angle
6. `REAL` Azimuth angle

### Disks

A Disk is a planar filled circle specified by the center point, radius and angle of the surface normal specified by polar and azimuth angles, in the order of

1. `TRIPLE`: Center of the disk.
2. `REAL`: Radius of the disk
3. `UINT`: Center index.
4. `UINT`: Material index.
5. `REAL` Polar angle
6. `REAL` Azimuth angle

### Cylinder

A Cylinder is specific by the center and radius of the bottom disk, alongside the height of the
cylinder indicating how long the cylinder is extruded from the base disk.

1. `TRIPLE`: Center of the disk.
2. `REAL`: Radius of the disk
3. `REAL`: Height of the cylinder
4. `UINT`: Center index.
5. `UINT`: Material index.
6. `REAL` Polar angle
7. `REAL` Azimuth angle.

### Tubes

A Tube is a deformed cylinder, without the end faces that follows a bezier curve as its center. It is specified by

1. `TRIPLEx4`: Four Bezier control points indicating the center "core" of the tube.
2. `REAL`: Width of the tube
3. `UINT`: Center index.
4. `UINT`: Material index.
5. `BOOL`: Whether or not the center curve should be drawn. This is called the "core" flag in Asymptote.

### Bezier curve

A Bezier curve is a curve specified by four control points $p, c_0, c_1, q \in \mathbb{R}^3$, producing a curve (which here, is described as a function $C: [0,1] \to \mathbb{R}^3$) by

$$
C: [0,1] \to \mathbb{R}^3, \quad t \mapsto (1-t)^3p + 3t(1-t^2)c_0 + 3t^2(1-t)c_1 + t^3q.
$$

Here, the curve is specified by four points by

1. `TRIPLEx4` The control points p, c_0, c_1 and q respectively.
2. `UINT`: Center index.
3. `UINT`: Material index.

### Line

A line is specified by

1. `TRIPLEx2` The points p, q respectively where the line is specfied as the line from p to q.
2. `UINT`: Center index.
3. `UINT`: Material index.

### Pixel

A `pixel` is a single point in 3D space drawn with a specified width measured in screen pixels.

1. `TRIPLE`: The position of the pixel;
2. `REAL`: The drawing width of the pixel;
3. `UINT`: Material index.
