import cv2
import numpy as np
import urllib
 
# based on example in https://www.youtube.com/watch?v=2xcUzXataIk 
url = "http://192.168.178.67:8080/?action=snapshot"  # note, the action is set to snapshot,
# in the webviewer it is set to stream
imgResp = urllib.urlopen(url)
print imgResp

imgNp = np.array(bytearray(imgResp.read()), dtype = np.uint8)
img = cv2.imdecode(imgNp,-1)
cv2.imshow("test",img)
cv2.imwrite( "Snapshot.jpg", img );
cv2.waitKey(10000)