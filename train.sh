#!/bin/bash
../darknet/darknet detector train voc.data yolov3-voc.cfg ../darknet/darknet53.conv.74 -gpus 0