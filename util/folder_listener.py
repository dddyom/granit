import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .config import BUFFERS, IMAGES
from .dat_converter import DatConverter
from .predictor import Predictor


class FolderListener(FileSystemEventHandler):

    def __init__(self, model):
        super().__init__()
        self.model = model

    def on_created(self, event):
        if not event.is_directory:
            image_file = DatConverter(dat_path=Path(BUFFERS), images_path=Path(IMAGES)).convert_single(
                dat_file_path=Path(event.src_path)
            )

            Predictor(image_file, self.model).call()


if __name__ == "__main__":
    folder_path = Path(BUFFERS)

    observer = Observer()
    observer.schedule(FolderListener(), folder_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
