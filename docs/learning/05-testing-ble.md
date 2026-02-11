# Testing BLE Mode

Now that your keyboard is flashed and paired, let's thoroughly test it to ensure everything works correctly.

## Testing Checklist

Use this checklist as you test:

- [ ] All keys on left half respond
- [ ] All keys on right half respond
- [ ] Modifiers work (Shift, Ctrl, Cmd, Alt)
- [ ] Layer switching works
- [ ] Special keys work (arrows, etc.)
- [ ] Bluetooth stays connected
- [ ] Battery indicator works (if visible)
- [ ] Sleep/wake works
- [ ] Multiple BLE profiles work (optional)

## Basic Connectivity Test

### Test 1: Both Halves Connected

**What to check**:
1. Mac shows "Anywhy Flake - Connected" in Bluetooth settings
2. Both keyboard halves are powered on
3. No error indicators

**Pass criteria**: ✅ Stable connection showing in Bluetooth settings

### Test 2: Open a Text Editor

1. Open TextEdit, Notes, or any text editor
2. Click in the text area
3. Ready to type

## Key Matrix Test

### Test 3: Left Half Keys

Type all keys on the left half systematically:

**Top row** (numbers/symbols):
- Press each key in the top row
- Verify each produces output

**Home row**:
- Press each key in the home row
- Check for consistent response

**Bottom row**:
- Press each key in the bottom row
- Verify all work

**Thumb keys**:
- Press each thumb key
- Check response

**Expected**: Every key produces some output (even if it's not the expected character - that's okay for now)

**Fail if**: Any key is completely dead (no output at all)

### Test 4: Right Half Keys

Repeat the same process for the right half:
- Top row
- Home row
- Bottom row
- Thumb keys

**Expected**: All keys respond

### Test 5: Simultaneous Typing

Type using both hands simultaneously:
- Type "asdf jkl;" quickly
- Type random words using both hands
- Roll fingers across keys

**Expected**: All key presses register, no missed keys

**Fail if**: Keys from one side don't register when typing on both sides

## Modifier Keys Test

### Test 6: Shift Keys

**Left shift**:
1. Hold left shift
2. Type letters
3. Should produce UPPERCASE

**Right shift**:
1. Hold right shift
2. Type letters
3. Should produce UPPERCASE

**Both shifts**:
1. Hold both shifts
2. Type letters
3. Should produce UPPERCASE

### Test 7: Control/Command/Alt

Test each modifier:

**Cmd+C** (copy):
1. Type some text
2. Select it
3. Press Cmd+C
4. Text should be copied

**Cmd+V** (paste):
1. Press Cmd+V
2. Text should paste

**Other combos**:
- Cmd+A (select all)
- Cmd+S (save)
- Cmd+Tab (switch apps)

**Expected**: All modifier combos work

## Layer Switching Test

### Understanding Layers

ZMK keyboards have **layers** (like Shift, but for entire layouts):

- **Layer 0**: Base layer (letters, numbers)
- **Layer 1**: Function layer (F-keys, arrows, media)
- **Layer 2**: Adjustment layer (Bluetooth, RGB, etc.)

### Finding Your Layer Keys

Check the default keymap in `flake-zmk-module`:
- Usually a thumb key activates layers
- Look for `&mo 1` (momentary layer 1)
- Or `&lt 1 SPACE` (layer-tap)

### Test 8: Switch to Layer 1

1. Hold the layer key (usually a thumb key)
2. While holding, press other keys
3. Should produce different output (F-keys, arrows, etc.)
4. Release layer key
5. Keys return to normal

**Expected**: Layer switch works smoothly

### Test 9: Layer Toggle (if available)

Some keymaps have `&tog 1` (toggle layer):
1. Tap the toggle key
2. Now on layer 1 permanently
3. All keys produce layer 1 output
4. Tap toggle again
5. Return to layer 0

## Bluetooth Features Test

### Test 10: Multiple BLE Profiles (Optional)

ZMK supports up to 5 BLE profiles (connect to 5 devices):

**Setup**:
- Layer with BT keys: `&bt BT_SEL 0`, `&bt BT_SEL 1`, etc.
- Usually on layer 2 or 3

**Test**:
1. Currently connected to Mac (profile 0)
2. Switch to profile 1: Press BT1 key
3. Keyboard disconnects from Mac
4. Keyboard starts advertising again
5. Connect to different device (iPhone, iPad, etc.)
6. Switch back to profile 0: Press BT0 key
7. Reconnects to Mac

**Expected**: Can switch between devices seamlessly

### Test 11: Clear Bluetooth Bonds

**Clear a profile**:
1. Access BT layer
2. Press `&bt BT_CLR` (clear current profile)
3. Keyboard should forget current pairing
4. Starts advertising for new pairing

**Expected**: Old pairing removed, ready to pair again

## Performance Tests

### Test 12: Typing Speed

Type normally for 30 seconds:
- No lag
- No missed keys
- Smooth experience

**Expected**: Responsive typing, no noticeable delay

### Test 13: Gaming/Fast Input

Rapidly press keys:
- Spam ASDF ASDF ASDF
- Press multiple keys simultaneously
- Rapid fire key presses

**Expected**: All presses register, no dropped inputs

### Test 14: Range Test

1. Start close to your Mac
2. Gradually move away while typing
3. Note where connection becomes unstable

**Expected range**:
- **Good**: 15-30 feet with clear line of sight
- **Acceptable**: 10-15 feet
- **Poor**: <10 feet (may indicate interference)

## Power Management Tests

### Test 15: Idle Timeout

1. Stop typing for 30 seconds
2. Keyboard should enter idle mode (low power)
3. Press any key
4. Should wake instantly and work

**Expected**: Instant wake, no lost key presses

### Test 16: Sleep Mode

1. Stop typing for 15 minutes (default sleep timeout)
2. Keyboard should deep sleep
3. Press any key to wake
4. May take 1-2 seconds to reconnect

**Expected**: Wakes within 2 seconds, reconnects to Mac

### Test 17: Battery Life Indication

**If you have a battery display**:
- Check battery percentage is shown
- Should be reasonable (>50% if recently charged)

**Without display**:
- You won't see battery level in BLE mode
- Use ZMK Studio or check logs (advanced)

## Split Communication Test

### Test 18: Half-to-Half Connection

**Test physical separation**:
1. Power on both halves
2. Move them apart gradually
3. Type on each half while separated
4. Note maximum distance

**Expected**:
- **Good**: 3-6 feet apart
- **Acceptable**: 2-3 feet apart
- **Poor**: Must be touching

### Test 19: Reconnection After Power Loss

1. Type normally (both halves working)
2. Power off RIGHT half
3. Left half keys still work, right doesn't
4. Power on RIGHT half
5. Should reconnect automatically within 5-10 seconds
6. Right keys work again

**Expected**: Automatic reconnection, no manual intervention

## Keymap Verification

### Test 20: Special Keys

Test any special keys in your layout:

- **Arrow keys**: Up, Down, Left, Right
- **Media keys**: Volume, Play/Pause, Next/Prev
- **Function keys**: F1-F12
- **Navigation**: Home, End, PgUp, PgDn

**Expected**: All special keys work as intended

### Test 21: Combos (if configured)

If your keymap has combos (multi-key shortcuts):

Example: Press Q+W together → Esc

Test each combo:
1. Press keys simultaneously
2. Should trigger combo action

## Common Issues & Solutions

### Some Keys Don't Work

**Possible causes**:
1. **Physical issue**: Bad solder joint, broken switch
2. **Matrix issue**: Wrong pin configuration
3. **Firmware issue**: Keymap error

**Diagnosis**:
- If entire row/column dead: Matrix issue
- If single key dead: Physical issue
- If wrong character: Keymap issue

**Solution**:
- Check hardware first
- Verify keymap syntax
- Test with default keymap

### Intermittent Disconnections

**Possible causes**:
1. **Interference**: Other Bluetooth devices nearby
2. **Low battery**: Charge the keyboard
3. **Range**: Too far from computer
4. **Firmware bug**: Rare, but possible

**Solution**:
- Move closer to Mac
- Charge battery
- Remove other BLE devices
- Re-flash firmware

### Right Half Doesn't Connect to Left

**Possible causes**:
1. **Wrong firmware**: Mixed up left/right
2. **Not paired**: Need to pair halves first
3. **Out of range**: Too far apart

**Solution**:
1. Flash `settings_reset.uf2` to BOTH halves
2. Re-flash correct firmware to each half
3. Power on LEFT first, wait 5 seconds, then RIGHT
4. Keep halves within 3 feet

### Modifier Keys Stuck

**Symptoms**: Everything types uppercase, or Cmd always active

**Cause**: Modifier state corrupted

**Solution**:
1. Press and release all modifier keys
2. If persists: Disconnect/reconnect Bluetooth
3. If still stuck: Reflash firmware

### Lag or Missed Keys

**Possible causes**:
1. **Interference**: Bluetooth congestion
2. **Low battery**: Not enough power
3. **Distance**: Too far from Mac
4. **Computer issue**: Mac Bluetooth problem

**Solution**:
- Change Wi-Fi channel (can interfere with BLE)
- Charge keyboard
- Move closer
- Restart Mac Bluetooth

## Test Results Documentation

Create a quick test log (optional but helpful):

```
Date: ___________
Firmware: anywhy_flake_left_ble / anywhy_flake_right_ble
Build: [commit hash from GitHub]

✅ All left keys working
✅ All right keys working
✅ Modifiers working
✅ Layer switching works
❌ BT profile switching: Not tested
✅ Range: ~20 feet
✅ Sleep/wake: Works

Notes:
- One key on right pinky column slightly unresponsive (hardware?)
- Battery level shows ~85%
- No lag or missed keys
```

## What You Learned

You now know:

- ✅ How to systematically test a keyboard
- ✅ What to expect from BLE performance
- ✅ How to test layer switching
- ✅ How to test BLE profiles
- ✅ Common issues and their solutions
- ✅ Your keyboard is working properly (or what needs fixing)

## Celebrate! 🎉

If most tests pass, **congratulations!** You have:
- Built firmware from source
- Flashed it to hardware
- Connected via Bluetooth
- Verified full functionality

This is a significant achievement!

## Next Steps

Now that BLE mode works, you can:

**Option A**: Use your keyboard and get comfortable with it
- Learn the layout
- Build muscle memory
- Identify what you want to customize

**Option B**: Dive deeper into understanding how it all works
- Learn about device trees
- Understand Kconfig
- Study the architecture

**Option C**: Start customizing
- Modify the keymap
- Adjust settings
- Make it yours

→ **For deep understanding**: [06-key-concepts.md](06-key-concepts.md)
→ **For customization**: [11-keymap-customization.md](11-keymap-customization.md)
→ **For dongle mode**: [08-dongle-hardware.md](08-dongle-hardware.md)
