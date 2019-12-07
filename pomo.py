from config import TASK, RUN_TIME, BREAK_TIME, NUM_RUNS, TEMP_FILE
import time
import pickle
import os
import math


class Pomodoro:
	"""
	Object containing all pomodoro data and functions
	"""

	def __init__(self, task=TASK, run_time=RUN_TIME, 
				 break_time=BREAK_TIME, num_runs=NUM_RUNS):
		"""
		Arguments:
			- task: str, Description of task at hand
			- run_time: int, Number of minutes per run
			- break_time: int, Number of minutes per break
			- num_runs: int, Number of runs
		"""

		# Fixed attributes
		self.task = task
		self.num_runs = num_runs
		self.run_time = run_time * 60
		self.break_time = break_time * 60
		# Flexible attributes
		self.run_count = 0


	def start_run(self):
		self.start_time = time.time()
		self.status = self.task
		self.run_count+=1
		# self.label = TASK_LABEL

	def start_break(self):
		self.start_time = time.time()
		self.status = 'Break'
		# self.label = BREAK_LABEL

	def terminate(self):
		self.status = 'Fin'
		# self.label = FIN_LABEL
		self.start_time = 0



def print_status(status, time_remaining):

	if time_remaining >= 60:
		mins_remaining = math.ceil(time_remaining / 60)

		print(' {}: {}m '.format(status, mins_remaining))

	elif time_remaining == 0:
		print(' {} {} '.format(status, ''))

	else:
		print(' {}: {}s '.format(status, math.floor(time_remaining)))



def pomo_update():
	"""
	Fetch update from current pomodoro process
	"""


	if os.path.exists(TEMP_FILE):
		with open(TEMP_FILE, 'rb') as f:
			p = pickle.load(f)

	else:
		p = Pomodoro()
		p.terminate()

	time_elapsed = time.time() - p.start_time

	# if client is in break mode
	if p.status == 'Break':
		time_remaining = p.break_time - time_elapsed

		if time_remaining <= 0:

			if p.run_count + 1 == p.num_runs:
				p.terminate()

			else:
				p.start_run()


	# if the client is in task mode
	elif p.status == p.task: 
		time_remaining = p.run_time - time_elapsed

		if time_remaining <= 0:

			p.start_break()

		else:
			
			print_status(p.status, time_remaining)

	# if there's no process running
	else:
		time_remaining = 0


	print_status(p.status, time_remaining)



	# dump the update
	with open(TEMP_FILE, 'wb') as f:
		pickle.dump(p, f)


def pomo_left():
	"""
	Left click action
		- if status = Fin: create a new pomodoro process
		- else: add a minute to the current process
	"""

	try:
		with open(TEMP_FILE, 'rb') as f:
			p = pickle.load(f)

	except FileNotFoundError:
		p = Pomodoro(task=TASK, run_time=RUN_TIME,
					 break_time=BREAK_TIME, num_runs=NUM_RUNS)
		p.start_run()

		with open(TEMP_FILE, 'wb') as f:
			pickle.dump(p, f)


	if p.status == 'Fin':
		p = Pomodoro(task=TASK, run_time=RUN_TIME,
					 break_time=BREAK_TIME, num_runs=NUM_RUNS)
		p.start_run()

	else:
		p.start_time = p.start_time - 60

	# dump the update
	with open(TEMP_FILE, 'wb') as f:
		pickle.dump(p, f)


def pomo_middle():
	"""
	Middle click action: terminate current stage
	"""

	with open(TEMP_FILE, 'rb') as f:
		p = pickle.load(f)

	if p.status == p.task:
		p.start_break()

	elif p.status == 'Break':

		if p.run_count + 1 == p.num_runs:
			p.terminate()

		else:
			p.start_run()

	else:
		pass

	with open(TEMP_FILE, 'wb') as f:
		pickle.dump(p, f)


def pomo_right():
	"""
	Right click action: 
		- if status = Fin: create a new pomodoro process
		- else: remove a minute from the current process
	"""

	try:
		with open(TEMP_FILE, 'rb') as f:
			p = pickle.load(f)

	except FileNotFoundError:
		p = Pomodoro()
		p.start_run()

		with open(TEMP_FILE, 'wb') as f:
			pickle.dump(p, f)


	if p.status == 'Fin':
		p = Pomodoro()
		p.start_run()

	else:
		p.start_time = p.start_time + 60

	# dump the update
	with open(TEMP_FILE, 'wb') as f:
		pickle.dump(p, f)