import logging
import numpy as np
from PIL import Image

from dicom_writer import DICOMWriter
from metadata import generate_uid


logger = logging.getLogger(__name__)


class ImageToDICOMConverter:
    """
    Converts JPEG/PNG images into DICOM format.
    """

    def __init__(self):
        self.writer = DICOMWriter()

    def load_image(self, image_path: str) -> np.ndarray:
        """
        Load image and convert to numpy array.
        """
        img = Image.open(image_path)

        # Convert all images to RGB for consistency
        if img.mode not in ["RGB", "L"]:
            img = img.convert("RGB")

        return np.array(img)

    def convert(self, image_path: str, output_path: str, metadata: dict = None):
        """
        Convert a single image to DICOM.
        """

        if metadata is None:
            metadata = {}

        metadata.setdefault("filename", output_path)
        metadata.setdefault("modality", "OT")
        metadata.setdefault("SeriesInstanceUID", generate_uid())

        logger.info(f"Converting image to DICOM: {image_path}")

        pixel_array = self.load_image(image_path)

        ds = self.writer.create_base_dataset(pixel_array, metadata)
        self.writer.save(ds, output_path)

        logger.info(f"Conversion complete: {output_path}")
        return output_path