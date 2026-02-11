# ZMK Firmware Learning Path for Anywhy Flake

## Welcome!

This learning path will guide you through building ZMK firmware for your Anywhy Flake keyboard from scratch. Work through these documents in order, taking time to understand each concept before moving on.

## Your Setup

- **Keyboard**: Anywhy Flake M (46-47 keys)
- **Controllers**: 3× Seeeduino XIAO BLE
- **Display**: ST7789V (for dongle)
- **Computer**: macOS
- **Approach**: Learn by building everything from scratch

## Learning Path

### Phase 1: Foundation
1. **[Understanding ZMK Structure](01-understanding-zmk-structure.md)** - Learn what a ZMK config repository is and how it works
2. **[Current State Assessment](02-current-state.md)** - Understand what you already have

### Phase 2: BLE Mode (Start Here)
3. **[BLE Mode Configuration](03-ble-mode-configuration.md)** - Build your first working firmware
4. **[Building and Flashing](04-building-and-flashing.md)** - Get firmware on your keyboard
5. **[Testing BLE Mode](05-testing-ble.md)** - Verify everything works

### Phase 3: Deep Understanding
6. **[Key Concepts Explained](06-key-concepts.md)** - Device trees, Kconfig, West modules
7. **[Architecture Deep Dive](07-architecture.md)** - BLE vs Dongle mode explained

### Phase 4: Dongle Mode
8. **[Dongle Hardware Preparation](08-dongle-hardware.md)** - Wiring and components
9. **[Dongle Configuration](09-dongle-configuration.md)** - Add dongle support to your repo
10. **[Dongle Testing](10-dongle-testing.md)** - Flash and test dongle mode

### Phase 5: Customization
11. **[Keymap Customization](11-keymap-customization.md)** - Make it yours
12. **[Screen Customization](12-screen-customization.md)** - Tweak the dongle display
13. **[Advanced Topics](13-advanced-topics.md)** - Local builds, debugging

### Reference
14. **[Complete File Reference](14-file-reference.md)** - All files explained
15. **[Troubleshooting Guide](15-troubleshooting.md)** - Common issues and solutions
16. **[Resources and Community](16-resources.md)** - Where to learn more

## How to Use This Guide

1. **Read in order** - Each document builds on previous knowledge
2. **Take your time** - Don't rush through concepts
3. **Hands-on practice** - Actually do the steps, don't just read
4. **Experiment** - Try things, break things, learn from mistakes
5. **Ask questions** - Use Claude to clarify anything confusing

## Current Status Checklist

Mark your progress as you go:

- [ ] Phase 1: Understanding ZMK structure
- [ ] Phase 2: BLE mode working
- [ ] Phase 3: Understand key concepts
- [ ] Phase 4: Dongle mode working
- [ ] Phase 5: Custom keymap and configuration

## Learning Goals

By the end of this path, you'll understand:
- ✅ What a ZMK user config repository is
- ✅ How West manages dependencies
- ✅ Device tree syntax and purpose
- ✅ Kconfig configuration system
- ✅ BLE vs Dongle architecture
- ✅ How to customize keymaps
- ✅ How to troubleshoot build issues
- ✅ How to add advanced features

## Time Estimate

- **Week 1**: BLE mode working (Phases 1-2)
- **Week 2**: Deep understanding (Phase 3)
- **Week 3**: Dongle mode working (Phase 4)
- **Week 4**: Customization (Phase 5)

**Remember**: This is a learning journey, not a race. Take time to understand each concept!

---

**Ready to start?** → [01-understanding-zmk-structure.md](01-understanding-zmk-structure.md)
