#!/usr/bin/env python3
import cv2
import os
import sys
import argparse
import subprocess
import datetime
import shutil

def main():
    parser = argparse.ArgumentParser(prog='effect_afterimage.py')
    parser.add_argument('-i', '--input', help='input mp4 file', required=True, dest='input')
    parser.add_argument('-o', '--output', help='output mp4 file', required=True, dest='output')
    parser.add_argument('-f', '--frame_rate', help='frame_rate fps', required=True, dest='frame_rate')
    parser.add_argument('-l', '--length_afterimage', help='length of afterimage', default=10, type=int, dest='length_afterimage')
    parser.add_argument('-a', '--alpha', help='alpha blend coeff', default=0.5, type=float, dest='alpha')
    args = parser.parse_args()
    
    effect_afterimage(args)

def effect_afterimage(args):
    video1_path = "230429_144425__.mp4"

    input = args.input
    output = args.output
    length_afterimage = args.length_afterimage
    alpha = args.alpha
    frame_rate = args.frame_rate
    dt_now = datetime.datetime.now()
    workdir = dt_now.strftime('%Y%m%d_%H%M%S')
    os.makedirs(workdir, exist_ok=True)

    cap = cv2.VideoCapture(input)
    if not cap.isOpened():
      print("ERROR: cannot open ", input)
      sys.exit()

    list_afterimage = []
    frame_no = 0

    ret1, frame0 = cap.read()
    height, width, channels = frame0.shape[:3]
    for i in range(length_afterimage-1):
        list_afterimage.append(frame0)

    canceled = False
    while True:
        ret1, frame_curr = cap.read()
        if not ret1:
            break

        list_afterimage.append(frame_curr)

        for i in range(length_afterimage):
            index = length_afterimage - i - 1
            if i==0:
                frame_output = list_afterimage[index]
            else:
                frame_output = cv2.addWeighted(
                    src1=frame_output, alpha=alpha,
                    src2=list_afterimage[index], beta=(1.0-alpha),
                    gamma=0)

        # enhance current_frame
        current_alpha = 0.6
        frame_output = cv2.addWeighted(
            src1=frame_curr, alpha=current_alpha,
            src2=frame_output, beta=(1.0-current_alpha),
            gamma=0)
        list_afterimage.pop(0)

        cv2.imshow("frame_curr", frame_output)
        cv2.imwrite(workdir+'/{}.png'.format(str(frame_no).zfill(8)), frame_output)
        frame_no+=1

        key = cv2.waitKey(30)
        if key == 27:
            canceled = True
            break

    cap.release()
    cv2.destroyAllWindows()

    # encode mp4
    if not canceled:
        file_and_dirs = os.listdir(workdir)
        frame_files = [f for f in file_and_dirs if os.path.isfile(os.path.join(workdir, f)) and f!='.git_keep']
        subprocess.run(('ffmpeg' ,
            '-loglevel', 'warning',
            '-y',
            '-framerate', str(frame_rate),
            '-i', workdir+'/%8d.png',
            '-vframes', str(len(frame_files)),
            '-vf', 'scale={0}:{1},format=yuv420p'.format(width, height),
            '-vcodec', 'libx264',
            '-r', str(frame_rate),
            output))

    # remove frames
    shutil.rmtree(workdir)
    
if __name__ == '__main__':
    main()