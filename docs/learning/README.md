# ZMK Firmware Learning Path

Welcome! This directory contains a structured learning path for building ZMK firmware for your Anywhy Flake keyboard.

## What You'll Learn

By working through these documents, you'll learn:
- How ZMK configuration repositories work
- Device tree, Kconfig, and West systems
- How to build firmware for BLE and dongle modes
- How to customize keymaps and configuration
- How to troubleshoot common issues

## How to Use This Guide

1. **Start with [00-index.md](00-index.md)** - Overview and roadmap
2. **Follow the numbered sequence** - Each document builds on previous knowledge
3. **Do the hands-on exercises** - Actually perform the steps, don't just read
4. **Use the reference docs** - Refer back as needed

## Quick Start

**Complete beginner?** Start here:
1. [01-understanding-zmk-structure.md](01-understanding-zmk-structure.md)
2. [02-current-state.md](02-current-state.md)
3. [03-ble-mode-configuration.md](03-ble-mode-configuration.md)

**Want to get BLE mode working ASAP?** Start here:
1. [03-ble-mode-configuration.md](03-ble-mode-configuration.md)
2. [04-building-and-flashing.md](04-building-and-flashing.md)
3. [05-testing-ble.md](05-testing-ble.md)

**Want to add dongle mode?** Start here:
1. [09-dongle-configuration.md](09-dongle-configuration.md)

**Need troubleshooting help?** Go here:
1. [15-troubleshooting.md](15-troubleshooting.md)

## Document Index

### Foundation (Start Here)
- **[00-index.md](00-index.md)** - Complete roadmap and overview
- **[01-understanding-zmk-structure.md](01-understanding-zmk-structure.md)** - What is a ZMK config repo?
- **[02-current-state.md](02-current-state.md)** - What you already have

### BLE Mode (Core Lessons)
- **[03-ble-mode-configuration.md](03-ble-mode-configuration.md)** - Configure build targets
- **[04-building-and-flashing.md](04-building-and-flashing.md)** - Flash firmware to hardware
- **[05-testing-ble.md](05-testing-ble.md)** - Verify everything works

### Deep Understanding
- **[06-key-concepts.md](06-key-concepts.md)** - Device tree, Kconfig, West explained
- **[07-architecture.md](07-architecture.md)** - BLE vs Dongle architecture (TODO)

### Dongle Mode
- **[08-dongle-hardware.md](08-dongle-hardware.md)** - Wiring guide (TODO)
- **[09-dongle-configuration.md](09-dongle-configuration.md)** - Add dongle support
- **[10-dongle-testing.md](10-dongle-testing.md)** - Flash and test dongle (TODO)

### Customization
- **[11-keymap-customization.md](11-keymap-customization.md)** - Custom keymaps (TODO)
- **[12-screen-customization.md](12-screen-customization.md)** - Tweak dongle display (TODO)
- **[13-advanced-topics.md](13-advanced-topics.md)** - Local builds, debugging (TODO)

### Reference
- **[14-file-reference.md](14-file-reference.md)** - Complete file documentation
- **[15-troubleshooting.md](15-troubleshooting.md)** - Common issues (TODO)
- **[16-resources.md](16-resources.md)** - Community and docs (TODO)

## Learning Tracks

### Track 1: Beginner - BLE Mode Only (Week 1)
Perfect if you're new to ZMK and want a working keyboard quickly.

1. Understanding ZMK Structure (01)
2. Current State Assessment (02)
3. BLE Mode Configuration (03)
4. Building and Flashing (04)
5. Testing BLE (05)
6. ✅ You have a working keyboard!

### Track 2: Deep Dive - Understanding Systems (Week 2)
For those who want to really understand how it all works.

1. Complete Track 1 first
2. Key Concepts Explained (06)
3. Architecture Deep Dive (07)
4. File Reference (14)
5. ✅ You understand the internals!

### Track 3: Advanced - Dongle Mode (Week 3)
Add dongle mode with screen support.

1. Complete Tracks 1 & 2 first
2. Dongle Hardware Preparation (08)
3. Dongle Configuration (09)
4. Dongle Testing (10)
5. ✅ You have both BLE and dongle modes!

### Track 4: Customization - Make It Yours (Week 4)
Customize keymap, display, and advanced features.

1. Complete Tracks 1-3 first
2. Keymap Customization (11)
3. Screen Customization (12)
4. Advanced Topics (13)
5. ✅ Your personalized keyboard!

## Current Completion Status

Documents completed:
- ✅ 00-index.md - Overview
- ✅ 01-understanding-zmk-structure.md - Structure explained
- ✅ 02-current-state.md - Assessment
- ✅ 03-ble-mode-configuration.md - BLE config
- ✅ 04-building-and-flashing.md - Flashing guide
- ✅ 05-testing-ble.md - Testing guide
- ✅ 06-key-concepts.md - Deep concepts
- ✅ 09-dongle-configuration.md - Dongle config
- ✅ 14-file-reference.md - Complete reference

TODO documents:
- ⏳ 07-architecture.md - Architecture comparison
- ⏳ 08-dongle-hardware.md - Wiring guide
- ⏳ 10-dongle-testing.md - Dongle testing
- ⏳ 11-keymap-customization.md - Keymap guide
- ⏳ 12-screen-customization.md - Screen tweaks
- ⏳ 13-advanced-topics.md - Advanced features
- ⏳ 15-troubleshooting.md - Common issues
- ⏳ 16-resources.md - External resources

## Your Current Status

Based on your repository state:
- ✅ You have `west.yml` with all modules
- ✅ You have `build.yaml` started
- ⚠️ BLE mode targets need artifact names
- ❌ Dongle shield files need to be created
- ❌ Peripheral config files need to be created

**Recommended next step**: Follow [03-ble-mode-configuration.md](03-ble-mode-configuration.md) to fix your BLE mode build first.

## Getting Help

While working through these documents:

**Ask Claude**: I can help with:
- Explaining concepts you don't understand
- Debugging build errors
- Finding configuration options
- Reviewing your files
- Suggesting improvements

**Check troubleshooting**: [15-troubleshooting.md](15-troubleshooting.md) has solutions to common issues

**Community resources**: [16-resources.md](16-resources.md) lists external help

## Tips for Success

1. **Don't rush** - Take time to understand each concept
2. **Do the exercises** - Reading isn't enough, you need hands-on practice
3. **Break when stuck** - If confused, take a break and come back fresh
4. **Ask questions** - There are no stupid questions
5. **Experiment** - Try things, break things, learn from mistakes
6. **Document your progress** - Keep notes of what you learn
7. **Celebrate wins** - Each working build is an achievement!

## Time Estimates

- **Week 1** (BLE mode): 4-6 hours total
  - Reading: 2 hours
  - Hands-on: 2-4 hours

- **Week 2** (Understanding): 3-4 hours total
  - Reading: 2-3 hours
  - Experimentation: 1-2 hours

- **Week 3** (Dongle mode): 5-7 hours total
  - Hardware: 1-2 hours
  - Configuration: 2 hours
  - Testing/debugging: 2-3 hours

- **Week 4** (Customization): Varies by goals
  - Simple keymap changes: 1-2 hours
  - Advanced customization: 5+ hours

**Total**: ~15-20 hours for complete mastery

## Philosophy

This learning path follows these principles:

1. **Learn by doing** - Hands-on practice beats passive reading
2. **Incremental complexity** - Start simple, add complexity gradually
3. **Explain the why** - Understand concepts, not just copy-paste
4. **Practical focus** - Learn what you need to be productive
5. **Reference available** - Detailed docs when you need them

## What Makes This Different

Unlike typical documentation:
- ✅ **Structured path** - Clear progression from beginner to advanced
- ✅ **Context for beginners** - Explains *why*, not just *what*
- ✅ **Real examples** - Based on your actual setup
- ✅ **Troubleshooting included** - Common issues and solutions
- ✅ **Reference docs** - Quick lookup when needed

## Contributing

Found an error or want to suggest an improvement?
- Fix typos directly
- Add clarifying examples
- Suggest better explanations
- Report outdated information

## Credits

Based on the original comprehensive learning plan for Anywhy Flake with dongle mode.

## License

These learning materials are provided as-is for educational purposes.

---

**Ready to start learning?** → [00-index.md](00-index.md)
