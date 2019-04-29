#!/bin/bash
../darknet/darknet detector train gun.data yolov3-gun.cfg ../darknet/darknet53.conv.74 -map | tee log.txt
