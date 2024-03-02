import struct
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

# Colormap creating
norm = Normalize(-1, 1)
CMAP = LinearSegmentedColormap.from_list("", [[norm(-1.0), "0"], [norm(1.0), "yellow"]])  # black

"""Source buffer cls"""


class Buffer:
    def __init__(self, dat_file_path: Path):
        """Init numpy array from path to SO dat file"""
        buffer = []
        dat_file = open(dat_file_path, "rb").read()

        for i in range(0, len(dat_file), 2):
            buffer.append(struct.unpack("<H", dat_file[i : i + 2]))

        self.matrix = np.reshape(np.array(buffer), (2048, 1200)).T

    def save_jpg(self, jpg_fname: Path) -> None:
        plt.imsave(fname=jpg_fname, arr=self.matrix, cmap=CMAP, format="jpg")


class DatConverter:
    def __init__(self, dat_path: Path, images_path: Path):
        self.dat_path = dat_path
        self.images_path = images_path

    def get_dat_files(self):
        return list(self.dat_path.glob("*.dat"))

    def convert(self):
        for dat_file_path in self.get_dat_files():
            jpg_fname = self.images_path / (dat_file_path.stem + ".jpg")
            if jpg_fname.exists():
                continue
            Buffer(dat_file_path=dat_file_path).save_jpg(jpg_fname=jpg_fname)
