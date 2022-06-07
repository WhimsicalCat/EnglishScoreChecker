import os
from .GradeSystem import run as GradeSystem
import joblib

cfp = os.path.dirname(os.path.abspath(__file__)) + os.sep

clf = joblib.load(
    "{cfp}{sep}GradeSystem{sep}model{sep}train.pkl".format(sep=os.sep, cfp=cfp)
)


def predict(inputs):
    return clf.predict(inputs)
