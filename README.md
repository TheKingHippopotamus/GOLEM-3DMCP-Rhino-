# GOLEM-3DMCP

> *"Shaped from clay, brought to life by words"*

**The most powerful MCP server for Rhinoceros 3D — 105 tools giving Claude full read/write access to Rhino 8.**

[![PyPI](https://img.shields.io/pypi/v/golem-3dmcp.svg)](https://pypi.org/project/golem-3dmcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Rhino 8](https://img.shields.io/badge/Rhino-8.x-blue.svg)](https://www.rhino3d.com/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/Protocol-MCP-purple.svg)](https://modelcontextprotocol.io/)

---

GOLEM-3DMCP implements the [Model Context Protocol](https://modelcontextprotocol.io/) to give Claude Code direct, programmatic control of Rhino 8 — create geometry, run booleans, drive Grasshopper, capture viewports, and execute arbitrary Python scripts, all through natural language.

---

## Demo — City Built Entirely by Claude

> An entire city generated in Rhino 8 through GOLEM-3DMCP — roads, skyscrapers, houses, trees, people, vehicles, a stadium, bridge, ferris wheel, harbor, wind turbines, and a floating GOLEM hologram. All created by Claude Code using natural language commands.

[![Watch the demo](https://img.youtube.com/vi/GoWN9vGlWCs/maxresdefault.jpg)](https://youtu.be/GoWN9vGlWCs)
<p align="center"><strong>Watch the full demo video on YouTube</strong></p>

<p align="center">
  <img src="screenshots/city_wide.png" alt="GOLEM City — Wide Overview" width="800"/>
</p>
<p align="center"><em>Full city overview — ground, roads, buildings, park, harbor, sky</em></p>

<p align="center">
  <img src="screenshots/city_skyline.png" alt="GOLEM City — Skyline" width="800"/>
</p>
<p align="center"><em>Skyline view — skyscrapers, bridge, wind turbines, floating GOLEM hologram</em></p>

<p align="center">
  <img src="screenshots/city_monument.png" alt="GOLEM City — Monument" width="800"/>
</p>
<p align="center"><em>Close-up — GOLEM monument plaza, residential buildings, fountain</em></p>

<p align="center">
  <img src="screenshots/city_street.png" alt="GOLEM City — Street Level" width="800"/>
</p>
<p align="center"><em>Street level — vehicles, people, street lamps, stadium, harbor with boats</em></p>

---

## Install in 30 seconds

### 1. Install the MCP server
```bash
pip install golem-3dmcp
```

### 2. Deploy the Rhino plugin (one-time)
```bash
golem install-rhino
```

### 3. Add to your AI agent

**Claude Code / Cursor / Windsurf / any MCP host:**
```json
{
  "mcpServers": {
    "golem-3dmcp": {
      "command": "uvx",
      "args": ["golem-3dmcp"]
    }
  }
}
```

### 4. Verify
```bash
golem doctor
```

That's it. Start talking to Rhino through AI.

---

## Architecture

```
 Claude Code
      |
      |  MCP (stdio, JSON-RPC)
      v
+---------------------------+
|     MCP Server            |
|     Python 3.10+          |
|     FastMCP + 9 tool      |
|     modules               |
+---------------------------+
      |
      |  TCP 127.0.0.1:9876
      |  Length-prefixed JSON
      v
+---------------------------+
|     Rhino Plugin          |
|     Python 3.9 (embedded) |
|     TCP Server            |
|     Dispatcher            |
|     9 handler modules     |
+---------------------------+
      |
      |  RhinoCommon + rhinoscriptsyntax
      v
+---------------------------+       +-------------------------+
|     Rhinoceros 3D         | <---> |   Grasshopper           |
|     UI Thread             |       |   Sub-server :9877      |
|     Document, Geometry,   |       |   Definitions, Params,  |
|     Layers, Views         |       |   Components, Bake      |
+---------------------------+       +-------------------------+
```

---

## 105 Tools Across 9 Categories

| Category | Tools | Highlights |
|----------|:-----:|------------|
| **Scene Intelligence** | 10 | Document info, layers, objects, groups, blocks — no object cap, full pagination |
| **Geometry Creation** | 38 | Points, curves, NURBS, solids, mesh, SubD, text, dimensions, hatches |
| **Geometry Operations** | 19 | Boolean union/difference/intersection, trim, split, offset, fillet, chamfer, intersect, mesh from NURBS |
| **Surface Operations** | 12 | Loft, sweep1/2, revolve, extrude, network surface, patch, edge surface, unroll |
| **Object Manipulation** | 21 | Move, copy, rotate, scale, mirror, array (linear/polar/along curve), join, explode, group, properties |
| **Grasshopper** | 9 | Open definitions, set/get parameters, recompute, bake, inspect component graph |
| **Viewport & Visualization** | 13 | Capture screenshots (base64 PNG), camera control, named views, display modes |
| **File Operations** | 9 | Save, open, import, export (STL, OBJ, STEP, IGES, FBX, 3MF, DWG, PDF, and more) |
| **Script Execution** | 4 | Execute arbitrary Python with full RhinoCommon access, run Rhino commands, evaluate expressions |

See [docs/TOOL_REFERENCE.md](docs/TOOL_REFERENCE.md) for the complete reference with parameters and examples.

---

## Quick Start

### 1. Install and set up

```bash
pip install golem-3dmcp
golem install-rhino
```

### 2. Load the plugin into Rhino

Open Rhino 8, then open the Script Editor (`Tools > Python Script > Edit`).
Open `startup.py` (deployed by `golem install-rhino`) and click **Run**.

```
GOLEM-3DMCP: Starting server on 127.0.0.1:9876...
GOLEM-3DMCP: Server started successfully!
GOLEM-3DMCP: 135 handler methods registered.
```

For auto-start on every Rhino launch: `Tools > Options > RhinoScript > Startup Scripts > Add startup.py`

### 3. Register with Claude Code

```bash
claude mcp add --config .mcp.json
```

### 4. Start modeling with Claude

Open Claude Code and try:

> *"Create a 200 x 100 x 50 box at the origin, then create a sphere of radius 30 centred at [100, 50, 50]. Boolean-union the two objects."*

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Rhinoceros 3D | 8.x (macOS) |
| Python | 3.10+ (for MCP server) |
| macOS | 12 Monterey or newer |

The Rhino plugin runs inside Rhino's embedded Python 3.9 with zero external dependencies.

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GOLEM_RHINO_HOST` | `127.0.0.1` | Rhino plugin host |
| `GOLEM_RHINO_PORT` | `9876` | Rhino plugin TCP port |
| `GOLEM_GH_PORT` | `9877` | Grasshopper sub-server port |
| `GOLEM_TIMEOUT` | `30` | Command timeout (seconds) |
| `GOLEM_HEAVY_TIMEOUT` | `120` | Heavy operation timeout (seconds) |

---

## Example Usage

### Create and combine geometry
```
Create a 100 x 50 x 30 box on a layer called 'Structure',
then boolean-union it with a sphere of radius 20 centred at [50, 25, 30].
```

### Query the scene
```
List all objects on the 'Walls' layer and tell me their volumes.
```

### Drive Grasshopper
```
Open parametric_facade.gh, set the 'PanelCount' slider to 24,
recompute, and bake the result to a 'Facade' layer.
```

### Capture a viewport
```
Set perspective view to shaded mode, zoom to extents, and capture a screenshot.
```

### Execute arbitrary Python
```python
# Claude runs this inside Rhino via execute_python:
import Rhino.Geometry as rg
pts = [rg.Point3d(i*10, 0, i**2) for i in range(20)]
crv = rg.Curve.CreateInterpolatedCurve(pts, 3)
sc.doc.Objects.AddCurve(crv)
__result__ = {"point_count": len(pts), "length": crv.GetLength()}
```

---

## Project Structure

```
golem-3dmcp/
├── src/golem_3dmcp/           # MCP Server package (Python 3.10+)
│   ├── __init__.py            #   Package init + version
│   ├── __main__.py            #   python -m entry point
│   ├── cli.py                 #   CLI (golem command)
│   ├── server.py              #   FastMCP entry point
│   ├── connection.py          #   TCP client (singleton, thread-safe)
│   ├── protocol.py            #   Wire format: 4-byte length prefix + JSON
│   ├── config.py              #   Environment variable configuration
│   ├── models/                #   Pydantic data models
│   ├── tools/                 #   9 MCP tool modules
│   └── _rhino_plugin/         #   Bundled Rhino plugin (deployed via golem install-rhino)
│
├── tests/                     # 226 tests (pytest)
├── docs/                      # Architecture, protocol spec, tool reference
├── .github/workflows/         # CI/CD (test + PyPI publish)
├── pyproject.toml             # Package definition
└── .mcp.json                  # Example MCP configuration
```

---

## Documentation

- [Architecture](docs/ARCHITECTURE.md) — System design, threading model, data flow
- [Tool Reference](docs/TOOL_REFERENCE.md) — All 105 tools with parameters and examples
- [Protocol Specification](docs/PROTOCOL.md) — TCP wire format, message framing, error codes
- [Troubleshooting](docs/TROUBLESHOOTING.md) — Common issues and solutions

---

## Testing

```bash
# Unit tests (no Rhino needed)
pytest tests/ -v --ignore=tests/test_integration.py

# Full suite (integration tests auto-skip if Rhino not running)
pytest tests/ -v

# Integration tests only (requires Rhino + plugin running)
pytest tests/test_integration.py -v -m integration
```

---

## Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Connection refused | Start Rhino + run `startup.py` |
| Port already in use | `lsof -i :9876` then kill the process |
| MCP server not in Claude | Run `claude mcp add --config .mcp.json` |
| Grasshopper tools fail | Open Grasshopper in Rhino first |
| Python version error | Need Python 3.10+ for MCP server |

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Credits

<p align="center">
  <img src="nexus-svgs/king-hippo.svg" alt="King Hippopotamus" width="250"/>
</p>

<p align="center">
  Created by <strong>King Hippopotamus</strong><br/>
  Built by <strong>NEXUS AI</strong> — 30 parallel agents across 3 phases
</p>

### The NEXUS Team That Built GOLEM

<p align="center">
  <img src="nexus-svgs/CEO.svg" alt="CEO — The Lion" width="120" title="CEO — The Lion"/>
  <img src="nexus-svgs/CTO.svg" alt="CTO — The Owl" width="120" title="CTO — The Owl"/>
  <img src="nexus-svgs/CPO.svg" alt="CPO — The Fox" width="120" title="CPO — The Fox"/>
  <img src="nexus-svgs/COO.svg" alt="COO — The Bear" width="120" title="COO — The Bear"/>
  <img src="nexus-svgs/CFO.svg" alt="CFO — The Cobra" width="120" title="CFO — The Cobra"/>
  <img src="nexus-svgs/CISO.svg" alt="CISO — The Scorpion" width="120" title="CISO — The Scorpion"/>
</p>
<p align="center">
  <img src="nexus-svgs/CMO.svg" alt="CMO — The Peacock" width="120" title="CMO — The Peacock"/>
  <img src="nexus-svgs/CRO.svg" alt="CRO — The Wolf" width="120" title="CRO — The Wolf"/>
  <img src="nexus-svgs/CHRO.svg" alt="CHRO — The Elephant" width="120" title="CHRO — The Elephant"/>
  <img src="nexus-svgs/CLO.svg" alt="CLO — The Raven" width="120" title="CLO — The Raven"/>
  <img src="nexus-svgs/CAIO.svg" alt="CAIO — The Octopus" width="120" title="CAIO — The Octopus"/>
</p>



<p align="center"><em>195 autonomous agents | 20 departments | 11 tiers</em></p>

---

**GOLEM-3DMCP** uses:
- [FastMCP](https://github.com/jlowin/fastmcp) — MCP server framework
- [RhinoCommon](https://developer.rhino3d.com/api/rhinocommon/) — Rhino geometry API
- [rhinoscriptsyntax](https://developer.rhino3d.com/api/RhinoScriptSyntax/) — Python scripting for Rhino
- [Grasshopper SDK](https://developer.rhino3d.com/api/grasshopper/) — Parametric design control

---

*"From formless clay, through the power of words, form emerges."*
