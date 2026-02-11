# Dongle Mode Configuration

Now let's add dongle support to your repository! This will allow you to use your keyboard with a dongle that has a screen showing battery, layer, and WPM info.

## Goal

By the end of this lesson, you'll have:
- Dongle shield configuration created
- Peripheral configuration for both keyboard halves
- Updated `build.yaml` with all dongle targets
- Firmware ready to build

## Prerequisites

- ✅ BLE mode working (completed previous lessons)
- ✅ Understanding of device trees and Kconfig (lesson 06)
- ✅ `config/west.yml` already has `prospector-zmk-module` (you do!)

## Understanding Dongle Mode Architecture

###BLE Mode vs Dongle Mode

**BLE Mode**:
```
Left (Central) ←→ Right (Peripheral)
     ↓ Bluetooth
   Computer
```

**Dongle Mode**:
```
Dongle (Central) ←→ Left (Peripheral)
       ↓ USB      ←→ Right (Peripheral)
    Computer
```

### Key Difference

**The role changes!**

| Device | BLE Mode | Dongle Mode |
|--------|----------|-------------|
| Left half | Central | **Peripheral** ← Changed! |
| Right half | Peripheral | Peripheral |
| Dongle | N/A | **Central** ← New! |

**Why this matters**: We need **different firmware** for dongle mode because the left half must be a peripheral, not central.

## Step 1: Create Dongle Shield Directory

The dongle is a new "shield" (hardware configuration) we're adding.

Create the directory:

```bash
mkdir -p config/boards/shields/anywhy_flake_dongle
```

This tells the build system: "There's a new shield called `anywhy_flake_dongle`"

## Step 2: Create Dongle Device Tree Overlay

**File**: `config/boards/shields/anywhy_flake_dongle/anywhy_flake_dongle.overlay`

Create this file with:

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

### What This Does

**Mock keyboard scanner**:
- `compatible = "zmk,kscan-mock"` - Not a real key scanner
- `columns = <0>` and `rows = <0>` - No keys!
- The dongle has no physical keys - it just relays wireless input

**Why mock scanner?**
- ZMK requires a kscan (key scanner)
- Dongle has no keys, but needs to satisfy this requirement
- Mock scanner does nothing, just exists

**`wakeup-source`**:
- Allows keyboard activity to wake dongle from sleep
- When you press a key on the keyboard halves, dongle wakes up

## Step 3: Create Dongle Configuration

**File**: `config/boards/shields/anywhy_flake_dongle/anywhy_flake_dongle.conf`

Create this file with:

```
# Disable sleep mode (dongle is always powered via USB)
CONFIG_ZMK_SLEEP=n

# Dongle display configuration
CONFIG_ZMK_DISPLAY=y
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y

# Enable battery level fetching from peripherals
CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_FETCHING=y
CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_PROXY=y

# Disable dongle's own battery monitoring (USB powered)
CONFIG_ZMK_DONGLE_DISPLAY_DONGLE_BATTERY=n

# Screen timeout (10 minutes)
CONFIG_DONGLE_SCREEN_IDLE_TIMEOUT_S=600

# Screen brightness
CONFIG_DONGLE_SCREEN_MAX_BRIGHTNESS=80
CONFIG_DONGLE_SCREEN_MIN_BRIGHTNESS=10
CONFIG_DONGLE_SCREEN_DEFAULT_BRIGHTNESS=50
CONFIG_DONGLE_SCREEN_BRIGHTNESS_STEP=10

# Enable all screen widgets
CONFIG_DONGLE_SCREEN_WPM_ACTIVE=y
CONFIG_DONGLE_SCREEN_MODIFIER_ACTIVE=y
CONFIG_DONGLE_SCREEN_LAYER_ACTIVE=y
CONFIG_DONGLE_SCREEN_OUTPUT_ACTIVE=y
CONFIG_DONGLE_SCREEN_BATTERY_ACTIVE=y

# macOS icon (0=macOS, 1=Linux, 2=Windows)
CONFIG_DONGLE_SCREEN_SYSTEM_ICON=0

# Screen orientation
CONFIG_DONGLE_SCREEN_HORIZONTAL=y
CONFIG_DONGLE_SCREEN_FLIP=n
```

### Understanding These Options

**Power management**:
```
CONFIG_ZMK_SLEEP=n
```
- Dongle is USB-powered, never needs to sleep
- Keeps screen always on (until idle timeout)

**Display basics**:
```
CONFIG_ZMK_DISPLAY=y
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y
```
- Enable display support
- Use custom status screen (from prospector module)

**Battery monitoring**:
```
CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_FETCHING=y
CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_PROXY=y
```
- Central (dongle) fetches battery levels from peripherals
- Shows battery for left and right halves on screen

```
CONFIG_ZMK_DONGLE_DISPLAY_DONGLE_BATTERY=n
```
- Don't show dongle's own battery (it's USB powered)

**Screen widgets**:
```
CONFIG_DONGLE_SCREEN_WPM_ACTIVE=y        # Words per minute counter
CONFIG_DONGLE_SCREEN_MODIFIER_ACTIVE=y   # Shift, Ctrl, Cmd indicators
CONFIG_DONGLE_SCREEN_LAYER_ACTIVE=y      # Current layer indicator
CONFIG_DONGLE_SCREEN_OUTPUT_ACTIVE=y     # USB/BLE output indicator
CONFIG_DONGLE_SCREEN_BATTERY_ACTIVE=y    # Battery levels
```

**Screen appearance**:
```
CONFIG_DONGLE_SCREEN_SYSTEM_ICON=0       # macOS icon (set to your OS)
CONFIG_DONGLE_SCREEN_HORIZONTAL=y        # Landscape orientation
CONFIG_DONGLE_SCREEN_FLIP=n              # Don't flip upside down
```

## Step 4: Create Dongle Kconfig Files

These files register the dongle as a valid shield.

### File 1: Kconfig.shield

**File**: `config/boards/shields/anywhy_flake_dongle/Kconfig.shield`

```kconfig
config SHIELD_ANYWHY_FLAKE_DONGLE
    def_bool $(shields_list_contains,anywhy_flake_dongle)

config SHIELD_ANYWHY_FLAKE_DONGLE_LEFT
    def_bool $(shields_list_contains,anywhy_flake_dongle_left)
    select SHIELD_ANYWHY_FLAKE_DONGLE

config SHIELD_ANYWHY_FLAKE_DONGLE_RIGHT
    def_bool $(shields_list_contains,anywhy_flake_dongle_right)
    select SHIELD_ANYWHY_FLAKE_DONGLE
```

**What this does**:
- Detects when `shield=anywhy_flake_dongle` is specified in build
- Registers the shield with the build system
- Allows left/right variants (for future expansion)

### File 2: Kconfig.defconfig

**File**: `config/boards/shields/anywhy_flake_dongle/Kconfig.defconfig`

```kconfig
if SHIELD_ANYWHY_FLAKE_DONGLE

config ZMK_KEYBOARD_NAME
    default "Anywhy Flake Dongle"

config ZMK_SPLIT
    default y

config ZMK_SPLIT_ROLE_CENTRAL
    default y

config ZMK_SPLIT_BLE_CENTRAL_PERIPHERALS
    default 2

endif
```

**What this does**:

```kconfig
config ZMK_KEYBOARD_NAME
    default "Anywhy Flake Dongle"
```
- Sets keyboard name (appears in USB device list)

```kconfig
config ZMK_SPLIT
    default y
```
- Enable split keyboard mode

```kconfig
config ZMK_SPLIT_ROLE_CENTRAL
    default y
```
- **CRITICAL**: Dongle acts as central!
- Receives input from both keyboard halves

```kconfig
config ZMK_SPLIT_BLE_CENTRAL_PERIPHERALS
    default 2
```
- Support 2 peripherals (left + right halves)

## Step 5: Create Peripheral Configurations

Now we need to create configs that force the keyboard halves to be peripherals.

### File 1: Left Peripheral Config

**File**: `config/anywhy_flake_left_dongle.conf`

```
# Force peripheral role (NOT central)
CONFIG_ZMK_SPLIT_ROLE_CENTRAL=n

# Split mode enabled
CONFIG_ZMK_SPLIT=y

# Enable sleep mode (battery powered)
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_TIMEOUT=30000
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000
```

### File 2: Right Peripheral Config

**File**: `config/anywhy_flake_right_dongle.conf`

```
# Force peripheral role
CONFIG_ZMK_SPLIT_ROLE_CENTRAL=n

# Split mode enabled
CONFIG_ZMK_SPLIT=y

# Enable sleep mode (battery powered)
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_TIMEOUT=30000
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000
```

### Why These Are Needed

**Remember**:
- In BLE mode, left half defaults to **central** (from flake-zmk-module)
- In dongle mode, we need left half to be **peripheral**
- We override the default by setting `CONFIG_ZMK_SPLIT_ROLE_CENTRAL=n`

**Sleep settings**:
- In dongle mode, halves are battery powered
- Enable sleep to save power
- 30 seconds idle, 15 minutes sleep

## Step 6: Update build.yaml

Now we add dongle targets to the build matrix.

**File**: `build.yaml`

Replace your current content with:

```yaml
---
include:
  # === BLE MODE ===
  # Left half acts as central (connects to computer)
  - board: xiao_ble
    shield: anywhy_flake_left
    snippet: studio-rpc-usb-uart
    artifact-name: anywhy_flake_left_ble

  # Right half acts as peripheral (connects to left half)
  - board: xiao_ble
    shield: anywhy_flake_right
    artifact-name: anywhy_flake_right_ble

  # === DONGLE MODE ===
  # Left half as peripheral (connects to dongle)
  - board: xiao_ble
    shield: anywhy_flake_left
    cmake-args:
      - -DCONFIG_FILE=anywhy_flake_left_dongle.conf
    artifact-name: anywhy_flake_left_dongle

  # Right half as peripheral (connects to dongle)
  - board: xiao_ble
    shield: anywhy_flake_right
    cmake-args:
      - -DCONFIG_FILE=anywhy_flake_right_dongle.conf
    artifact-name: anywhy_flake_right_dongle

  # Dongle with screen
  - board: xiao_ble
    shields:
      - anywhy_flake_dongle
      - prospector_adapter
    cmake-args:
      - -DCONFIG_LOG_PROCESS_THREAD_STARTUP_DELAY_MS=8000
    snippet: zmk-usb-logging
    artifact-name: anywhy_flake_dongle

  # === UTILITY ===
  # Settings reset (clears BLE pairing data)
  - board: xiao_ble
    shield: settings_reset
```

### Understanding the New Targets

**Left peripheral**:
```yaml
- board: xiao_ble
  shield: anywhy_flake_left        # Same shield as BLE!
  cmake-args:
    - -DCONFIG_FILE=anywhy_flake_left_dongle.conf  # Different config!
  artifact-name: anywhy_flake_left_dongle
```

**Key insight**: Same shield, different config file!
- `-DCONFIG_FILE=` tells CMake to use a specific `.conf` file
- This overrides the defaults and forces peripheral role

**Right peripheral**:
```yaml
- board: xiao_ble
  shield: anywhy_flake_right
  cmake-args:
    - -DCONFIG_FILE=anywhy_flake_right_dongle.conf
  artifact-name: anywhy_flake_right_dongle
```

**Dongle**:
```yaml
- board: xiao_ble
  shields:                           # Multiple shields!
    - anywhy_flake_dongle            # Your dongle config
    - prospector_adapter             # Screen support
  cmake-args:
    - -DCONFIG_LOG_PROCESS_THREAD_STARTUP_DELAY_MS=8000
  snippet: zmk-usb-logging
  artifact-name: anywhy_flake_dongle
```

**Multiple shields**:
- `anywhy_flake_dongle` - Your config (mock scanner, central role)
- `prospector_adapter` - Screen driver and widgets

**cmake-args**:
- `-DCONFIG_LOG_PROCESS_THREAD_STARTUP_DELAY_MS=8000` - Delay logging startup
- Prevents conflicts between display and USB logging initialization

**snippet**:
- `zmk-usb-logging` - Enable USB debugging output (optional)
- Helpful for troubleshooting

## Step 7: Verify Your File Structure

Before committing, verify you have:

```
zmk-config/
├── config/
│   ├── west.yml                                    ✅ Already have
│   ├── anywhy_flake_left_dongle.conf               ✅ Just created
│   ├── anywhy_flake_right_dongle.conf              ✅ Just created
│   └── boards/shields/anywhy_flake_dongle/
│       ├── anywhy_flake_dongle.overlay             ✅ Just created
│       ├── anywhy_flake_dongle.conf                ✅ Just created
│       ├── Kconfig.shield                          ✅ Just created
│       └── Kconfig.defconfig                       ✅ Just created
├── build.yaml                                      ✅ Just updated
└── .github/workflows/build.yml                     ✅ Already have
```

## Step 8: Commit and Push

```bash
cd /Users/D068994/SAPDevelop/github.com/fgeck/zmk-config

# Add all new files
git add config/boards/shields/anywhy_flake_dongle/
git add config/anywhy_flake_left_dongle.conf
git add config/anywhy_flake_right_dongle.conf
git add build.yaml

# Commit
git commit -m "Add dongle mode configuration"

# Push
git push
```

## Step 9: Build and Download

1. Go to GitHub Actions
2. Watch the build progress
3. Should take 10-15 minutes (more targets now)
4. Download `firmware` artifact

You'll now get **6 firmware files**:

**BLE Mode**:
1. `anywhy_flake_left_ble-xiao_ble-zmk.uf2`
2. `anywhy_flake_right_ble-xiao_ble-zmk.uf2`

**Dongle Mode**:
3. `anywhy_flake_left_dongle-xiao_ble-zmk.uf2`
4. `anywhy_flake_right_dongle-xiao_ble-zmk.uf2`
5. `anywhy_flake_dongle-xiao_ble-zmk.uf2`

**Utility**:
6. `settings_reset-xiao_ble-zmk.uf2`

## Troubleshooting Build Errors

### Error: "Shield anywhy_flake_dongle not found"

**Cause**: Kconfig files not properly registered

**Check**:
- `Kconfig.shield` exists and has correct content
- File name is exact (case-sensitive)
- Directory structure is correct

### Error: "CONFIG_DONGLE_SCREEN_* not found"

**Cause**: prospector-zmk-module not imported

**Check**:
- `config/west.yml` has `prospector-zmk-module`
- Using `feat/new-status-screens` branch
- West update succeeded

### Error: "Multiple definitions of kscan0"

**Cause**: Conflict between shields

**Check**:
- Only using `anywhy_flake_dongle` for dongle (not also `anywhy_flake_left`)
- Device tree syntax is correct

### Build Succeeds but Wrong Behavior

**Issue**: Left/right still act as central/peripheral wrong

**Check**:
- Using correct firmware files (dongle versions)
- `CONFIG_FILE` path in `build.yaml` is correct
- Config files have `CONFIG_ZMK_SPLIT_ROLE_CENTRAL=n`

## What You Created

Let's review what each file does:

1. **anywhy_flake_dongle.overlay** - Mock scanner (no keys)
2. **anywhy_flake_dongle.conf** - Dongle settings (display, central role)
3. **Kconfig.shield** - Registers dongle shield
4. **Kconfig.defconfig** - Sets dongle defaults
5. **anywhy_flake_left_dongle.conf** - Forces left to peripheral
6. **anywhy_flake_right_dongle.conf** - Forces right to peripheral
7. **build.yaml** - Builds all 6 firmware variants

## What You Learned

You now understand:

- ✅ How to create a custom shield
- ✅ Why dongle mode needs different firmware
- ✅ How to force role changes with `.conf` files
- ✅ How to combine multiple shields in a build
- ✅ The complete dongle configuration

## Next Steps

Now you need to:
1. Wire the dongle hardware (display to XIAO BLE)
2. Flash the firmware
3. Test dongle mode

→ **Next**: [08-dongle-hardware.md](08-dongle-hardware.md) - Wiring guide
→ **Then**: [10-dongle-testing.md](10-dongle-testing.md) - Testing guide
