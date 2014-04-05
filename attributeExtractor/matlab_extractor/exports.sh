#!/bin/sh

# ANTES de correr el extractor hay que exportar algunas variables para que funcione el wrapper de matlab
# ejecutar esto antes de ejecutar el extractor 
# ejecutar de esta forma: $ source exports.sh

export PATH=/home/fernando/Programas/MatlabR13a/bin:$PATH
export C_INCLUDE_PATH=/home/fernando/Programas/MatlabR13a/extern/include/
export LIBRARY_PATH=/home/fernando/Programas/MatlabR13a/bin/glnxa64/
