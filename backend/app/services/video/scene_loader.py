from pathlib import Path

from backend.app.utils.logger import log_info, log_error


class SceneLoader:
    """
    Load all scene images from storage/datasets/Images.
    """

    def __init__(self):
        self.scene_folder = Path(
            "backend/app/storage/datasets/Images"
        )
        log_info("SceneLoader initialized.")

    def load_images(self) -> list:
        """Load all images from the scenes folder.Returns
        -------
        list
            List of image paths.
        """
        try:
            if not self.scene_folder.exists():

                raise FileNotFoundError(
                    f"Scene folder not found : {self.scene_folder}"
                )
            image_extensions = (
                "*.jpg",
                "*.jpeg",
                "*.png",
                "*.webp"
            )
            scene_images = []
            for extension in image_extensions:
                scene_images.extend(
                    self.scene_folder.glob(extension)
                )
            scene_images = sorted(scene_images)
            if len(scene_images) == 0:

                raise Exception(
                    "No scene images found."
                )
            log_info(
                f"{len(scene_images)} scene images loaded."
            )
            return [
                str(image)
                for image in scene_images
            ]
        except Exception as error:
            log_error(
                f"Scene Loading Failed : {error}"
            )
            raise