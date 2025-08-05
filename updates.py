import subprocess
import os
import sys
import datetime
import time

CHECK_HOUR = 14
CHECK_MINUTE = 30
BRANCH = "main"
REPO = "origin"

## Commit Message Check

def get_local_commit():
	return subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()

def get_remote_commit():
	return subprocess.check_output(['git','ls-remote',REPO,f'refs/heads/{BRANCH}']).decode().split()[0]

def update_needed():
	try:
		local = get_local_commit()
		remote = get_remote_commit()
		return local != remote
	except Exception as e:
		print (f"[UPDATE] Error checking for updates: {e}")
		return False

def self_update_and_restart():
	print("[UPDATE] Update detected! Pulling changes and restarting...")
	subprocess.run(['git','pull'],check=True)

	python = sys.executable
	os.execv(python,[python]+sys.argv)

while True:
	if update_needed():
		self_update_and_restart()
	else:
		print("Update] No updates found.")

	time.sleep(10)
