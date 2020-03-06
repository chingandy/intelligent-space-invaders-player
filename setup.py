import cx_Freeze

executables = [cx_Freeze.Executable("alien_invasion.py")]


cx_Freeze.setup(
    name="Kai and Andy",
    options={"build_exe":{"packages":["pygame"]}},
    executables = executables
)



# cx_Freeze.setup(
#     name="Kai and Andy",
#     options={"build_exe":{"packages":["pygame"],
#               "include_files":["images/kai.png", "andy.png", "background.jpg"]}},
#     executables = executables
# )
