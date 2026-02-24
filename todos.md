# Todo

## Still do address

1. Concern: alt+tab+ arrow key for app switching --> Fully rely on Aerospace or use HomeRowMods: ; + tab or ; + shift + tab
2. Concern ctrl+tab, ctrl+shift+tab for in browser tab switching --> HomeRowMods: k + tab or k + shift + tab
3. Concern: copy, cut, paste, undo, redo. Myrioku Nav Layer? --> Myrioku layer as safety net AND HomeRowMods ; + C, ; + V, ; + X, ; + Z, ; + F + Z AND Left Hand Combos for Mouse as Urob does it: X + C = Cmd+X (Cut)
X + D = Cmd+C (Copy)
C + V = Cmd+V (Paste)
Z + X = Cmd+Z (Undo)

## Aerospace remapping and german umlauts conflict resolution

1. Until now aerospace workspaces were mapped to: 1,2,3,4 q,w,e,r. They need to be mapped to: q,w,e,r a,s,d,f. This would conflict with opt+a and german umlauts keyboard. Remap aerospace workspaces as described. Config can be found in: ~/.config/aerospace/* modify all 3 configs.
2. Use Urobs Unicode ZMK module to directly send the Umlaut on double tap and I can switch to plain US International Keyboard Layout in MacOS. Remove the alt+a/o/u that are currently configured. 

### Conclusion

Not implemented, as using MacOS Hex Input would deactivate important behavior like opt+arrow keys for movement.
Therefore, use ctrl for aerospace and move workspaces to: q,w,e,r,a,s,d,f

## Build HomeRowMods Urob style on Base layer

1. build urobs timeless homerowmods, but use the myrioku layout (from left to right: gui alt ctrl shift on left and shift ctrl alt gui on right). Consider on some layers the sticky homerow mods. See the drawins in the comments and consult urobs repo if needed.

## Urobs Combo Layers

1. Build urobs vertical combo layers for the symbols: q+a -> !, w+s -> @ etc.

## Build the Nav Layer

1. On the Nav layer, Build urobs Arrow-cluster doubles as home, end, begin/end of document on long-press. But remember I work on a mac. So instead of ctrl I need to use alt/opt.
Hold-tap on navigation keys:
| Tap | Hold |
|-----|------|
| ← Left | Home |
| → Right | End |
| ↑ Up | Alt+Home (begin of document) |
| ↓ Down | Alt+End (end of document) |
| Backspace | Alt+Backspace (delete word) |
| Delete | Alt+Delete (delete word forward) |

## Move the Fn Layer

1. The Fn layer of flake can be moved to a hard to reach thumb key. Most important I need to have control over BT profile selection and BT profile clearance and ST_UNLOCK to unlock while in ZMK studio. 


## IntelliJ Layer (Hold outer thumb), needs to be adapted. 

What I use most: 
- double shift
- cmd shift f
- cmd shift r
- ctrl t
- cmd b (declaration usage)
- cmd shift b (is implemented by)
- opt cmd left (go to last navigated element)
- opt up/down (move line up/down)
- F2 (go to err)
- F3
- F4
- copy/paste/cut undo/redo

There is no need to map those all to a dedicated intellij layer, but the overall layout must make sense!

Idea: 

- right in-intillij nav: 
  - top row: project, copilot, git
  - middle row: terminal, debug, run, services coverage
  - lower row: structure, gradle, database

- left side hotkeys: 
  - top row: cmd b (declaration usage), cmd shift b (is implemented by)
  - middle row:
  - lower row:
//                                In-IntelliJ-Navigation                                                          In-IntelliJ-Edit/Nav
//         ┏╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┓                     ┏╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┳╍╍╍╍╍╍╍╍╍┓
//         ┃ ------  ┃ ------  ┃ ------  ┃ ------  ┃ ------  ┃ ------  ┃                     ┃ ------  ┃ ------  ┃ ------  ┃ ------  ┃ ------  ┃ ------  ┃
//         ┣━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┫                     ┣━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┫
//         ┃  ENTER  ┃ CMD+1   ┃ CMD+2   ┃ CMD+3   ┃ CMD+4   ┃  CMD+5  ┃                     ┃OPT+CMD+←┃OPT+CMD+→┃ CMD+B   ┃CMD+Shift┃         ┃  BSPC   ┃
//         ┃         ┃         ┃         ┃         ┃         ┃         ┃                     ┃ go back ┃go forwd.┃         ┃   + B   ┃         ┃         ┃
//         ┣━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┫                     ┣━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┫
//         ┃   TAB   ┃ CMD+    ┃ CMD+    ┃ CMD+    ┃ CMD+    ┃ CMD+    ┃                     ┃  F2     ┃         ┃         ┃         ┃         ┃         ┃
//         ┃         ┃ Shift+1 ┃ Shift+2 ┃ Shift+3 ┃ Shift+4 ┃ Shift+5 ┃                     ┃ go err  ┃         ┃         ┃         ┃         ┃         ┃
//         ┣━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┫                     ┣━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┫
//         ┃         ┃ CTRL+1  ┃ CTRL+2  ┃ CTRL+3  ┃ CTRL+4  ┃ CTRL+5  ┃                     ┃ Shift + ┃CMD+SHIFT┃CMD+SHIFT┃ CTRL+T  ┃         ┃  ESC    ┃
//         ┃         ┃         ┃         ┃         ┃         ┃         ┃                     ┃  Shift  ┃  +F     ┃  +R     ┃         ┃         ┃         ┃
//         ┗━━━━━━━━━┻━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┓ ┏━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┻━━━━━━━━━┛
//                             ┃  ████   ┃   ALT   ┃   GUI   ┃  SPACE  ┃   NAV   ┃ ┃   NUM   ┃  SHIFT  ┃  GUI    ┃  ALT    ┃   FN    ┃
//                             ┗━━━━━━━━━┻━━━━━━━━━┻━━━━━━━━━┻━━━━━━━━━┻━━━━━━━━━┛ ┗━━━━━━━━━┻━━━━━━━━━┻━━━━━━━━━┻━━━━━━━━━┻━━━━━━━━━┛
