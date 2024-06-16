from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """

    Returns:
        List of requirements mentioned in the requirements.txt file
    """
    requirements:List[str]= []
    with open('requirements.txt') as f:
        for line in f.readlines():
            requirements.append(line)
    return requirements



setup(
    name="text-speech-classification",
    version="1.0.0",
    description="This is an end to end NLP pipeline for classification of hate speech",
    author="Pranay",
    author_email="pranaynaik007@hotmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)