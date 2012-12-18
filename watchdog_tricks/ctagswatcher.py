#!/usr/bin/env python
from argh import arg, dispatch_command
from watchdog.watchmedo import observe_with
from watchdog_tricks.compiler import CtagsTrick
from watchdog_tricks import utils

def main():
    @arg('filetypes', metavar='FILETYPE', nargs='+',  help='Included file types for generating targs')
    @arg('--rebuild', default=False, help='Force rebuild all tags at start')
    @arg('--ctags', default='ctags', help='Path to ctags program.(default: ctags)')
    def _watcher(args):
        from watchdog.observers import Observer 
        handler = CtagsTrick(filetypes=args.filetypes, ctags=args.ctags, rebuild=args.rebuild)
        observer = Observer(timeout=1.0)
        observe_with(observer, handler, ['.'], True) 
    dispatch_command(_watcher)

if __name__ == '__main__':
    main()
