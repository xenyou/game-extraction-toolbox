
import importlib
from inspect import isclass
import inspect
import os
import pkgutil
import sys
import types

from gex.lib.tasks.basetask import BaseTask

def cleanpath(path_str):
    if path_str.startswith("\""):
        path_str = path_str[1:]
    if path_str.endswith("\""):
        path_str = path_str[:-1]
    return path_str

def preparepath(out_path):
    if not os.path.exists(out_path):
        try:
            os.makedirs(out_path)
        except Exception as x:
            raise Exception("Cannot create output folder.")
    else:
        if not os.access(out_path, os.W_OK):
            raise Exception("Cannot write to output folder.")

def load_task(task):
    package = f'gex.lib.tasks.impl.{task}'
    transform_module = importlib.import_module(package)
    clsmembers = inspect.getmembers(transform_module, inspect.isclass)
    for name, typedef in clsmembers:
        if not name == 'BaseTask' and issubclass(typedef, BaseTask):
            return typedef()
    return None
