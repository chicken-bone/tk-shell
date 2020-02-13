import os
import sys
import sgtk.context
from sgtk.platform import SoftwareLauncher, SoftwareVersion, LaunchInformation


class ShellLauncher(SoftwareLauncher):

    def scan_software(self):

        ICON_LOCATION = os.path.join(self.disk_location, "icon_256.png")
        TERMINAL_SOFTWARE = {
            "darwin": [
                SoftwareVersion(
                    " ",
                    "Console",
                    "/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal",
                    icon=ICON_LOCATION,
                    args=None
                ),
                # SoftwareVersion(
                #     "2",
                #     "iTerm",
                #     "/Applications/iTerm.app/Contents/MacOS/iTerm2",
                #     icon=ICON_LOCATION,
                #     args=None
                # )
            ],
            "win32": [
                SoftwareVersion(
                    " ",
                    "Console",
                    r"C:\WINDOWS\system32\cmd.exe",
                    icon=ICON_LOCATION,
                    args=None
                )
            ],
            "linux2": [
                SoftwareVersion(
                    " ",
                    "Console",
                    r"/usr/bin/gnome-terminal",
                    icon=ICON_LOCATION,
                    args=None
                )
            ]
        }

        return TERMINAL_SOFTWARE[sys.platform]

    def prepare_launch(self, exec_path, args, file_to_open=None):
        # Construct an environment to launch the DCC in,
        # confirm the correct executable path to
        # launch, and provide required command line args.
        # Return this information as a
        # LaunchInformation instance.
        correct_executable_path = ""
        command_line_args = "/k python -i {}".format(os.path.join(self.disk_location, "startup", "bootstrap.py"))
        # command_line_args = ""
        launch_environment = {}

        # once the software has launched, execute
        # startup script startup/userSetup.py
        # launch_environment["PYTHONPATH"] = os.path.join(self.disk_location, "startup")
        launch_environment["PATH"] = os.environ["PATH"] + os.pathsep + os.path.dirname(sys.executable)
        launch_environment["SGTK_ENGINE"] = self.engine_name
        launch_environment["SGTK_CONTEXT"] = sgtk.context.serialize(self.context)
        launch_environment["SGTK_TERMINAL"] = exec_path
        launch_environment["SGTK_MODULE_PATH"] = sgtk.get_sgtk_module_path()

        # make sure to include some standard fields describing the current context and site
        std_env = self.get_standard_plugin_environment()
        launch_environment.update(std_env)

        launch_information = LaunchInformation(
            correct_executable_path,
            command_line_args,
            launch_environment
        )
        return launch_information
