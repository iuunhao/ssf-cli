#!/usr/bin/env python3
"""
简单的typer测试
"""

import typer

app = typer.Typer()

@app.command()
def hello():
    """Hello command"""
    print("Hello World!")

@app.command()
def debug():
    """Debug command"""
    print("Debug info")

if __name__ == "__main__":
    app() 