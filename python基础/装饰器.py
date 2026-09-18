


def log_class(cls):
    class Wrapper:
        def __init__(self, *args, **kwargs):
            self.wrapped = cls(*args, **kwargs)

        def __getattr__(self, name):
            return getattr(self.wrapped, name)

        def display(self):
            print("调用前")
            self.wrapped.display()
            print("调用后")

    return Wrapper

@log_class
class MyClass:
    def display(self):
        print("原方法")

obj = MyClass()
obj.display()