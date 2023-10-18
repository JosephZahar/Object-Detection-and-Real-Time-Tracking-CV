import cv2
import pandas as pd


x1 = []
y1 = []


video_name = 9721
n_track = 1
experiment_name = "CatheterExp_9"
cap = cv2.VideoCapture(f"/Volumes/LaCie/Fadi FYP Experiments/Catheter Experiment/{experiment_name}.MOV")
trackers = cv2.legacy.MultiTracker_create()

ret, frame = cap.read()
frame = frame[:, :]

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

        data = pd.DataFrame(list(zip(x1, y1)),
                            columns=['cat_x1', 'cat_y1'])
        data.to_csv(f'{experiment_name}.csv')

    ret, boundaryboxes = trackers.update(frame)

    x1.append(boundaryboxes[0][0] + boundaryboxes[0][2] / 2)
    y1.append(boundaryboxes[0][1] + boundaryboxes[0][3] / 2)

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
