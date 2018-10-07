#!/bin/sh
opencv_traincascade -data model -bg bg.txt -numPos 30 -numNeg 798 -w 64 -h 64 -numStages 3 -vec positives.vec -featureType HAAR
