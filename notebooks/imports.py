import torch
import torch.nn as nn
import torchvision
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from torchvision.datasets.kinetics import Kinetics400

from IPython.display import Video
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

Path.ls = lambda x: [o.name for o in x.iterdir()]