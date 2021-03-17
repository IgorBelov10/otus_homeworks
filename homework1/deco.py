#!/usr/bin/env python
# -*- coding: utf-8 -*-




def decorator(func):
    """
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    """
    def wrapper_decorator(*args, **kwargs):
        return_value = func(*args, **kwargs)
        return_value.__doc__ = args[0].__doc__
        return return_value

    return wrapper_decorator

@decorator
def disable(func):
    def wrapper_disable(*args, **kwargs):
        # print(func)
        return_value = func(*[args], **kwargs)
        return wrapper_disabled
    def wrapper_disabled(*args, **kwargs):
        return_value = func(*args, **kwargs)
        return return_value
    return wrapper_disable


@decorator

def countcalls(func):
    """Decorator that counts calls made to the function decorated."""


    def wrapper_countcalls(*args, **kwargs):
        """decccooo"""
        return_value = func(*args, **kwargs)
        wrapper_countcalls.calls += 1
        return return_value

    try:
        wrapper_countcalls.calls is None
    except AttributeError:
        wrapper_countcalls.calls = 0
    return wrapper_countcalls

@decorator
def memo(func):
    """
    Memoize a function so that it caches all return values for
    faster future lookups.
    """


    def wrapper_memo(*args, **kwargs):
        key_string = \
                    "_|_".join(map(str, args))+"_|||_"+"_||_".join(list(str(str(i[0]) +
                    "_|_"+str(i[1])) for i in sorted(kwargs.items())))
        if key_string in wrapper_memo.memo_cache:
            print("using_cache...")
            return wrapper_memo.memo_cache[key_string]
        else:

            return_value = func(*args, **kwargs)
            wrapper_memo.memo_cache[key_string] = return_value

        return return_value

    try:
        wrapper_memo.memo_cache is None
    except AttributeError:
        wrapper_memo.memo_cache = {}
    return wrapper_memo

@decorator
def n_ary(func):
    """
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    """


    def wrapper_n_ary(*args, **kwargs):
        if len(kwargs) > 0 or len(args) == 0:
            print("Некорректные входные параметры.")
            return None
        if len(args) == 1:
            return args[0]
        else:
            return_value = func(list(reversed(args))[1], list(reversed(args))[0])
            for i in range(2, len(args)):
                return_value = func(list(reversed(args))[i], return_value)

        return return_value

    return wrapper_n_ary


def trace(tabulation):
    """Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    #>>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    """

    @decorator
    @disable
    def actual_decorator(func):

        def wrapper_trace(*args, **kwargs):
            print(tabulation * wrapper_trace.trace_heap, "-->"+func.__name__+"("+", ".join(map(str, args))+")")
            wrapper_trace.trace_heap += 1
            return_value = func(*args, **kwargs)
            wrapper_trace.trace_heap -= 1
            print(tabulation * wrapper_trace.trace_heap, "<--" + func.__name__ + "(" + ", ".join(map(str, args)) +
                  ") == "+str(return_value))
            return return_value

        try:
            wrapper_trace.trace_heap is None
        except AttributeError:
            wrapper_trace.trace_heap = 0
        return wrapper_trace



    return actual_decorator


@countcalls
@memo
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@memo
@trace("####")
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    print(fib.__doc__)   # Непонятно, каким образом сделать передачу информации из основной функции в декоратор, т.к. в
    # функции декоратора нет переменной, из которой можно было бы вытянуть метаинформацию/ метаинформация присутсвует
    # только в функциях, которые отвечают непосредственно за обработку в декотраторе, который находится последним
    # в объявлении декораторов
    fib(3)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
