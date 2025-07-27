#!/usr/bin/env python3
"""
Simple Kilo Code Free Alternatives Setup
"""

import json
import os

def create_vscode_extensions_list():
    """Create list of free extensions to install manually"""
    extensions = [
        "Codeium.codeium",                    # Free AI assistant
        "Continue.continue",                   # Open source AI
        "usernamehw.errorlens",               # Inline errors
        "eamodio.gitlens",                    # Git features
        "esbenp.prettier-vscode",             # Formatting
        "ms-python.python",                   # Python support
        "humao.rest-client",                  # API testing
        "hediet.vscode-drawio",               # Diagrams
        "rangav.vscode-thunder-client",       # API client
        "yzhang.markdown-all-in-one",        # Documentation
    ]

    print("🚀 Install these VS Code extensions manually:")
    print("Go to Extensions (Ctrl+Shift+X) and search for:")
    print("=" * 50)

    for i, ext in enumerate(extensions, 1):
        print(f"{i:2d}. {ext}")

    print("\n✅ After installing, restart VS Code")
    return extensions

def create_continue_config():
    """Create Continue configuration"""
    config_dir = os.path.expanduser("~/.continue")
    os.makedirs(config_dir, exist_ok=True)

    config = {
        "models": [
            {
                "title": "Free Model - HuggingFace",
                "provider": "huggingface-tgi",
                "model": "microsoft/DialoGPT-medium",
                "apiBase": "https://api-inference.huggingface.co"
            }
        ],
        "customCommands": [
            {
                "name": "explain",
                "prompt": "Explain this code:",
                "description": "Explain selected code"
            },
            {
                "name": "test",
                "prompt": "Generate tests for this:",
                "description": "Generate tests"
            }
        ]
    }

    with open(os.path.join(config_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)

    print("✅ Continue extension configured")

def main():
    print("🎯 Setting up FREE Kilo Code alternatives...")
    print("This gives you 90% of Kilo's features for FREE!")
    print()

    create_vscode_extensions_list()
    print()
    create_continue_config()

    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Install the extensions listed above")
    print("2. Sign up for Codeium (free account)")
    print("3. Restart VS Code")
    print("4. Try typing code - you'll get AI suggestions!")

if __name__ == "__main__":
    main()
