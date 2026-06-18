import os
import datetime
import logging

import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian, SecondaryCaptureImageStorage

from metadata import (
    generate_uid,
    get_dicom_datetime,
    get_default_patient_metadata,
    get_default_study_metadata,
    get_default_series_metadata
)


logger = logging.getLogger(__name__)


class DICOMWriter:
    """
    Core DICOM writer responsible for creating and saving DICOM files.
    """

    def __init__(self):
        self.transfer_syntax = ExplicitVRLittleEndian
        self.sop_class = SecondaryCaptureImageStorage

    def create_base_dataset(self, pixel_array, metadata: dict) -> FileDataset:
        """
        Create a base DICOM dataset from pixel data and metadata.
        """

        filename = metadata.get("filename", "output.dcm")

        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = self.sop_class
        file_meta.MediaStorageSOPInstanceUID = generate_uid()
        file_meta.ImplementationClassUID = generate_uid()
        file_meta.TransferSyntaxUID = self.transfer_syntax

        ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

        # ---- Patient ----
        patient = get_default_patient_metadata(metadata)
        ds.PatientName = patient["PatientName"]
        ds.PatientID = patient["PatientID"]

        # ---- Study ----
        study = get_default_study_metadata(metadata)
        ds.StudyInstanceUID = study["StudyInstanceUID"]
        ds.StudyDate = study["StudyDate"]
        ds.StudyTime = study["StudyTime"]
        ds.StudyDescription = study["StudyDescription"]

        # ---- Series ----
        series = get_default_series_metadata(metadata)
        ds.SeriesInstanceUID = series["SeriesInstanceUID"]
        ds.SeriesNumber = series["SeriesNumber"]

        # ---- SOP ----
        ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
        ds.SOPClassUID = self.sop_class

        # ---- Image ----
        ds.Modality = metadata.get("modality", "OT")
        ds.PhotometricInterpretation = "RGB" if len(pixel_array.shape) == 3 else "MONOCHROME2"
        ds.SamplesPerPixel = 3 if len(pixel_array.shape) == 3 else 1
        ds.Rows, ds.Columns = pixel_array.shape[:2]

        if ds.SamplesPerPixel == 3:
            ds.PlanarConfiguration = 0

        ds.BitsAllocated = 8
        ds.BitsStored = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0

        ds.PixelData = pixel_array.tobytes()

        # ---- Timing ----
        ds.ContentDate, ds.ContentTime = get_dicom_datetime()

        return ds

    def save(self, dataset: FileDataset, output_path: str):
        """
        Save DICOM dataset to disk safely.
        """

        directory = os.path.dirname(output_path)

        # FIX: handle empty directory (current folder case)
        if directory:
            os.makedirs(directory, exist_ok=True)

        dataset.is_little_endian = True
        dataset.is_implicit_VR = False

        dataset.save_as(output_path, write_like_original=False)

        logger.info(f"DICOM saved: {output_path}")