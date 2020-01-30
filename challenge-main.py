class TriangleNode:
    def __init__(self, left, right, bv):
        self.right = right
        self.left = left
        self.bv = bv

    def __str__(self):
        return self.bv.__str__()


class BV:
    # 8-DOPS
    def __init__(self, Amin, Amax, Bmin, Bmax, Cmin, Cmax, Dmin, Dmax):
        self.Amin = Amin
        self.Bmin = Bmin
        self.Cmin = Cmin
        self.Dmin = Dmin
        self.Amax = Amax
        self.Bmax = Bmax
        self.Cmax = Cmax
        self.Dmax = Dmax

    def __str__(self):
        return str(self.Amax) + " " + str(self.Amin) + " " + str(self.Bmax) + " " + str(self.Bmin) + " " + str(
            self.Cmax) + " " + str(
            self.Cmin) + " " + str(self.Dmax) + " " + str(self.Dmin)

    @staticmethod
    def get_max_min(a_list):
        min = a_list[0]
        max = a_list[0]
        a_list = a_list[1:]
        for element in a_list:
            if element > max:
                max = element
            if element < min:
                min = element
        return min, max

    @staticmethod
    def create_bv(left_child, right_child):
        if isinstance(left_child, Triangle) and isinstance(right_child, Triangle):
            Amin, Amax = BV.get_max_min(
                [left_child.y1, left_child.y2, left_child.y3, right_child.y1, right_child.y2, right_child.y3])
            Bmin, Bmax = BV.get_max_min(
                [left_child.x1, left_child.x2, left_child.x3, right_child.x1, right_child.x2, right_child.x3])
            Cmin, Cmax = BV.get_max_min([(left_child.y1 - left_child.x1), (left_child.y2 - left_child.x2),
                                         (left_child.y3 - left_child.x3),
                                         (right_child.y1 - right_child.x1), (right_child.y2 - right_child.x2),
                                         (right_child.y3 - right_child.x3)])
            Dmin, Dmax = BV.get_max_min([(left_child.y1 + left_child.x1), (left_child.y2 + left_child.x2),
                                         (left_child.y3 + left_child.x3),
                                         (right_child.y1 + right_child.x1), (right_child.y2 + right_child.x2),
                                         (right_child.y3 + right_child.x3)])
            return BV(Amin, Amax, Bmin, Bmax, Cmin, Cmax, Dmin, Dmax)
        elif isinstance(left_child, Triangle):
            tri = left_child
            bv = right_child
            return BV.create_bv_tri_bv(tri, bv)
        elif isinstance(right_child, Triangle):
            tri = right_child
            bv = left_child
            return BV.create_bv_tri_bv(tri, bv)
        else:
            return BV(Amax=max(left_child.Amax, right_child.Amax),
                      Amin=min(left_child.Amin, right_child.Amin),
                      Bmin=min(left_child.Bmin, right_child.Bmin),
                      Bmax=max(left_child.Bmax, right_child.Bmax),
                      Cmax=max(left_child.Cmax, right_child.Cmax),
                      Cmin=min(left_child.Cmin, right_child.Cmin),
                      Dmin=min(left_child.Dmin, right_child.Dmin),
                      Dmax=max(left_child.Dmax, right_child.Dmax))

    @staticmethod
    def create_bv_tri_bv(tri, bv):
        Amax = max(tri.y1, tri.y2, tri.y3, bv.Amax)
        Amin = min(tri.y1, tri.y2, tri.y3, bv.Amin)
        Bmax = max(tri.x1, tri.x2, tri.x3, bv.Bmax)
        Bmin = min(tri.x1, tri.x2, tri.x3, bv.Bmin)
        Cmax = max((tri.y1 - tri.x1), (tri.y2 - tri.x2),
                   (tri.y3 - tri.x3), bv.Cmax)
        Cmin = min((tri.y1 - tri.x1), (tri.y2 - tri.x2),
                   (tri.y3 - tri.x3), bv.Cmin)
        Dmax = max((tri.y1 + tri.x1), (tri.y2 + tri.x2),
                   (tri.y3 + tri.x3), bv.Dmax)
        Dmin = min((tri.y1 + tri.x1), (tri.y2 + tri.x2),
                   (tri.y3 + tri.x3), bv.Dmin)
        return BV(Amin, Amax, Bmin, Bmax, Cmin, Cmax, Dmin, Dmax)

    @staticmethod
    def overlap_interval(first_min, first_max, second_min, second_max):
        if second_min <= first_min <= second_max:
            return True
        if second_min <= first_max <= second_max:
            return True
        if first_min <= second_min and first_max >= second_max:
            return True
        return False

    @staticmethod
    def collide(first_bv, second_bv):
        if BV.overlap_interval(first_bv.Amin, first_bv.Amax, second_bv.Amin, second_bv.Amax) and \
                BV.overlap_interval(first_bv.Bmin, first_bv.Bmax, second_bv.Bmin, second_bv.Bmax) and \
                BV.overlap_interval(first_bv.Cmin, first_bv.Cmax, second_bv.Cmin, second_bv.Cmax) and \
                BV.overlap_interval(first_bv.Dmin, first_bv.Dmax, second_bv.Dmin, second_bv.Dmax):
            return True
        else:
            return False


class Triangle(TriangleNode):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        TriangleNode.__init__(self, None, None, self)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.y3 = y3
        self.x3 = x3

    def __str__(self):
        return str(self.x1) + " " + str(self.y1) + " " + str(self.x2) + " " + str(self.y2) + " " + str(
            self.x3) + " " + str(self.y3)

    def collide_bv(self, bv):
        self_bv = BV.create_bv(self, self)
        return BV.collide(self_bv, bv)


class Polygon:
    def __init__(self, id):
        self.triangles = []
        self.root = None
        self.minX = None
        self.minY = None
        self.maxX = None
        self.maxY = None
        self.id = id

    def add_triangle(self, triangle):
        self.triangles.append(triangle)
        min_x = min(triangle.x1, triangle.x2, triangle.x3)
        max_x = max(triangle.x1, triangle.x2, triangle.x3)
        min_y = min(triangle.y1, triangle.y2, triangle.y3)
        max_y = max(triangle.y1, triangle.y2, triangle.y3)
        if not self.minX or min_x < self.minX:
            self.minX = min_x
        if not self.maxX or max_x > self.maxX:
            self.maxX = max_x
        if not self.minY or min_y < self.minY:
            self.minY = min_y
        if not self.maxY or max_y > self.maxY:
            self.maxY = max_y

    @staticmethod
    def get_root_node(triangles):
        result_tris = []
        length = len(triangles)
        if length == 1:
            return triangles[0]
        newlen = length
        if length % 2 == 1:
            newlen -= 1
        for i in range(0, newlen, 2):
            bv = BV.create_bv(triangles[i].bv, triangles[i + 1].bv)
            result_tris.append(TriangleNode(triangles[i], triangles[i + 1], bv))
        if length % 2 == 1:
            bv = BV.create_bv(result_tris[-1].bv, triangles[-1].bv)
            result_tris[-1] = TriangleNode(result_tris[-1], triangles[-1], bv)
        return Polygon.get_root_node(result_tris)

    def compute_root(self):
        self.root = Polygon.get_root_node(self.triangles)

    @staticmethod
    def line_intersect2(v1, v2, v3, v4):
        d = (v4[1] - v3[1]) * (v2[0] - v1[0]) - (v4[0] - v3[0]) * (v2[1] - v1[1])
        u = (v4[0] - v3[0]) * (v1[1] - v3[1]) - (v4[1] - v3[1]) * (v1[0] - v3[0])
        v = (v2[0] - v1[0]) * (v1[1] - v3[1]) - (v2[1] - v1[1]) * (v1[0] - v3[0])
        if d < 0:
            u, v, d = -u, -v, -d
        return (0 < u < d) and (0 < v < d)

    @staticmethod
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

    @staticmethod
    def tri_intersect2(t1, t2):
        if Polygon.line_intersect2(t1[0], t1[1], t2[0], t2[1]): return True
        if Polygon.line_intersect2(t1[0], t1[1], t2[0], t2[2]): return True
        if Polygon.line_intersect2(t1[0], t1[1], t2[1], t2[2]): return True
        if Polygon.line_intersect2(t1[0], t1[2], t2[0], t2[1]): return True
        if Polygon.line_intersect2(t1[0], t1[2], t2[0], t2[2]): return True
        if Polygon.line_intersect2(t1[0], t1[2], t2[1], t2[2]): return True
        if Polygon.line_intersect2(t1[1], t1[2], t2[0], t2[1]): return True
        if Polygon.line_intersect2(t1[1], t1[2], t2[0], t2[2]): return True
        if Polygon.line_intersect2(t1[1], t1[2], t2[1], t2[2]): return True
        inTri = True
        inTri = inTri and Polygon.point_in_triangle2(t1[0], t1[1], t1[2], t2[0])
        inTri = inTri and Polygon.point_in_triangle2(t1[0], t1[1], t1[2], t2[1])
        inTri = inTri and Polygon.point_in_triangle2(t1[0], t1[1], t1[2], t2[2])
        if inTri == True: return True
        inTri = True
        inTri = inTri and Polygon.point_in_triangle2(t2[0], t2[1], t2[2], t1[0])
        inTri = inTri and Polygon.point_in_triangle2(t2[0], t2[1], t2[2], t1[1])
        inTri = inTri and Polygon.point_in_triangle2(t2[0], t2[1], t2[2], t1[2])
        if inTri == True: return True
        return False

    @staticmethod
    def collide(first_node, second_node):
        if isinstance(first_node, Triangle) and isinstance(second_node, Triangle):
            return Polygon.tri_intersect2(
                [[first_node.x1, first_node.y1], [first_node.x2, first_node.y2], [first_node.x3, first_node.y3]],
                [[second_node.x1, second_node.y1], [second_node.x2, second_node.y2], [second_node.x3, second_node.y3]])
        elif isinstance(first_node, Triangle):
            tri = first_node
            bv = second_node
            return tri.collide_bv(bv.bv)
        elif isinstance(second_node, Triangle):
            return second_node.collide_bv(first_node.bv)
        else:
            return BV.collide(first_node.bv, second_node.bv)

    @staticmethod
    def check_collision(first_root, second_root):
        # if not first_root or not second_root:
        #     return False
        if Polygon.collide(first_root, second_root):
            if isinstance(first_root, Triangle):
                if isinstance(second_root, Triangle):
                    return True
                else:
                    if Polygon.check_collision(first_root, second_root.left):
                        return True
                    if Polygon.check_collision(first_root, second_root.right):
                        return True
                    return False
            else:
                if Polygon.check_collision(first_root.left, second_root):
                    return True
                if Polygon.check_collision(first_root.right, second_root):
                    return True
                return False
        else:
            return False

    def check_collide(self, second_poly):
        return Polygon.check_collision(self.root, second_poly.root)


class PartitionNode:
    def __init__(self, length, centerX, centerY, isLeaf=False):
        self.length = length  # length of the square
        self.centerX = centerX
        self.centerY = centerY
        self.isLeaf = isLeaf
        self.list = []
        self.A = None  # a part ( child )
        self.B = None
        self.C = None
        self.D = None


def construct_quad_tree(root, this_depth, max_depth):
    if this_depth > max_depth:
        root.isLeaf = True
        return
    root.A = PartitionNode(root.length / 2, root.centerX + root.length / 4, root.centerY + root.length / 4)
    construct_quad_tree(root.A, this_depth + 1, max_depth)
    root.B = PartitionNode(root.length / 2, root.centerX - root.length / 4, root.centerY + root.length / 4)
    construct_quad_tree(root.B, this_depth + 1, max_depth)
    root.C = PartitionNode(root.length / 2, root.centerX - root.length / 4, root.centerY - root.length / 4)
    construct_quad_tree(root.C, this_depth + 1, max_depth)
    root.D = PartitionNode(root.length / 2, root.centerX + root.length / 4, root.centerY - root.length / 4)
    construct_quad_tree(root.D, this_depth + 1, max_depth)


def input_triangle(string):
    s = string.split()
    return Triangle(int(s[0]), int(s[1]), int(s[2]), int(s[3]), int(s[4]),
                    int(s[5]))


def add_polygon(root, polygon):
    if root.isLeaf:
        for prev_node in root.list:
            if polygon.check_collide(prev_node):
                # print(prev_node.id, polygon.id)
                file = open("output.txt", 'a')
                file.write(str(prev_node.id) + " " + str(polygon.id) + "\n")
                file.close()
        root.list.append(polygon)
    else:
        nodes = [root.A, root.B, root.C, root.D]
        if polygon.minX >= root.centerX:
            nodes[1] = None
            nodes[2] = None
        if polygon.maxX <= root.centerX:
            nodes[0] = None
            nodes[3] = None
        if polygon.minY >= root.centerY:
            nodes[2] = None
            nodes[3] = None
        if polygon.maxY <= root.centerY:
            nodes[0] = None
            nodes[1] = None
        for node in nodes:
            if node:
                add_polygon(node, polygon)


if __name__ == '__main__':
    # partitioning the field
    depth = 8
    root = PartitionNode(20000, 0, 0)
    construct_quad_tree(root, 0, depth)
    # reading input
    file = open("input.txt")
    all_inputs = file.read()
    file.close()
    all_inputs = all_inputs.split("\n")
    all_inputs = all_inputs[1:]
    current_polygon = None
    id = 0
    for inp in all_inputs:
        if inp == "end":
            current_polygon.compute_root()
            add_polygon(root, current_polygon)
            current_polygon = None
        elif current_polygon:
            current_polygon.add_triangle(input_triangle(inp))
        else:
            current_polygon = Polygon(id)
            id += 1
            current_polygon.add_triangle(input_triangle(inp))
    #
