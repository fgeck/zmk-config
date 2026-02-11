# BLE Mode Configuration

Let's get BLE mode working! This will give you a working keyboard and teach you the fundamentals.

## Goal

By the end of this lesson, you'll have:
- A clean `build.yaml` that builds BLE mode firmware
- Understanding of what each build target does
- Firmware files ready to flash

## Current vs. Target State

### What You Have

```yaml
include:
  - board: xiao_ble
    shield: anywhy_flake_left
    snippet: studio-rpc-usb-uart
  - board: xiao_ble
    shield: anywhy_flake_right
  - board: xiao_ble
    shield: settings_reset
  - board: xiao_ble
    shield: anywhy_flake_dongle prospector_adapter
```

### What You Need for BLE Mode

```yaml
include:
  # BLE Mode - Left half acts as central
  - board: xiao_ble
    shield: anywhy_flake_left
    snippet: studio-rpc-usb-uart
    artifact-name: anywhy_flake_left_ble

  # BLE Mode - Right half acts as peripheral
  - board: xiao_ble
    shield: anywhy_flake_right
    artifact-name: anywhy_flake_right_ble

  # Settings reset utility
  - board: xiao_ble
    shield: settings_reset
```

## Understanding Each Build Target

### Target 1: Left Half (BLE Mode)

```yaml
- board: xiao_ble
  shield: anywhy_flake_left
  snippet: studio-rpc-usb-uart
  artifact-name: anywhy_flake_left_ble
```

**What each field means**:

- **`board: xiao_ble`** - The microcontroller
  - This tells ZMK: "Build for Seeeduino XIAO BLE hardware"
  - Board definitions come from ZMK core (not a module)
  - Defines: CPU, memory, pin names, bootloader

- **`shield: anywhy_flake_left`** - The keyboard hardware
  - This tells ZMK: "Use the left half of Anywhy Flake keyboard"
  - Shield definition comes from `flake-zmk-module`
  - Defines: Key matrix, column/row pins, default keymap
  - By default (from module): Left half acts as **central**

- **`snippet: studio-rpc-usb-uart`** - Optional feature
  - Enables ZMK Studio support
  - Allows wireless key remapping via ZMK Studio app
  - Only needed on central side (left half)
  - Uses USB connection to configure the keyboard

- **`artifact-name: anywhy_flake_left_ble`** - Output filename
  - Without this: `xiao_ble-anywhy_flake_left-zmk.uf2` (generic)
  - With this: `anywhy_flake_left_ble-xiao_ble-zmk.uf2` (clear!)
  - Makes it easy to identify which firmware is which

### Target 2: Right Half (BLE Mode)

```yaml
- board: xiao_ble
  shield: anywhy_flake_right
  artifact-name: anywhy_flake_right_ble
```

**What's different**:
- No `snippet` - Right half doesn't need Studio support
- Shield is `anywhy_flake_right` instead of `_left`
- By default (from module): Right half acts as **peripheral**

**How it works**:
- Right half connects wirelessly to left half
- Left half acts as the "host"
- Right half just sends key presses to left half
- Only left half connects to your computer

### Target 3: Settings Reset

```yaml
- board: xiao_ble
  shield: settings_reset
```

**What this does**:
- Special utility firmware
- Clears all saved settings (BLE pairings, etc.)
- Useful when:
  - Switching between BLE and dongle mode
  - Fixing pairing issues
  - Starting fresh

**How to use**:
1. Flash this firmware to any XIAO BLE
2. Wait a few seconds
3. Flash your actual firmware
4. All settings are cleared!

## Step-by-Step: Update Your build.yaml

### Step 1: Open the File

Open `build.yaml` in your text editor.

### Step 2: Replace the Content

Replace everything with:

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

  # === UTILITY ===
  # Settings reset (clears BLE pairing data)
  - board: xiao_ble
    shield: settings_reset
```

### Step 3: Save the File

Save and close.

### Step 4: Commit and Push

```bash
cd /Users/D068994/SAPDevelop/github.com/fgeck/zmk-config
git add build.yaml
git commit -m "Configure BLE mode build targets"
git push
```

## Understanding the Defaults from flake-zmk-module

You might wonder: "How does the left half know to be central and the right to be peripheral?"

This is configured in the **module**, not your repo!

### In flake-zmk-module

**File**: `boards/shields/anywhy_flake/anywhy_flake_left.overlay`

Near the top, there's a section like:

```dts
#include "anywhy_flake.dtsi"

&default_transform {
    col-offset = <0>;
};

/ {
    chosen {
        zmk,kscan = &kscan0;
        zmk,matrix-transform = &default_transform;
    };
};
```

**File**: `boards/shields/anywhy_flake/Kconfig.defconfig`

```kconfig
if SHIELD_ANYWHY_FLAKE_LEFT

config ZMK_SPLIT_ROLE_CENTRAL
    default y    # This makes left half central!

endif
```

**Key insight**: The module sets `ZMK_SPLIT_ROLE_CENTRAL=y` for the left shield. You don't need to configure this yourself for BLE mode!

### For the right half:

```kconfig
if SHIELD_ANYWHY_FLAKE_RIGHT

config ZMK_SPLIT_ROLE_CENTRAL
    default n    # This makes right half peripheral!

endif
```

## What Happens When You Build

### Build Process Flow

1. **GitHub Actions starts**
   - Triggered by your push
   - Sets up build environment

2. **West initialization**
   - Reads `config/west.yml`
   - Clones `zmk`, `flake-zmk-module`, `prospector-zmk-module`
   - Creates `.zmk/` directory with everything

3. **For each target in build.yaml**:

   **Building left half**:
   - Load board definition: `xiao_ble`
   - Load shield: `anywhy_flake_left` from module
   - Apply snippet: `studio-rpc-usb-uart`
   - Merge config from shield's `Kconfig.defconfig`
     - `ZMK_SPLIT_ROLE_CENTRAL=y` ← Left is central!
   - Compile firmware
   - Output: `anywhy_flake_left_ble-xiao_ble-zmk.uf2`

   **Building right half**:
   - Load board definition: `xiao_ble`
   - Load shield: `anywhy_flake_right` from module
   - Merge config from shield's `Kconfig.defconfig`
     - `ZMK_SPLIT_ROLE_CENTRAL=n` ← Right is peripheral!
   - Compile firmware
   - Output: `anywhy_flake_right_ble-xiao_ble-zmk.uf2`

4. **Upload artifacts**
   - All .uf2 files packaged in `firmware.zip`
   - Available for download

## Checking the Build

### Step 1: Go to GitHub

1. Navigate to: `https://github.com/YOUR-USERNAME/zmk-config`
2. Click **Actions** tab
3. You should see your recent "Configure BLE mode build targets" commit

### Step 2: Watch the Build

Click on the running workflow to see:
- West initialization
- Dependencies being fetched
- Each target being built
- Build logs

### Step 3: Wait for Completion

Builds typically take 5-10 minutes. You'll see:
- ✅ Green checkmark = Success!
- ❌ Red X = Failed (check logs)

### Step 4: Download Artifacts

Once complete:
1. Scroll to bottom of workflow run
2. Find **Artifacts** section
3. Click `firmware` to download
4. Unzip the file

You'll get:
- `anywhy_flake_left_ble-xiao_ble-zmk.uf2`
- `anywhy_flake_right_ble-xiao_ble-zmk.uf2`
- `settings_reset-xiao_ble-zmk.uf2`

## Understanding the Output Files

### File Naming Convention

Format: `{artifact-name}-{board}-zmk.uf2`

- `anywhy_flake_left_ble` - Your custom name
- `xiao_ble` - The board it's built for
- `zmk` - It's ZMK firmware
- `.uf2` - UF2 bootloader format

### UF2 Format

**What is UF2?**
- USB Flashing Format
- Drag-and-drop flashing (no tools needed!)
- Supported by most modern bootloaders
- Contains firmware + metadata

**Why UF2?**
- Easy: Just drag to USB drive
- Safe: Bootloader validates before flashing
- Universal: Works on Windows, Mac, Linux

## What You Learned

You now understand:

- ✅ The structure of `build.yaml`
- ✅ What `board`, `shield`, `snippet`, and `artifact-name` mean
- ✅ How left half becomes central (default from module)
- ✅ How right half becomes peripheral (default from module)
- ✅ The build process flow
- ✅ How to trigger and monitor builds
- ✅ What the output .uf2 files are

## Common Issues

### Build Fails: "Shield not found"

**Problem**: Can't find `anywhy_flake_left`

**Solution**:
- Check `west.yml` includes `flake-zmk-module`
- Check spelling in `build.yaml`
- Make sure module path is correct

### Build Fails: "snippet not found"

**Problem**: Can't find `studio-rpc-usb-uart`

**Solution**:
- This snippet comes from ZMK core
- Make sure you're using a recent ZMK version
- Try removing the snippet line temporarily

### No Artifacts Section

**Problem**: Build succeeded but no artifacts

**Solution**:
- Scroll all the way to bottom
- Look for "Artifacts" header
- If truly missing, re-run the workflow

### Artifacts Have Wrong Names

**Problem**: Files are named `xiao_ble-anywhy_flake_left-zmk.uf2`

**Solution**:
- You forgot `artifact-name` in `build.yaml`
- Add it and rebuild

## Quiz Yourself

Before moving on:

- ✅ Can you explain what each field in build.yaml does?
- ✅ Do you know where the left=central setting comes from?
- ✅ Can you describe the build process flow?
- ✅ Do you understand what a .uf2 file is?

## Next Steps

Now that you have firmware files, let's flash them to your keyboard!

→ **Next**: [04-building-and-flashing.md](04-building-and-flashing.md)
