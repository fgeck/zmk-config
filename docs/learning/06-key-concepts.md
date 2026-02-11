# Key Concepts Explained

Now that you have a working keyboard, let's understand the systems that make it work. This knowledge will help you customize and troubleshoot effectively.

## The Three Configuration Systems

ZMK uses three different but interconnected configuration systems:

1. **Device Tree** - Hardware description
2. **Kconfig** - Build-time configuration
3. **West** - Dependency management

Let's understand each one.

## Device Tree (Hardware Description)

### What is Device Tree?

**Device Tree** is a hardware description language. It tells the firmware:
- What pins are connected to what
- How the hardware is organized
- What peripherals exist

Think of it as a "map" of your hardware.

### Device Tree Syntax Basics

Device trees use `.dts` (source) and `.dtsi` (include) files:

```dts
/ {
    // Root node - represents the entire device

    chosen {
        // Special node: tells ZMK what to use
        zmk,kscan = &kscan0;    // Use kscan0 for scanning keys
    };

    kscan0: kscan {
        // Node named "kscan0" of type "kscan"
        compatible = "zmk,kscan-gpio-matrix";
        diode-direction = "col2row";

        row-gpios = <&xiao_d 6 GPIO_ACTIVE_HIGH>,
                    <&xiao_d 7 GPIO_ACTIVE_HIGH>;

        col-gpios = <&xiao_d 0 GPIO_ACTIVE_HIGH>,
                    <&xiao_d 1 GPIO_ACTIVE_HIGH>;
    };
};
```

### Breaking Down the Syntax

**Nodes**:
```dts
node_name: label {
    property = value;
}
```

- `node_name` - Actual name
- `label` - Reference label (like a variable)
- Properties inside `{}`

**References**:
```dts
zmk,kscan = &kscan0;
```
- `&kscan0` = Reference to the node labeled `kscan0`
- Like a pointer in programming

**GPIO Syntax**:
```dts
<&xiao_d 6 GPIO_ACTIVE_HIGH>
```
- `&xiao_d` - Reference to XIAO GPIO controller
- `6` - Pin number (D6)
- `GPIO_ACTIVE_HIGH` - Active when HIGH (3.3V)

**Arrays**:
```dts
row-gpios = <pin1>, <pin2>, <pin3>;
```
- Comma-separated list of pins

### Example: Anywhy Flake Key Matrix

The Flake uses a **key matrix** (rows × columns):

```dts
kscan0: kscan {
    compatible = "zmk,kscan-gpio-matrix";
    diode-direction = "col2row";

    // 4 rows
    row-gpios = <&xiao_d 6 GPIO_ACTIVE_HIGH>,
                <&xiao_d 7 GPIO_ACTIVE_HIGH>,
                <&xiao_d 8 GPIO_ACTIVE_HIGH>,
                <&xiao_d 9 GPIO_ACTIVE_HIGH>;

    // Left half: 6 columns
    col-gpios = <&xiao_d 0 GPIO_ACTIVE_HIGH>,
                <&xiao_d 1 GPIO_ACTIVE_HIGH>,
                <&xiao_d 2 GPIO_ACTIVE_HIGH>,
                <&xiao_d 3 GPIO_ACTIVE_HIGH>,
                <&xiao_d 4 GPIO_ACTIVE_HIGH>,
                <&xiao_d 5 GPIO_ACTIVE_HIGH>;
};
```

**What this means**:
- 4 rows × 6 columns = 24 possible keys on left half
- Diodes are oriented column-to-row
- When a key is pressed, it connects a row to a column
- Firmware scans the matrix to detect key presses

### Device Tree Files in Your Build

**From flake-zmk-module**:

1. **`anywhy_flake.dtsi`** - Shared base
   - Keyboard name
   - Matrix transform (maps physical to logical layout)
   - Common properties

2. **`anywhy_flake_left.overlay`** - Left half specific
   - Column pins for left side
   - Reference to base
   - Left-specific chosen nodes

3. **`anywhy_flake_right.overlay`** - Right half specific
   - Column pins for right side
   - Right-specific configuration

### Why Split into Multiple Files?

**Reusability**:
- Shared definitions in `.dtsi`
- Side-specific in `.overlay`
- Don't repeat yourself

**Example**:
```dts
// anywhy_flake.dtsi - shared
/ {
    default_transform: keymap_transform_0 {
        compatible = "zmk,matrix-transform";
        columns = <12>;  // Total columns (6 left + 6 right)
        rows = <4>;
        // ... key positions
    };
};

// anywhy_flake_left.overlay
#include "anywhy_flake.dtsi"

&kscan0 {
    col-gpios = /* left side columns */;
};

// anywhy_flake_right.overlay
#include "anywhy_flake.dtsi"

&kscan0 {
    col-gpios = /* right side columns */;
};
```

## Kconfig (Build Configuration)

### What is Kconfig?

**Kconfig** is a configuration system from the Linux kernel. It defines:
- What features to enable/disable
- Build-time options
- Dependencies between features

Think of it as "compile-time settings."

### Kconfig Syntax

**Defining options** (`Kconfig` file):
```kconfig
config ZMK_SLEEP
    bool "Enable sleep mode"
    default y
    help
      Enables deep sleep after idle timeout to save power
```

**Setting defaults** (`Kconfig.defconfig`):
```kconfig
if SHIELD_ANYWHY_FLAKE_LEFT

config ZMK_SPLIT_ROLE_CENTRAL
    default y

endif
```

**Overriding values** (`.conf` file):
```
CONFIG_ZMK_SLEEP=n
CONFIG_ZMK_IDLE_TIMEOUT=30000
```

### Kconfig Value Types

- `bool` - Yes/no (y/n)
- `int` - Integer number
- `string` - Text value
- `hex` - Hexadecimal number

### Kconfig Files in Your Build

**From flake-zmk-module**:

1. **`Kconfig.shield`** - Registers the shield
```kconfig
config SHIELD_ANYWHY_FLAKE_LEFT
    def_bool $(shields_list_contains,anywhy_flake_left)
```

Detects when `shield=anywhy_flake_left` is specified.

2. **`Kconfig.defconfig`** - Sets defaults
```kconfig
if SHIELD_ANYWHY_FLAKE_LEFT

config ZMK_KEYBOARD_NAME
    default "Anywhy Flake"

config ZMK_SPLIT_ROLE_CENTRAL
    default y    # Left is central!

endif
```

**Your overrides** (`.conf` files):

Create `boards/shields/anywhy_flake/anywhy_flake.conf` to override:
```
# Disable sleep
CONFIG_ZMK_SLEEP=n

# Increase BLE TX power
CONFIG_BT_CTLR_TX_PWR_PLUS_8=y

# Enable experimental features
CONFIG_ZMK_BLE_EXPERIMENTAL_FEATURES=y
```

### Configuration Priority

From lowest to highest priority:

1. **Kconfig** - Default defined in option
2. **Kconfig.defconfig** - Default per shield/board
3. **`.conf` file** - Your explicit overrides

**Example**:
```
ZMK core:      CONFIG_ZMK_SLEEP default y
Shield:        (no override)
Your .conf:    CONFIG_ZMK_SLEEP=n

Result:        Sleep is DISABLED
```

### Common Kconfig Options

**Power management**:
```
CONFIG_ZMK_SLEEP=y                      # Enable sleep mode
CONFIG_ZMK_IDLE_TIMEOUT=30000           # 30 seconds to idle
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000    # 15 minutes to sleep
```

**Bluetooth**:
```
CONFIG_BT_CTLR_TX_PWR_PLUS_8=y          # Increase BLE power
CONFIG_ZMK_BLE_EXPERIMENTAL_FEATURES=y  # Experimental features
CONFIG_BT_MAX_CONN=3                    # Max connections
```

**Display**:
```
CONFIG_ZMK_DISPLAY=y                    # Enable display
CONFIG_ZMK_WIDGET_BATTERY_STATUS=y      # Battery widget
CONFIG_ZMK_WIDGET_WPM=y                 # WPM counter
```

**Split keyboard**:
```
CONFIG_ZMK_SPLIT=y                      # Enable split
CONFIG_ZMK_SPLIT_ROLE_CENTRAL=y         # This is central
CONFIG_ZMK_SPLIT_BLE_CENTRAL_PERIPHERALS=2  # Support 2 peripherals
```

### Finding Available Options

**In ZMK source** (`.zmk/zmk/app/Kconfig`):
- All ZMK options defined here
- Read the help text for each option

**Search GitHub**:
```
site:github.com/zmkfirmware/zmk CONFIG_ZMK_SLEEP
```

**Community configs**:
- Look at other users' `.conf` files
- Check ZMK Discord for examples

## West (Dependency Management)

### What is West?

**West** is Zephyr's meta-tool for managing multi-repository projects.

Think of it like:
- `npm` for Node.js
- `pip` for Python
- But for embedded systems

### West Manifest Structure

Your `config/west.yml`:

```yaml
manifest:
  defaults:
    revision: main          # Default branch

  remotes:
    - name: zmkfirmware
      url-base: https://github.com/zmkfirmware

  projects:
    - name: zmk
      remote: zmkfirmware
      revision: main
      import: app/west.yml  # Import ZMK's dependencies

    - name: flake-zmk-module
      url: https://github.com/anywhy-io/flake-zmk-module
      path: modules/flake-zmk-module

  self:
    path: config            # This manifest is in config/
```

### Key Concepts

**Remotes**:
- Like "npm registries"
- Define base URLs
- Multiple remotes allowed

**Projects**:
- Repositories to clone
- Each has: name, remote, revision
- Can import other manifests

**Import**:
```yaml
import: app/west.yml
```
- ZMK's manifest lists Zephyr, LVGL, etc.
- You don't need to list them
- Transitive dependencies

**Paths**:
```yaml
path: modules/flake-zmk-module
```
- Where to clone the repo
- Relative to workspace root (`.zmk/`)

### West Workflow

When GitHub Actions runs `west update`:

1. **Read `config/west.yml`**
2. **Clone `zmk`** to `.zmk/zmk/`
3. **Read `zmk/app/west.yml`** (imported)
4. **Clone Zephyr, LVGL, etc.** (from ZMK's manifest)
5. **Clone `flake-zmk-module`** to `.zmk/modules/flake-zmk-module/`
6. **Clone `prospector-zmk-module`** to `.zmk/modules/prospector-zmk-module/`
7. **Result**: Complete dependency tree

### Pinning Versions

**Use specific commits** for reproducibility:

```yaml
projects:
  - name: zmk
    revision: abc123def456  # Specific commit

  - name: flake-zmk-module
    revision: v1.2.3         # Tag
```

**Or use branches** for latest updates:

```yaml
projects:
  - name: zmk
    revision: main           # Latest main
```

### Module Registration

Each module needs `zephyr/module.yml`:

```yaml
name: flake
build:
  kconfig: Kconfig          # Where to find Kconfig
  cmake: .                  # Where to find CMakeLists.txt (optional)
settings:
  board_root: .             # Where to find boards/
  dts_root: .               # Where to find device trees
```

**What this does**:
- Registers module with Zephyr build system
- Tells build system where to find files
- Enables automatic discovery

## How It All Fits Together

### Build Process Flow

1. **West reads manifests**
   - Clones all dependencies

2. **CMake configuration phase**
   - Reads `build.yaml`
   - For each target:
     - Load board definition
     - Load shield definition(s)
     - Find all Kconfig files
     - Merge device trees

3. **Kconfig phase**
   - Load all Kconfig files
   - Apply `.conf` overrides
   - Generate `autoconf.h`

4. **Device tree phase**
   - Parse `.dtsi` files
   - Apply `.overlay` files
   - Generate `devicetree_generated.h`

5. **Compilation phase**
   - Compile C code
   - Link with Zephyr RTOS
   - Link with ZMK firmware
   - Generate `.elf` binary

6. **Post-processing**
   - Convert `.elf` to `.uf2`
   - Add metadata
   - Output firmware file

### Your Files' Journey

**Your repo** (`zmk-config`):
```
build.yaml          → Defines targets
config/west.yml     → Fetches dependencies
config/*.conf       → Overrides defaults
```

**Pulled from modules**:
```
zmk                 → Core firmware code
flake-zmk-module    → Hardware definitions
  ├── .dtsi/.overlay  → Device trees
  ├── Kconfig.*       → Configuration
  └── .keymap         → Default keymap
```

**Build output**:
```
.uf2 files          → Flash to hardware!
```

## Practical Applications

### Example 1: Disable Sleep

**Problem**: Keyboard sleeps too quickly

**Solution**: Override in `.conf`

1. Create `boards/shields/anywhy_flake/anywhy_flake.conf`:
```
CONFIG_ZMK_SLEEP=n
```

2. Commit, push, rebuild
3. Flash new firmware
4. Sleep is disabled!

### Example 2: Increase BLE Power

**Problem**: Short BLE range

**Solution**: Increase TX power

1. Add to `boards/shields/anywhy_flake/anywhy_flake.conf`:
```
CONFIG_BT_CTLR_TX_PWR_PLUS_8=y
```

2. Rebuild and flash
3. Longer range (at cost of battery)

### Example 3: Custom Pin Mapping

**Problem**: Need to swap two pins

**Solution**: Override in your own `.overlay`

1. Create `config/boards/shields/anywhy_flake_left.overlay`:
```dts
&kscan0 {
    col-gpios = <&xiao_d 1 GPIO_ACTIVE_HIGH>,  // Swapped!
                <&xiao_d 0 GPIO_ACTIVE_HIGH>,  // Swapped!
                <&xiao_d 2 GPIO_ACTIVE_HIGH>,
                // ... rest unchanged
};
```

2. This overrides the module's pins
3. Rebuild and flash

## What You Learned

You now understand:

- ✅ **Device Tree**: Hardware description, pin mappings, key matrix
- ✅ **Kconfig**: Build options, feature flags, configuration
- ✅ **West**: Dependency management, module system
- ✅ How these three systems work together
- ✅ Configuration priority (who overrides whom)
- ✅ How to customize your build

## Quiz Yourself

- Can you explain the difference between `.dtsi` and `.overlay`?
- What's the difference between `Kconfig.defconfig` and `.conf`?
- Why do we need West instead of just one Git repo?
- How would you disable sleep mode?
- Where would you change a pin assignment?

## Next Steps

Now that you understand the underlying systems:

→ **Learn BLE vs Dongle architecture**: [07-architecture.md](07-architecture.md)
→ **Start customizing**: [11-keymap-customization.md](11-keymap-customization.md)
→ **Add dongle mode**: [08-dongle-hardware.md](08-dongle-hardware.md)
