import cv2
import cameras.utils_database as utils_database

def list_available_cameras(max_index=10):
    """
    Returns a list of available webcam indices by attempting to open each one.
    
    Args:
        max_index (int): Maximum index to check.

    Returns:
        List[int]: Indices of available cameras.
    """
    available_cameras = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras

def take_a_photo(status="healthy", plant_id=1, camera_index=0):
    """
    Captures a photo from the specified webcam, displays it briefly,
    and uploads it to the database.

    Args:
        status (str): Health status of the plant (e.g. 'healthy', 'sick').
        plant_id (int): Numeric ID of the plant.
        camera_index (int): Index of the camera to use.
    """
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"ERROR.1 = Unable to open webcam with index {camera_index}")
        return

    ret, frame = cap.read()
    if not ret:
        print("ERROR.2 = Failed to capture frame from webcam")
    else:
        # Convert the frame to bytes (JPEG format)
        _, buffer = cv2.imencode('.jpg', frame)
        photo_bytes = buffer.tobytes()

        # Upload the photo to the database
        success = utils_database.post_photo(photo_bytes, status, plant_id)
        if success:
            print("INFO.1 = Photo uploaded to database successfully")
        else:
            print("ERROR.3 = Failed to upload photo to database")

    cap.release()
    cv2.destroyAllWindows()

def save_photo_to_file(photo_data, output_path):
    """
    Saves raw photo bytes to a file.

    Args:
        photo_data (bytes): Binary data of the photo.
        output_path (str): Full path where the file should be saved.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(output_path, 'wb') as file:
            file.write(photo_data)
        print(f"INFO.2 = Photo saved to: {output_path}")
        return True
    except Exception as e:
        print(f"ERROR.4 = Failed to save photo to file: {e}")
        return False
