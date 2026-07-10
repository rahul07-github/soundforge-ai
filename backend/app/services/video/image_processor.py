<<<<<<< HEAD
"""
Project : SoundForge AI

Module : Image Processor

Description:
Professional cinematic image processing for AI Music Video Generation.
"""

import random
=======
##   ==== 

>>>>>>> origin
import cv2
import numpy as np

from backend.app.utils.logger import log_info, log_error
<<<<<<< HEAD
from backend.app.utils.constants import (
    VIDEO_WIDTH,
    VIDEO_HEIGHT
)
=======
from backend.app.utils.constants import VIDEO_WIDTH, VIDEO_HEIGHT
>>>>>>> origin


class ImageProcessor:
    """
<<<<<<< HEAD
    Professional Image Processor
    """

    def __init__(self):

        log_info("ImageProcessor initialized.")

    ###########################################################
    # Resize Landscape Image
    ###########################################################

    def resize_and_crop(self, image):

        h, w = image.shape[:2]

        target_ratio = VIDEO_WIDTH / VIDEO_HEIGHT
        image_ratio = w / h

        if image_ratio > target_ratio:

            new_h = VIDEO_HEIGHT
            new_w = int(new_h * image_ratio)

        else:

            new_w = VIDEO_WIDTH
            new_h = int(new_w / image_ratio)

        image = cv2.resize(
            image,
            (new_w, new_h),
            interpolation=cv2.INTER_LINEAR
        )

        x = (new_w - VIDEO_WIDTH) // 2
        y = (new_h - VIDEO_HEIGHT) // 2
=======
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
>>>>>>> origin

        image = image[
            y:y + VIDEO_HEIGHT,
            x:x + VIDEO_WIDTH
        ]

        return image
<<<<<<< HEAD

    ###########################################################
    # Portrait Background Blur
    ###########################################################

    def blur_background(self, image):

        background = cv2.resize(
            image,
            (VIDEO_WIDTH, VIDEO_HEIGHT)
=======
    
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
>>>>>>> origin
        )

        background = cv2.GaussianBlur(
            background,
<<<<<<< HEAD
            (81, 81),
=======
            (51, 51),
>>>>>>> origin
            0
        )

        return background
    

<<<<<<< HEAD
    ############################################################
    # Color Grading
    ############################################################

    def color_grade(
        self,
        image,
        brightness=1.02,
        contrast=1.08,
        saturation=1.15
    ):
        """
        Apply cinematic color grading.
        """

        image = image.astype("float32")

        # Brightness
        image *= brightness

        # Contrast
        image = (image - 127.5) * contrast + 127.5

        image = image.clip(0, 255).astype("uint8")

        # Saturation
        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2HSV
        )

        hsv = hsv.astype("float32")

        hsv[:, :, 1] *= saturation

        hsv[:, :, 1] = hsv[:, :, 1].clip(0, 255)

        hsv = hsv.astype("uint8")

        image = cv2.cvtColor(
            hsv,
            cv2.COLOR_HSV2RGB
        )

        return image
    


    ############################################################
    # Depth / Parallax
    ############################################################

    def apply_parallax(
        self,
        image,
        frame_id
    ):
        """
        Create fake depth by moving foreground
        slightly more than background.
        """

        h, w = image.shape[:2]

        crop = 60

        image = image[
            crop:h-crop,
            crop:w-crop
        ]

        image = cv2.resize(
            image,
            (VIDEO_WIDTH, VIDEO_HEIGHT)
        )

        return image

    ###########################################################
    # Portrait Fit
    ###########################################################

    def fit_portrait(self, image):
=======
    def fit_portrait(self, image):
        """
        Place portrait image over blurred background.
        """
>>>>>>> origin

        background = self.blur_background(image)

        h, w = image.shape[:2]

        scale = min(
            VIDEO_WIDTH / w,
            VIDEO_HEIGHT / h
        )

        new_w = int(w * scale)
<<<<<<< HEAD

=======
>>>>>>> origin
        new_h = int(h * scale)

        foreground = cv2.resize(
            image,
<<<<<<< HEAD
            (new_w, new_h),
            interpolation=cv2.INTER_LINEAR
=======
            (
                new_w,
                new_h
            )
>>>>>>> origin
        )

        x = (VIDEO_WIDTH - new_w) // 2
        y = (VIDEO_HEIGHT - new_h) // 2

        background[
            y:y + new_h,
            x:x + new_w
        ] = foreground

        return background

<<<<<<< HEAD
    ###########################################################
    # Brightness
    ###########################################################

    def adjust_brightness(self, image):

        value = random.randint(-10, 15)

        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2HSV
        )

        hsv = np.array(hsv, dtype=np.float32)

        hsv[:, :, 2] = np.clip(
            hsv[:, :, 2] + value,
            0,
            255
        )

        hsv = hsv.astype(np.uint8)

        return cv2.cvtColor(
            hsv,
            cv2.COLOR_HSV2RGB
        )

    ###########################################################
    # Contrast
    ###########################################################

    def adjust_contrast(self, image):

        alpha = random.uniform(1.05, 1.25)

        beta = random.randint(-5, 5)

        return cv2.convertScaleAbs(
            image,
            alpha=alpha,
            beta=beta
        )

    ###########################################################
    # Saturation
    ###########################################################

    def adjust_saturation(self, image):

        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2HSV
        )

        hsv = np.array(
            hsv,
            dtype=np.float32
        )

        saturation = random.uniform(
            1.05,
            1.30
        )

        hsv[:, :, 1] *= saturation

        hsv[:, :, 1] = np.clip(
            hsv[:, :, 1],
            0,
            255
        )

        hsv = hsv.astype(np.uint8)

        return cv2.cvtColor(
            hsv,
            cv2.COLOR_HSV2RGB
        )

    ###########################################################
    # Sharpen
    ###########################################################

    def sharpen(self, image):

        kernel = np.array(
            [
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ]
        )

        return cv2.filter2D(
            image,
            -1,
            kernel
        )

    ###########################################################
    # Vignette
    ###########################################################

    def apply_vignette(self, image):

        rows, cols = image.shape[:2]

        kernel_x = cv2.getGaussianKernel(cols, cols / 2)

        kernel_y = cv2.getGaussianKernel(rows, rows / 2)

        kernel = kernel_y * kernel_x.T

        mask = kernel / kernel.max()

        output = np.empty_like(image)

        for i in range(3):

            output[:, :, i] = image[:, :, i] * mask

        return output

    ###########################################################
    # Cinematic Filter
    ###########################################################

    def cinematic_filter(self, image):

        image = self.adjust_brightness(image)

        image = self.adjust_contrast(image)

        image = self.adjust_saturation(image)

        image = self.sharpen(image)

        image = self.apply_vignette(image)

        return image

    ###########################################################
    # Dynamic Ken Burns Effect
    ###########################################################

    def apply_ken_burns(
        self,
        image,
        frame_index
    ):

        h, w = image.shape[:2]

        zoom = random.uniform(
            1.10,
            1.30
        )

        resized = cv2.resize(
            image,
            None,
            fx=zoom,
            fy=zoom
        )

        new_h, new_w = resized.shape[:2]

        mode = frame_index % 8

        if mode == 0:

            x = 0
            y = 0

        elif mode == 1:

            x = new_w - w
            y = 0

        elif mode == 2:

            x = 0
            y = new_h - h

        elif mode == 3:

            x = new_w - w
            y = new_h - h

        elif mode == 4:

            x = (new_w - w) // 2
            y = 0

        elif mode == 5:

            x = (new_w - w) // 2
            y = new_h - h

        elif mode == 6:

            x = 0
            y = (new_h - h) // 2

        else:

            x = new_w - w
            y = (new_h - h) // 2

        return resized[
            y:y + h,
            x:x + w
        ]
    


    ############################################################
    # Main Processor
    ############################################################

    def process_images(
        self,
        scheduled_images: list
    ) -> list:

        """
        Process all scheduled images into cinematic frames.
=======
    def process_images(
        self,
        frames: list,
        scene_images: list
    ) -> list:
        
        """
        Process scene images for each frame.
>>>>>>> origin
        """

        try:

            processed_frames = []

<<<<<<< HEAD
            motion_styles = [
                "zoom_in",
                "zoom_out",
                "pan_left",
                "pan_right",
                "pan_up",
                "pan_down",
                "diagonal_left",
                "diagonal_right"
            ]

            transitions = [
                "crossfade",
                "fade",
                "dissolve"
            ]

            for item in scheduled_images:

                frame = item["frame"]

                image_path = item["image_path"]

                log_info(
                    f"Loading image : {image_path}"
=======
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
>>>>>>> origin
                )

                image = cv2.imread(image_path)

                if image is None:

                    raise FileNotFoundError(
                        f"Image not found : {image_path}"
                    )

<<<<<<< HEAD
                ################################################
                # Portrait / Landscape
                ################################################

                h, w = image.shape[:2]

                if h > w:
=======
                ###################################################
                # Resize
                ###################################################

                height, width = image.shape[:2]

                if height > width:
>>>>>>> origin

                    image = self.fit_portrait(image)

                else:

                    image = self.resize_and_crop(image)
<<<<<<< HEAD

                ################################################
                # Convert RGB
                ################################################
=======
                

                ###################################################
                # Convert BGR → RGB
                ###################################################
>>>>>>> origin

                image = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2RGB
                )

<<<<<<< HEAD
                ################################################
                # Cinematic Filter
                ################################################

                image = self.cinematic_filter(image)

                ################################################
                # Camera Motion
                ################################################

                image = self.apply_ken_burns(
                    image,
                    frame["frame_id"]
                )


                ################################################
                # Color Grading
                ################################################

                image = self.color_grade(
                    image,
                    brightness=item.get("brightness", 1.02),
                    contrast=item.get("contrast", 1.05),
                    saturation=1.15
                )

                image=self.apply_parallax(image, frame["frame_id"])

                # Metadata

                motion = item.get("motion","zoom_in")
                transition = item.get("transition","crossfade")
                processed_frames.append(

=======
                image = self.apply_ken_burns(image,frame["frame_id"])

                ###################################################
                # Store Frame
                ###################################################

                processed_frames.append(
>>>>>>> origin
                    {
                        "frame_id": frame["frame_id"],
                        "image": image.copy(),
                        "start_time": frame["start_time"],
                        "end_time": frame["end_time"],
<<<<<<< HEAD
                        "duration": frame["duration"],
                        "motion": motion,
                        "transition": transition,
                        "zoom": item.get("zoom",1.08),
                        "brightness": item.get("brightness",1.00),
                        "contrast": item.get("contrast",1.05)
                    }
                )
            log_info(
                f"{len(processed_frames)} cinematic frames processed."
            )
            return processed_frames

        except Exception as error:
            log_error(
                f"Image Processing Failed : {error}"
            )
            raise

=======
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
>>>>>>> origin
