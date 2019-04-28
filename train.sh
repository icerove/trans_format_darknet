#!/bin/bash
../darknet/darknet detector train voc.data ../darknet/cfg/yolov3-voc.cfg ../darknet/darknet53.conv.74 -gpus 0