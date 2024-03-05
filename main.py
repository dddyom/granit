import os
import pathlib
import platform
from pathlib import Path

import yolov5
from dotenv import load_dotenv

import util.config as c
from util import DatConverter, log

if platform.system() == "Windows":
    pathlib.PosixPath = pathlib.WindowsPath

load_dotenv()


def main():
    log.info("Загружается модель нейросети")
    try:
        model = yolov5.load(Path(c.WEIGHTS))


        model.conf = float(os.environ.get("THRES", 0.1))
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


    all_path = Path(c.RESULTS) / "all.txt"
    if all_path.exists():
        os.remove(all_path)

    for img_file in img_files:

        log.info("Поиск на " + img_file.name)
        result_path = Path(c.RESULTS) / (img_file.stem + "_r.txt")
        if result_path.exists():
            os.remove(result_path)
        results = model(img_file, size=c.IMG_SIZE)

        if os.environ.get('SHOW_RESULTS', False):
          results.show()

        predictions = results.pred[0]
        with open(Path(c.RESULTS) / "all.txt", "a") as f:
            f.write(f"{img_file.name}\n")

        for det in reversed(predictions):
            xyxy = det[:4]
            # conf = det[4]
            # cls = det[5]

            x = int(xyxy[0] + ((xyxy[2] - xyxy[0]) / 2))
            y = int(xyxy[1] + ((xyxy[3] - xyxy[1]) / 2))
            azimuth = round((x / 2048) * 360, 3)
            distance = round((y / 1200) * 360, 3)

            s = f"Az = {azimuth:.2f}, D = {distance * 1000:.2f},  N\n"

            with open(Path(c.RESULTS) / (img_file.stem + "_r.txt"), "w") as f:
                f.write(s)


            with open(Path(c.RESULTS) / "all.txt", "a") as f:
                f.write('\t' + s)

        with open(Path(c.RESULTS) / "all.txt", "a") as f:
            f.write('\n')


    log.info("Поиск завершен")
    log.info("Результаты записаны в " + c.RESULTS)


if __name__ == "__main__":
    main()
