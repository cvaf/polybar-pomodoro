import click
from pomo import Pomodoro, pomo_left, pomo_right, pomo_middle, pomo_update

@click.command()
@click.option('--opt', default='update', help='Mouse click option')

def action(opt):
	if opt == 'left':
		pomo_left()
	elif opt == 'right':
		pomo_right() 
	elif opt == 'middle':
		pomo_middle()
	else:
		pomo_update()


if __name__ == '__main__':
	action()
