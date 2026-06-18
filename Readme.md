\# Media to DICOM Converter



A lightweight production-ready Python tool that converts \*\*JPEG images and MP4 videos into DICOM files\*\* compatible with systems like:



\- Orthanc PACS

\- DICOM viewers (OHIF, RadiAnt, etc.)

\- Medical imaging workflows (secondary capture use cases)



\---



\## 📌 Features



\### 🖼 Image Conversion

\- JPEG / PNG → DICOM (Secondary Capture)

\- RGB and grayscale support

\- Automatic metadata injection

\- Orthanc-compatible output



\### 🎥 Video Conversion

\- MP4 → Multi-frame DICOM

\- OpenCV-based frame extraction

\- RGB frame stacking into single DICOM instance

\- Configurable frame limits



\### 🧠 Metadata Support

\- Patient ID \& Name

\- Study / Series UID generation

\- Timestamping (DICOM-compliant)

\- Extensible metadata system



\### 📦 Output

\- Standard DICOM (.dcm)

\- Compatible with Orthanc ingestion

\- Transfer syntax: Explicit VR Little Endian



\---



\## 🏗 Project Structure



