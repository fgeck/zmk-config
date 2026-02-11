# Building and Flashing BLE Mode Firmware

Time to get firmware onto your keyboard! This is where it gets exciting.

## Prerequisites

Before flashing:

- ✅ You've built BLE mode firmware (previous lesson)
- ✅ Downloaded and unzipped `firmware.zip`
- ✅ Have USB-C cable that supports **data** (not charge-only!)
- ✅ Have both keyboard halves ready

## Understanding the Flashing Process

### What is "Flashing"?

**Flashing** = Writing firmware to the microcontroller's flash memory

Think of it like:
- Installing an operating system on your computer
- But for a tiny embedded device
- Replaces everything that was there before

### UF2 Bootloader Mode

The XIAO BLE has a built-in **bootloader**:
- Special mode for receiving new firmware
- Shows up as a USB drive when activated
- Accepts .uf2 files via drag-and-drop
- Automatically flashes and reboots

### How to Enter Bootloader Mode

**Method**: Double-tap the reset button

1. Connect XIAO BLE via USB-C
2. Quickly press reset button twice (like double-clicking a mouse)
3. USB drive appears named "XIAO-SENSE" or similar
4. LED may pulse or stay solid (depends on version)

**Timing**: Double-tap within ~0.5 seconds

## Step-by-Step: Flash Left Half

### Step 1: Connect Left Half

1. Disconnect any other XIAO BLE devices
2. Connect left keyboard half to your Mac via USB-C
3. Verify USB is working (device should power on)

### Step 2: Enter Bootloader Mode

1. Find the tiny reset button on the XIAO BLE
2. Double-tap it quickly
3. Wait 1-2 seconds

**Expected result**: A USB drive appears in Finder

- Drive name: "XIAO-SENSE" (or "XIAO_BLE", "XINIAO")
- Contains: `INDEX.HTM`, `INFO_UF2.TXT`, `CURRENT.UF2`

**Troubleshooting**:
- No drive appears? Try double-tapping again (timing is tricky)
- Still nothing? Check your USB cable (must support data)
- LED not responding? Check power connection

### Step 3: Flash the Firmware

1. Open the folder where you unzipped firmware
2. Find `anywhy_flake_left_ble-xiao_ble-zmk.uf2`
3. Drag it to the XIAO USB drive
4. Drop it

**What happens**:
- File copies to the drive
- Bootloader validates the firmware
- Automatically flashes the chip
- Drive disappears (device reboots)
- **This is normal!**

**Duration**: 2-5 seconds

### Step 4: Verify

After the drive disappears:
- LED behavior may change
- Device is now running ZMK firmware
- It's trying to connect via Bluetooth

**Don't pair yet!** Flash the right half first.

## Step-by-Step: Flash Right Half

### Step 1: Disconnect Left Half

1. Unplug left half from USB
2. Wait a few seconds
3. Make sure it's fully disconnected

**Why?** Prevents confusion between halves during flashing.

### Step 2: Connect Right Half

1. Connect right keyboard half via USB-C
2. Verify it powers on

### Step 3: Enter Bootloader Mode

1. Double-tap reset button on right half
2. Wait for USB drive to appear

### Step 4: Flash the Firmware

1. Find `anywhy_flake_right_ble-xiao_ble-zmk.uf2`
2. Drag it to the XIAO USB drive
3. Wait for auto-disconnect

**Critical**: Make sure you're using the **RIGHT** firmware file!
- Left firmware on left half
- Right firmware on right half
- **Never mix them up!**

### Step 5: Both Halves Flashed

You now have:
- ✅ Left half with BLE central firmware
- ✅ Right half with BLE peripheral firmware

## Understanding First Boot

### What Happens After Flashing

**Left half (central)**:
1. Boots up
2. Initializes BLE radio
3. Starts advertising as "Anywhy Flake" keyboard
4. Also starts scanning for right half
5. LED may blink (indicates BLE activity)

**Right half (peripheral)**:
1. Boots up
2. Initializes BLE radio
3. Starts advertising to left half
4. Waits for connection from left
5. LED may blink differently

### First Pairing Sequence

The first time, the halves need to pair with each other:

1. **Power on LEFT half first**
   - Starts advertising to your Mac
   - Starts scanning for right half

2. **Power on RIGHT half**
   - Starts advertising
   - LEFT half discovers it
   - They pair automatically

3. **Wait 5-10 seconds**
   - Pairing completes
   - LEDs may stabilize
   - Both halves are now connected

**Important**: Always power on left half first (the central)!

## Pairing with macOS

Now let's connect your keyboard to your Mac.

### Step 1: Ensure Both Halves Are On

- Left half powered on
- Right half powered on
- Wait 10 seconds for them to pair

### Step 2: Open Bluetooth Settings

1. Click  → **System Settings** (or **System Preferences**)
2. Click **Bluetooth**
3. Make sure Bluetooth is **On**

### Step 3: Find Your Keyboard

In the device list, you should see:
- **"Anywhy Flake"** (or similar name)
- Status: "Not Connected" or "Discoverable"

**Don't see it?**
- Wait a bit longer (up to 30 seconds)
- Check left half is powered on
- Try toggling Mac's Bluetooth off and on

### Step 4: Connect

1. Click **Connect** next to "Anywhy Flake"
2. Wait for "Connected" status
3. Done!

**No pairing code needed** - ZMK keyboards just connect.

### Step 5: Test

Open a text editor and type on both halves:
- Left side keys should work
- Right side keys should work
- All keys should produce output

🎉 **Success!** Your keyboard is working!

## LED Indicators (If Present)

Some XIAO BLE boards have LEDs that indicate status:

| LED Pattern | Meaning |
|-------------|---------|
| Solid/breathing | Normal operation |
| Fast blink | Advertising (looking for computer) |
| Slow blink | Connected, low activity |
| Off | Sleep mode or powered off |

**Note**: LED behavior varies by firmware version and settings.

## Power Management

### Battery vs USB Power

**Left half (BLE mode)**:
- Can run on battery OR USB
- When typing, uses power from active source
- USB charges the battery (if connected)

**Right half (BLE mode)**:
- Typically runs on battery
- Connects wirelessly to left half
- Can plug in USB for charging only

### Sleep Mode

ZMK has built-in power saving:

**Idle timeout**: 30 seconds
- Keyboard enters low-power mode
- Wakes on key press

**Sleep timeout**: 15 minutes
- Keyboard deep sleeps
- Press any key to wake
- May take 1-2 seconds to reconnect

**To disable sleep** (while learning):
- Create `boards/shields/anywhy_flake/anywhy_flake.conf`
- Add: `CONFIG_ZMK_SLEEP=n`
- Rebuild and reflash

## Troubleshooting

### Left Half Won't Connect to Mac

**Check**:
- Is left half powered on?
- Is Bluetooth enabled on Mac?
- Try: Settings → Bluetooth → Turn off/on

**Try**:
- Power cycle left half (off/on)
- Forget device on Mac, reconnect
- Flash `settings_reset.uf2`, then reflash firmware

### Right Half Keys Don't Work

**Check**:
- Is right half powered on?
- Are both halves close together? (within 3 feet)

**Try**:
- Power cycle right half
- Power on LEFT first, wait 5 seconds, then RIGHT
- Flash `settings_reset.uf2` to BOTH halves, reflash firmware

### Only Left or Right Side Works

**Problem**: Wrong firmware on wrong half

**Solution**:
1. Flash `settings_reset.uf2` to BOTH halves
2. Re-flash correct firmware:
   - LEFT firmware → left half
   - RIGHT firmware → right half
3. Power on left first, then right

### Keys Produce Wrong Characters

**Problem**: Keymap issue (not flashing issue)

**Solution**:
- This is expected if using default keymap
- You'll customize keymap later
- For now, just verify keys respond

### Can't Enter Bootloader Mode

**Problem**: Double-tap not working

**Try**:
- Practice the timing (faster double-tap)
- Use a pen/stylus for precision
- Check if reset button is functional
- Try single long press, release, quick tap

**Alternative** (if button broken):
- Short RST pin to GND twice (advanced)
- Use existing bootloader files if present

### Drive Disappears Immediately

**Problem**: Wrong file dragged, or corrupt firmware

**Solution**:
- Re-download firmware from GitHub Actions
- Verify file is .uf2 format
- Check file isn't corrupted (re-download artifact)

### Mac Shows Multiple "Anywhy Flake" Devices

**Problem**: Old BLE profiles from previous flashing

**Solution**:
1. Forget all "Anywhy Flake" entries
2. Flash `settings_reset.uf2` to left half
3. Reflash left half with BLE firmware
4. Reconnect

## What You Learned

You now know:

- ✅ How to enter UF2 bootloader mode (double-tap reset)
- ✅ How to flash firmware via drag-and-drop
- ✅ The proper flashing sequence (left, then right)
- ✅ How to pair keyboard halves
- ✅ How to connect to macOS via Bluetooth
- ✅ Basic troubleshooting steps

## Important Reminders

1. **Always match firmware to hardware**
   - Left firmware → left half
   - Right firmware → right half

2. **Power on sequence matters**
   - Left (central) first
   - Wait a few seconds
   - Then right (peripheral)

3. **Settings reset is your friend**
   - Fixes most pairing issues
   - Use it when switching modes
   - Flash it, wait, then flash normal firmware

4. **USB cable quality matters**
   - Must support data, not just charging
   - If flashing fails, try a different cable

## Next Steps

Now that your keyboard is flashed and working, let's test it thoroughly!

→ **Next**: [05-testing-ble.md](05-testing-ble.md)
