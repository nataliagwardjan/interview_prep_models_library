from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="interview_prep_models_library",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    description="Shared Pydantic models for Interview Prep App",
    url="https://github.com/nataliagwardjan/interview_prep_models_library",
)
