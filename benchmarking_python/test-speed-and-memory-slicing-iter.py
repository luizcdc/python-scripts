"""Tests memory usage and performance of two methods \
for acessing adjacent items of a list inside a loop.
"""
from os import getpid
from psutil import Process
from time import sleep, time

def mem_in_mb(process):
     return int(process.memory_info().rss / 1048576)
    
def averager():
    """Returns a function that returns the average of the values \
    that have been passed to it as arguments in all previous calls.
    """
    avg = 0
    called = 0
    def avg_counter(num=None):
         nonlocal avg,called
         if num:
              avg = avg * called + num
              called += 1
              avg /= called
         return avg
    return avg_counter

process = Process(getpid())
print(f"Memory before making list: {mem_in_mb(process)} MiB\n\n")
repetitions = 1
size = 50000000 # 50000000 uses about 2GB of system memory
list_ = list(range(size))


avg_time_slicing = averager()
avg_mem_slicing = averager()
print(f"Memory before entering the 'slicing' loop: {mem_in_mb(process)} MiB")
for _ in range(repetitions):
     tb = time()
     for x,y in zip(list_, list_[1:]):
          if not x:
               avg_mem_slicing(mem_in_mb(process))
     ta = time()
     avg_time_slicing(ta-tb)
print(f"Memory inside the 'slicing' loop: {int(avg_mem_slicing())} MiB")
print(f"Average time for the 'slicing' loop: {avg_time_slicing()} seconds.")
print(f"Memory after the 'slicing' loop: {mem_in_mb(process)} MiB\n")


avg_time_iter = averager()
avg_mem_iter = averager()
print(f"Memory before entering the 'iterators' loop: {mem_in_mb(process)} MiB")
for _ in range(repetitions):
     tb = time()
     i1,i2 = iter(list_),iter(list_)
     next(i2)
     for x,y in zip(i1,i2):
          if not x:
               avg_mem_iter(mem_in_mb(process))
     ta = time()
     avg_time_iter(ta-tb)
print(f"Memory inside the 'iterators' loop: {int(avg_mem_iter())} MiB")
print(f"Average time for the 'iterators' loop: {avg_time_iter()} seconds.")
print(f"Memory after the 'iterators' loop: {mem_in_mb(process)} MiB\n\n")

print(f"Slicing was {int(avg_time_slicing()/avg_time_iter()*100) - 100}% slower.\n")


        

     
