from pycliff import Console


class Name:

    def __init__(self):
        self.value = ''


con = Console()
con.useGreeting('./greeting.txt')
con.attach('name', Name())


@con.register('q')
@con.register('quit')
def stop(*a, **kw):
    name = con.getObject('name')
    if name.value:
        con.display(f'Goodbye, {name.value}!')
    else:
        con.display('Goodbye!')
    con.stop()


@con.register('help')
@con.register('?')
def listCommands(*a, **kw):
    con.display(
        'Available commands:',
        '   ask     -- The console asks for your name',
        '   greet   -- The console greets you',
        '   ?, help -- Display the help message',
        '   q, quit -- Exit the console',
    )


@con.register('ask')
def askName(*a, **kw):
    name = con.getObject('name')
    name.value = input('What is your name?\n')


@con.register('greet')
def sayHello(*a, **kw):
    name = con.getObject('name')
    if name.value:
        con.display(f'Hello, {name.value}!')
        return
    con.display("Hello there!")


if __name__ == "__main__":
    con.run()
