"""
================================================================================
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
"""
import time
import shutil
from pathlib import Path
from mooseherder import (MooseConfig,
                         MooseRunner,
                         GmshRunner)

GMSH_TAG = "stc_astested"
MOOSE_FILE = "stc_therm_funchs_wrad_std_ad"

GMSH_FILE = GMSH_TAG+".geo"
GMSH_PATH = Path("sims/") / GMSH_FILE
MOOSE_PATH = Path("sims/") / MOOSE_FILE
USER_DIR = Path.home()


def main() -> None:

    gmsh_runner = GmshRunner(USER_DIR / "gmsh/bin/gmsh")

    gmsh_start = time.perf_counter()
    gmsh_runner.run(GMSH_PATH,parse_only=True)
    gmsh_run_time = time.perf_counter()-gmsh_start

    shutil.copyfile(GMSH_PATH.parent / str(GMSH_TAG+".msh"),
                    MOOSE_PATH.parent / str(GMSH_TAG+".msh"))

    config = {"main_path": USER_DIR / "moose",
              "app_path": USER_DIR / "proteus",
              "app_name": "proteus-opt"}

    moose_config = MooseConfig(config)
    moose_runner = MooseRunner(moose_config)

    moose_runner.set_run_opts(n_tasks = 1,
                              n_threads = 8,
                              redirect_out = False)

    moose_start_time = time.perf_counter()
    moose_runner.run(MOOSE_PATH)
    moose_run_time = time.perf_counter() - moose_start_time

    print()
    print("="*80)
    print(f"Gmsh run time = {gmsh_run_time:.2f} seconds")
    print(f"MOOSE run time = {moose_run_time:.3f} seconds")
    print("="*80)
    print()

if __name__ == "__main__":
    main()

