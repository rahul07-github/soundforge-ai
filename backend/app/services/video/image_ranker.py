import open_clip
import torch
import cv2

from PIL import Image

from backend.app.utils.logger import (
    log_info,
    log_error
)


class ImageRanker:
    """
    Rank images using classical image quality metrics
    combined with CLIP-based semantic similarity to a prompt.
    """

    def __init__(self):

        log_info("ImageRanker initialized.")

        self.device = (
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained="laion2b_s34b_b79k",
            device=self.device
        )

        self.model.eval()

        self.tokenizer = open_clip.get_tokenizer("ViT-B-32")

        log_info(f"CLIP model loaded on device : {self.device}")

    ####################################################
    # Sharpness
    ####################################################

    def sharpness(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    ####################################################
    # Brightness
    ####################################################

    def brightness(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return hsv[:, :, 2].mean()

    ####################################################
    # Contrast
    ####################################################

    def contrast(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray.std()

    ####################################################
    # Resolution
    ####################################################

    def resolution(self, image):
        h, w = image.shape[:2]
        return w * h

    ####################################################
    # Normalize
    ####################################################

    def normalize(self, value, maximum):
        if maximum == 0:
            return 0
        return value / maximum

    ####################################################
    # CLIP Score (was completely missing — now implemented)
    ####################################################

    def clip_score(self, image_path: str, prompt: str) -> float:
        """
        Compute semantic similarity between an image and a
        text prompt using CLIP embeddings (cosine similarity).
        """

        try:

            image = Image.open(image_path).convert("RGB")

            image_input = self.preprocess(image).unsqueeze(0).to(self.device)

            text_input = self.tokenizer([prompt]).to(self.device)

            with torch.no_grad():

                image_features = self.model.encode_image(image_input)
                text_features = self.model.encode_text(text_input)

                image_features = image_features / image_features.norm(
                    dim=-1, keepdim=True
                )
                text_features = text_features / text_features.norm(
                    dim=-1, keepdim=True
                )

                similarity = (image_features @ text_features.T).item()

            # Cosine similarity is between -1 and 1; normalize to 0-1
            normalized_similarity = (similarity + 1) / 2

            return round(normalized_similarity, 4)

        except Exception as error:
            log_error(f"CLIP Score Failed for {image_path} : {error}")
            return 0.0

    ####################################################
    # Rank Images
    ####################################################

    def rank_images(self, image_paths: list, prompt: str) -> list:

        try:

            temp_scores = []

            for image_path in image_paths:

                image = cv2.imread(image_path)

                if image is None:
                    continue

                sharp = self.sharpness(image)
                bright = self.brightness(image)
                contrast = self.contrast(image)
                resolution = self.resolution(image)

                clip_similarity = self.clip_score(image_path, prompt)

                temp_scores.append({
                    "image_path": image_path,
                    "sharpness": sharp,
                    "brightness": bright,
                    "contrast": contrast,
                    "resolution": resolution,
                    "clip_score": clip_similarity
                })

            if not temp_scores:
                return []

            max_sharp = max(item["sharpness"] for item in temp_scores)
            max_bright = 255
            max_contrast = max(item["contrast"] for item in temp_scores)
            max_resolution = max(item["resolution"] for item in temp_scores)

            results = []

            for item in temp_scores:

                quality_score = (
                    0.40 * self.normalize(item["sharpness"], max_sharp)
                    + 0.20 * self.normalize(item["brightness"], max_bright)
                    + 0.20 * self.normalize(item["contrast"], max_contrast)
                    + 0.20 * self.normalize(item["resolution"], max_resolution)
                )

                quality_score = round(quality_score, 4)

                final_score = (
                    0.40 * quality_score
                    + 0.60 * item["clip_score"]
                )

                item["quality_score"] = quality_score
                item["final_score"] = round(final_score, 4)

                results.append(item)

            results.sort(
                key=lambda x: x["final_score"],
                reverse=True
            )

            log_info(
                f"{len(results)} images ranked using CLIP."
            )

            return results

        except Exception as error:
            log_error(f"Image Ranking Failed : {error}")
            raise