#wget 'https://www.dropbox.com/scl/fi/5pc5ez93owfoh643bo9gk/ParaView-5.11.2-egl-MPI-Linux-Python3.9-x86_64.tar.gz?rlkey=k10isaw37phe1xl58zyetckv2' -O $HOME/paraview.tar.gz

mkdir -p $HOME/ParaView-5.11.2-egl

tar zxvf $HOME/paraview.tar.gz -C $HOME/ParaView-5.11.2-egl

mv $HOME/ParaView-5.11.2-egl/ParaView-5.11.2-egl-MPI-Linux-Python3.9-x86_64/* $HOME/ParaView-5.11.2-egl
rmdir $HOME/ParaView-5.11.2-egl/ParaView-5.11.2-egl-MPI-Linux-Python3.9-x86_64

echo 'export PATH=$HOME/ParaView-5.11.2-egl/bin:$PATH' >> $HOME/.bashrc

