class Node:
    def __init__(self, left, right, bv):
        self.right = right
        self.left = left
        self.bv = bv

    def __str__(self):
        return self.left.bv.__str__() + " " + self.right.bv.__str__()


class Triangle(Node):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        Node.__init__(self, None, None, self)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.y3 = y3
        self.x3 = x3
        self.centroidX = 0
        self.centroidY = 0
        self.compute_centroid()

    def compute_centroid(self):
        self.centroidX = (self.x1 + self.x2 + self.x3) / 3
        self.centroidY = (self.y1 + self.y2 + self.y3) / 3

    def __str__(self):
        return str(self.x1) + str(self.y1) + str(self.x2) + str(self.y2) + str(self.x3) + str(self.y3)


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
        return str(self.Amax) + str(self.Amin) + str(self.Bmax) + str(self.Bmin) + str(self.Cmax) + str(
            self.Cmin) + str(self.Dmax) + str(self.Dmin)

    @staticmethod
    def create_bv(left_child, right_child):
        if isinstance(left_child, Triangle) and isinstance(right_child, Triangle):
            Amax = max(left_child.y1, left_child.y2, left_child.y3, right_child.y1, right_child.y2, right_child.y3)
            Amin = min(left_child.y1, left_child.y2, left_child.y3, right_child.y1, right_child.y2, right_child.y3)
            Bmax = max(left_child.x1, left_child.x2, left_child.x3, right_child.x1, right_child.x2, right_child.x3)
            Bmin = min(left_child.x1, left_child.x2, left_child.x3, right_child.x1, right_child.x2, right_child.x3)
            Cmax = max((left_child.y1 - left_child.x1), (left_child.y2 - left_child.x2),
                       (left_child.y3 - left_child.x3),
                       (right_child.y1 - right_child.x1), (right_child.y2 - right_child.x2),
                       (right_child.y3 - right_child.x3))
            Cmin = min((left_child.y1 - left_child.x1), (left_child.y2 - left_child.x2),
                       (left_child.y3 - left_child.x3),
                       (right_child.y1 - right_child.x1), (right_child.y2 - right_child.x2),
                       (right_child.y3 - right_child.x3))
            Dmax = max((left_child.y1 + left_child.x1), (left_child.y2 + left_child.x2),
                       (left_child.y3 + left_child.x3),
                       (right_child.y1 + right_child.x1), (right_child.y2 + right_child.x2),
                       (right_child.y3 + right_child.x3))
            Dmin = min((left_child.y1 + left_child.x1), (left_child.y2 + left_child.x2),
                       (left_child.y3 + left_child.x3),
                       (right_child.y1 + right_child.x1), (right_child.y2 + right_child.x2),
                       (right_child.y3 + right_child.x3))
            return BV(Amin, Amax, Bmin, Bmax, Cmin, Cmax, Dmin, Dmax)
        elif isinstance(left_child, Triangle) or isinstance(right_child, Triangle):
            tri = None
            bv = None
            if isinstance(left_child, Triangle):
                tri = left_child
                bv = right_child
            else:
                tri = right_child
                bv = left_child
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
        else:
            return BV(Amax=max(left_child.Amax, right_child.Amax),
                      Amin=min(left_child.Amin, right_child.Amin),
                      Bmin=min(left_child.Bmin, right_child.Bmin),
                      Bmax=max(left_child.Bmax, right_child.Bmax),
                      Cmax=max(left_child.Cmax, right_child.Cmax),
                      Cmin=min(left_child.Cmin, right_child.Cmin),
                      Dmin=min(left_child.Dmin, right_child.Dmin),
                      Dmax=max(left_child.Dmax, right_child.Dmax))


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
        result_tris.append(Node(triangles[i], triangles[i + 1], bv))
    if length % 2 == 1:
        bv = BV.create_bv(result_tris[-1].bv, triangles[-1].bv)
        result_tris[-1] = Node(result_tris[-1], triangles[-1], bv)
    return get_root_node(result_tris)


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i].centroidX < R[j].centroidX:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def sort_triangles(triangles):
    # just on X axis
    merge_sort(triangles)


def collide(first_node, second_node):
    if isinstance(first_node, Triangle) and isinstance(second_node, Triangle):
        pass


if __name__ == '__main__':
    first_triangles = []
    second_triangles = []
    string = ""
    while True:
        string = input()
        if string == "end1":
            break
        split = string.split()
        triangle = Triangle(int(split[0]), int(split[1]), int(split[2]), int(split[3]), int(split[4]), int(split[5]))
        first_triangles.append(triangle)
    while True:
        string = input()
        if string == "end2":
            break
        split = string.split()
        triangle = Triangle(int(split[0]), int(split[1]), int(split[2]), int(split[3]), int(split[4]), int(split[5]))
        second_triangles.append(triangle)
    sort_triangles(first_triangles)
    sort_triangles(second_triangles)
    first_root = get_root_node(first_triangles)
    second_root = get_root_node(second_triangles)
