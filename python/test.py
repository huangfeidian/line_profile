# encoding = utf-8
import inspect
from line_stat import stat_func, add_line_stat
from line_profile import begin_frame, end_frame, add_line, dump_stat, add_line_arg
import time
def func_1(a):
	return ["11111" for i in xrange(a)]

def fib(a):
	if a== 0 or a == 1:
		return 1
	return fib(a - 1) + fib(a-2)

def func_2(a, b):
	temp_1 = fib(a)
	temp_2 = fib(b)
	return temp_1 + temp_2

@stat_func
def func_3(a, b):
	func_id = func_3.func_closure[0].cell_contents.__name__
	frame_id = id(inspect.currentframe().f_back.f_back)
	print "cur func name is %s id is %s frame_id is %s" % (func_3.__name__, func_id, frame_id)
	add_line_stat(func_id, frame_id, 0)
	temp_1 = func_1(a)
	add_line_stat(func_id, frame_id, 1)
	temp_2 = func_1(b)
	add_line_stat(func_id, frame_id, 2)
	return temp_1.extend(temp_2)

def func_4(a, b):
	# cur_frame = inspect.currentframe()
	# frame_id = id(cur_frame.f_back)
	# print "cur func name is %s frame_id_1  is %s" % (func_4.__name__, frame_id)
	add_line()
	temp_1 = fib(a)
	add_line()
	temp_2 = fib(b)
	add_line()
	return a + b


def empty_func_1():
	
	a = 0
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	a = a + 1
	
	return a

def add(a):
	return a + 1

def empty_func_2():
	a = 0
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	a = add(a)
	
	return a

def empty_func_3():
	add_line()
	a = 0
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	a = a + 1
	add_line()
	return a

def empty_func_4():
	add_line_arg(0)
	a = 0
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	a = a + 1
	add_line_arg(a)
	return a

def func_5(a, b):
	try:
		begin_frame()
		result = func_4(a, b)
		end_frame()
		return result
	except Exception as e:
		end_frame()
		raise e

def func_6(a, b, c):
	begin_ts = time.time()
	for i in xrange(c):
		func_2(a, b)

	end_ts = time.time()
	print "a %s b %s c %s func_2 cost %s" % (a, b, c, end_ts - begin_ts)

	begin_ts = time.time()
	for i in xrange(c):
		func_5(a, b)

	end_ts = time.time()
	print "a %s b %s c %s func_5 cost %s" % (a, b, c, end_ts - begin_ts)

	begin_ts = time.time()
	for i in xrange(c):
		begin_frame()
		func_4(a, b)
		end_frame()

	end_ts = time.time()
	print "a %s b %s c %s func_4 cost %s" % (a, b, c, end_ts - begin_ts)

def func_7(a):
	begin_ts = time.time()
	for i in xrange(a):
		empty_func_1()

	end_ts = time.time()
	print "a %s empty_func_1 cost %s" % (a, end_ts - begin_ts)

	begin_ts = time.time()
	for i in xrange(a):
		empty_func_2()

	end_ts = time.time()
	print "a %s empty_func_2 cost %s" % (a, end_ts - begin_ts)

	begin_ts = time.time()
	for i in xrange(a):
		begin_frame()
		empty_func_3()
		end_frame()

	end_ts = time.time()
	print "a %s empty_func_3 cost %s" % (a, end_ts - begin_ts)

	begin_ts = time.time()
	for i in xrange(a):
		begin_frame()
		empty_func_4()
		end_frame()

	end_ts = time.time()
	print "a %s empty_func_4 cost %s" % (a, end_ts - begin_ts)