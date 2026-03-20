"""
rhino_plugin/startup.py
=======================
Bootstrap script for starting the GOLEM-3DMCP TCP server inside Rhino 3D.

HOW TO USE:
  1. Open Rhino 3D.
  2. Run the 'EditPythonScript' command (or open the Python Script Editor).
  3. Open this file and press Run, OR paste its contents into the editor.

Alternatively, add this script to Rhino's startup scripts list:
  Tools > Options > RhinoScript > Add startup script > select this file.

What this script does:
  - Adds the GOLEM-3DMCP project root to sys.path so all package imports work.
  - Calls start_server() to bind a TCP socket on 127.0.0.1:9876.
  - Registers all domain handler modules and reports the method count.
  - The server runs in a background daemon thread and does not block Rhino.

To stop the server:  call stop_server() or run rhino_plugin/shutdown.py
To restart:          call restart_server()
To send a command:   send a 'shutdown' method via the MCP client
"""

import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_HOST = "127.0.0.1"
_PORT = 9876

# Adjust this path if you have cloned GOLEM-3DMCP to a different location.
project_root = "/Users/kinghippo/Documents/GOLEM-3DMCP"

# ---------------------------------------------------------------------------
# Path setup — must happen before any rhino_plugin imports
# ---------------------------------------------------------------------------

if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"GOLEM-3DMCP: Added {project_root} to sys.path.")

# ---------------------------------------------------------------------------
# Import server machinery
# ---------------------------------------------------------------------------

try:
    from rhino_plugin.dispatcher import get_registered_methods  # noqa: E402
    from rhino_plugin.server import _is_running, start_server, stop_server  # noqa: E402
except Exception as _import_exc:
    print(
        "GOLEM-3DMCP: ERROR — Failed to import server modules.\n"
        f"  Ensure '{project_root}' is the correct project root and all\n"
        "  required packages are present.\n"
        f"  Detail: {_import_exc}"
    )
    raise

# ---------------------------------------------------------------------------
# Convenience helpers exposed in the Rhino Python console
# ---------------------------------------------------------------------------

def stop_golem():
    # type: () -> None
    """
    Stop the GOLEM-3DMCP TCP server.

    Call this from Rhino's Python console or script editor::

        import rhino_plugin.startup as golem
        golem.stop_golem()
    """
    if not _is_running():
        print("GOLEM-3DMCP: Server is not running.")
        return
    try:
        stop_server()
        print("GOLEM-3DMCP: Server stopped.")
    except Exception as exc:
        print(f"GOLEM-3DMCP: ERROR while stopping server — {exc}")


def restart_golem(host=_HOST, port=_PORT):
    # type: (str, int) -> None
    """
    Stop and restart the GOLEM-3DMCP TCP server.

    Useful when you have made changes to handler modules and want to reload
    without restarting Rhino.

    Args:
        host: IP address to bind (default: 127.0.0.1).
        port: TCP port to listen on (default: 9876).
    """
    print(f"GOLEM-3DMCP: Restarting server on {host}:{port}...")
    if _is_running():
        stop_golem()
    _start(host, port)


def _start(host, port):
    # type: (str, int) -> None
    """Internal helper: start the server and print diagnostics."""
    if _is_running():
        print(
            f"GOLEM-3DMCP: Server is already running on {host}:{port}. "
            "Call restart_golem() to restart."
        )
        return

    print(f"GOLEM-3DMCP: Starting server on {host}:{port}...")

    try:
        start_server(host, port)
    except OSError as exc:
        print(
            f"GOLEM-3DMCP: ERROR — Could not bind {host}:{port}.\n"
            "  The port may already be in use by another process.\n"
            f"  Detail: {exc}\n"
            "  Try: restart_golem() or change _PORT at the top of startup.py."
        )
        return
    except Exception as exc:
        print(
            f"GOLEM-3DMCP: ERROR — Unexpected failure starting server: {exc}"
        )
        return

    # Report registered methods.
    try:
        methods = sorted(get_registered_methods())
        print(
            f"GOLEM-3DMCP: Server started successfully on {host}:{port}."
        )
        print(f"GOLEM-3DMCP: {len(methods)} handler methods registered:")
        for method_name in methods:
            print(f"    {method_name}")
    except Exception as exc:
        # Diagnostics failure is non-fatal; the server is already running.
        print(
            "GOLEM-3DMCP: Server started, but could not retrieve method list: "
            f"{exc}"
        )


# ---------------------------------------------------------------------------
# Auto-start when the script is run directly
# ---------------------------------------------------------------------------

_start(_HOST, _PORT)
