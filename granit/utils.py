import shutil
from pathlib import Path
import time

import os
import re
from loguru import logger

from granit.Buffer import Buffer


def mkdir_images_from_dat_path(dat_path: Path, CF=0) -> str | None:
    """
    creating directory with jpg files by path with dat files
    """
    try:
        buffers = list(dat_path.iterdir())
    except FileNotFoundError as err:
        return str(err)

    image_path = dat_path / 'images'
    if not os.path.exists(image_path):
        os.mkdir(image_path)

    for buf in sorted(buffers):
        if not re.search("^SO.*dat$", buf.name):
            continue

        jpg_fname = image_path / (buf.stem + '.jpg')
        if jpg_fname.exists():
            continue

        Buffer(dat_file_path=dat_path / buf, CF=CF).save_jpg(jpg_fname=jpg_fname)
        logger.info(f"Save {buf.stem}.jpg to {image_path}")


def move_processed_dat(source_path: Path) -> str | None:
    logger.info('Move processed dat')
    try:
        buffers = list(source_path.iterdir())
    except FileNotFoundError as err:
        return str(err)

    processed_path = Path.joinpath(source_path, "processed")
    if not os.path.exists(processed_path):
        os.mkdir(processed_path)

    for buf in sorted(buffers):
        if not re.search("^SO.*dat$", buf.name):
            continue
        Path.rename(buf, processed_path / buf.name)


def handle_resolved_dirs(source_path: Path,
                         is_rm_images=True,
                         is_move_dat_to_processed=True):

    if is_rm_images:
        shutil.rmtree(
            source_path / "images"
        )
    if is_move_dat_to_processed:
        move_processed_dat(
            source_path=source_path
        )


def stopwatch(func):
    start_time = time.time()
    func()
    end_time = time.time()
    return round((end_time - start_time), 2)
