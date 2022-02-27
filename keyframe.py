import ffmpeg
import shutil
import os
import math

YOUR_FILE = 'test.mp4'
PICPERMIN=20
#------------------------------------if os.path.exists("./out"):
if os.path.exists("./out"):
    shutil.rmtree("./out")
os.mkdir("./out")
probe = ffmpeg.probe(YOUR_FILE)
width=480  # default 480 

info=None
for i in probe["streams"]:
    if "width" in i.keys():
        info=i
        break
# Set how many spots you want to extract a video from. 
if info is  None:
    print("cannot find a video stream")
    exit(-1)
    
width=info["width"]
time = math.ceil(float(info['duration']))-1

parts=math.ceil(time/ (60/PICPERMIN))
intervals = time // parts
intervals=math.ceil(intervals)
interval_list = [(i * intervals, (i + 1) * intervals) for i in range(parts)]
i = 0

for item in interval_list:
    (
        ffmpeg
        .input(YOUR_FILE, ss=item[1])
        .filter('scale', width, -1)
        .output('out/Image' + str(i) + '.jpg', vframes=1)
        .run()
    )
    i += 1
