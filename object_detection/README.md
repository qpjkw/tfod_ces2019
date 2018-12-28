# Object Dection API on TF for CES 2019



## Starting a container

Make sure you have already imported the customized docker image into container station. You can pull images from Dockerhub repository (Remind you we provide two different version, CPU or GPU.). In CES, we recommend GPU-based docker image.

```sh
# docker pull qhub/tfod-ces2019:1.0
# docker pull qhub/tfod-ces2019:1.0-gpu
```

And then instantiate a container via the below command.

```sh
# CPU
# docker run --rm -it --name ces2019 --ipc=host -p 18888:8888 -p 16006:6006 tfod-ces2019:1.0

# GPU
# docker run --rm -it --name ces2019gpu --ipc=host -p 28888:8888 -p 26006:6006 --device /dev/nvidia0:/dev/nvidia0 --device /dev/nvidiactl:/dev/nvidiactl --device /dev/nvidia-uvm:/dev/nvidia-uvm -v /share/CACHEDEV1_DATA/.qpkg/NVIDIA_GPU_DRV/usr/:/usr/local/nvidia tfod-ces2019:1.0-gpu
```

You now can surf the web link to use jupyter notebook (online IDE). 

```text
CPU: http://<IP>:18888/?token="(fetch from terminal)"
GPU: http://<IP>:28888/?token="(fetch from terminal)"
```



## Training

Execute the bash script to start a training. 

You can open a terminal by clicking the buttons [`new > terminal`].

After you open a terminal, copy the below command and paste on it to start a retraining task.

```sh
# bash /notebooks/object_detection/start_object_detection.sh
```

You now can surf the web link to monitor training progresses via Tensorboard.

```text
CPU: http://<IP>:16006"
GPU: http://<IP>:26006"
```

After the training, you can find the model (.pb) on `/notebooks/object_detection/model`.

**If you stop the training unexpectedly, you can type the above starting training command to continue the training.**



## Inference

Back to jupyter notebook editor, you can edit the notebook `object_detection_demo.ipynb` to demo the object detection on images.

