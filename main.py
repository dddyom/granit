import os
from pathlib import Path

import yolov5

from util import DatConverter

# Веса обученной сети
WEIGHTS = "weights/best.pt"
# Директория с исходными буферами dat
BUFFERS = "buffers"
# Вероятность, при которой найденные объекты учитываются ( Чувствительность )
CONFIDENCE_THRESHOLD = 0.1
# Путь для директории с результатами предсказания
RESULTS = "results"


IMAGES = "images"
# Размер изображения для нейросети (совпадает с размером, используемым во время обучения)
IMG_SIZE = 1056


def main():
    DatConverter(Path(BUFFERS), Path(IMAGES)).convert()

    model = yolov5.load(WEIGHTS)
    model.conf = float(CONFIDENCE_THRESHOLD)

    img_files = list(Path(IMAGES).glob("*.jpg"))

    for img_file in img_files:
        result_path = Path(RESULTS) / (img_file.stem + "_r.txt")
        if result_path.exists():
            os.remove(result_path)

        results = model(img_file, size=IMG_SIZE)
        predictions = results.pred[0]

        for det in reversed(predictions):
            xyxy = det[:4]
            # conf = det[4]
            # cls = det[5]

            x = int(xyxy[0] + ((xyxy[2] - xyxy[0]) / 2))
            y = int(xyxy[1] + ((xyxy[3] - xyxy[1]) / 2))
            azimuth = round((x / 2048) * 360, 3)
            distance = round((y / 1200) * 360, 3)

            with open(Path(RESULTS) / (img_file.stem + "_r.txt"), "a") as f:
                f.write(f"Az = {azimuth:.2f}, D = {distance * 1000:.2f},  N\n")


if __name__ == "__main__":
    main()
