import os

from ..fundamentals import load_templates # import the Template and Templates class

path = os.path.dirname(os.path.abspath(__file__))
load_templates(path)