"""Vimrc Generator

Usage:
  vimrcgen.py generate -i <input_json> [-o <output_file>]
  vimrcgen.py default-config [-o <output_file>]
  vimrcgen.py (-h | --help)
  vimrcgen.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from docopt import docopt
from config_mgr import ConfigMgr

if __name__ == '__main__':
    args = docopt(__doc__, version='vimrcgen 0.1')
    config_mgr = ConfigMgr()  # type: ConfigMgr

    if args['default-config']:
        config_mgr.write_default_config(args['<output_file>'])
    elif args['generate']:
        config_mgr.generate(args['<input_json>'])
