#!/usr/bin/env python3
"""Display downloaded radar frames as a quick preview slideshow."""

from pathlib import Path
import cv2

WINDOW_NAME = "bom"


def iter_images():
    return sorted(Path(".").glob("*.png"))


def preview_frames() -> None:
    images = iter_images()
    if not images:
        print("No PNG files found to preview.")
        return

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    for image_path in images:
        frame = cv2.imread(str(image_path))
        if frame is None:
            print(f"Skipping unreadable file: {image_path.name}")
            continue
        cv2.imshow(WINDOW_NAME, frame)
        if cv2.waitKey(200) & 0xFF == 27:  # ESC to exit
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    preview_frames()
