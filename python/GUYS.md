# GUYS!!

## MAKE FUNCTIONS LIKE THIS!!!!
```python
def aaa(ls: list[int], x:float) -> list[float]:
    return [x * multiplier for x in int_list]

print(aaa([1, 2, 3, 4], 5.1))
```

## DECORATERS ARE KEY!!!
```python
# this is the decorator function
def add_exclamation(func):
  def wrapper(name):
    return func(name) + '!'
  return wrapper

# this is the function being decorated -- the decoratee (?)
def hello(name):
  return 'hello ' + name

# actually decorating the function
hello = add_exclamation(hello)

# now our function's behaviour has changed slightly
print(hello('tom'))    # hello tom!
```
```python
def add_exclamation(func):
  def wrapper(name):
    return func(name) + '!'
  return wrapper

@add_exclamation
def hello(name):
  return 'hello ' + name

print(hello('tom'))    # hello tom!
```

## gnerator function
```python
def test():
  yield 1
  yield 2
  yield 3

x = test()
print(x)    #
```
