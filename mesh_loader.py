import os, torch

# Util function for loading meshes
from pytorch3d.io import load_obj, load_ply

# Data structures and functions for rendering
from pytorch3d.structures import Meshes, Textures
from pytorch3d.ops import GraphConv, sample_points_from_meshes, vert_align
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

    def set_phong_renderer(self, light_location):
        # Place a point light in front of the object
        self.light_location = light_location
        lights = PointLights(device=self.device, location=[light_location])

        # Create a phong renderer by composing a rasterizer and a shader
        self.phong_renderer = MeshRenderer(
                rasterizer=MeshRasterizer(
                cameras=self.cameras,
                raster_settings=self.raster_settings
            ),
            shader=HardPhongShader(device=self.device, lights=lights)
        )

    def initialize_renderer(self):
        # Initialize an OpenGL perspective camera
        self.cameras = OpenGLPerspectiveCameras(device=self.device)

        self.raster_settings = RasterizationSettings(
            image_size = 1024,
            blur_radius = 0.0,
            faces_per_pixel=1,
        )

        self.set_phong_renderer([0.0,3.0,5.0])

    def load(self, obj_filename):
        # Load obj file
        extension = obj_filename[-3:]
        
        if extension == 'obj':
            verts, faces, aux = load_obj(obj_filename)
            verts_idx = faces.verts_idx
        elif extension == 'ply':
            verts, faces = load_ply(obj_filename)
            verts_idx = faces

        # Initialize each vertex to be white in color
        verts_rgb = torch.ones_like(verts)[None]
        textures = Textures(faces_uvs=faces.textures_idx[None,...], verts_uvs=aux.verts_uvs[None,...], verts_rgb=verts_rgb.to(self.device))

        # Create a Meshes object for the face.
        self.face_mesh = Meshes(
            verts = [verts.to(self.device)],
            faces = [verts_idx.to(self.device)],
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

    def change_light(self, light_location):
        self.set_phong_renderer(light_location)
        return self.render(self.distance, self.elevation, self.azimuth)
    
    def get_camera_params(self):
        return self.distance, self.elevation, self.azimuth

    def get_light_location(self):
        return self.light_location