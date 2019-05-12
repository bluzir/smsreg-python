import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smsreg-python",
    version="1.0.0",
    author="Vladislav Kooklev",
    author_email="kouklevv@gmail.com",
    description="Python client for sms-reg.com API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bluzir/smsreg-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)