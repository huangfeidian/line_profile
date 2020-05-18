# encoding = utf-8
import inspect
from line_stat import stat_func, add_line_stat
from line_profile import begin_frame, end_frame, add_line, dump_stat
def func_1(a):
	return ["11111" for i in xrange(a)]

def func_2(a, b):
	temp_1 = func_1(a)
	temp_2 = func_1(b)
	return temp_1.extend(temp_2)

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
	cur_frame = inspect.currentframe()
	frame_id = id(cur_frame.f_back)
	print "cur func name is %s frame_id_1  is %s" % (func_4.__name__, frame_id)
	add_line()
	temp_1 = func_1(a)
	add_line()
	temp_2 = func_1(b)
	add_line()
	return temp_1.extend(temp_2)

def func_5(a, b):
	try:
		begin_frame()
		result = func_4(a, b)
		end_frame()
		return result
	except Exception as e:
		end_frame()
		raise e