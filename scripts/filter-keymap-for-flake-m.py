#!/usr/bin/env python3
"""Filter Flake L (58 keys) → Flake M (46 keys). Adds virtual Combos layer."""

import sys
import yaml


def filter_for_flake_m(data, add_combos_layer=True):
    if "layers" in data:
        for layer_name in data["layers"]:
            keys = data["layers"][layer_name]
            if isinstance(keys, list) and len(keys) == 58:
                data["layers"][layer_name] = keys[12:]

    num_keys = 46
    if "layers" in data and data["layers"]:
        first_layer = list(data["layers"].values())[0]
        if isinstance(first_layer, list):
            num_keys = len(first_layer)

    if "combos" in data:
        new_combos = []
        for combo in data["combos"]:
            if "p" in combo:
                if all(p >= 12 for p in combo["p"]):
                    combo["p"] = [p - 12 for p in combo["p"]]
                    if add_combos_layer:
                        combo["l"] = ["Combos"]
                    new_combos.append(combo)
        data["combos"] = new_combos

    if add_combos_layer and "layers" in data:
        old_layers = data["layers"]
        new_layers = {}

        if "Base" in old_layers:
            new_layers["Base"] = old_layers["Base"]

        new_layers["Combos"] = [""] * num_keys

        for layer_name in ["Nav", "Num", "Fn", "Idea"]:
            if layer_name in old_layers:
                new_layers[layer_name] = old_layers[layer_name]

        for layer_name in old_layers:
            if layer_name not in new_layers:
                new_layers[layer_name] = old_layers[layer_name]

        data["layers"] = new_layers

    data["layout"] = {"qmk_info_json": "docs/keymap-drawer/anywhy_flake_m.json"}
    return data


if __name__ == "__main__":
    add_combos_layer = "--no-combos-layer" not in sys.argv
    data = yaml.safe_load(sys.stdin)
    filtered = filter_for_flake_m(data, add_combos_layer=add_combos_layer)
    yaml.dump(
        filtered,
        sys.stdout,
        default_flow_style=None,
        allow_unicode=True,
        sort_keys=False,
        width=160,
    )
