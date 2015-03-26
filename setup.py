from cx_Freeze import setup, Executable

includefiles = ['levels.py', 'npcs.py', 'params.py',
	'platforms.py', 'tiles.py']
includes = []
excludes = []
packages = []

exe = Executable(
	script = "main.py",
	initScript = None,
	base = "Win32GUI",
	#target_name = "start.exe",
	copyDependentFiles = True,
	compress = True,
	appendScriptToExe = True,
	appendScriptToLibrary = True,
	icon = None
)

setup(
	name = "Pong Quest",
	version = "0.1",
	description = "Mini LD game",
	author = "zeglor",
	author_email = "zeglor@gmail.com",
	options = {"build_exe": {
		"excludes": excludes,
		"packages": packages,
		"include_files": includefiles
		}},
	executables=[exe]
)