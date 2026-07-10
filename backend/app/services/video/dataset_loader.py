"""
Project : SoundForge AI

Module : Dataset Loader

Description:
Load image datasets from selected categories.
"""

from pathlib import Path

from backend.app.utils.logger import (log_info,log_error)

class DatasetLoader:
    """Load image datasets grouped by category."""

    def __init__(self):

        self.dataset_path = Path(
            "backend/app/storage/datasets/Images"
        )

        log_info("DatasetLoader initialized.")

    def load_datasets(
        self,
        categories: list = None
    ) -> dict:
        """
        Load image datasets.
        Parameters
        ----------
        categories : list, optional
            Dataset categories to load.
            If None, load all categories.

        Returns
        -------
        dict
        """

        try:

            
            # Validate Dataset Folder
            

            if not self.dataset_path.exists():

                raise FileNotFoundError(
                    f"Dataset folder not found : {self.dataset_path}"
                )

            # Decide Which Folders To Load

            if categories is None:
                folders = [
                    folder
                    for folder in sorted(
                        self.dataset_path.iterdir()
                    )
                    if folder.is_dir()
                ]

            else:
                folders = []
                for category in categories:
                    folder = self.dataset_path / category
                    if folder.exists() and folder.is_dir():
                        folders.append(folder)

                    else:
                        log_info(
                            f"Category not found : {category}"
                        )
            # Load Images
            datasets = {}

            image_extensions = (
                ".jpg",
                ".jpeg",
                ".png",
                ".webp"
            )

            for folder in folders:
                images = []
                for image in sorted(folder.iterdir()):
                    if (
                        image.is_file()
                        and image.suffix.lower()
                        in image_extensions
                    ):
                        images.append(str(image))

                if images:
                    datasets[folder.name] = images
                    log_info(
                        f"{folder.name} : {len(images)} images"
                    )
            # Validation
            if len(datasets) == 0:

                raise Exception(
                    "No image datasets found."
                )            
            # Success
            log_info(
                f"Loaded Categories : {list(datasets.keys())}"
            )

            return datasets
        
        except Exception as error:
            log_error(
                f"Dataset Loading Failed : {error}"
            )
            raise