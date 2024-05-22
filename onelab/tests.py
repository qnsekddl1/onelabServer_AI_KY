from django.test import TestCase

# Create your tests here.
import joblib
# import numpy as np
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from member.models import Member

import joblib
import os
# import numpy as np
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tag.models import Tag
from member.models import Member
from onelab.models import OneLab
import os.path
from pathlib import Path

model = joblib.load(os.path.join(Path(__file__).resolve().parent, '../ai/api/test_onelab.pkl'))

print(model)