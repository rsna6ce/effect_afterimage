# effect_afterimage
What is effect_afterimage
* Script to add alpha blend afterimage to mp4 file
* Video audio is removed

## environment
* python3
  * install opencv
     ```
     $ pip3 install -r requirement.txt
     ```
* ffmpeg
  ```
  $ sudo apt-get -y install ffmpeg
  ```

## run
* example
  ```
  $ cd effect_afterimage
  $ ./effect_afterimage.py -i input.mp4 -o output.mp4 -f 30 -l 10 -a 0.5
  ```
* help
  ```
  ./effect_afterimage.py -h
  usage: effect_afterimage.py [-h] -i INPUT -o OUTPUT -f FRAME_RATE [-l LENGTH_AFTERIMAGE] [-a ALPHA]
  
  options:
    -h, --help            show this help message and exit
    -i INPUT, --input INPUT
                          input mp4 file
    -o OUTPUT, --output OUTPUT
                          output mp4 file
    -f FRAME_RATE, --frame_rate FRAME_RATE
                          frame_rate fps
    -l LENGTH_AFTERIMAGE, --length_afterimage LENGTH_AFTERIMAGE
                          length of afterimage
    -a ALPHA, --alpha ALPHA
                          alpha blend coeff
  ```
