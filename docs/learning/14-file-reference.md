# Complete File Reference

A comprehensive guide to every file in your zmk-config repository and what it does.

## Repository Structure

```
zmk-config/
├── .github/workflows/
│   └── build.yml
├── config/
│   ├── west.yml
│   ├── anywhy_flake.keymap (optional)
│   ├── anywhy_flake.conf (optional)
│   ├── anywhy_flake_left_dongle.conf
│   ├── anywhy_flake_right_dongle.conf
│   └── boards/shields/anywhy_flake_dongle/
│       ├── anywhy_flake_dongle.overlay
│       ├── anywhy_flake_dongle.conf
│       ├── Kconfig.shield
│       └── Kconfig.defconfig
├── build.yaml
└── README.md
```

## Root Directory Files

### build.yaml

**Purpose**: Defines what firmware to build

**Format**: YAML

**Content Structure**:
```yaml
include:
  - board: <microcontroller>
    shield: <keyboard_hardware>
    snippet: <optional_features>
    cmake-args:
      - <build_flags>
    artifact-name: <output_filename>
```

**Key Fields**:
- `board` - Microcontroller (e.g., `xiao_ble`)
- `shield` - Keyboard definition (e.g., `anywhy_flake_left`)
- `shields` - Multiple shields (array)
- `snippet` - Additional features (e.g., `studio-rpc-usb-uart`)
- `cmake-args` - Build flags (e.g., `-DCONFIG_FILE=...`)
- `artifact-name` - Output .uf2 filename

**Your Current Targets**:
1. `anywhy_flake_left_ble` - BLE left (central)
2. `anywhy_flake_right_ble` - BLE right (peripheral)
3. `anywhy_flake_left_dongle` - Dongle left (peripheral)
4. `anywhy_flake_right_dongle` - Dongle right (peripheral)
5. `anywhy_flake_dongle` - Dongle with screen
6. `settings_reset` - Utility

**When to Edit**:
- Adding new build targets
- Changing features (snippets)
- Adjusting output names
- Switching between modes

### README.md (optional)

**Purpose**: Repository documentation

**Content**:
- What this repo builds
- How to build
- How to flash
- Keymap reference
- Links to resources

**Example**:
```markdown
# ZMK Config for Anywhy Flake

Builds firmware for Anywhy Flake split keyboard.

## Modes

- **BLE Mode**: Wireless to computer
- **Dongle Mode**: Wireless to dongle with screen

## Building

Push to GitHub - Actions builds automatically.

## Flashing

Download .uf2 files from Actions artifacts.
Double-tap reset, drag-and-drop .uf2 file.
```

## .github/workflows/

### build.yml

**Purpose**: GitHub Actions workflow for automated builds

**Format**: YAML

**Content**:
```yaml
name: Build ZMK firmware
on: [push, pull_request, workflow_dispatch]

jobs:
  build:
    uses: zmkfirmware/zmk/.github/workflows/build-user-config.yml@main
```

**How It Works**:
1. Triggers on push/PR/manual
2. Delegates to ZMK's reusable workflow
3. Clones dependencies via West
4. Builds all targets from `build.yaml`
5. Uploads firmware artifacts

**When to Edit**:
- Change ZMK version (`@main` → `@v0.3`)
- Add build notifications
- Customize artifact names
- Add matrix variables (advanced)

**Rarely needs changes** - ZMK's workflow handles everything.

## config/

### west.yml

**Purpose**: Dependency manifest - defines what to clone

**Format**: YAML

**Content Structure**:
```yaml
manifest:
  defaults:
    revision: main
  remotes:
    - name: <remote_name>
      url-base: <github_url_base>
  projects:
    - name: <project_name>
      remote: <remote>
      revision: <branch_or_commit>
      import: <manifest_to_import>
      path: <clone_location>
  self:
    path: config
```

**Your Current Projects**:
1. `zmk` - Core firmware from zmkfirmware
2. `flake-zmk-module` - Keyboard hardware from anywhy-io
3. `prospector-zmk-module` - Dongle screen from carrefinho

**When to Edit**:
- Add new modules (e.g., RGB underglow)
- Pin to specific ZMK version
- Change module branches
- Add your own custom modules

**Example - Pin ZMK Version**:
```yaml
- name: zmk
  remote: zmkfirmware
  revision: abc123def456  # Specific commit
  import: app/west.yml
```

### anywhy_flake.keymap (optional)

**Purpose**: Custom keymap - overrides module default

**Format**: Device Tree

**Content Structure**:
```c
#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>

/ {
    keymap {
        compatible = "zmk,keymap";

        layer_0 {
            bindings = <
                &kp Q  &kp W  &kp E  /* ... */
            >;
        };
    };
};
```

**Key Behaviors**:
- `&kp` - Key press
- `&mt` - Mod-tap (tap for key, hold for modifier)
- `&lt` - Layer-tap
- `&mo` - Momentary layer
- `&tog` - Toggle layer
- `&bt` - Bluetooth control

**When to Edit**:
- Customize key layout
- Add layers
- Add combos/macros
- Remap any key

**If omitted**: Uses default from `flake-zmk-module`

### anywhy_flake.conf (optional)

**Purpose**: Custom configuration - overrides module defaults

**Format**: Kconfig

**Content**: One option per line
```
CONFIG_OPTION_NAME=value
```

**Common Options**:
```
# Power
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_TIMEOUT=30000
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000

# Bluetooth
CONFIG_BT_CTLR_TX_PWR_PLUS_8=y
CONFIG_ZMK_BLE_EXPERIMENTAL_FEATURES=y

# Split
CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_FETCHING=y
```

**When to Edit**:
- Disable sleep
- Adjust timeouts
- Increase BLE power
- Enable experimental features

**If omitted**: Uses defaults from ZMK and shield

**Priority**: This file > `Kconfig.defconfig` > `Kconfig` defaults

### anywhy_flake_left_dongle.conf

**Purpose**: Forces left half to be peripheral for dongle mode

**Key Content**:
```
CONFIG_ZMK_SPLIT_ROLE_CENTRAL=n  # NOT central!
CONFIG_ZMK_SPLIT=y
CONFIG_ZMK_SLEEP=y
```

**Why Needed**:
- Default: left half is central (from module)
- Dongle mode: left must be peripheral
- This file overrides the default

**Referenced in build.yaml**:
```yaml
cmake-args:
  - -DCONFIG_FILE=anywhy_flake_left_dongle.conf
```

### anywhy_flake_right_dongle.conf

**Purpose**: Same as left, but for right half

**Content**: Identical to left_dongle.conf

**Why Separate Files**:
- Could add half-specific settings
- Clearer intent in build.yaml
- Future-proofing

## config/boards/shields/anywhy_flake_dongle/

This directory defines the dongle as a custom shield.

### anywhy_flake_dongle.overlay

**Purpose**: Device tree for dongle hardware

**Format**: Device Tree

**Content**:
```dts
/ {
    chosen {
        zmk,kscan = &kscan0;
    };

    kscan0: kscan {
        compatible = "zmk,kscan-mock";
        columns = <0>;
        rows = <0>;
        events = <0>;
        exit-after;
        wakeup-source;
    };
};
```

**What It Does**:
- Creates mock keyboard scanner (no physical keys)
- Satisfies ZMK's requirement for a kscan
- `wakeup-source` allows key events to wake dongle

**Why Mock**:
- Dongle has no keys
- Just relays wireless input to computer
- Still needs kscan node for ZMK to work

### anywhy_flake_dongle.conf

**Purpose**: Dongle configuration options

**Key Sections**:

**Power**:
```
CONFIG_ZMK_SLEEP=n  # Always on (USB powered)
```

**Display**:
```
CONFIG_ZMK_DISPLAY=y
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y
```

**Battery**:
```
CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_FETCHING=y  # Get peripheral battery
CONFIG_ZMK_DONGLE_DISPLAY_DONGLE_BATTERY=n             # Don't show dongle battery
```

**Screen widgets** (from prospector-zmk-module):
```
CONFIG_DONGLE_SCREEN_WPM_ACTIVE=y
CONFIG_DONGLE_SCREEN_MODIFIER_ACTIVE=y
CONFIG_DONGLE_SCREEN_LAYER_ACTIVE=y
CONFIG_DONGLE_SCREEN_OUTPUT_ACTIVE=y
CONFIG_DONGLE_SCREEN_BATTERY_ACTIVE=y
```

**Appearance**:
```
CONFIG_DONGLE_SCREEN_SYSTEM_ICON=0  # macOS
CONFIG_DONGLE_SCREEN_HORIZONTAL=y
CONFIG_DONGLE_SCREEN_DEFAULT_BRIGHTNESS=50
```

**When to Edit**:
- Adjust brightness
- Change timeout
- Enable/disable widgets
- Change OS icon

### Kconfig.shield

**Purpose**: Registers dongle as a valid shield option

**Format**: Kconfig

**Content**:
```kconfig
config SHIELD_ANYWHY_FLAKE_DONGLE
    def_bool $(shields_list_contains,anywhy_flake_dongle)
```

**What It Does**:
- Detects when `shield=anywhy_flake_dongle` is used
- Enables shield-specific options
- Makes shield visible to build system

**Rarely needs changes** unless adding variants

### Kconfig.defconfig

**Purpose**: Sets default config values for dongle shield

**Format**: Kconfig

**Content**:
```kconfig
if SHIELD_ANYWHY_FLAKE_DONGLE

config ZMK_KEYBOARD_NAME
    default "Anywhy Flake Dongle"

config ZMK_SPLIT
    default y

config ZMK_SPLIT_ROLE_CENTRAL
    default y  # Dongle is central!

config ZMK_SPLIT_BLE_CENTRAL_PERIPHERALS
    default 2  # Support 2 peripherals

endif
```

**What It Does**:
- Sets keyboard name
- Enables split mode
- Makes dongle central
- Supports 2 peripherals

**When to Edit**:
- Change keyboard name
- Support more peripherals (e.g., 3+)
- Add shield-specific defaults

## Files from Modules (NOT in your repo)

These exist in `.zmk/modules/` after `west update`:

### flake-zmk-module

**Location**: `.zmk/modules/flake-zmk-module/boards/shields/anywhy_flake/`

**Files**:
- `anywhy_flake.dtsi` - Shared hardware definition
- `anywhy_flake_left.overlay` - Left half pins
- `anywhy_flake_right.overlay` - Right half pins
- `anywhy_flake.keymap` - Default keymap
- `anywhy_flake.conf` - Default config
- `Kconfig.shield` - Shield registration
- `Kconfig.defconfig` - Default settings (left=central!)

**Don't edit these** - they're external module files!

### prospector-zmk-module

**Location**: `.zmk/modules/prospector-zmk-module/`

**Provides**:
- `prospector_adapter` shield
- Display widgets
- Screen configuration options

**Don't edit** - external module

## Build Output (Not in Repo)

### Firmware Artifacts

**Location**: GitHub Actions artifacts

**Format**: `.uf2` files

**Naming**: `{artifact-name}-{board}-zmk.uf2`

**Your Files**:
1. `anywhy_flake_left_ble-xiao_ble-zmk.uf2`
2. `anywhy_flake_right_ble-xiao_ble-zmk.uf2`
3. `anywhy_flake_left_dongle-xiao_ble-zmk.uf2`
4. `anywhy_flake_right_dongle-xiao_ble-zmk.uf2`
5. `anywhy_flake_dongle-xiao_ble-zmk.uf2`
6. `settings_reset-xiao_ble-zmk.uf2`

## File Creation Checklist

### Minimal BLE Mode

Required files:
- [ ] `.github/workflows/build.yml`
- [ ] `config/west.yml`
- [ ] `build.yaml`

Optional files:
- [ ] `config/anywhy_flake.keymap` (custom keymap)
- [ ] `config/anywhy_flake.conf` (custom config)

### Complete with Dongle Mode

Additional required:
- [ ] `config/anywhy_flake_left_dongle.conf`
- [ ] `config/anywhy_flake_right_dongle.conf`
- [ ] `config/boards/shields/anywhy_flake_dongle/anywhy_flake_dongle.overlay`
- [ ] `config/boards/shields/anywhy_flake_dongle/anywhy_flake_dongle.conf`
- [ ] `config/boards/shields/anywhy_flake_dongle/Kconfig.shield`
- [ ] `config/boards/shields/anywhy_flake_dongle/Kconfig.defconfig`

## Quick Reference: Which File to Edit

**Want to...**

| Goal | Edit This File |
|------|----------------|
| Add/remove build targets | `build.yaml` |
| Change keymap | `config/anywhy_flake.keymap` |
| Adjust sleep timeout | `config/anywhy_flake.conf` |
| Add new module | `config/west.yml` |
| Pin ZMK version | `config/west.yml` |
| Change screen brightness | `config/boards/shields/anywhy_flake_dongle/anywhy_flake_dongle.conf` |
| Enable/disable widgets | `config/boards/shields/anywhy_flake_dongle/anywhy_flake_dongle.conf` |
| Change dongle name | `config/boards/shields/anywhy_flake_dongle/Kconfig.defconfig` |
| Add custom hardware | Create new shield in `config/boards/shields/` |

## Common Patterns

### Pattern 1: Add Custom Config Option

1. Find option name in ZMK docs or source
2. Add to `config/anywhy_flake.conf`:
   ```
   CONFIG_OPTION_NAME=value
   ```
3. Commit, push, rebuild

### Pattern 2: Use Different Config for Same Shield

1. Create `config/my_custom.conf`
2. Add in `build.yaml`:
   ```yaml
   - board: xiao_ble
     shield: anywhy_flake_left
     cmake-args:
       - -DCONFIG_FILE=my_custom.conf
     artifact-name: left_custom
   ```
3. Commit, push, rebuild

### Pattern 3: Create New Shield

1. Create directory: `config/boards/shields/my_shield/`
2. Create files:
   - `my_shield.overlay` (device tree)
   - `my_shield.conf` (config)
   - `Kconfig.shield` (registration)
   - `Kconfig.defconfig` (defaults)
3. Add to `build.yaml`:
   ```yaml
   - board: xiao_ble
     shield: my_shield
   ```
4. Commit, push, rebuild

## What You Learned

You now have a complete reference for:

- ✅ Every file in your repository
- ✅ What each file does
- ✅ When to edit each file
- ✅ File syntax and structure
- ✅ Build output files
- ✅ Common patterns

## Next Steps

→ **Troubleshooting**: [15-troubleshooting.md](15-troubleshooting.md)
→ **Resources**: [16-resources.md](16-resources.md)
