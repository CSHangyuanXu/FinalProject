import cv2


stream_addr2 ='rtsp://192.168.1.115:9554/webcam'
cap = cv2.VideoCapture(stream_addr2)

while(True):
  ret, frame = cap.read()
  cv2.imshow('capture', frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
