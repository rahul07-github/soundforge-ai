##   ==== 

import cv2
import numpy as np

from backend.app.utils.logger import log_info, log_error
from backend.app.utils.constants import VIDEO_WIDTH, VIDEO_HEIGHT


class ImageProcessor:
    """
    Image processing for AI Video Generation.
    """

    def __init__(self):
        log_info("ImageProcessor initialized.")
    
    def apply_ken_burns(
        self,
        image,
        frame_index: int
    ):
        """
        Apply Ken Burns Effect
        (Zoom + Pan).
        """

        height, width = image.shape[:2]

        #################################################
        # Zoom
        #################################################

        zoom = 1.10

        resized = cv2.resize(
            image,
            None,
            fx=zoom,
            fy=zoom
        )

        new_height, new_width = resized.shape[:2]

        #################################################
        # Pan Direction
        #################################################

        mode = frame_index % 4

        if mode == 0:

            # Left → Right

            start_x = 0
            start_y = (new_height - height) // 2

        elif mode == 1:

            # Right → Left

            start_x = new_width - width
            start_y = (new_height - height) // 2

        elif mode == 2:

            # Top → Bottom

            start_x = (new_width - width) // 2
            start_y = 0

        else:

            # Bottom → Top

            start_x = (new_width - width) // 2
            start_y = new_height - height

        #################################################
        # Crop
        #################################################

        cropped = resized[
            start_y:start_y + height,
            start_x:start_x + width
        ]

        return cropped

    def resize_and_crop(self, image):
        """
        Resize image while maintaining aspect ratio
        and crop center.
        """

        height, width = image.shape[:2]

        target_ratio = VIDEO_WIDTH / VIDEO_HEIGHT
        image_ratio = width / height

        if image_ratio > target_ratio:

            new_height = VIDEO_HEIGHT
            new_width = int(new_height * image_ratio)

        else:

            new_width = VIDEO_WIDTH
            new_height = int(new_width / image_ratio)

        image = cv2.resize(
            image,
            (
                new_width,
                new_height
            )
        )

        x = (new_width - VIDEO_WIDTH) // 2
        y = (new_height - VIDEO_HEIGHT) // 2

        image = image[
            y:y + VIDEO_HEIGHT,
            x:x + VIDEO_WIDTH
        ]

        return image
    
    def blur_background(self, image):
        """
        Create blurred background for portrait images.
        """

        background = cv2.resize(
            image,
            (
                VIDEO_WIDTH,
                VIDEO_HEIGHT
            )
        )

        background = cv2.GaussianBlur(
            background,
            (51, 51),
            0
        )

        return background
    

    def fit_portrait(self, image):
        """
        Place portrait image over blurred background.
        """

        background = self.blur_background(image)

        h, w = image.shape[:2]

        scale = min(
            VIDEO_WIDTH / w,
            VIDEO_HEIGHT / h
        )

        new_w = int(w * scale)
        new_h = int(h * scale)

        foreground = cv2.resize(
            image,
            (
                new_w,
                new_h
            )
        )

        x = (VIDEO_WIDTH - new_w) // 2
        y = (VIDEO_HEIGHT - new_h) // 2

        background[
            y:y + new_h,
            x:x + new_w
        ] = foreground

        return background

    def process_images(
        self,
        frames: list,
        scene_images: list
    ) -> list:
        
        """
        Process scene images for each frame.
        """

        try:

            processed_frames = []

            ###################################################
            # Validate Scene Images
            ###################################################

            if len(scene_images) < len(frames):

                raise Exception(
                    f"Not enough scene images.\n"
                    f"Required : {len(frames)}\n"
                    f"Available : {len(scene_images)}"
                )

            ###################################################
            # Process Each Scene Image
            ###################################################

            for frame, image_path in zip(frames, scene_images):

                log_info(
                    f"Loading scene image : {image_path}"
                )

                image = cv2.imread(image_path)

                if image is None:

                    raise FileNotFoundError(
                        f"Image not found : {image_path}"
                    )

                ###################################################
                # Resize
                ###################################################

                height, width = image.shape[:2]

                if height > width:

                    image = self.fit_portrait(image)

                else:

                    image = self.resize_and_crop(image)
                

                ###################################################
                # Convert BGR → RGB
                ###################################################

                image = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2RGB
                )

                image = self.apply_ken_burns(image,frame["frame_id"])

                ###################################################
                # Store Frame
                ###################################################

                processed_frames.append(
                    {
                        "frame_id": frame["frame_id"],
                        "image": image.copy(),
                        "start_time": frame["start_time"],
                        "end_time": frame["end_time"],
                        "duration": frame["duration"]
                    }
                )

            log_info(
                f"{len(processed_frames)} images processed."
            )

            return processed_frames

        except Exception as error:

            log_error(
                f"Image Processing Failed : {error}"
            )
            raise