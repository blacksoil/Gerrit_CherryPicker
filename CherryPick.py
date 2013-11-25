import os
import array

# Required env variables
# Top is used as the base cherry picking directory
_env_vars = ['TOP', 'OUT']

# File where the cherry-picks is determined
_input_file = "/Users/antoniusharijanto/Desktop/Scripts/mine/input.txt"

# Last chdir-ed path
_last_chdir_path = ""

# This is the comment that is right before folder specification
_last_path_description

# Cherry-pick commands to be executed
_cherry_pick_cmds = []

_DEBUG = False

# Called exit from the script
def exit_error(reason):
	print "Script aborted : " + reason
	exit()

def log(str):
	if _DEBUG:
		print str

def check_env_variables():
	def validate_vars(env_var):
		try:
			os.environ[env_var]
		except KeyError:
			exit_error("Environment variable not set up: " + 
				env_var)
		

	map(validate_vars, _env_vars)

def chdir(path):
	global _last_chdir_path
	path = os.environ['TOP'] + '/' + path.strip()
	try:
		os.chdir(path)
		_last_chdir_path = path
	except OSError:
		exit_error("Path doesn't exist: " + path)

def cherrypick(command):
	global _last_chdir_path
	_cherry_pick_cmds.append([_last_chdir_path, command.strip()])
	# print _last_chdir_path

def parse_input_file(input_file):
	def isSkipped(line): return (line.strip() == "" or line.strip()[0] == '#')
	def isChangeFolder(line): return (line[0] != '\t')
	def isCherryPick(line): return (line[0] == '\t')
	
	f = open(input_file, 'r')
	lineNumber = 0
	for line in f:
		lineNumber+=1
		#log("\t" + str(lineNumber) + line)
		# Ignore comments
		if (isSkipped(line)): log("isSkipped: " + line);
		elif (isChangeFolder(line)): log("isChangeFolder: " + line); chdir(line)
		elif (isCherryPick(line)): log("isCherryPick: " + line); cherrypick(line)
		else: log("other: " + line)



check_env_variables()
parse_input_file(_input_file)
print _cherry_pick_cmds