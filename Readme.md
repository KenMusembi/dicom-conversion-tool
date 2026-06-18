\# Media to DICOM Converter



A lightweight production-ready Python tool that converts \*\*JPEG images and MP4 videos into DICOM files\*\* compatible with systems like:



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

\- Compatible with most PACS servers ingestion

\- Transfer syntax: Explicit VR Little Endian



\---



\## 🏗 How to Run it


\- For image

python media_to_dicom.py \
  --image input.jpg \
  --output output.dcm \
  --patient_name "John Doe" \
  --patient_id "12345"

\- For Video
python media_to_dicom.py \
  --video input.mp4 \
  --output output.dcm \
  --patient_name "John Doe" \
  --patient_id "12345"
  --max_frames 60

 have the max frame as 60 as most videos above this will caus ean import error 

