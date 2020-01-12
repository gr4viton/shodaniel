# shodaniel

## what?

shodan search for open webcam streams and random show them in a loop = screensaver

## how

- docker container runs gui via Xserver sharing (sorry applindows)
- code in python

### packages:
```
# viz reqs.in
shodan
opencv
vidgear
# future
kivy?
Qt?
```

# plan
## classes

Streamer
- control what is shown
- UI
  - holds video canvas
- timings of random cycling
- main loop
    - crawler get 5 stream ips
    - create 5 streams
    - add 5 streams to queue
    - cycle in queue
    - user input (exit, next previous)

Crawler
- acquire ips via shodan
- get mutliple ips

Stream(CamGear)
- holds open video
- check whether not empty

StreamQueue
- loads streams
- holds loaded streams
- cycles through streams
- method
    - add() - adds new Stream
    - next()


# test

test gui via docker-compose - shodan screensaver?

## multiplatform?

- it needs X to run - so probly only linux
- platforms
  - linux
    - with X11 = OK
  - mac
    - not tested - maybe possible with x-quartz / [xrdp](https://github.com/deskor/xrdp)
    - read [thread here](https://forums.docker.com/t/how-to-run-gui-apps-in-containiers-in-osx-docker-for-mac/17797/6)
  - windows
    - ??

via VNC it should be possible on "any system"
- not tested

## run

Make sure you have docker and docker-compose installed.
```sh
docker-compose build
docker-compose up
```


# troubleshoot

## x could not connect to display
if you get error
```
No protocol specified
QXcbConnection: Could not connect to display :0
```
you may need to run this on your host - localmachine
```sh
xhost +local:docker
```

[source](https://forums.docker.com/t/start-a-gui-application-as-root-in-a-ubuntu-container/17069)

it happens cuz in docker container you are using the user `root`.

if you would use user `user` (non-root priviledged) it would work normaly,

but the opencv docker image is done in a way you need to work as root in the docker container



# links

[opencv in docker](https://www.learnopencv.com/install-opencv-docker-image-ubuntu-macos-windows/)
[elegant venv in dockerfile](https://pythonspeed.com/articles/activate-virtualenv-dockerfile/)

[vidgear](https://github.com/abhiTronix/vidgear/wiki/CamGear)


[xeyes in docker](https://nelkinda.com/blog/xeyes-in-docker/)
[rtsp url suffix example](https://community.ui.com/questions/How-do-i-view-Aircam-stream-in-VLC-media-player/44edbcad-f4f1-4e16-9531-faccb3f8cae2)
[rtsp url documentation](https://www.leadtools.com/help/leadtools/v20/multimedia/transforms/rtsp-source-url-syntax.html)
