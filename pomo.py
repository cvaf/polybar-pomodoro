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
    self.perma_run_time = run_time * 60
    self.break_time = break_time * 60
    # Flexible attributes
    self.run_time = run_time * 60
    self.run_count = 0
    self.elapsed_time = 0


  def start_run(self):
    self.start_time = time.time()
    self.run_time = self.perma_run_time
    self.status = self.task
    self.run_count+=1
    self.elapsed_time = 0

  def resume_run(self):
    self.start_time = time.time()
    self.run_time = self.run_time - self.elapsed_time
    self.status = self.task
    self.elapsed_time = 0

  def pause_run(self):
    self.elapsed_time = time.time() - self.start_time
    self.status = 'Pause'

  def start_break(self):
    self.start_time = time.time()
    self.status = 'Break'

  def terminate(self):
    self.status = 'Fin'
    self.start_time = 0
    self.remaining_time = 0




def print_status(status, time_remaining):

  if time_remaining >= 60:
    mins_remaining = math.ceil(time_remaining / 60)
    print(f' {status}: {mins_remaining}m ')

  elif time_remaining == 0:
    print(f' {status} ')

  else:
    secs_remaining = math.floor(time_remaining)
    print(f' {status}: {secs_remaining}s ')



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
    - if paused: resume run
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

  elif p.status == 'Pause':
    p.resume_run()

  else:
    p.start_time = p.start_time - 60

  # dump the update
  with open(TEMP_FILE, 'wb') as f:
    pickle.dump(p, f)


def pomo_middle():
  """
  Middle click action:
    - if working on task: toggle pause
    - if on break: resume task
    - else: start task
  """

  with open(TEMP_FILE, 'rb') as f:
    p = pickle.load(f)

  if p.status == 'Pause':
    p.resume_run()

  elif p.status == p.task:
    p.pause_run()

  elif p.status == 'Break':

    if p.run_count + 1 == p.num_runs:
      p.terminate()

    else:
      p.start_run()

  else:
    p.start_run()

  with open(TEMP_FILE, 'wb') as f:
    pickle.dump(p, f)


def pomo_right():
  """
  Right click action: 
    - if Fin: create a new pomodoro process
    - if Pause: resume run
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

  elif p.status == 'Pause':
    p.resume_run()

  else:
    p.start_time = p.start_time + 60

  # dump the update
  with open(TEMP_FILE, 'wb') as f:
    pickle.dump(p, f)
