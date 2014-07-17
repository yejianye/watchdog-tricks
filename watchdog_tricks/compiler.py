#!/usr/bin/env python
import os
import sys
from string import Template
from watchdog.tricks import Trick
from watchdog_tricks import utils

class AutoCompileTrick(Trick):
    def __init__(self, src_dir, dest_dir, **kwargs):
        self.src_dir = os.path.abspath(src_dir)
        self.dest_dir = os.path.abspath(dest_dir)
        self.compiler = kwargs.pop('compiler')
        self.src_ext = kwargs.pop('src_ext')
        self.dest_ext = kwargs.pop('dest_ext')
        self.compile_command = kwargs.pop('compile_command')
        self.compile_opts = kwargs.pop('compile_opts', '')
        kwargs.setdefault('patterns', [os.path.join('*', self.src_dir, '*.' + self.src_ext)])
        super(AutoCompileTrick, self).__init__(**kwargs)

    @utils.trace_event
    def on_modified(self, event):
        self.compile(event.src_path)

    @utils.trace_event
    def on_deleted(self, event):
        self.remove(event.src_path)

    @utils.trace_event
    def on_created(self, event):
        self.compile(event.src_path)

    @utils.trace_event
    def on_moved(self, event):
        self.remove(event.src_path)
        if event.dest_path.endswith(self.src_ext) and event.dest_path.startswith(self.src_dir):
            self.compile(event.dest_path)

    def get_dest_fname(self, src_fname):
        return src_fname.replace(self.src_dir, self.dest_dir).rsplit('.', 1)[0] + '.' + self.dest_ext

    def compile(self, filename):
        utils.exec_cmd(self.assemble_compile_cmdline(filename, self.get_dest_fname(filename)))
    
    def assemble_compile_cmdline(self, src, dst):
        return Template(self.compile_command).substitute({
            'src' : src,
            'dst' : dst,
            'compiler' : self.compiler,
            'opts' : self.compile_opts
        })

    def remove(self, filename):
        utils.exec_cmd('rm ' + self.get_dest_fname(filename))

class LessTrick(AutoCompileTrick):
    def __init__(self, src_dir, dest_dir, **kwargs):
        kwargs.setdefault('compiler', 'lessc')
        super(LessTrick, self).__init__(src_dir, dest_dir,
            src_ext = 'less',
            dest_ext = 'css',
            compile_command = '$compiler $src > $dst',
            **kwargs
        )

class CoffeeScriptTrick(AutoCompileTrick):
    def __init__(self, src_dir, dest_dir, **kwargs):
        kwargs.setdefault('compiler', 'coffee')
        super(CoffeeScriptTrick, self).__init__(src_dir, dest_dir,
            src_ext = 'coffee',
            dest_ext = 'js',
            compile_command = '$compiler -cp $opts $src > $dst',
            **kwargs
        )

class CtagsTrick(Trick):
    def __init__(self, filetypes, ctags='ctags', rebuild=False, **kwargs):
        kwargs.setdefault('patterns', ['*.%s' % ext for ext in filetypes])
        super(CtagsTrick, self).__init__(**kwargs)
        self.ctags = ctags
        self.filetypes = filetypes
        if rebuild:
            self.rebuild_all()

    @utils.trace_event
    def on_any_event(self, event):
        src_dir = os.path.dirname(event.src_path)
        self.rebuild_tags(src_dir)
        if hasattr(event, 'dest_path'):
            dest_dir = os.path.dirname(event.src_path)
            if dest_dir != src_dir:
                self.rebuild_tags(dest_dir)

    def rebuild_tags(self, fdir):
        utils.build_tags(fdir, self.filetypes, ctags=self.ctags, recursive=False)

    def rebuild_all(self):
        utils.build_tags('.', self.filetypes, ctags=self.ctags, recursive=True)
