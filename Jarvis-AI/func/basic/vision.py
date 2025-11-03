"""
Computer Vision Module
Handles face detection, object recognition, and OCR
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
import os


class VisionSystem:
    """
    Class for computer vision operations
    """

    def __init__(self, camera_index: int = 0):
        """
        Initialize vision system

        Args:
            camera_index: Camera device index
        """
        self.camera_index = camera_index
        self.face_cascade = None
        self.eye_cascade = None
        self.ocr_reader = None

        self._load_face_detection()

    def _load_face_detection(self) -> None:
        """
        Load face detection cascade classifiers
        """
        try:
            cascade_path = cv2.data.haarcascades
            face_cascade_path = os.path.join(cascade_path, 'haarcascade_frontalface_default.xml')
            eye_cascade_path = os.path.join(cascade_path, 'haarcascade_eye.xml')

            self.face_cascade = cv2.CascadeClassifier(face_cascade_path)
            self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
        except Exception as e:
            print(f"Error loading face detection: {e}")

    def detect_faces(self, image_path: Optional[str] = None,
                     use_camera: bool = False) -> Tuple[int, Optional[np.ndarray]]:
        """
        Detect faces in image or camera feed

        Args:
            image_path: Path to image file
            use_camera: If True, use camera

        Returns:
            Tuple of (number of faces, annotated image)
        """
        if self.face_cascade is None:
            print("Face detection not initialized")
            return 0, None

        try:
            if use_camera:
                cap = cv2.VideoCapture(self.camera_index)
                ret, frame = cap.read()
                cap.release()
                if not ret:
                    return 0, None
                image = frame
            elif image_path:
                image = cv2.imread(image_path)
            else:
                return 0, None

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(image, (x + ex, y + ey),
                                (x + ex + ew, y + ey + eh), (0, 255, 0), 2)

            return len(faces), image

        except Exception as e:
            print(f"Error detecting faces: {e}")
            return 0, None

    def capture_photo(self, filename: Optional[str] = None) -> Optional[str]:
        """
        Capture photo from camera

        Args:
            filename: Optional filename to save

        Returns:
            Path to saved image or None
        """
        try:
            cap = cv2.VideoCapture(self.camera_index)
            ret, frame = cap.read()
            cap.release()

            if not ret:
                print("Failed to capture image")
                return None

            if filename is None:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"capture_{timestamp}.jpg"

            save_path = os.path.join(os.path.expanduser("~"), "Pictures", filename)
            cv2.imwrite(save_path, frame)
            return save_path

        except Exception as e:
            print(f"Error capturing photo: {e}")
            return None

    def perform_ocr(self, image_path: str, languages: List[str] = ['en']) -> Optional[str]:
        """
        Perform OCR on image

        Args:
            image_path: Path to image
            languages: List of language codes

        Returns:
            Extracted text or None
        """
        try:
            if self.ocr_reader is None:
                import easyocr
                self.ocr_reader = easyocr.Reader(languages)

            result = self.ocr_reader.readtext(image_path)

            text_results = [detection[1] for detection in result]
            extracted_text = ' '.join(text_results)

            return extracted_text if extracted_text else None

        except Exception as e:
            print(f"Error performing OCR: {e}")
            return None

    def detect_objects(self, image_path: Optional[str] = None,
                       use_camera: bool = False) -> List[str]:
        """
        Detect objects in image (basic color detection)

        Args:
            image_path: Path to image file
            use_camera: If True, use camera

        Returns:
            List of detected objects/colors
        """
        try:
            if use_camera:
                cap = cv2.VideoCapture(self.camera_index)
                ret, frame = cap.read()
                cap.release()
                if not ret:
                    return []
                image = frame
            elif image_path:
                image = cv2.imread(image_path)
            else:
                return []

            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            color_ranges = {
                'red': ([0, 100, 100], [10, 255, 255]),
                'blue': ([100, 100, 100], [130, 255, 255]),
                'green': ([40, 100, 100], [80, 255, 255]),
                'yellow': ([20, 100, 100], [40, 255, 255]),
            }

            detected_colors = []
            for color, (lower, upper) in color_ranges.items():
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                if cv2.countNonZero(mask) > 1000:
                    detected_colors.append(color)

            return detected_colors

        except Exception as e:
            print(f"Error detecting objects: {e}")
            return []

    def start_camera_preview(self, duration: int = 10) -> None:
        """
        Start camera preview window

        Args:
            duration: Duration in seconds (0 for indefinite)
        """
        try:
            cap = cv2.VideoCapture(self.camera_index)
            print("Press 'q' to exit camera preview")

            import time
            start_time = time.time()

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow('JARVIS Camera', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                if duration > 0 and (time.time() - start_time) > duration:
                    break

            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"Error in camera preview: {e}")


vision_system = VisionSystem()
