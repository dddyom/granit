import os
from dataclasses import dataclass
from pathlib import Path

from yolov5.models.yolo import DetectMultiBackend

from .config import IMG_SIZE, RESULTS
from .logger import log


@dataclass
class Predictor:
    img_file: Path
    model: DetectMultiBackend

    def _get_result_path(self):
        result_path = Path(RESULTS) / (self.img_file.stem + "_r.txt")
        if result_path.exists():
            os.remove(result_path)

        return result_path

    def _predict_and_get_results(self):
        results = self.model(self.img_file, size=IMG_SIZE)

        if os.environ.get("SHOW_RESULTS", False):
            results.show()
        return results.pred[0]

    @staticmethod
    def format_coords(detection):
        xyxy = detection[:4]
        conf = detection[4]
        # cls = det[5]

        x = int(xyxy[0] + ((xyxy[2] - xyxy[0]) / 2))
        y = int(xyxy[1] + ((xyxy[3] - xyxy[1]) / 2))
        azimuth = round((x / 2048) * 360, 3)
        distance = round((y / 1200) * 360, 3)
        return azimuth, distance, conf

    def write_summary(self, path, predictions):
        with open(Path(RESULTS) / "all.txt", "a") as f:
            f.write(f"{self.img_file.name}\n")

        for det in reversed(predictions):
            azimuth, distance, conf = self.format_coords(det)

            s = f"Az = {azimuth:.2f}, D = {distance:.2f}, CONF = {conf:.2f}  N\n"

            with open(Path(RESULTS) / (self.img_file.stem + "_r.txt"), "w") as f:
                f.write(s)

            with open(Path(RESULTS) / "all.txt", "a") as f:
                f.write("\t" + s)

        with open(Path(RESULTS) / "all.txt", "a") as f:
            f.write("\n")

    def call(self):
        log.info("Поиск на " + self.img_file.name)
        result_path = self._get_result_path()
        predictions = self._predict_and_get_results()
        self.write_summary(result_path, predictions)
