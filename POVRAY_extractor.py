from paraview.simple import *
from paraview.util import Glob
from pathlib import Path
import os

print("Input root_directory")
root_directory = input()
print("Input target variable name")
target = input()

# files = Glob(path = os.path.join(root_directory, "CaseA_30_*.vts") )
# reader = OpenDataFile(files)
# Show()
# Render()

# threshold = Threshold(Scalars=target, UpperThreshold=0.0001)
# threshold.ThresholdMethod = 'Above Upper Threshold'
contour = Contour()
contour.ContourBy = target
contour.Isosurfaces = [0.0]
Show()
Render()

timesteps = GetTimeKeeper().TimestepValues
view = GetAnimationScene()
renderView1 = GetActiveViewOrCreate('RenderView')

Path(os.path.join(root_directory, "POV")).mkdir(parents=True, exist_ok=True)

for i in range(len(timesteps)):

    view.AnimationTime = timesteps[i]

    ExportView(os.path.join(root_directory, "POV", str(i)+'.pov'), view=renderView1)

    with open(os.path.join(root_directory, "POV", str(i)+'.pov'), "r") as f:
        content=f.readlines()

    start_matrix = False
    end_matrix = False
    write_mesh=False

    start_camera = False
    end_camera = False

    start_ls = False
    end_ls = False

    with open(os.path.join(root_directory, "POV", str(i)+'.pov'), "w") as f: 
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

            if end_camera and not os.path.exists(os.path.join(root_directory, "POV", 'camera.inc')):
                with open(os.path.join(root_directory, "POV", 'camera.inc'),"w") as f_cam:
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

            if end_ls and not os.path.exists(os.path.join(root_directory, "POV", 'light_source.inc')):
                with open(os.path.join(root_directory, "POV", 'light_source.inc'),"w") as f_ls:
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
