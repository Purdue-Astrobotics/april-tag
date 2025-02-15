import robotpy_apriltag as apriltag
import cv2

camera_id = 0 #1 for external

#open camera
cap = cv2.VideoCapture(camera_id)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

detector = apriltag.AprilTagDetector()
detector.addFamily('tag36h11')

#To add a family of tags to the detector, run detector.addFamily(<tag>) on a family from the list below.

#tags = ['tag16h5', 'tag25h9', 'tag36h11', 'tagCircle21h7', 'tagCircle49h12', 'tagCustom48h12', 'tagStandard41h12', 'tagStandard52h13']

def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
    results = detector.detect(gray_image)

    corners = [result.getCorner(i) for i in range(4) for result in results] #get corners of apriltag
    
    if corners: #draw bounding box
        #print((corners[0].x, corners[0].y))
        #cv2.rectangle(vid, (int(corners[0].x), int(corners[0].y)), (int(corners[2].x), int(corners[2].y)), (0, 255, 0), 4) #draw rectangle
        cv2.line(vid, (int(corners[0].x), int(corners[0].y)), (int(corners[1].x), int(corners[1].y)), (0, 255, 0), 4)
        cv2.line(vid, (int(corners[1].x), int(corners[1].y)), (int(corners[2].x), int(corners[2].y)), (0, 255, 0), 4)
        cv2.line(vid, (int(corners[2].x), int(corners[2].y)), (int(corners[3].x), int(corners[3].y)), (0, 255, 0), 4)
        cv2.line(vid, (int(corners[3].x), int(corners[3].y)), (int(corners[0].x), int(corners[0].y)), (0, 255, 0), 4)

    return results

while True:
    ret, frame = cap.read()  # Read frame from the camera
    if not ret:
        print("Failed to grab frame")   
        break

    detect_bounding_box(frame)  # Detect and draw bounding boxes

    # Display the frame
    cv2.imshow("External Camera Feed", frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# Release the camera and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
