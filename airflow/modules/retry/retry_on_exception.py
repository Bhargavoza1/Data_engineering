import functools
from modules import log


@log
class RetryOnException: # creating our custom class python decorator. like class wrapper on function.
    def __init__(self, retries):
        self._retries = retries

    def __call__(self, function):
        functools.update_wrapper(self, function)

        def wrapper(*args, **kwargs):
            self.log.info(f"Retries: {self._retries}")
            while self._retries != 0:
                try:
                    return function(*args, **kwargs)
                    self._retries = 0
                except Exception as err:
                    self.log.info(f"Error occured: {err}")
                    self._retries -= 1
                    self._raise_on_condition(self._retries, err)
        return wrapper

    def _raise_on_condition(self, retries, exception):
        if retries == 0:
            raise exception
        else:
            self.log.info(f"Retries: {retries}")

#<editor-fold desc=" testing  ">
'''
@RetryOnException(5)
def example():
    try:
        x:int = int(input("Enter number: "))
        x = 1 + x
        print(x)
    except Exception as err:
        print("Invalid input")
        raise err


example()
'''
#</editor-fold>