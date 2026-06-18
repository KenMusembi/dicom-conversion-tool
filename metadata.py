import datetime
import uuid
from typing import Dict


# -----------------------------
# UID GENERATION
# -----------------------------
def generate_uid(prefix: str = "1.2.826.0.1.3680043.10.1"):
    """
    Generate a DICOM-compliant UID.
    Default prefix is a safe private root (change for production org usage).
    """
    return f"{prefix}.{uuid.uuid4().int}"


# -----------------------------
# DICOM DATE/TIME HELPERS
# -----------------------------
def get_dicom_datetime():
    """
    Returns current DICOM-formatted date and time.
    """
    now = datetime.datetime.now()

    return now.strftime("%Y%m%d"), now.strftime("%H%M%S")


# -----------------------------
# DEFAULT PATIENT METADATA
# -----------------------------
def get_default_patient_metadata(metadata: Dict):
    return {
        "PatientName": metadata.get("PatientName", "Anonymous^Patient"),
        "PatientID": metadata.get("PatientID", "000000"),
    }


# -----------------------------
# DEFAULT STUDY METADATA
# -----------------------------
def get_default_study_metadata(metadata: Dict):
    now = datetime.datetime.now()

    return {
        "StudyInstanceUID": metadata.get("StudyInstanceUID", generate_uid()),
        "StudyDate": now.strftime("%Y%m%d"),
        "StudyTime": now.strftime("%H%M%S"),
        "StudyDescription": metadata.get("StudyDescription", "Media Conversion Study"),
    }


# -----------------------------
# DEFAULT SERIES METADATA
# -----------------------------
def get_default_series_metadata(metadata: Dict):
    return {
        "SeriesInstanceUID": metadata.get("SeriesInstanceUID", generate_uid()),
        "SeriesNumber": metadata.get("SeriesNumber", 1),
    }


# -----------------------------
# CLEAN METADATA BUILDER (optional utility)
# -----------------------------
def build_dicom_metadata(**kwargs):
    """
    Convenience helper if you want to build metadata inline.
    """
    return {
        "PatientName": kwargs.get("patient_name", "Anonymous^Patient"),
        "PatientID": kwargs.get("patient_id", "000000"),
        "Modality": kwargs.get("modality", "OT"),
        "StudyDescription": kwargs.get("study_description", "Media Conversion Study"),
        "SeriesNumber": kwargs.get("series_number", 1),
    }