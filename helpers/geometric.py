import numpy as np


class GeometricMethods:

    def ang_vectors(self, u, v):
        u = np.array(u)
        v = np.array(v)
        dot_product = np.dot(u, v)
        norms = self.norma(u)*self.norma(v)
        try:
            arc = dot_product/norms
            if np.fabs(arc) > 1:
                raise ValueError('Arco maior que 1 !!!')
        except ValueError:
            arc = np.around(arc)
        ang = np.arccos(arc)
        # print(ang, arc, dot_product, norms, u, v)
        return ang

    def spin_orient(self, coords, ref_coord):
        dirs = np.array([ref_coord - coords for crd_node in coords])
        slopes = np.zeros(len(dirs))
        for j in range(len(dirs)):
            angle_x = self.ang_vectors(dirs[j], [1, 0, 0])
            if dirs[j, 1] <= 0:
                slopes[j] = 2.0 * np.pi - angle_x
            else:
                slopes[j] = angle_x
        indices = np.argsort(slopes)
        return indices

    def order_coords(self, coords):
        ref_coord = sum(coords) / len(coords)
        indices = self.spin_orient(coords, ref_coord)
        coords_sorted = coords[indices]
        return coords_sorted

    def _counterclock_sort(self, coords):
        inner_coord = sum(coords)/(len(coords))
        vectors = np.array(
            [crd_node - inner_coord for crd_node in coords])

        directions = np.zeros(len(vectors))
        for j in range(len(vectors)):
            direction = self.ang_vectors(vectors[j], [1, 0, 0])
            if vectors[j, 1] <= 0:
                directions[j] = directions[j] + 2.0 * np.pi - direction
            else:
                directions[j] = directions[j] + direction
        indices = np.argsort(directions)
        return indices
