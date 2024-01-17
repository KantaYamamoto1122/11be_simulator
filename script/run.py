import main
import config
import csv
import numpy as np


for i in range(1,10):
    config.LOAD = i
    main.main()