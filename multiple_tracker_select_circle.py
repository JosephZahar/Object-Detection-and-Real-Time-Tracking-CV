import cv2
import pandas as pd

centerx = []
centery = []

circle_x1 = []
circle_y1 = []

circle_x2 = []
circle_y2 = []

circle_x3 = []
circle_y3 = []

rect_x4 = []
rect_y4 = []

rect_x5 = []
rect_y5 = []

# define path of video
n_track = 6
experiment_name = "Exp4_10"
cap = cv2.VideoCapture(f"/Volumes/LaCie/Fadi FYP Experiments/Rotation Experiment 4/{experiment_name}.MOV")
trackers = cv2.legacy.MultiTracker_create()

ret, frame = cap.read()
# zoom on frame
# frame = frame[2350:3400, 400:1450]

# define number of object to track
for i in range(n_track):
    cv2.imshow("Tracking Box", frame)
    boundarybox_i = cv2.selectROI("Select Box", frame, False)
    tracker_i = cv2.legacy.TrackerCSRT_create()
    trackers.add(tracker_i, frame, boundarybox_i)

def keepBox(frame, boundarybox):
    x, y, width, height = int(boundarybox[0]), int(boundarybox[1]), int(boundarybox[2]), int(boundarybox[3])
    cv2.rectangle(frame, (x,y), ((x+width),(y+height)),(0, 255, 0), 2, 1)
    cv2.putText(frame, "Tracking Mark", (25, 25), cv2.FONT_HERSHEY_COMPLEX, 0.8, (225,6,0), 2)

while True:
    ret, frame = cap.read()
    try:
        frame = frame[:, :]
    except TypeError:

        data = pd.DataFrame(list(zip(centerx, centery, circle_x1, circle_y1, circle_x2, circle_y2, circle_x3, circle_y3, rect_x4, rect_y4, rect_x5, rect_y5)),
                            columns=['centerx', 'centery', 'circle_x1', 'circle_y1', 'circle_x2', 'circle_y2', 'circle_x3', 'circle_y3', 'rect_x4', 'rect_y4', 'rect_x5', 'rect_y5'])
        data.to_csv(f'{experiment_name}.csv')

    ret, boundaryboxes = trackers.update(frame)

    centerx.append(boundaryboxes[0][0] + boundaryboxes[0][2]/2)
    centery.append(boundaryboxes[0][1] + boundaryboxes[0][3]/2)
    circle_x1.append(boundaryboxes[1][0] + boundaryboxes[1][2] / 2)
    circle_y1.append(boundaryboxes[1][1] + boundaryboxes[1][3] / 2)
    circle_x2.append(boundaryboxes[2][0] + boundaryboxes[2][2] / 2)
    circle_y2.append(boundaryboxes[2][1] + boundaryboxes[2][3] / 2)
    circle_x3.append(boundaryboxes[3][0] + boundaryboxes[3][2] / 2)
    circle_y3.append(boundaryboxes[3][1] + boundaryboxes[3][3] / 2)
    rect_x4.append(boundaryboxes[4][0] + boundaryboxes[4][2] / 2)
    rect_y4.append(boundaryboxes[4][1] + boundaryboxes[4][3] / 2)
    rect_x5.append(boundaryboxes[5][0] + boundaryboxes[5][2] / 2)
    rect_y5.append(boundaryboxes[5][1] + boundaryboxes[5][3] / 2)

    for boundarybox in boundaryboxes:
        if ret:
            keepBox(frame, boundarybox)
        else:
            cv2.putText(frame, "Lost Mark", (25, 25), cv2.FONT_HERSHEY_COMPLEX, 0.8, (8,39,245), 2)

    cv2.imshow("Tracking Box", frame)

    if cv2.waitKey(1) & 0xff==ord('q'):
        break

cap.release()
cv2.DestroyAllWindows()
