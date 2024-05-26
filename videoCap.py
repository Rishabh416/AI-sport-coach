import cv2

class videoRecorder:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        print("videocap")

        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        print("videodimensions")

        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.writer = cv2.VideoWriter('sportVideo.mp4', self.fourcc, 30.0, (1280,720))
        print("videowriter")

        self.recording = False

    def recording(self):
        self.recording = True

        while self.recording:
            ret, frame = self.cap.read(self)

            if ret:
                cv2.imshow('recording', frame)
                if self.recording:
                    self.writer.write(frame)
           
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.recording = False
                print(self.recording)

        self.cap.release()
        self.capwriter.release()
        cv2.destroyAllWindows()