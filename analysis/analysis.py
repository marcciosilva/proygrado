import sys

import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import proygrado.problem_classification.problem_instance_classifier

def main():
    proygrado.problem_classification.problem_instance_classifier.classify_problem_instance('../')
