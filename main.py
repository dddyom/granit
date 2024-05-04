import os
import pathlib
import platform
import time
from pathlib import Path

import yolov5
from dotenv import load_dotenv
from watchdog.observers import Observer

import util.config as c
from util import DatConverter, FolderListener, Predictor, log

if platform.system() == "Windows":
    pathlib.PosixPath = pathlib.WindowsPath

load_dotenv()


def load_model():
    log.info("Загружается модель нейросети")
    try:
        model = yolov5.load(Path(c.WEIGHTS))
        model.conf = float(os.environ.get("THRES", 0.1))
        return model
    except Exception:
        log.error("Не удалось загрузить модель")
        return


def convert_dat_buffers():
    dat_converter = DatConverter(Path(c.BUFFERS), Path(c.IMAGES))

    if not dat_converter.has_dat_files():
        log.warning(f"Файлы dat в {c.BUFFERS} не обнаружены")
        return
    else:
        log.info("Запущена конвертация dat в jpg")
        dat_converter.convert()


def predict(model):
    img_files = list(Path(c.IMAGES).glob("*.jpg"))

    log.info("Запускается предсказание и запись в txt")

    all_path = Path(c.RESULTS) / "all.txt"
    if all_path.exists():
        os.remove(all_path)

    for img_file in img_files:
        Predictor(img_file, model).call()

    log.info("Поиск завершен")
    log.info("Результаты записаны в " + c.RESULTS)


def default_run(model):
    convert_dat_buffers()
    predict(model)


def run_as_folder_listener(model):
    folder_path = Path(c.BUFFERS)

    observer = Observer()
    observer.schedule(FolderListener(model=model), folder_path, recursive=True)
    observer.start()

    try:
        log.info("Запущен слушатель изменений в " + str(folder_path))
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def main():
    model = load_model()
    if not model:
        log.info("Модель загружена")
        return

    if os.environ.get("BUFFER_LISTENER"):
        run_as_folder_listener(model)
    else:
        default_run(model)


if __name__ == "__main__":
    main()
