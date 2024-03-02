import os
import yolov5

from pathlib import Path
from loguru import logger

from granit.ArgsParser import ArgsParser
# from granit.Summary import Summary
# from granit.utils import handle_resolved_dirs

CONFIG_PATH = '/home/user/code/config.ini'


def main():
    logger.info('parse config')
    args_parser = ArgsParser(CONFIG_PATH)
    logger.info('start detection')
    args = args_parser._args
    print(f'\033[93m{args_parser._args}\033[0m')


    model = yolov5.load(args['weights'])
    model.conf = float(args['conf-thres'])

    img_folder = Path(args['source'])
    img_files = list(img_folder.glob('*.jpg'))

    for img_file in img_files:
        results = model(img_file, size=int(args['imgsz']))

    # results = model(args['source'], augment=True)

    # parse results
    predictions = results.pred[0]
    boxes = predictions[:, :4] # x1, y1, x2, y2
    scores = predictions[:, 4]
    categories = predictions[:, 5]

    print(f'\033[93m{predictions}\033[0m')

    # show detection bounding boxes on image
    results.show()
    # os.system('python detect.py ' + ' '.join(args_parser.get_args()))

    # logger.info('write summary')
    # Summary(
    #     project_path=Path(args_parser.by_key('project')),
    #     source_path=Path(args_parser.by_key('source')),
    #     exp_name=args_parser.by_key('name'),
    # ).write_custom_summaries(rm_exp=False)

    # handle_resolved_dirs(
    #     source_path=Path(args_parser.by_key('source'), ),
    #     is_rm_images=True,
    #     is_move_dat_to_processed=False
    # )
    logger.info('finished')


if __name__ == '__main__':
    main()
