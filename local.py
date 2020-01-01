# import libraries
from vidgear.gears import CamGear
import cv2

stream = CamGear(source='myvideo.avi').start()  # open any valid video stream(for e.g `myvideo.avi` file)

# infinite loop
while True:
    frame = stream.read()
    # read frames

    # check if frame is None
    if frame is None:
        # if True break the infinite loop
        break

    # do something with frame here

    cv2.imshow("Output Frame", frame)
    # Show output window

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        # if 'q' key-pressed break out
        break

# close output window
cv2.destroyAllWindows()
# safely close video stream.
stream.stop()
