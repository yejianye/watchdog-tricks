watchdog-tricks
===============

This package includes several useful `Trick` for `watchdog` (Python API for monitoring file system events, https://github.com/gorakhargosh/watchdog).

Tricks could be running in standalone mode or combined via a configuration file. They will perform specific tasks upon file change event.

- LessTrick: Auto recompiling LessCSS to CSS 
- CoffeeScriptTrick: Auto recompiling CoffeeScript to Javascript 
- AutoCompileTrick: A generic trick to auto recompiling source code 


Standalone watcher - lesswatcher
--------------------------------
`lesswatcher` is a standalone script that auto recompiling lessCSS files. An example usage is

    $ lesswatcher --lessc-path /path/to/lessc static/less static/css

if `lessc` is already in your search path, you could just skip `--lessc-path` arg. 

Configuration File - trick.yaml
-------------------------------
The true power of watchdog tricks is shown via configuration files, which could combine different tricks together and give you a fully automated development and building system. Here is an example of trick configuration file

    tricks:
    - watchdog.tricks.ShellCommandTrick:
        patterns: ["*.py","*.html"]
        shell_command: "cat gunicorn.pid | xargs kill -HUP"
        wait_for_process: true
    - watchdog_tricks.compiler.LessTrick:
        src_dir: 'static/less'
        dest_dir: 'static/css'
    - watchdog_tricks.compiler.CoffeeScriptTrick:
        src_dir: 'static/cs'
        dest_dir: 'static/js'
        compile_opts: '-b'

Put the configuration file to the root directory that needs to be monitored. Assume the filename is `tricks.yaml`. To run watchdog with this configuration file
  
    $ watchmedo tricks tricks.yaml

API Documentation
-----------------
watchdog_tricks.compiler.LessTrick:
- src_dir: Directory of LessCSS source files
- dest_dir: Directory of output CSS files
- compile_opts: Command-line options for LessCSS compiler
- compiler: LessCSS compiler path. Default is 'lessc'

watchdog_tricks.compiler.CoffeeScriptTrick:
- src_dir: Directory of CoffeeScript source files
- dest_dir: Directory of output JavaScript files
- compile_opts: Command-line options for CoffeeScript compiler 
- compiler: CoffeeScript compiler path. Default is 'coffee'

`AutoCompileTrick` provides a generic way to auto recompile your source files once it's been modified. Both `LessTricks` and `CoffeeScriptTrick` are extended from `AutoCompileTrick`.
watchdog_tricks.compiler.AutoCompileTrick:
- src_dir: Directory of source files
- dest_dir: Directory of compiled files
- src_ext: Extension of source files
- dest_ext: Extension of compiled files
- compile_opts: Command-line options for the compiler
- compiler: Path to the compiler
- compile_command: Template to build the compile command. See details below.

`compile_command` takes several predefined variables which you might need to form a compile command. Those variables include:
- src: Path to the source file
- dst: Path to the compiled file
- compiler: Path toe the compiler
- opts: Command-line options for the compiler

An example configuration file to auto recompile markdown files to html for example.com
    
    tricks:
    - watchdog_tricks.compiler.AutoCompileTrick:
        src_dir: 'docs'
        dest_dir: 'build/docs'
        src_ext: 'md'
        dest_ext: 'html'
        compiler: 'markdown'
        opts: '-b http://example.com'
        compile_command: '$compiler $opts < $src > $dst'

watchdog_tricks.compiler.CtagsTrick:
- filetypes: file types to be monitored 
- rebuild: whether rebuilding all tags on startup

An example configuration file to auto re-generate tag files for python and coffeescript source files

    tricks:
    - watchdog_tricks.compiler.CtagsTrick:
        filetypes: ['py', 'coffee']
        rebuild: true

Installation
------------

Install directly from github.com

    $ pip install git+git://github.com/yejianye/watchdog-tricks.git

Or clone this repository and run

	$ python setup.py install

