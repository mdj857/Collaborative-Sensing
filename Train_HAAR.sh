#!/bin/sh

opencv_traincascade -data model -bg bg.txt -numPos 229 -numNeg 977 -w 50 -h 50 -numStages 2 -vec positives.vec -maxFalseAlarmRate 0.75 -featureType HAAR >> train_out.txt
opencv_traincascade -data model_2 -bg bg2.txt -numPos 229 -numNeg 179 -w 50 -h 50 -numStages 2 -vec positives.vec -maxFalseAlarmRate 0.25 -featureType HAAR >> train2_out.txt
opencv_traincascade -data model_better -bg bg.txt -numPos 229 -numNeg 977 -w 50 -h 50 -numStages 2 -vec positives.vec -maxFalseAlarmRate 0.75 -featureType HAAR >>trainb_out.txt
opencv_traincascade -data model_2_better -bg bg2.txt -numPos 229 -numNeg 179 -w 50 -h 50 -numStages 2 -vec positives.vec -maxFalseAlarmRate 0.25 -featureType HAAR >>train2b.txt
