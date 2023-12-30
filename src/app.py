
import os
from pathlib import Path
from cli.main import CLI
from tools.configs_editor import read_config, write_config
from project_manager.cim_project import CimProject


def main():

    # App directories setting
    if read_config("USER", "WORK_DIR") is None:
        documents_path = Path.home() / "Documents"
        work_dir = documents_path.joinpath(
            read_config("DEFAULT", "work_folder"))
        projects_dir = work_dir.joinpath(
            read_config("DEFAULT", "projects_folder"))
        work_dir = str(work_dir)
        projects_dir = str(projects_dir)
        write_config("USER", "work_dir", work_dir)
        write_config("USER", "projects_dir", projects_dir)
        os.mkdir(read_config("USER", "work_dir"))
        os.mkdir(read_config("USER", "projects_dir"))

    cli = CLI()
    cli.cmdloop()


if __name__ == "__main__":
    main()
