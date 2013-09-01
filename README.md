# SwagScript v1

SwagScript, or PySwagScript, is an amazing scripting language. It's easy to use, and it appeals to youngsters!
It's implemented in Python. It was developed under Python 3.3, but probably it's compatible with >=2.6.

## Components

There are two main components in SwagScript Suite:

### SwagScript Compiler Core

The file `sws.py` contains the class `SwsComp`, it's **THE** compiler. I know, it's not a compiler technically, but it basically compiles into Python and that Python is later interpretated.

It's a very simple class; it has some helper methods (`open_temp`, `open_sws`, etc.) and two interesting methods:

* `parse_file` - The method that the frontend (see below) should use. It applies `parse_line` to each line of the specified file.
* `parse_line` - Basically, it has a dictionary with all the regex to translate SWS to Python. Then, there are a series of if/elif's that return a line depending on which of those regex is true.

### SwagScript Compiler

The file `ssc.py` and the built-in frontend. Basically, you should create your own or feel free to modify this one.
Basically it checks if the user wants verbosity, creates a `SwsComp` and runs the `parse_file` method passing the sws file given in the arguments.

## Usage

Create a `.sws` file. Here you have a "hello world":

    yo Hello World
    hai

(It looks esoterical but it isn't, it's all what it has today!)

Then, run your desired front-end. I'm using `ssc.py`, of course:

    $ python ssc.py helloworld.sws

You should see `Hai homie yo!`. If you don't, try using the `--verbose` option:

    $ python ssc.py helloworld.sws --verbose

You'll see each step of the compilation/interpretation, and if there are any errors you'll see them as well.

## How does it work?

Easy-peasy:

1. Open the specified SwagScript file.
2. Create a temporary file (`swstemp.py`).
3. Read first line of the SwagScript file, parse it, write it to `swstemp.py`.
4. Same as above until all the lines are parsed.
5. `import swstemp`, so run the compiled SwagScript-to-Python code.
6. Close and tide everything ;)

## Mixing Python and SwagScript

Since if a line read from a SwagScript file doesn't match any of the regular expressions it will be returned "as it is," and later interpreted by
Python, you can write all the Python things you want inside a SwagScript file. It shouldn't conflict.

You can import any Python module by using the `gimme` statement:

    `gimme module bro`

It works with "Python's batteries" but of course with any `.py` files.

You can also import a SwagScript file into Python! All what you need is to import `sws.py` and implement a frontend inside of your script.

### Example

`hi.sws`:

    yo
    hai

`hi.py`:

```python
from sws import SwsComp
swag = SwsComp()
print("This comes from Python.")
swag.parse_file("hi.sws")
```

See? It's not that difficult!

**IMPORTANT**: If you want to do something like above, you'll have to ship `sws.py` with your software, unless you know for sure
that the target will have it somewhere. But it's better to ship it "next to" your file because of the following reasons:

* You're free to modify `sws.py`, so perhaps the target and you don't have the same one!
* It's not so simple to import a module given a full path; but even if you do so, how do you know where does your target have `sws.py`?

Because of that, feel free to ship `sws.py` with your products if you want to! Just credit me if possible.