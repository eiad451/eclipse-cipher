"""
𖤐 𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐 — JokerM4 Encryption Engine
Setup script for PyPI publishing.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="joker-m4",
    version="1.0.0",
    author="𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐",
    author_email="joker@sanctum.dev",
    description="𖤐 𝕰𝖈𝖑𝖎𝖕𝖘𝖊 — Multi-Layer Encryption Engine by 𝓙𝓸𝓴𝓮𝓻丨𝓜4. 10 Top-Tier Ciphers (AES-256, ChaCha20, Serpent, Twofish, Camellia, Blowfish, CAST, TripleDES, SM4, SEED)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eiad451/eclipse-cipher",
    project_urls={
        "Telegram": "https://t.me/VT_YC",
        "Source": "https://github.com/eiad451/eclipse-cipher",
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pycryptodome>=3.15.0",
        "cryptography>=41.0.0",
    ],
    keywords=[
        "encryption", "aes", "chacha20", "serpent", "twofish",
        "camellia", "blowfish", "cast5", "tripledes", "sm4", "seed",
        "cryptography", "security", "joker", "protection",
        "multi-layer", "code-protection", "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    ],
)
