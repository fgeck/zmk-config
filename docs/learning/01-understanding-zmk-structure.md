# Understanding ZMK Repository Structure

## What is a ZMK User Config Repository?

A ZMK user config repo is a **lightweight configuration layer** that doesn't contain the ZMK firmware itself. Think of it as a recipe that tells the build system what to make.

### The Core Concept

```
Your Repo (zmk-config)
    ↓ references
ZMK Firmware (zmk)
    +
Hardware Modules (flake-zmk-module)
    +
Additional Features (prospector-zmk-module)
    ↓ builds into
Firmware Files (.uf2)
```

### What Your Repository Does

1. **References ZMK modules** via West (Zephyr's package manager)
2. **Imports keyboard shields** (hardware definitions)
3. **Defines build targets** via `build.yaml`
4. **Customizes keymaps and settings** in config files
5. **Triggers automated builds** via GitHub Actions

### What Your Repository Does NOT Do

- ❌ Contain the actual ZMK firmware code
- ❌ Define the hardware (pins, matrix) - that's in modules
- ❌ Require local build tools (GitHub Actions handles it)

## Minimal ZMK User Config Structure

```
zmk-config/
├── .github/workflows/
│   └── build.yml                     # GitHub Actions workflow
├── config/
│   └── west.yml                      # Dependencies manifest
└── build.yaml                        # Build matrix definition
```

**That's it!** Just 3 required files to get started.

## Full Structure with Customizations

```
zmk-config/
├── .github/workflows/
│   └── build.yml                     # GitHub Actions workflow
├── boards/shields/
│   ├── anywhy_flake/                 # Your customizations (OPTIONAL)
│   │   ├── anywhy_flake.keymap       # Custom keymap
│   │   └── anywhy_flake.conf         # Custom config
│   └── anywhy_flake_dongle/          # Your dongle shield (OPTIONAL)
│       └── ...dongle files...
├── config/
│   └── west.yml                      # Dependencies manifest
└── build.yaml                        # Build matrix definition
```

**Note**: Keymap/config files go in `boards/shields/` per official ZMK structure.

## Understanding Each Component

### 1. GitHub Actions Workflow (`.github/workflows/build.yml`)

**Purpose**: Automates building firmware when you push changes

**What it does**:
```yaml
name: Build Firmware
on: [push, pull_request, workflow_dispatch]

jobs:
  build:
    uses: zmkfirmware/zmk/.github/workflows/build-user-config.yml@main
```

- Triggers on every push or PR
- Delegates to ZMK's official build workflow
- No need to configure Docker, Zephyr, or build tools
- Outputs firmware artifacts you can download

### 2. West Manifest (`config/west.yml`)

**Purpose**: Defines what gets pulled into your build

**What it does**:
```yaml
manifest:
  projects:
    - name: zmk                      # Core firmware
    - name: flake-zmk-module         # Your keyboard hardware
    - name: prospector-zmk-module    # Dongle screen support
```

When you run `west update` (or GitHub Actions runs it):
1. Clones ZMK firmware
2. Clones keyboard hardware definitions
3. Clones additional feature modules
4. Sets up the complete build environment

**Key insight**: The keyboard hardware definitions (device tree, pin mappings) live in **external modules**, not your repo!

### 3. Build Matrix (`build.yaml`)

**Purpose**: Defines what firmware files to build

**What it does**:
```yaml
include:
  - board: xiao_ble              # Microcontroller
    shield: anywhy_flake_left    # Keyboard hardware
    artifact-name: my_left_ble   # Output filename
```

- `board` = The microcontroller (XIAO BLE)
- `shield` = The keyboard hardware definition
- `artifact-name` = What to name the .uf2 file
- Each entry creates one firmware file

## Understanding Module Import

### What is West?

**West** is Zephyr's package manager. It manages multi-repository projects where code is spread across multiple Git repos.

### How West Works

Your `west.yml` creates a dependency tree:

```
zmk-config (your repo)
├── west.yml says "I need zmk, flake-zmk-module, prospector-zmk-module"
    │
    ├── zmk (cloned to .zmk/zmk/)
    │   ├── ZMK firmware code
    │   └── app/west.yml says "I need Zephyr, LVGL, etc."
    │       │
    │       ├── Zephyr RTOS (cloned automatically)
    │       ├── LVGL graphics library (cloned automatically)
    │       └── Other dependencies
    │
    ├── flake-zmk-module (cloned to .zmk/modules/flake-zmk-module/)
    │   ├── Device tree files (.dtsi, .overlay)
    │   ├── Shield definitions (Kconfig.shield)
    │   └── Default keymap
    │
    └── prospector-zmk-module (cloned to .zmk/modules/prospector-zmk-module/)
        ├── Dongle screen widgets
        └── Display configuration
```

**Result**: A complete `.zmk/` directory with everything needed to build

### What Gets Cloned Where

After `west update`, you'll have:

```
zmk-config/
├── config/              # Your files
│   └── west.yml
├── build.yaml
└── .zmk/               # Everything else (auto-generated)
    ├── zmk/            # Core firmware
    ├── zephyr/         # RTOS
    ├── modules/
    │   ├── lib/
    │   │   └── lvgl/   # Graphics library
    │   ├── flake-zmk-module/      # Your keyboard
    │   └── prospector-zmk-module/ # Dongle screen
    └── ...many other dependencies
```

**Important**: Never edit files in `.zmk/` - they get overwritten on `west update`!

## Module Requirements

Each module must have a `zephyr/module.yml` file:

```yaml
# Example: flake-zmk-module/zephyr/module.yml
name: flake
build:
  kconfig: Kconfig
settings:
  board_root: .
```

This tells Zephyr:
- Module name is "flake"
- Look for `Kconfig` files in the module root
- Look for boards/shields in the module's `boards/` directory

## What the flake-zmk-module Contains

Let's peek inside the keyboard hardware module:

```
flake-zmk-module/
├── zephyr/
│   └── module.yml                    # Module registration
└── boards/
    └── shields/
        └── anywhy_flake/
            ├── anywhy_flake.dtsi     # Shared hardware definition
            ├── anywhy_flake_left.overlay    # Left half pins
            ├── anywhy_flake_right.overlay   # Right half pins
            ├── anywhy_flake.keymap          # Default keymap
            ├── anywhy_flake.conf            # Default config
            ├── Kconfig.shield               # Shield registration
            └── Kconfig.defconfig            # Default settings
```

**Key files**:
- `.dtsi` = Device Tree Source Include (shared hardware)
- `.overlay` = Device Tree Overlay (side-specific pins)
- `.keymap` = Key layout and layers
- `.conf` = Configuration options
- `Kconfig.*` = Build system integration

### Overriding Module Defaults

To customize the keymap or config, create matching files in **your repo**:

```
zmk-config/boards/shields/anywhy_flake/
├── anywhy_flake.keymap    # Overrides module's default keymap
└── anywhy_flake.conf      # Overrides module's default config
```

The build system searches your local `boards/shields/` first, then falls back to the module's files.

## Build Process Overview

When you push to GitHub:

1. **GitHub Actions triggers**
2. **West reads your `west.yml`** and clones all dependencies
3. **Build system reads `build.yaml`**
4. **For each build target**:
   - Loads the board definition (xiao_ble)
   - Loads the shield(s) from modules
   - Applies your config overrides
   - Compiles everything
   - Outputs a .uf2 firmware file
5. **Artifacts uploaded** (all .uf2 files in one zip)

## Key Takeaways

1. **Your repo is lightweight** - It's just configuration, not code
2. **Modules contain the hardware definitions** - Don't reinvent the wheel
3. **West manages dependencies** - Like npm/pip for embedded systems
4. **GitHub Actions does the heavy lifting** - No local tools needed
5. **Multiple build targets from one repo** - BLE and dongle from the same config

## Quiz Yourself

Before moving on, make sure you understand:

- ✅ What files are required in a minimal ZMK config repo?
- ✅ What does `west.yml` do?
- ✅ What does `build.yaml` do?
- ✅ Where do the actual hardware definitions live?
- ✅ What happens when you push to GitHub?

## Next Steps

Now that you understand the structure, let's look at what you already have:

→ **Next**: [02-current-state.md](02-current-state.md)
