import re
import os
from pathlib import Path
from configparser import ConfigParser

from granit.utils import mkdir_images_from_dat_path


def parse_line(source_line: str) -> dict[str, float] | None:
    A, D = 0, 0

    for coord_string in source_line.split(','):
        if len(coord_string.split('=')) >= 2:
            if coord_string.split('=')[0].strip() == 'Az':
                A = float(
                    coord_string.split('=')[-1])

            elif coord_string.split('=')[0].strip() == 'D':
                D = float(
                    coord_string.split('=')[-1])

    return {
        "azimuth": A,
        "distance": D
    }


def parse_so_txt(source_path):
    row_coordinates_dict = {}
    txt_files_list = list(source_path.iterdir())
    for txt_file in sorted(txt_files_list):
        if not re.search("^SO.*txt$", txt_file.name):
            continue

        with open(txt_file) as f:
            cur_coord_list = []
            for line in f.readlines():
                cur_coord_list.append(parse_line(line))

        row_coordinates_dict[txt_file.stem] = cur_coord_list
    return row_coordinates_dict


def create_layout_files(source_path, raw_coords_dict):
    for so_name, coord_list in raw_coords_dict.items():
        if len(coord_list) == 0:
            os.remove(source_path / 'images' / f"{so_name}.jpg")
        else:
            with open(source_path / 'images' / f'{so_name}.txt', 'a') as f:
                for coord_pair in coord_list:
                    f.write(
                        f"0 {round(coord_pair['azimuth'] / 360, 6)} {round(coord_pair['distance'] /1000 / 360, 6)} {round(10 / 360, 6)} {round(5 / 360, 6)}")
                    f.write('\n')


if __name__ == "__main__":

    config = ConfigParser()
    config.read('config.ini')

    source_path = Path(config['DEFAULT']['path_for_autolayout'])
    mkdir_images_from_dat_path(source_path)
    raw_coords_dict = parse_so_txt(source_path)
    create_layout_files(source_path, raw_coords_dict)
