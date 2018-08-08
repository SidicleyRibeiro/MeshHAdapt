import numpy as np


class GeometricMethods:

    def spin_orient(self, coords, ref_coord):
        dirs = np.array([ref_coord - coords for crd_node in coords])
        slopes = np.zeros(len(dirs))
        for j in range(len(dirs)):
            angle_x = ang_vectors(dirs[j], [1, 0, 0])
            if dirs[j, 1] <= 0:
                slopes[j] = 2.0 * pi - angle_x
            else:
                slopes[j] = angle_x
        indices = np.argsort(slopes)
        return indices

    def order_coords(self, coords):
        ref_coord = sum(coords) / len(coords)
        indices = self.spin_orient(coords, ref_coord)
        coords_sorted = coords[indices]
        return coords_sorted
