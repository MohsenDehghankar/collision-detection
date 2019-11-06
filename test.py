def line_intersect2(v1, v2, v3, v4):
    d = (v4[1] - v3[1]) * (v2[0] - v1[0]) - (v4[0] - v3[0]) * (v2[1] - v1[1])
    u = (v4[0] - v3[0]) * (v1[1] - v3[1]) - (v4[1] - v3[1]) * (v1[0] - v3[0])
    v = (v2[0] - v1[0]) * (v1[1] - v3[1]) - (v2[1] - v1[1]) * (v1[0] - v3[0])
    if d < 0:
        u, v, d = -u, -v, -d
    return (0 <= u <= d) and (0 <= v <= d)


def point_in_triangle2(A, B, C, P):
    v0 = [C[0] - A[0], C[1] - A[1]]
    v1 = [B[0] - A[0], B[1] - A[1]]
    v2 = [P[0] - A[0], P[1] - A[1]]
    cross = lambda u, v: u[0] * v[1] - u[1] * v[0]
    u = cross(v2, v0)
    v = cross(v1, v2)
    d = cross(v1, v0)
    if d < 0:
        u, v, d = -u, -v, -d
    return u >= 0 and v >= 0 and (u + v) <= d


def tri_intersect2(t1, t2):
    if line_intersect2(t1[0], t1[1], t2[0], t2[1]): return True
    if line_intersect2(t1[0], t1[1], t2[0], t2[2]): return True
    if line_intersect2(t1[0], t1[1], t2[1], t2[2]): return True
    if line_intersect2(t1[0], t1[2], t2[0], t2[1]): return True
    if line_intersect2(t1[0], t1[2], t2[0], t2[2]): return True
    if line_intersect2(t1[0], t1[2], t2[1], t2[2]): return True
    if line_intersect2(t1[1], t1[2], t2[0], t2[1]): return True
    if line_intersect2(t1[1], t1[2], t2[0], t2[2]): return True
    if line_intersect2(t1[1], t1[2], t2[1], t2[2]): return True
    inTri = True
    inTri = inTri and point_in_triangle2(t1[0], t1[1], t1[2], t2[0])
    inTri = inTri and point_in_triangle2(t1[0], t1[1], t1[2], t2[1])
    inTri = inTri and point_in_triangle2(t1[0], t1[1], t1[2], t2[2])
    if inTri == True: return True
    inTri = True
    inTri = inTri and point_in_triangle2(t2[0], t2[1], t2[2], t1[0])
    inTri = inTri and point_in_triangle2(t2[0], t2[1], t2[2], t1[1])
    inTri = inTri and point_in_triangle2(t2[0], t2[1], t2[2], t1[2])
    if inTri == True: return True
    return False


if __name__ == '__main__':
    t1 = [[1, 1], [2, 1], [2, 2]]
    t2 = [[3, 1], [1, 3], [3, 3]]
    print(tri_intersect2(t1, t2))
