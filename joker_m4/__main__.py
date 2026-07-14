"""
𖤐 𝕰𝖈𝖑𝖎𝖕𝖘𝖊 CLI — Run from command line: python -m joker_m4
"""

from joker_m4.core import JokerM4Engine


def main():
    engine = JokerM4Engine()
    info = engine.info()

    print("=" * 60)
    print(f"  {info['engine']}")
    print(f"  Version: {info['version']}")
    print(f"  Author: {info['author']}")
    print(f"  Contact: {info['contact']}")
    print("=" * 60)
    print(f"\n  Supported Algorithms ({info['ciphers']}):")
    for i, algo in enumerate(info['algorithms'], 1):
        print(f"    {i}. {algo}")
    print()
    print("  Usage:")
    print("    from joker_m4 import JokerM4Engine")
    print("    engine = JokerM4Engine()")
    print('    result = engine.encrypt(b"data", ciphers=["aes", "serpent"])')
    print("    original = engine.decrypt(result)")
    print()
    print("  Install:")
    print("    pip install eclipse-cipher")
    print("=" * 60)


if __name__ == "__main__":
    main()
