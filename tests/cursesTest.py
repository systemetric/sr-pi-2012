import curses
from systemetric import Robot
def main():
	stdscr = curses.initscr()
	curses.echo()

	while 1:
	    c = stdscr.getch()
	    if c == ord('q'): break; curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
