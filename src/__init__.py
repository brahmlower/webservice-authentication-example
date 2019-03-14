import sys
import yaml

from .server import BuildingsApi

def load_config(cfg_path):
    try:
        with open(cfg_path, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                sys.exit(exc)
    except FileNotFoundError:
        sys.exit("No such file or directory: '{}'".format(cfg_path))
    except:
        sys.exit("General error while opening config file: '{}'".format(cfg_path))

def build_app(settings_path="./settings.yml"):
    """ Main entrypoint for Building API """
    app_config = load_config(settings_path)
    app = BuildingsApi(app_config)
    return app
