import argparse
import os
import logging

from image_converter import ImageToDICOMConverter
from video_converter import VideoToDICOMConverter
from logger import setup_logger


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert media (JPG/MP4) to DICOM format"
    )

    parser.add_argument("--image", help="Path to input image (JPG/PNG)")
    parser.add_argument("--video", help="Path to input video (MP4)")
    parser.add_argument("--output", required=True, help="Output DICOM file path")

    parser.add_argument("--patient_name", default="Anonymous")
    parser.add_argument("--patient_id", default="000000")

    parser.add_argument("--modality", default="OT")
    parser.add_argument("--max_frames", type=int, default=None, help="Limit video frames")

    return parser.parse_args()


def build_metadata(args):
    return {
        "PatientName": args.patient_name,
        "PatientID": args.patient_id,
        "modality": args.modality,
    }


def main():
    setup_logger()
    logger = logging.getLogger(__name__)

    args = parse_args()
    metadata = build_metadata(args)

    if args.image and args.video:
        raise ValueError("Provide either --image or --video, not both")

    if not args.image and not args.video:
        raise ValueError("You must provide either --image or --video")

    # ---- IMAGE ----
    if args.image:
        logger.info("Starting image to DICOM conversion")

        converter = ImageToDICOMConverter()
        converter.convert(
            image_path=args.image,
            output_path=args.output,
            metadata=metadata
        )

    # ---- VIDEO ----
    elif args.video:
        logger.info("Starting video to DICOM conversion")

        converter = VideoToDICOMConverter()
        converter.convert(
            video_path=args.video,
            output_path=args.output,
            metadata=metadata,
            max_frames=args.max_frames
        )

    logger.info("Conversion completed successfully")


if __name__ == "__main__":
    main()