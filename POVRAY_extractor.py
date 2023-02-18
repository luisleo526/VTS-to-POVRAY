from paraview.simple import *
from paraview.util import Glob
from pathlib import Path
from argparse import ArgumentParser
import os


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--r", "-r", type=str, help="root directory")
    parser.add_argument("--p", "-p", type=str, help='predix of data')
    parser.add_argument("--t", "-t", type=str, help="target variable name")
    parser.add_argument("--o", "-o", type=str, help="output directory")
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = parse_args()

    files = Glob(path = os.path.join(args.r, args.p) )
    reader = OpenDataFile(files)
    Show()
    Render()

    # threshold = Threshold(Scalars=args.t, UpperThreshold=0.0001)
    # threshold.ThresholdMethod = 'Above Upper Threshold'
    contour = Contour()
    contour.ContourBy = args.t
    contour.Isosurfaces = [0.0]
    Show()
    Render()

    timesteps = GetTimeKeeper().TimestepValues
    view = GetAnimationScene()
    renderView1 = GetActiveViewOrCreate('RenderView')

    Path(args.o).mkdir(parents=True, exist_ok=True)

    for i in range(len(timesteps)):

        view.AnimationTime = timesteps[i]

        ExportView(os.path.join(args.o, str(i)+'.pov'), view=renderView1)

        with open(os.path.join(args.o, str(i)+'.pov'), "r") as f:
            content=f.readlines()

        start_matrix = False
        end_matrix = False
        write_mesh=False

        start_camera = False
        end_camera = False

        start_ls = False
        end_ls = False

        with open(os.path.join(args.o, str(i)+'.pov'), "w") as f: 
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

                if end_camera and not os.path.exists(os.path.join(args.o, 'camera.inc')):
                    with open(os.path.join(args.o, 'camera.inc'),"w") as f_cam:
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

                if end_ls and not os.path.exists(os.path.join(args.o, 'light_source.inc')):
                    with open(os.path.join(args.o, 'light_source.inc'),"w") as f_ls:
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

