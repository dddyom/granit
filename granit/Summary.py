import json
import shutil
import sys
from pathlib import Path
import re


class Summary:
    def __init__(self, project_path, source_path, exp_name):
        # path to default summaries (exp/labels)
        self.project_path = project_path
        self.save_path = source_path  # path for save_summaries
        self.exp_name = exp_name

        self.exp_path = self.get_creating_exp_path()
        print(self.exp_path)

    def write_custom_summaries(self, rm_exp=True):
        if not self.exp_path:
            sys.exit("exp path not found")

        all_summary_list = []
        for label in sorted(list((self.exp_path / 'labels').iterdir())):
            with open(label, 'r') as f:
                single_coord_list = f.read().splitlines()
                all_summary_list.append(self.format_all_summary_line(single_coord_list))

            single_log_path = self.save_path / (label.stem + '_r.txt')
            if not single_log_path.exists():
                for coord in single_coord_list:
                    self.write_single(
                        single_log_path=single_log_path,
                        dict_coord=json.loads(coord)
                    )
        if rm_exp:
            shutil.rmtree(self.exp_path)  # remove dir and all contains
        else:
            self.write_all(all_log_path=self.save_path / 'summary.txt',
                           all_summary_list=all_summary_list)

    @staticmethod
    def format_all_summary_line(single_coord_list):
        return '; '.join([f"azimuth={json.loads(coord)['a']}, distance={json.loads(coord)['d']}" for coord in single_coord_list])

    @staticmethod
    def write_all(all_log_path, all_summary_list):
        with open(all_log_path, 'a') as f:
            for single_line in all_summary_list:
                f.write(f"{single_line}\n")

    @staticmethod
    def write_single(single_log_path, dict_coord):
        with open(single_log_path, 'a') as f:
            f.write(
                f"Az = {dict_coord['a']:.2f}, D = {dict_coord['d'] * 1000:.2f},  N\n")

    def get_creating_exp_path(self) -> Path | None:
        correct: list[Path] = []
        for exp in self.project_path.iterdir():
            if re.search(f"^{self.exp_name}", exp.name):
                correct.append(exp)
        if correct:
            return sorted(correct)[-1]
