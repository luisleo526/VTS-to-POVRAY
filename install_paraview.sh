#wget 'https://www.dropbox.com/scl/fi/d288giczfxf6dpqfvavzo/paraview.tar.gz?rlkey=b2l5lfkml75twp58qsby80epf&dl=0' -O $HOME/paraview.tar.gz

mkdir -p $HOME/ParaView-5.11.2

tar zxvf $HOME/paraview.tar.gz -C $HOME/ParaView-5.11.2

mv $HOME/ParaView-5.11.2/ParaView-5.11.2-osmesa-MPI-Linux-Python3.9-x86_64/* $HOME/ParaView-5.11.2
rmdir $HOME/ParaView-5.11.2/ParaView-5.11.2-osmesa-MPI-Linux-Python3.9-x86_64

echo 'export PATH=$HOME/ParaView-5.11.2/bin:$PATH' >> $HOME/.bashrc

