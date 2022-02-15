import os

from ..fundamentals.template import load_templates # import the Template and Templates class so load

path = os.path.dirname(os.path.abspath(__file__))
load_templates(path)