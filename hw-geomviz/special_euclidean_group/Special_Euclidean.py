"""Visualization for Geometric Statistics."""
import logging

import geomstats.backend as gs
import geomstats.visualization as visualization
import matplotlib.pyplot as plt
from geomstats.geometry.special_euclidean import SpecialEuclidean
from mpl_toolkits.mplot3d import Axes3D  # NOQA

SE3_GROUP = SpecialEuclidean(n=3, point_type="matrix")
SE3_VECT = SpecialEuclidean(n=3, point_type="vector")

METRIC = SE3_VECT.left_canonical_metric


class SpecialEuclidean3:
    """Class used to plot points in the 3d special euclidean group."""

    def __init__(self, points=None, point_type="matrix"):
        """Initialize SE(3) objects."""
        self.points = []
        self.point_type = point_type
        if points is not None:
            self.add_points(points)

    @staticmethod
    def set_ax(ax=None, x_lim=None, y_lim=None):
        """Define SE(3) plot axes."""
        if ax is None:
            ax = plt.subplot(111, projection="3d")
        if x_lim is not None:
            ax.set_xlim(x_lim)
        if y_lim is not None:
            ax.set_ylim(y_lim)
        return ax

    def add_points(self, points):
        """Add points to SE(3) object."""
        if self.point_type == "vector":
            points = SE3_VECT.matrix_from_vector(points)
        if not gs.all(SE3_GROUP.belongs(points)):
            logging.warning("Some points do not belong to SE3.")
        if not isinstance(points, list):
            points = list(points)
        self.points.extend(points)

    def draw_points(self, ax, points=None, **kwargs):
        """Visualization for SE(3) points."""
        if points is None:
            points = gs.array(self.points)
        translation = points[..., :3, 3]
        frame_1 = points[:, :3, 0]
        frame_2 = points[:, :3, 1]
        frame_3 = points[:, :3, 2]
        ax.quiver(
            translation[:, 0],
            translation[:, 1],
            translation[:, 2],
            frame_1[:, 0],
            frame_1[:, 1],
            frame_1[:, 2],
            color="b",
        )
        ax.quiver(
            translation[:, 0],
            translation[:, 1],
            translation[:, 2],
            frame_2[:, 0],
            frame_2[:, 1],
            frame_2[:, 2],
            color="r",
        )
        ax.quiver(
            translation[:, 0],
            translation[:, 1],
            translation[:, 2],
            frame_3[:, 0],
            frame_3[:, 1],
            frame_3[:, 2],
            color="g",
        )
        ax.scatter(
            translation[:, 0], translation[:, 1],
            translation[:, 2], s=20, **kwargs
        )

    def plot_geodesic(
        self, initial_point, initial_tangent_vec, METRIC, N_STEPS, **kwargs
    ):
        """Visualization of SE(3) geodesic."""
        geodesic = METRIC.geodesic(
            initial_point=initial_point,
            initial_tangent_vec=initial_tangent_vec
        )
        t = gs.linspace(-3.0, 3.0, N_STEPS)

        points = geodesic(t)

        visualization.plot(points, space="SE3_GROUP")
        plt.show()
