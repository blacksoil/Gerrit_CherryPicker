import os
import array

# Required env variables
# Top is used as the base cherry picking directory
_env_vars = ['TOP', 'OUT']

# File where the cherry-picks is determined
# _input_file = "/Users/antoniusharijanto/Desktop/Scripts/mine/input.txt"
_input_file = "/home/aharijanto/Desktop/Scripts/mine/input.txt"

# Last chdir-ed path
_last_chdir_path = ""

# Cherry-pick commands to be executed
_cherry_pick_cmds = []

_DEBUG = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


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
	path_ = os.environ['TOP'] + '/' + path.strip()
	try:
		os.chdir(path_)
		_last_chdir_path = path
	except OSError:
		exit_error("Path doesn't exist: " + path)

# Execute the command in _cherry_pick_cmds
def execute_commands():
	# [0] -> description
	# [1] -> folder
	# [2] -> cherry-pick command
	for command in _cherry_pick_cmds:
		print command[0]
		print command[1]
		chdir(command[1])
		
		do = True
		while(do):
			do = False
			err_code = os.system(command[2])
			if(err_code == 0):
				print bcolors.OKGREEN + "Success!" + bcolors.ENDC
			else if(err_code == 256):
				print bcolors.WARNING +"Patch is already applied" + bcolors.ENDC
			else:

				print bcolors.FAIL + "Failed! Err code: " + err_code + bcolors.ENDC
				i = raw_input("['Enter' to skip / 'r' to retry]")
				if (i == 'r'):
					do = True


def parse_input_file(input_file):
	last_comment = ""
	# This is the comment that is right before folder specification
	last_path_description = ""

	def isSkipped(line): return (line.strip() == "" or line.strip()[0] == '#')
	def isChangeFolder(line): return (line[0] != '\t')
	def isCherryPick(line): return (line[0] == '\t')
	def cherrypick(command, description):
		global _last_chdir_path
		# Remove out # and \n
		description = description.strip()[1:].strip()
		_cherry_pick_cmds.append([description, _last_chdir_path, command.strip()])

	f = open(input_file, 'r')
	lineNumber = 0
	for line in f:
		lineNumber+=1
		# log("\t" + str(lineNumber) + line)
		# Ignore comments
		if (isSkipped(line)): 
			log("isSkipped: " + line)
			last_comment = line
		elif (isChangeFolder(line)): 
			log("isChangeFolder: " + line)
			chdir(line)
			last_path_description = last_comment
		elif (isCherryPick(line)): 
			log("isCherryPick: " + line)
			cherrypick(line, last_path_description)
		else: log("other: " + line)



check_env_variables()
parse_input_file(_input_file)
#print _cherry_pick_cmds
execute_commands()