from setuptools import setup, find_packages

setup(
    name="conversation-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "requests>=2.26.0",
        "tqdm>=4.62.0",
        "jupyter>=1.0.0",
        "pytest>=6.2.5",
        "python-dotenv>=0.19.0"
    ],
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Generador de conversaciones sintéticas con gobierno conversacional",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/conversation-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8"
)