"""Application code defining the view of the application and its behaviors."""
import os
import sys
import tkinter as tk
from tkinter import filedialog, ttk
from typing import NoReturn

LOG_DIR = "C:\\Games\\War of the Ring\\logs"
VIEW_FREE_CMD = "<~Controls.464~>"
VIEW_SHADOW_CMD = "<~Controls.479~>"


class App(tk.Tk):
    """Tk application representing how the app looks and can be interacted with."""

    def __init__(self) -> None:
        super().__init__()

        # Basic app configuration
        self.title("War of the Ring Logfile Updater")
        self.geometry("350x120")

        # App state. Which logfile is currently selected, and how should it be displayed
        # in the GUI.
        self.selected_logfile_path = ""
        self.selected_logfile_display = tk.StringVar(self, value="")

        # Labels and input fields for password entry. These will be written into the
        # logfile.
        ttk.Label(self, text="FP PASSWORD: ", foreground="#00f").grid(row=0, column=0)
        self.fp_pw = tk.Entry(self)
        self.fp_pw.grid(row=0, column=1)

        ttk.Label(self, text="SP PASSWORD: ", foreground="#f00").grid(row=1, column=0)
        self.sp_pw = tk.Entry(self)
        self.sp_pw.grid(row=1, column=1)

        # Button to select which logfile should be annotated
        ttk.Button(self, text="Select Logfile", command=self.select_logfile).grid(
            row=2, column=0
        )
        ttk.Label(self, textvariable=self.selected_logfile_display).grid(
            row=2, column=1
        )

        # Final confirm button. Mutates the logfile with all the entered information.
        self.grid_rowconfigure(3, weight=1)
        ttk.Button(self, text="Confirm", command=self.modify_logfile).grid(row=3)

    def select_logfile(self) -> None:
        """Update the application state with a selected logfile. This selected log will
        have its name displayed to the user, and will be modified upon confirmation.
        """
        self.selected_logfile_path = filedialog.askopenfilename(initialdir=LOG_DIR)
        self.selected_logfile_display.set(os.path.basename(self.selected_logfile_path))

    def modify_logfile(self) -> NoReturn:
        """Write passwords to the logfile, and then exit the application.

        In the WotR Java client, if passwords are input prior to the point where BOTH
        players actually viewed their hands, file corruption can occur. To help prevent
        this, passwords are only annotated in the logfile after that happens. So by the
        time the watcher of a replay knows the password, it is safe to enter it.

        The point in the logfile where hands were viewed can be determined by looking
        for a specific command.
        """
        filepath = self.selected_logfile_path

        # Slurp the logfile
        with open(filepath, "r", encoding="utf8") as logfile:
            lines = logfile.readlines()

        first_hand_viewed = False

        # Insert the passwords
        for line_number, line in enumerate(lines):
            if VIEW_FREE_CMD in line or VIEW_SHADOW_CMD in line:
                if not first_hand_viewed:
                    first_hand_viewed = True
                else:
                    lines.insert(
                        line_number + 1, f"<Game> SP Password: {self.sp_pw.get()} \n"
                    )
                    lines.insert(
                        line_number + 1, f"<Game> FP Password: {self.fp_pw.get()} \n"
                    )
                    break

        # Write back the modified data
        with open(filepath, "w", encoding="utf8") as logfile:
            modified_content = "".join(lines)
            logfile.write(modified_content)

        sys.exit(0)
