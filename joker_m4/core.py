"""
𖤐 𝕰𝖈𝖑𝖎𝖕𝖘𝖊 Core Engine 𖤐
Multi-layer encryption chaining engine with code protection.
"""

import os
import re
import base64
import random
import json
import hashlib
from base64 import b64encode, b64decode

from joker_m4.ciphers import (
    encrypt_aes256_gcm, decrypt_aes256_gcm,
    encrypt_chacha20_poly1305, decrypt_chacha20_poly1305,
    encrypt_camellia256_cbc, decrypt_camellia256_cbc,
    encrypt_serpent256_cbc, decrypt_serpent256_cbc,
    encrypt_twofish256_cbc, decrypt_twofish256_cbc,
    encrypt_blowfish448_cbc, decrypt_blowfish448_cbc,
    encrypt_cast5_128_cbc, decrypt_cast5_128_cbc,
    encrypt_tripledes192_cbc, decrypt_tripledes192_cbc,
    encrypt_sm4_cbc, decrypt_sm4_cbc,
    encrypt_seed_cbc, decrypt_seed_cbc,
    _derive_key,
)

CIPHER_MAP = {
    "aes": encrypt_aes256_gcm,
    "chacha": encrypt_chacha20_poly1305,
    "camellia": encrypt_camellia256_cbc,
    "serpent": encrypt_serpent256_cbc,
    "twofish": encrypt_twofish256_cbc,
    "blowfish": encrypt_blowfish448_cbc,
    "cast": encrypt_cast5_128_cbc,
    "des3": encrypt_tripledes192_cbc,
    "sm4": encrypt_sm4_cbc,
    "seed": encrypt_seed_cbc,
}

DECRYPT_MAP = {
    "aes": decrypt_aes256_gcm,
    "chacha": decrypt_chacha20_poly1305,
    "camellia": decrypt_camellia256_cbc,
    "serpent": decrypt_serpent256_cbc,
    "twofish": decrypt_twofish256_cbc,
    "blowfish": decrypt_blowfish448_cbc,
    "cast": decrypt_cast5_128_cbc,
    "des3": decrypt_tripledes192_cbc,
    "sm4": decrypt_sm4_cbc,
    "seed": decrypt_seed_cbc,
}

CIPHER_NAMES = {
    "aes": "AES-256-GCM",
    "chacha": "ChaCha20-Poly1305",
    "camellia": "Camellia-256-CBC",
    "serpent": "Serpent-256-CBC",
    "twofish": "Twofish-256-CBC",
    "blowfish": "Blowfish-448-CBC",
    "cast": "CAST5-128-CBC",
    "des3": "TripleDES-192-CBC",
    "sm4": "SM4-CBC",
    "seed": "SEED-CBC",
}

JOKER_HEADER = b"ECLIPSE_V1"
SIGNATURE_TEXT = (
    "Protected by 𝕰𝖈𝖑𝖎𝖕𝖘𝖊 Encryption Engine\n"
    "Copyright © 2026 𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐\n"
    "Crafted with 暗黒 — All Rights Reserved\n"
    "Contact: Telegram @VT_YC\n"
)


class JokerM4Engine:
    """
    𖤐 𝕰𝖈𝖑𝖎𝖕𝖘𝖊 Multi-Layer Encryption Engine 𖤐
    By 𝓙𝓸𝓴𝓮𝓻丨𝓜4
    
    Encrypt data with any combination of the top 10 encryption algorithms,
    chained in sequence for maximum security.
    
    Usage:
        engine = JokerM4Engine()
        result = engine.encrypt(b"secret data", ciphers=["aes"])
        original = engine.decrypt(result)
    """
    
    def __init__(self):
        self.version = "1.0.0"
        self.author = "𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐"
    
    def encrypt(self, plaintext: bytes, ciphers: list = None, key: bytes = None) -> dict:
        if ciphers is None:
            ciphers = ["aes", "serpent", "twofish"]
        for c in ciphers:
            if c not in CIPHER_MAP:
                raise ValueError(f"Unknown cipher: {c}. Available: {list(CIPHER_MAP.keys())}")
        
        result = {
            "format": "joker_v1",
            "author": "𝓙𝓸𝓴𝓮𝓻丨𝓜4",
            "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐",
            "ciphers": ciphers,
            "chain": [CIPHER_NAMES[c] for c in ciphers],
            "key_protected": key is not None,
            "layers": [],
        }
        
        data = plaintext
        for i, cid in enumerate(ciphers):
            layer_key = None
            if key is not None:
                layer_key = _derive_key(key, f"joker_layer_{i}".encode(), 32)[:self._key_size(cid)]
            
            enc_func = CIPHER_MAP[cid]
            layer_result = enc_func(data, key=layer_key)
            result["layers"].append({
                "index": i,
                "algorithm": CIPHER_NAMES[cid],
                "cipher_id": cid,
                "data": layer_result,
            })
            data = b64decode(layer_result["ciphertext"])
        
        return result
    
    def decrypt(self, encrypted: dict, key: bytes = None) -> bytes:
        ciphers = encrypted["ciphers"]
        layers = encrypted["layers"]
        
        data = None
        for i, layer in enumerate(reversed(layers)):
            cid = layer["cipher_id"]
            layer_data = layer["data"]
            
            layer_key = None
            if key is not None:
                layer_key = _derive_key(key, f"joker_layer_{len(ciphers)-1-i}".encode(), 32)[:self._key_size(cid)]
            
            if data is not None:
                layer_data["ciphertext"] = b64encode(data).decode()
            
            dec_func = DECRYPT_MAP[cid]
            data = dec_func(layer_data, key=layer_key)
        
        return data
    
    def _key_size(self, cipher_id: str) -> int:
        sizes = {
            "aes": 32, "chacha": 32, "camellia": 32, "serpent": 32,
            "twofish": 32, "blowfish": 56, "cast": 16, "des3": 24,
            "sm4": 16, "seed": 16,
        }
        return sizes.get(cipher_id, 32)
    
    def encrypt_file(self, filepath: str, ciphers: list = None, key: bytes = None, output: str = None) -> dict:
        with open(filepath, "rb") as f:
            data = f.read()
        
        header = JOKER_HEADER + b"\n" + SIGNATURE_TEXT.encode() + b"\n"
        result = self.encrypt(header + data, ciphers=ciphers, key=key)
        
        if output:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        
        return result
    
    def decrypt_file(self, encrypted: dict, key: bytes = None, output: str = None) -> bytes:
        data = self.decrypt(encrypted, key=key)
        
        if data[:len(JOKER_HEADER)] == JOKER_HEADER:
            data = data[len(JOKER_HEADER):]
            sig_end = data.find(b"\n\n")
            if sig_end != -1:
                data = data[sig_end+2:]
        
        if output:
            with open(output, "wb") as f:
                f.write(data)
        
        return data
    
    def protect_code(self, source_code: str, ciphers: list = None, key: bytes = None,
                     rename: bool = True, strip_docs: bool = True,
                     deadcode: bool = True, encode_strings: bool = False,
                     fake_imports: bool = False, anti_debug: bool = False) -> str:
        
        result = source_code
        
        if fake_imports:
            fake_imports_list = [
                'import sys, json, csv, re, math',
                'from os import path, getcwd, listdir',
                'import warnings, traceback, logging',
                'from collections import defaultdict, Counter',
                'import itertools, functools, operator',
                'from datetime import datetime, timedelta',
            ]
            random.shuffle(fake_imports_list)
            result = '\n'.join(fake_imports_list[:3]) + '\n' + result
        
        if strip_docs:
            result = re.sub(r"'''[\s\S]*?'''", '', result)
            result = re.sub(r'"""[\s\S]*?"""', '', result)
            result = re.sub(r'#.*$', '', result, flags=re.MULTILINE)
        
        if encode_strings:
            result = re.sub(r'"([^"\\]*(\\.[^"\\]*)*)"', self._encode_string, result)
            result = re.sub(r"'([^'\\]*(\\.[^'\\]*)*)'", self._encode_string, result)
        
        if rename:
            result = self._rename_identifiers(result)
        
        if deadcode:
            deads = ['_ = lambda: None', 'if 0: pass', '_x = 0xdeadbeef', '_ = [_ for _ in []]']
            result = re.sub(
                r'^(\s*def\s+\w+\s*\([^)]*\):\s*)$',
                lambda m: m.group(1) + '\n    ' + random.choice(deads),
                result,
                flags=re.MULTILINE
            )
        
        if anti_debug:
            ads = ['if __debug__: pass', 'import sys as _sys; _sys_settrace = getattr(_sys, "settrace", lambda: None)']
            result = re.sub(r'^(import\s+)', random.choice(ads) + '\n\\1', result, flags=re.MULTILINE)
        
        result = (
            f'# ===== Protected by 𝕰𝖈𝖑𝖎𝖕𝖘𝖊 Encryption Engine =====\n'
            f'# Copyright © 2026 𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐\n'
            f'# Telegram: @VT_YC\n'
            f'# ================================================\n\n'
            + result
        )
        
        if ciphers:
            loader = self._generate_loader(result, ciphers, key)
            return loader
        
        return result
    
    def _encode_string(self, match):
        s = match.group(1)
        if len(s) < 3:
            return match.group(0)
        enc = base64.b64encode(s.encode()).decode()
        return f"__import__('base64').b64decode('{enc}').decode()"
    
    def _rename_identifiers(self, source):
        id_map = {}
        counter = 0
        skip = {
            'self', 'cls', 'True', 'False', 'None', '__init__', '__name__',
            '__main__', '__file__', '__class__', '__dict__', '__doc__',
            '__module__', '__builtins__', '__import__', 'range', 'len',
            'print', 'int', 'str', 'list', 'dict', 'set', 'tuple', 'float',
            'bool', 'bytes', 'bytearray', 'object', 'type', 'super',
            'staticmethod', 'classmethod', 'property', 'enumerate', 'zip',
            'map', 'filter', 'sorted', 'reversed', 'open', 'hasattr',
            'getattr', 'setattr', 'isinstance', 'issubclass', 'eval', 'exec',
            'compile', 'Exception', 'BaseException', 'ValueError', 'TypeError',
            'KeyError', 'IndexError', 'AttributeError', 'ImportError',
            'ModuleNotFoundError', 'NameError', 'SyntaxError',
        }
        
        for m in re.finditer(r'(?:def|class)\s+(\w+)', source):
            name = m.group(1)
            if name not in skip and name not in id_map:
                counter += 1
                id_map[name] = f'_{counter:04x}'
        
        for m in re.finditer(r'def\s+\w+\s*\([^)]*\)', source):
            args = re.findall(r'\b([a-zA-Z_]\w*)\b', m.group(0))
            for a in args:
                if a not in skip and a != 'def' and a not in id_map:
                    counter += 1
                    id_map[a] = f'_{counter:04x}'
        
        for orig, repl in sorted(id_map.items(), key=lambda x: -len(x[0])):
            source = re.sub(r'\b' + re.escape(orig) + r'\b', repl, source)
        
        return source
    
    def _generate_loader(self, source, ciphers, key=None):
        encrypted = self.encrypt(source.encode(), ciphers=ciphers, key=key)
        payload_json = json.dumps(encrypted, ensure_ascii=False)
        payload_b64 = base64.b64encode(payload_json.encode()).decode()
        
        loader = f'''
# ===== Protected by 𝕰𝖈𝖑𝖎𝖕𝖘𝖊 Encryption Engine =====
# Copyright © 2026 𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐
# Telegram: @VT_YC
# Algorithms: {', '.join(CIPHER_NAMES[c] for c in ciphers)}
# ==================================================

import base64 as _b64
import json as _json
from joker_m4 import JokerM4Engine

_JOKER_PAYLOAD = {repr(payload_b64)}

def _joker_run():
    _data = _b64.b64decode(_JOKER_PAYLOAD)
    _enc = _json.loads(_data.decode())
    _engine = JokerM4Engine()
    _code = _engine.decrypt(_enc)
    exec(_code.decode())

if __name__ == '__main__':
    _joker_run()
'''
        return loader.strip()
    
    def list_ciphers(self) -> dict:
        return dict(CIPHER_NAMES)
    
    def info(self) -> dict:
        return {
            "engine": "𝕰𝖈𝖑𝖎𝖕𝖘𝖊 Encryption Engine",
            "version": self.version,
            "author": self.author,
            "contact": "Telegram: @VT_YC",
            "ciphers": len(CIPHER_NAMES),
            "algorithms": list(CIPHER_NAMES.values()),
            "signature": "𝓙𝓸𝓴𝓮𝓻丨𝓜4 : 𖤐𝕰𝖈𝖑𝖎𝖕𝖘𝖊𖤐",
        }
