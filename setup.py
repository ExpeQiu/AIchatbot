from setuptools import setup, find_packages

setup(
    name="raspberry-chatbot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=0.19.0",
        "pyaudio>=0.2.11",
        "SpeechRecognition>=3.8.1",
        "gTTS>=2.2.3",
        "openai>=0.27.0",
        "pvporcupine>=2.1.0",
        "requests>=2.26.0",
        "sentence-transformers>=2.2.0",
        "faiss-cpu>=1.7.0",
        "numpy>=1.19.5",
        "netifaces>=0.11.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Raspberry Pi based voice assistant with various features",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/raspberry-chatbot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
) 