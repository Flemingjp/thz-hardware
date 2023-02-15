import setuptools

setuptools.setup(
    name="thzware",
    version="0.0.1",
    author="James Fleming",
    author_email="jamesfleming91@gmail.com",
    description="Control of THz hardware",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy>=1.23.5",
        "pycromanager==0.26.0",
        "nidaqmx==0.6.4",
    ],
    python_requires=">=3.7.0"
)