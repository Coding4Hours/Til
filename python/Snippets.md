---
layout: default
title: Python
---
# Snippets

## F-Strings!!
Don't use format or '+'
```python
# ANNOYING
name = 'tom'
age = 5

s = 'my name is ' + name + ' and my age is ' + str(age)

# using f-strings
name = 'tom'
age = 5

s = f'my name is {name} and my age is {age}'
```

Why?
```python
name = 'tom'
age = 5
height = 1.44

s = f'{name=} {age=} {height=}'
# name='tom' age=5 height=1.44

pi = 3.14159265
s = f'pi is {pi:.2f}'
# pi is 3.14
```


Have fun: [https://readcache.xyz/api/p?url=https://levelup.gitconnected.com/30-python-concepts-i-wish-i-knew-way-earlier-3add72af6433](https://readcache.xyz/api/p?url=https://levelup.gitconnected.com/30-python-concepts-i-wish-i-knew-way-earlier-3add72af6433)
