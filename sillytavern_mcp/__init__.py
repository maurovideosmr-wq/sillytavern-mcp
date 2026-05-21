from fastmcp import FastMCP

mcp = FastMCP("sillytavern-mcp")

from sillytavern_mcp.server import setup as _setup

_setup()


def main():
    mcp.run()


if __name__ == "__main__":
    main()
