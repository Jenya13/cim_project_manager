import cmd
from typing import IO
from project_manager.manager import ProjectManager
from tools.welcom_text import welcome_text


class CLI(cmd.Cmd):
    prompt = "$ -> "
    intro = "Cim Data Manager"  # welcome_text + "\n"

    def __init__(self, completekey: str = "tab", stdin: IO[str] = None, stdout: IO[str] = None):
        super().__init__(completekey, stdin, stdout)
        self._project_manager = ProjectManager()

    def do_objects(self, line):
        cmd, args, original_line = self.parseline(line)

        if cmd:
            if cmd == "create" or cmd == "update":
                if args and args == "-a":
                    self._project_manager.create_objects()
                else:
                    self._project_manager.create_objects(args)
            else:
                print(f"No command: [objects {original_line}]")
        else:
            print(f"No command: [objects {original_line}]")

    def do_project(self, line):
        """Run project command."""
        cmd, args, original_line = self.parseline(line)
        if cmd:
            if cmd == "create":
                if args:
                    self._project_manager.init_project(args)
                    return
                print("No project id was provided")

            elif cmd == "set":
                if args:
                    self._project_manager.set_project(args)
                    return
                print("No project id was provided")

            elif cmd == "id":
                project_id = self._project_manager.get_current_project_name()
                if project_id:
                    print(f"Project id: {project_id}")
                    return
                print("No project was set")

            elif cmd == "ls":
                projects = self._project_manager.get_projects_names()
                ls = ", ".join(proj for proj in projects)
                print(f"Projects: {ls}")

            elif cmd == "del":
                # create a prompt that asking if the user shure that he want to delete projects
                if args:
                    if args == "-a":
                        self._project_manager.delet_project()
                    else:
                        self._project_manager.delet_project(args)
                    return
                print(f"No command: [project {original_line}], pass parameter")

            else:
                print(f"No command: [project {original_line}]")
        else:
            print(f"No command: [project {original_line}]")

    def do_template(self, line):
        """Run project command."""
        cmd, args, original_line = self.parseline(line)

        if cmd == "update":
            self._project_manager.update_template()
        else:
            print(f"No command [template {original_line}]")

    def default(self, line: str):
        print(
            f"Unknown command: [{line}]. Type 'help' for available commands.")

    def do_EOF(self, line):
        """Exit the CLI."""
        return True

    # aliases
    do_exit = do_EOF


if __name__ == "__main__":
    cli = CLI()
    cli.cmdloop()
