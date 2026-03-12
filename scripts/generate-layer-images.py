#!/usr/bin/env python3
"""Generate separate SVG images for each layer.

Base layer includes a dedicated Combos layer drawing below it.
Other layers are rendered individually.
"""

import sys
import yaml
import copy


def filter_for_flake_m(data):
    """Convert Flake L (58 keys) to Flake M (46 keys)."""
    if "layers" in data:
        for layer_name in data["layers"]:
            keys = data["layers"][layer_name]
            if isinstance(keys, list) and len(keys) == 58:
                data["layers"][layer_name] = keys[12:]

    if "combos" in data:
        new_combos = []
        for combo in data["combos"]:
            if "p" in combo:
                if all(p >= 12 for p in combo["p"]):
                    combo["p"] = [p - 12 for p in combo["p"]]
                    new_combos.append(combo)
        data["combos"] = new_combos

    data["layout"] = {"qmk_info_json": "docs/keymap-drawer/anywhy_flake_m.json"}
    return data


def extract_base_with_combos(data):
    """Extract Base layer with a dedicated Combos layer below it."""
    result = copy.deepcopy(data)

    if "layers" not in result or "Base" not in result["layers"]:
        return None

    num_keys = len(result["layers"]["Base"])

    # Create two layers: Base and Combos
    result["layers"] = {
        "Base": result["layers"]["Base"],
        "Combos": [""] * num_keys,  # Empty keys, combos will be drawn on top
    }

    # Assign all combos to the Combos layer
    if "combos" in result:
        for combo in result["combos"]:
            combo["l"] = ["Combos"]

    return result


def extract_single_layer(data, layer_name):
    """Extract a single layer from the keymap data (no combos)."""
    result = copy.deepcopy(data)

    if "layers" not in result or layer_name not in result["layers"]:
        return None

    # Keep only the specified layer
    result["layers"] = {layer_name: result["layers"][layer_name]}

    # No combos for individual layers
    result["combos"] = []

    return result


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: generate-layer-images.py <layer_name> [--with-combos]",
            file=sys.stderr,
        )
        print(
            "       Reads keymap YAML from stdin, outputs filtered YAML to stdout",
            file=sys.stderr,
        )
        print("", file=sys.stderr)
        print("Layers: Base, Num, Nav, Fn, Idea", file=sys.stderr)
        print("", file=sys.stderr)
        print(
            "--with-combos: For Base layer, adds a dedicated Combos layer drawing",
            file=sys.stderr,
        )
        sys.exit(1)

    layer_name = sys.argv[1]
    include_combos = "--with-combos" in sys.argv

    data = yaml.safe_load(sys.stdin)
    filtered = filter_for_flake_m(data)

    if layer_name == "Base" and include_combos:
        layer_data = extract_base_with_combos(filtered)
    else:
        layer_data = extract_single_layer(filtered, layer_name)

    if layer_data is None:
        print(f"Error: Layer '{layer_name}' not found", file=sys.stderr)
        sys.exit(1)

    yaml.dump(
        layer_data,
        sys.stdout,
        default_flow_style=None,
        allow_unicode=True,
        sort_keys=False,
        width=160,
    )


if __name__ == "__main__":
    main()
