import logging
import numpy as np
import cv2

from dicom_writer import DICOMWriter
from metadata import generate_uid


logger = logging.getLogger(__name__)


class VideoToDICOMConverter:
    """
    Converts MP4 video files into multi-frame DICOM.
    Each frame becomes a slice in a single DICOM object.
    """

    def __init__(self):
        self.writer = DICOMWriter()

    def extract_frames(self, video_path: str, max_frames: int = None):
        """
        Extract frames from video using OpenCV.
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")

        frames = []
        frame_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Convert BGR → RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)

            frame_count += 1
            if max_frames and frame_count >= max_frames:
                break

        cap.release()

        if not frames:
            raise ValueError("No frames extracted from video")

        return np.array(frames)

    def convert(self, video_path: str, output_path: str, metadata: dict = None, max_frames: int = None):
        """
        Convert MP4 video to multi-frame DICOM.
        """

        if metadata is None:
            metadata = {}

        metadata.setdefault("filename", output_path)
        metadata.setdefault("modality", "OT")
        metadata.setdefault("SeriesInstanceUID", generate_uid())
        metadata.setdefault("StudyInstanceUID", generate_uid())

        logger.info(f"Converting video to DICOM: {video_path}")

        frames = self.extract_frames(video_path, max_frames=max_frames)

        num_frames, rows, cols, channels = frames.shape

        logger.info(f"Extracted frames: {num_frames}, size: {rows}x{cols}")

        # Flatten frames for DICOM PixelData
        pixel_array = frames

        ds = self.writer.create_base_dataset(pixel_array[0], metadata)

        # ---- Multi-frame DICOM tags ----
        ds.NumberOfFrames = str(num_frames)

        # Override pixel data (all frames)
        ds.PixelData = pixel_array.tobytes()

        # Required for multi-frame
        ds.Rows = rows
        ds.Columns = cols
        ds.SamplesPerPixel = 3
        ds.PhotometricInterpretation = "RGB"
        ds.PlanarConfiguration = 0

        self.writer.save(ds, output_path)

        logger.info(f"Video conversion complete: {output_path}")

        return output_path