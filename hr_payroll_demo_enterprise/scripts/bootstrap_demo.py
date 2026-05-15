#!/usr/bin/env python3
"""Bootstrap ALLNETWORKS demo data (full or supplementary).

Usage:

  python hr_payroll_demo_enterprise/scripts/bootstrap_demo.py -c odoo.conf -d mydb
  python hr_payroll_demo_enterprise/scripts/bootstrap_demo.py -c odoo.conf -d mydb --supplementary
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-c", "--config", required=True, help="Odoo configuration file")
    parser.add_argument("-d", "--database", required=True, help="Database name")
    parser.add_argument(
        "--supplementary",
        action="store_true",
        help="Run idempotent loaders only (existing demo company)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Run full bootstrap even if demo company exists (dangerous on non-empty DBs)",
    )
    return parser.parse_args()


def _find_odoo_source(module_root: Path) -> Path:
    for parent in [module_root, *module_root.parents]:
        candidate = parent / "odoo19"
        if (candidate / "odoo").is_dir():
            return candidate
    raise SystemExit("Cannot find Odoo source directory (expected .../odoo19/odoo).")


def _load_hooks(module_root: Path):
    spec = importlib.util.spec_from_file_location("hr_payroll_demo_hooks", module_root / "hooks.py")
    hooks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hooks)
    return hooks


def main():
    args = _parse_args()
    module_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(_find_odoo_source(module_root)))

    import odoo
    from odoo import SUPERUSER_ID, api
    from odoo.modules.registry import Registry

    hooks = _load_hooks(module_root)
    odoo.tools.config.parse_config(["-c", args.config, "-d", args.database])
    registry = Registry(args.database)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        if args.supplementary:
            ok = hooks.bootstrap_supplementary_demo_data(env)
            label = "supplementary"
        else:
            ok = hooks.bootstrap_all_demo_data(env, force=args.force)
            label = "full"
        cr.commit()
        print(f"Demo bootstrap ({label}): {'completed' if ok else 'skipped (already present)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
