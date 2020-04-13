import os, torch

# Util function for loading meshes
from pytorch3d.io import load_obj

# Data structures and functions for rendering
from pytorch3d.structures import Meshes, Textures
from pytorch3d.renderer import (
    look_at_view_transform,
    OpenGLPerspectiveCameras,
    PointLights, HardPhongShader,
    RasterizationSettings,
    MeshRenderer, MeshRasterizer,
    TexturedSoftPhongShader, BlendParams
)
import numpy as np


class MeshLoader(object):
    def __init__(self, device='cuda:0'):
        self.device = torch.device(device)
        torch.cuda.set_device(self.device)
        self.initialize_renderer()

    def initialize_renderer(self):
        # Initialize an OpenGL perspective camera
        cameras = OpenGLPerspectiveCameras(device=self.device)

        raster_settings = RasterizationSettings(
            image_size = 1024,
            blur_radius = 0.0,
            faces_per_pixel=1,
        )

        # Place a point light in front of the object
        lights = PointLights(device=self.device, location=[[10.0,10.0,6.0]])

        # Create a phong renderer by composing a rasterizer and a shader
        self.phong_renderer = MeshRenderer(
            rasterizer=MeshRasterizer(
                cameras=cameras,
                raster_settings=raster_settings
            ),
            shader=HardPhongShader(device=self.device, lights=lights)
        )

    def load(self, obj_filename):
        # Load obj file
        verts, faces_idx, _ = load_obj(obj_filename)
        faces = faces_idx.verts_idx


        # Initialize each vertex to be white in color
        verts_rgb = torch.ones_like(verts)[None]
        textures = Textures(verts_rgb=verts_rgb.to(self.device))

        # Create a Meshes object for the face.
        self.face_mesh = Meshes(
            verts = [verts.to(self.device)],
            faces = [faces.to(self.device)],
            textures = textures
        )

    def render(self, distance=3, elevation=1.0, azimuth=0.0):
        """ Select the viewpoint using spherical angles"""

        self.distance = distance
        self.elevation = elevation
        self.azimuth = azimuth

        # Get the position of the camera based on the spherical angles
        R, T = look_at_view_transform(distance, elevation, azimuth, device=self.device)

        # Render the face providing the values of R and T
        image_ref = self.phong_renderer(meshes_world=self.face_mesh, R=R, T=T)

        #silhouette = silhouette.cpu().numpy()
        image_ref = image_ref.cpu().numpy()

        return image_ref.squeeze()

    
    def get_camera_params(self):
        return self.distance, self.elevation, self.azimuth
