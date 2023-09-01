# PyCliff
Lightweight Python CLI Framework

## Usage

Create a Python CLI in 3 easy steps!

```python
from pycliff import Console

## 1. Create a console.
con = Console(greeting="Hello, there!\n===============\n")

## 2. Register one or more commands
@con.register('myCommand')
def command(*args, **kwargs):
    con.display("You've just executed a command")

## 3. Start the console
con.run()
```

Result:
```
Hello, there!
===============

> myCommand
You've just executed a command

> ^C
Exiting...
```
