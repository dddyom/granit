import os
from pathlib import Path

import yolov5

import util.config as c
from util import DatConverter, log


def main():
    log.info("Загружается модель нейросети")
    try:
        model = yolov5.load(c.WEIGHTS)
        model.conf = float(c.CONFIDENCE_THRESHOLD)
        log.info("Модель загружена")
    except Exception:
        log.error("Не удалось загрузить модель")
        return

    dat_converter = DatConverter(Path(c.BUFFERS), Path(c.IMAGES))

    if not dat_converter.has_dat_files():
        log.warning(f"Файлы dat в {c.BUFFERS} не обнаружены")
        return
    else:
        log.info("Запущена конвертация dat в jpg")
        dat_converter.convert()

    img_files = list(Path(c.IMAGES).glob("*.jpg"))

    log.info("Запускается предсказание и запись в txt")
    for img_file in img_files:
        log.info("Поиск на " + img_file.name)
        result_path = Path(c.RESULTS) / (img_file.stem + "_r.txt")
        if result_path.exists():
            os.remove(result_path)

        results = model(img_file, size=c.IMG_SIZE)
        predictions = results.pred[0]

        for det in reversed(predictions):
            xyxy = det[:4]
            # conf = det[4]
            # cls = det[5]

            x = int(xyxy[0] + ((xyxy[2] - xyxy[0]) / 2))
            y = int(xyxy[1] + ((xyxy[3] - xyxy[1]) / 2))
            azimuth = round((x / 2048) * 360, 3)
            distance = round((y / 1200) * 360, 3)

            with open(Path(c.RESULTS) / (img_file.stem + "_r.txt"), "a") as f:
                f.write(f"Az = {azimuth:.2f}, D = {distance * 1000:.2f},  N\n")

    log.info("Поиск завершен")
    log.info("Результаты записаны в " + c.RESULTS)


if __name__ == "__main__":
    main()
