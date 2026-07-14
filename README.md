# 𖤐 𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐

**Multi-Layer Code Protection Engine — Top 10 Encryption Algorithms**

Crafted by **𝓙𝓸𝓴𝓮𝓻丨𝓜4**

> ⚠️ **Proprietary Software** — Copyright © 2026 𝓙𝓸𝓴𝓮𝓻丨𝓜4. All rights reserved.

---

## 📦 Installation

```bash
pip install joker-m4
```

Or directly from GitHub:

```bash
pip install git+https://github.com/eiad451/eclipse-cipher.git
```

---

## 🚀 Quick Start

```python
from joker_m4 import JokerM4Engine

engine = JokerM4Engine()

# Encrypt with default ciphers (AES → Serpent → Twofish)
encrypted = engine.encrypt(b"Hello, this is secret data!")
decrypted = engine.decrypt(encrypted)
print("Decrypted:", decrypted.decode())
```

### Choose Your Ciphers

```python
from joker_m4 import JokerM4Engine

engine = JokerM4Engine()

# Single cipher
result = engine.encrypt(b"data", ciphers=["aes"])

# All 10 ciphers
result = engine.encrypt(b"data", ciphers=[
    "aes", "chacha", "camellia", "serpent", "twofish",
    "blowfish", "cast", "des3", "sm4", "seed"
])
```

---

## 🔐 Supported Algorithms (10)

| # | Algorithm | Key Size | Mode |
|---|-----------|----------|------|
| 1 | **AES-256-GCM** | 256-bit | GCM |
| 2 | **ChaCha20-Poly1305** | 256-bit | AEAD |
| 3 | **Camellia-256-CBC** | 256-bit | CBC |
| 4 | **Serpent-256-CBC** | 256-bit | CBC |
| 5 | **Twofish-256-CBC** | 256-bit | CBC |
| 6 | **Blowfish-448-CBC** | 448-bit | CBC |
| 7 | **CAST5-128-CBC** | 128-bit | CBC |
| 8 | **TripleDES-192-CBC** | 192-bit | CBC |
| 9 | **SM4-CBC** | 128-bit | CBC |
| 10 | **SEED-CBC** | 128-bit | CBC |

---

## 🔗 Multi-Layer Chaining

```python
from joker_m4 import JokerM4Engine

engine = JokerM4Engine()

# 4-layer military-grade protection
result = engine.encrypt(
    b"Top secret data",
    ciphers=["aes", "serpent", "twofish", "chacha"]
)
original = engine.decrypt(result)
```

---

## 🛡️ Code Protection

```python
from joker_m4 import JokerM4Engine

engine = JokerM4Engine()

with open("my_script.py", "r") as f:
    code = f.read()

protected = engine.protect_code(
    source_code=code,
    ciphers=["aes", "serpent"],
    rename=True, strip_docs=True, deadcode=True,
    encode_strings=True, fake_imports=True, anti_debug=True
)

with open("protected_script.py", "w") as f:
    f.write(protected)
```

---

## 📁 File Encryption

```python
from joker_m4 import JokerM4Engine

engine = JokerM4Engine()

result = engine.encrypt_file("document.pdf", ciphers=["aes", "twofish", "serpent"])
original = engine.decrypt_file(result, output="decrypted_document.pdf")
```

---

## 🔑 Custom Key

```python
from joker_m4 import JokerM4Engine

engine = JokerM4Engine()
my_key = b"my-secret-key-32bytes-long!!!!!"

encrypted = engine.encrypt(b"data", ciphers=["aes", "chacha"], key=my_key)
decrypted = engine.decrypt(encrypted, key=my_key)
```

---

## ℹ️ Engine Info

```python
from joker_m4 import JokerM4Engine

engine = JokerM4Engine()
print(engine.info())
```

---

## 📦 Build

```bash
pip install build twine
python -m build
twine upload dist/*
```

---

## 📞 Contact

- **Developer:** 𝓙𝓸𝓴𝓮𝓻丨𝓜4
- **Telegram:** [@VT_YC](https://t.me/VT_YC)

---

> 𖤐 **𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐** — Encrypt Everything. Protect Everything. 𖤐
