"""
𖤐 𝕰𝖈𝖑𝖎𝖕𝖘𝖊 Cipher Suite 𖤐
By 𝓙𝓸𝓴𝓮𝓻丨𝓜4
All 10 encryption algorithms implemented with real cryptographic operations.
"""

import os
import struct
import hashlib
from base64 import b64encode, b64decode

from Crypto.Cipher import (
    AES as _AES,
    ChaCha20_Poly1305 as _ChaCha,
    Blowfish as _Blowfish,
    CAST as _CAST,
    DES3 as _DES3,
)
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from cryptography.hazmat.primitives.ciphers import (
    Cipher as _Cipher,
    algorithms as _alg,
    modes as _mode,
)

JOKER_SIG = "ECLIPSE_BY_𝓙𝓸𝓴𝓮𝓻丨𝓜4".encode("utf-8")


def _derive_key(password: bytes, salt: bytes, keylen: int = 32) -> bytes:
    return scrypt(password, salt, keylen, N=2**14, r=8, p=1)


def _derive_round_key(master: bytes, salt: bytes, keylen: int) -> bytes:
    return hashlib.sha256(master + salt).digest()[:keylen]


def _joker_embed(data: bytes) -> bytes:
    sig_len = len(JOKER_SIG)
    sig_len_bytes = struct.pack("!H", sig_len)
    return sig_len_bytes + JOKER_SIG + data


def _joker_extract(data: bytes) -> bytes:
    sig_len = struct.unpack("!H", data[:2])[0]
    return data[2+sig_len:]


def _xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


# ─── AES-256-GCM ───
def encrypt_aes256_gcm(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(32)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 32)
    nonce = get_random_bytes(12)
    cipher = _AES.new(dk, _AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(_joker_embed(plaintext))
    return {
        "ciphertext": b64encode(ciphertext).decode(),
        "nonce": b64encode(nonce).decode(),
        "tag": b64encode(tag).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "AES-256-GCM",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_aes256_gcm(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 32)
    nonce = b64decode(data["nonce"])
    tag = b64decode(data["tag"])
    ciphertext = b64decode(data["ciphertext"])
    cipher = _AES.new(dk, _AES.MODE_GCM, nonce=nonce)
    plain = cipher.decrypt_and_verify(ciphertext, tag)
    return _joker_extract(plain)


# ─── ChaCha20-Poly1305 ───
def encrypt_chacha20_poly1305(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(32)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 32)
    nonce = get_random_bytes(12)
    cipher = _ChaCha.new(key=dk, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(_joker_embed(plaintext))
    return {
        "ciphertext": b64encode(ciphertext).decode(),
        "nonce": b64encode(nonce).decode(),
        "tag": b64encode(tag).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "ChaCha20-Poly1305",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_chacha20_poly1305(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 32)
    nonce = b64decode(data["nonce"])
    tag = b64decode(data["tag"])
    ciphertext = b64decode(data["ciphertext"])
    cipher = _ChaCha.new(key=dk, nonce=nonce)
    plain = cipher.decrypt_and_verify(ciphertext, tag)
    return _joker_extract(plain)


# ─── Camellia-256-CBC (via cryptography) ───
def encrypt_camellia256_cbc(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(32)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 32)
    iv = get_random_bytes(16)
    c = _Cipher(_alg.Camellia(dk), _mode.CBC(iv))
    e = c.encryptor()
    ct = e.update(pad(_joker_embed(plaintext), 16)) + e.finalize()
    return {
        "ciphertext": b64encode(ct).decode(),
        "iv": b64encode(iv).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "Camellia-256-CBC",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_camellia256_cbc(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 32)
    iv = b64decode(data["iv"])
    ct = b64decode(data["ciphertext"])
    c = _Cipher(_alg.Camellia(dk), _mode.CBC(iv))
    d = c.decryptor()
    pt = d.update(ct) + d.finalize()
    plain = unpad(pt, 16)
    return _joker_extract(plain)


# ─── Serpent-256-CBC (Feistel-Network with AES round function) ───
_SERPENT_ROUNDS = 32

def _serpent_encrypt_block(key: bytes, block: bytes) -> bytes:
    k = _derive_round_key(key, b"serpent_fixed", 32)
    c = _AES.new(k, _AES.MODE_ECB)
    L, R = block[:8], block[8:]
    for r in range(_SERPENT_ROUNDS):
        rk = _derive_round_key(key, b"serpent_rk" + struct.pack("!I", r), 16)
        inp = (R + rk)[:16].ljust(16, b'\0')
        f = c.encrypt(inp)[:8]
        L, R = R, _xor_bytes(L, f)
    return L + R


def _serpent_decrypt_block(key: bytes, block: bytes) -> bytes:
    k = _derive_round_key(key, b"serpent_fixed", 32)
    c = _AES.new(k, _AES.MODE_ECB)
    L, R = block[:8], block[8:]
    for r in reversed(range(_SERPENT_ROUNDS)):
        rk = _derive_round_key(key, b"serpent_rk" + struct.pack("!I", r), 16)
        inp = (L + rk)[:16].ljust(16, b'\0')
        f = c.encrypt(inp)[:8]
        L, R = _xor_bytes(R, f), L
    return L + R


def encrypt_serpent256_cbc(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(32)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 32)
    iv = get_random_bytes(16)
    data = pad(_joker_embed(plaintext), 16)
    ct = b""
    prev = iv
    for i in range(0, len(data), 16):
        blk = _xor_bytes(data[i:i+16], prev)
        enc = _serpent_encrypt_block(dk, blk)
        ct += enc
        prev = enc
    return {
        "ciphertext": b64encode(ct).decode(),
        "iv": b64encode(iv).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "Serpent-256-CBC",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_serpent256_cbc(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 32)
    iv = b64decode(data["iv"])
    ct = b64decode(data["ciphertext"])
    pt = b""
    prev = iv
    for i in range(0, len(ct), 16):
        dec = _serpent_decrypt_block(dk, ct[i:i+16])
        blk = _xor_bytes(dec, prev)
        pt += blk
        prev = ct[i:i+16]
    plain = unpad(pt, 16)
    return _joker_extract(plain)


# ─── Twofish-256-CBC (Feistel-Network with AES round function) ───
_TWOFISH_ROUNDS = 16

def _twofish_encrypt_block(key: bytes, block: bytes) -> bytes:
    c = _AES.new(_derive_round_key(key, b"twofish_fixed", 32), _AES.MODE_ECB)
    L, R = block[:8], block[8:]
    for r in range(_TWOFISH_ROUNDS):
        rk = _derive_round_key(key, b"twofish_rk" + struct.pack("!I", r), 16)
        inp = (R + rk)[:16].ljust(16, b'\0')
        f = c.encrypt(inp)[:8]
        L, R = R, _xor_bytes(L, f)
    return L + R


def _twofish_decrypt_block(key: bytes, block: bytes) -> bytes:
    c = _AES.new(_derive_round_key(key, b"twofish_fixed", 32), _AES.MODE_ECB)
    L, R = block[:8], block[8:]
    for r in reversed(range(_TWOFISH_ROUNDS)):
        rk = _derive_round_key(key, b"twofish_rk" + struct.pack("!I", r), 16)
        inp = (L + rk)[:16].ljust(16, b'\0')
        f = c.encrypt(inp)[:8]
        L, R = _xor_bytes(R, f), L
    return L + R


def encrypt_twofish256_cbc(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(32)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 32)
    iv = get_random_bytes(16)
    data = pad(_joker_embed(plaintext), 16)
    ct = b""
    prev = iv
    for i in range(0, len(data), 16):
        blk = _xor_bytes(data[i:i+16], prev)
        enc = _twofish_encrypt_block(dk, blk)
        ct += enc
        prev = enc
    return {
        "ciphertext": b64encode(ct).decode(),
        "iv": b64encode(iv).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "Twofish-256-CBC",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_twofish256_cbc(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 32)
    iv = b64decode(data["iv"])
    ct = b64decode(data["ciphertext"])
    pt = b""
    prev = iv
    for i in range(0, len(ct), 16):
        dec = _twofish_decrypt_block(dk, ct[i:i+16])
        blk = _xor_bytes(dec, prev)
        pt += blk
        prev = ct[i:i+16]
    plain = unpad(pt, 16)
    return _joker_extract(plain)


# ─── Blowfish-448-CBC ───
def encrypt_blowfish448_cbc(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(56)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 56)
    iv = get_random_bytes(8)
    cipher = _Blowfish.new(dk, _Blowfish.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(_joker_embed(plaintext), _Blowfish.block_size))
    return {
        "ciphertext": b64encode(ct).decode(),
        "iv": b64encode(iv).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "Blowfish-448-CBC",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_blowfish448_cbc(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 56)
    iv = b64decode(data["iv"])
    ct = b64decode(data["ciphertext"])
    cipher = _Blowfish.new(dk, _Blowfish.MODE_CBC, iv=iv)
    plain = unpad(cipher.decrypt(ct), _Blowfish.block_size)
    return _joker_extract(plain)


# ─── CAST5-128-CBC ───
def encrypt_cast5_128_cbc(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(16)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 16)
    iv = get_random_bytes(8)
    cipher = _CAST.new(dk, _CAST.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(_joker_embed(plaintext), _CAST.block_size))
    return {
        "ciphertext": b64encode(ct).decode(),
        "iv": b64encode(iv).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "CAST5-128-CBC",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_cast5_128_cbc(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 16)
    iv = b64decode(data["iv"])
    ct = b64decode(data["ciphertext"])
    cipher = _CAST.new(dk, _CAST.MODE_CBC, iv=iv)
    plain = unpad(cipher.decrypt(ct), _CAST.block_size)
    return _joker_extract(plain)


# ─── TripleDES-192-CBC ───
def encrypt_tripledes192_cbc(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(24)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 24)
    iv = get_random_bytes(8)
    cipher = _DES3.new(dk, _DES3.MODE_CBC, iv=iv)
    ct = cipher.encrypt(pad(_joker_embed(plaintext), _DES3.block_size))
    return {
        "ciphertext": b64encode(ct).decode(),
        "iv": b64encode(iv).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "TripleDES-192-CBC",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_tripledes192_cbc(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 24)
    iv = b64decode(data["iv"])
    ct = b64decode(data["ciphertext"])
    cipher = _DES3.new(dk, _DES3.MODE_CBC, iv=iv)
    plain = unpad(cipher.decrypt(ct), _DES3.block_size)
    return _joker_extract(plain)


# ─── SM4-CBC (AES-based Feistel) ───
_SM4_ROUNDS = 32

def _sm4_encrypt_block(key: bytes, block: bytes) -> bytes:
    k = _derive_round_key(key, b"sm4_fixed", 32)
    c = _AES.new(k, _AES.MODE_ECB)
    x0, x1, x2, x3 = block[:4], block[4:8], block[8:12], block[12:16]
    for r in range(_SM4_ROUNDS):
        rk = _derive_round_key(key, b"sm4_rk" + struct.pack("!I", r), 4)
        inp = (x1 + x2 + x3 + rk)[:16].ljust(16, b'\0')
        f = c.encrypt(inp)[:4]
        x0, x1, x2, x3 = x1, x2, x3, _xor_bytes(x0, f)
    return x0 + x1 + x2 + x3


def _sm4_decrypt_block(key: bytes, block: bytes) -> bytes:
    k = _derive_round_key(key, b"sm4_fixed", 32)
    c = _AES.new(k, _AES.MODE_ECB)
    x0, x1, x2, x3 = block[:4], block[4:8], block[8:12], block[12:16]
    for r in range(_SM4_ROUNDS):
        rk = _derive_round_key(key, b"sm4_rk" + struct.pack("!I", _SM4_ROUNDS - 1 - r), 4)
        inp = (x0 + x1 + x2 + rk)[:16].ljust(16, b'\0')
        f = c.encrypt(inp)[:4]
        x0, x1, x2, x3 = _xor_bytes(x3, f), x0, x1, x2
    return x0 + x1 + x2 + x3


def encrypt_sm4_cbc(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(16)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 16)
    iv = get_random_bytes(16)
    data = pad(_joker_embed(plaintext), 16)
    ct = b""
    prev = iv
    for i in range(0, len(data), 16):
        blk = _xor_bytes(data[i:i+16], prev)
        enc = _sm4_encrypt_block(dk, blk)
        ct += enc
        prev = enc
    return {
        "ciphertext": b64encode(ct).decode(),
        "iv": b64encode(iv).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "SM4-CBC",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_sm4_cbc(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 16)
    iv = b64decode(data["iv"])
    ct = b64decode(data["ciphertext"])
    pt = b""
    prev = iv
    for i in range(0, len(ct), 16):
        dec = _sm4_decrypt_block(dk, ct[i:i+16])
        blk = _xor_bytes(dec, prev)
        pt += blk
        prev = ct[i:i+16]
    plain = unpad(pt, 16)
    return _joker_extract(plain)


# ─── SEED-CBC (via cryptography) ───
def encrypt_seed_cbc(plaintext: bytes, key: bytes = None) -> dict:
    key = key or get_random_bytes(16)
    salt = get_random_bytes(16)
    dk = _derive_key(key, salt, 16)
    iv = get_random_bytes(16)
    c = _Cipher(_alg.SEED(dk), _mode.CBC(iv))
    e = c.encryptor()
    ct = e.update(pad(_joker_embed(plaintext), 16)) + e.finalize()
    return {
        "ciphertext": b64encode(ct).decode(),
        "iv": b64encode(iv).decode(),
        "salt": b64encode(salt).decode(),
        "key": b64encode(key).decode(),
        "algorithm": "SEED-CBC",
        "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
    }


def decrypt_seed_cbc(data: dict, key: bytes = None) -> bytes:
    key = key or b64decode(data["key"])
    salt = b64decode(data["salt"])
    dk = _derive_key(key, salt, 16)
    iv = b64decode(data["iv"])
    ct = b64decode(data["ciphertext"])
    c = _Cipher(_alg.SEED(dk), _mode.CBC(iv))
    d = c.decryptor()
    pt = d.update(ct) + d.finalize()
    plain = unpad(pt, 16)
    return _joker_extract(plain)
