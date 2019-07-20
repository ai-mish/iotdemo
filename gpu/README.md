
## Table of Contents
- [Install NVIDIA Graphics Driver via run file](#install nvidia driver)
- [Install CUDA](#Install CUDA driver and toolkit)




## install nvidia driver
```
export yum_cmd="yum --disablerepo=sas-*"
sudo /usr/local/cuda/bin/uninstall_cuda_10.0.pl
sudo /usr/bin/nvidia-uninstall
sudo yum remove nvidia*
sudo rpm -e --nodeps cuda-drivers
sudo $yum_cmd groupinstall "Development Tools"
sudo $yum_cmd install kernel-devel kernel-headers dkms
export PKG_CONFIG_PATH=/usr/lib/pkgconfig
bash NVIDIA-Linux-x86_64-430.30-grid.run
Select no for xorg
```


### Install CUDA driver and toolkit
```
curl -O https://developer.download.nvidia.com/compute/cuda/10.1/secure/Prod/local_installers/cuda_10.1.168_418.67_linux.run?llA_0Rk5s95NDlHAab0Udk7JaO943Riw7vddWSwTmAbXsW5uzZ97ijqbhp9vjvknJQpjJARpK746bgqIvezllo-5F1RGR1JdyizVGPVqZquTGcXRuz31NHVbt4Kae_JNv2rUDainRnavGX5Qbu5ZBiM0E-Ppxp9Cx9wP2FJpQ1gnEBsI7p_DQ9ijwnA
sudo mv cuda_10.1.168_418.67_linux.run* cuda_10.1.168_418.67_linux.run
sudo ./cuda_10.1.168_418.67_linux.run.run -noprompt
#sudo ./cuda_10.1.168_418.67_linux.run -cudaprefix=/usr/local/cuda-9.0 -noprompt

## enable persistent mode
```
nvidia-smi -pm 1
```


```
Please make sure that
 -   PATH includes /usr/local/cuda-10.1/bin
 -   LD_LIBRARY_PATH includes /usr/local/cuda-10.1/lib64, or, add /usr/local/cuda-10.1/lib64 to /etc/ld.so.conf and run ldconfig as root

 sudo <CudaInstaller>.run --silent --driver
 e.g. bash cuda_10.1.168_418.67_linux.run --silent --driver
```
## Uninstall

```
sudo /usr/local/cuda/bin/cuda-uninstaller
sudo /usr/bin/nvidia-uninstall
```

## PATH
```
export PATH=/usr/local/cuda-10.1/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64:$LD_LIBRARY_PATH

OR

sudo bash -c "echo /usr/local/cuda/lib64/ > /etc/ld.so.conf.d/cuda.conf"
sudo ldconfig
```

## Verify
```
cat /proc/driver/nvidia/version
```

## Sample
```
cd /usr/local/cuda-9.0/samples
sudo make
cd /usr/local/cuda/samples/bin/x86_64/linux/release
./deviceQuery
```


```
(base) [ec2-user@esp61 release]$ ./deviceQuery
./deviceQuery Starting...

 CUDA Device Query (Runtime API) version (CUDART static linking)

Detected 1 CUDA Capable device(s)

Device 0: "Tesla M60"
  CUDA Driver Version / Runtime Version          10.1 / 10.1
  CUDA Capability Major/Minor version number:    5.2
  Total amount of global memory:                 7619 MBytes (7988903936 bytes)
  (16) Multiprocessors, (128) CUDA Cores/MP:     2048 CUDA Cores
  GPU Max Clock rate:                            1178 MHz (1.18 GHz)
  Memory Clock rate:                             2505 Mhz
  Memory Bus Width:                              256-bit
  L2 Cache Size:                                 2097152 bytes
  Maximum Texture Dimension Size (x,y,z)         1D=(65536), 2D=(65536, 65536), 3D=(4096, 4096, 4096)
  Maximum Layered 1D Texture Size, (num) layers  1D=(16384), 2048 layers
  Maximum Layered 2D Texture Size, (num) layers  2D=(16384, 16384), 2048 layers
  Total amount of constant memory:               65536 bytes
  Total amount of shared memory per block:       49152 bytes
  Total number of registers available per block: 65536
  Warp size:                                     32
  Maximum number of threads per multiprocessor:  2048
  Maximum number of threads per block:           1024
  Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
  Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
  Maximum memory pitch:                          2147483647 bytes
  Texture alignment:                             512 bytes
  Concurrent copy and kernel execution:          Yes with 2 copy engine(s)
  Run time limit on kernels:                     No
  Integrated GPU sharing Host Memory:            No
  Support host page-locked memory mapping:       Yes
  Alignment requirement for Surfaces:            Yes
  Device has ECC support:                        Enabled
  Device supports Unified Addressing (UVA):      Yes
  Device supports Compute Preemption:            No
  Supports Cooperative Kernel Launch:            No
  Supports MultiDevice Co-op Kernel Launch:      No
  Device PCI Domain ID / Bus ID / location ID:   0 / 0 / 30
  Compute Mode:
     < Default (multiple host threads can use ::cudaSetDevice() with device simultaneously) >

deviceQuery, CUDA Driver = CUDART, CUDA Driver Version = 10.1, CUDA Runtime Version = 10.1, NumDevs = 1
Result = PASS
(base) [ec2-user@esp61 release]$
```


https://developer.download.nvidia.com/compute/cuda/9.1/Prod/docs/sidebar/CUDA_Installation_Guide_Linux.pdf

(Optional) Enable GPU Functionality
https://go.documentation.sas.com/api/docsets/dplyesp0phy0lax/6.1/content/dplyesp0phy0lax.pdf?locale=en




set of NVIDIA libraries 

CUDA    10.0.166
cuDNN	7.5
NCCL	2.4
CUB     1.8.0
JetPack 4.2

The latest NVIDIA driver version for CUDA 10.0 is 410.1
