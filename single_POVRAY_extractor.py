from paraview.simple import *
from paraview.util import Glob
from pathlib import Path
from argparse import ArgumentParser
import os


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", type=str)
    parser.add_argument("-o", type=str)
    parser.add_argument("-t", type=str, default="Phi")
    parser.add_argument("-v", type=float, default=0.0)
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = parse_args()

    reader = OpenDataFile([args.i])
    Show()
    Render()

    contour = Contour()
    contour.ContourBy = args.t
    contour.Isosurfaces = [args.v]
    Show()
    Render()

    timesteps = GetTimeKeeper().TimestepValues
    view = GetAnimationScene()
    renderView = GetActiveViewOrCreate('RenderView')

    Path(args.o).parent.mkdir(parents=True, exist_ok=True)

    ExportView(str(Path(args.o).with_suffix('.pov')), view=renderView)

    with open(str(Path(args.o).with_suffix('.pov')), "r") as f:
        content=f.readlines()

    start_matrix = False
    end_matrix = False
    write_mesh=False

    start_camera = False
    end_camera = False

    start_ls = False
    end_ls = False

    with open(str(Path(args.o).with_suffix('.pov')), "w") as f: 
        f.write('#include "my setting.inc" \n')
        f.write('#include "camera.inc" \n')
        f.write('#include "light_source.inc" \n')
        objnum=0
        for line in content:

            if 'camera' in line:
                start_camera = True
                info = ""

            if start_camera and not end_camera:
                info += line + "\n"
                if '}' in line:
                    end_camera = True

            if end_camera and not os.path.exists(str(Path(args.o).with_name('camera.inc'))):
                with open(str(Path(args.o).with_name('camera.inc')),"w") as f_cam:
                    f_cam.write(info)

            if 'light_source' in line and not start_ls:
                start_ls = True
                info = ""

            if "mesh2" in line:
                end_ls = True
                write_mesh=True

            if "matrix" in line: 
                start_matrix = True
                end_ls = True

            if start_ls and not end_ls:
                info += line + '\n'

            if end_ls and not os.path.exists(str(Path(args.o).with_name('light_source.inc'))):
                with open(str(Path(args.o).with_name('light_source.inc')),"w") as f_ls:
                    f_ls.write(info)

            if start_matrix and ">" in line:
                end_matrix = True

            if write_mesh:
                f.write(line)

            if end_matrix:
                if objnum == 0:
                    f.write("material {milk}")
                else:
                    f.write("material {gate}")
                start_matrix = end_matrix = False
                objnum+=1
                f.write("}")
                write_mesh = False

