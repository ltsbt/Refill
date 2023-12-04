import trimesh
import numpy as np
import pyqtgraph.opengl as gl
from typing import Optional


COLOR_ITEM = (0.5, 0.5, 0.5, 0.5)
COLOR_COM = (1, 0, 0, 1)
COLOR_LINE = (0, 0, 1, 1)


class Scene:
    def __init__(self) -> None:
        self.view = gl.GLViewWidget()

        self.mesh: Optional[trimesh.Trimesh] = None
        self.item: Optional[gl.GLMeshItem] = None
        self.com: Optional[gl.GLScatterPlotItem] = None
        self.com_projection_line: Optional[gl.GLLinePlotItem] = None

    def get_view(self):
        return self.view

    def open_from_file(self, filename):
        mesh = trimesh.load(filename)

        if not isinstance(mesh, trimesh.Trimesh):
            return

        self.mesh = mesh
        vertices = self.mesh.vertices
        faces = self.mesh.faces

        if vertices[:, 2].min() < 0:
            vertices[:, 2] -= vertices[:, 2].min()
            faces[:, 2] -= faces[:, 2].min()

        self.item = gl.GLMeshItem(
            vertexes=vertices,
            faces=faces,
            smooth=False,
            color=COLOR_ITEM,
            shader="balloon",
            drawEdges=True,
            drawFaces=False,
        )

        com_coords = self.mesh.center_mass
        self.com = gl.GLScatterPlotItem(
            pos=np.array([com_coords]), color=COLOR_COM, size=10
        )

        com_projection = com_coords.copy()
        com_projection[2] = 0

        self.com_projection_line = gl.GLLinePlotItem(
            pos=np.array([com_coords, com_projection]),
            color=COLOR_LINE,
            width=3,
            mode="line_strip",
        )

        self.update_view()

    def update_view(self):
        self.view.clear()

        self.view.addItem(self.item)
        self.view.addItem(self.com)
        self.view.addItem(self.com_projection_line)
