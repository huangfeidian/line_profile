# -- encoding = utf-8 --
import inspect
import time
frame_func_stat = {}
total_func_stat = {}

def stat_func(f):
	def wrap_f(*args, **kwargs):
		global frame_func_stat
		func_id = f.__name__
		pre = frame_func_stat.setdefault(func_id, {})
		frame_id = id(inspect.currentframe().f_back)
		print "wrap_f for func %s func_id %s frame_id %s" % (f.__name__, func_id, frame_id)
		frame_info = pre.setdefault(frame_id, [])
		try:
			result = f(*args, **kwargs)
			finish_one_call(func_id, frame_id)
			return result
		except Exception as e:
			finish_one_call(func_id, frame_id)
			raise e
	return wrap_f

def finish_one_call(func_id, frame_id):
	global frame_func_stat
	global total_func_stat
	cur_time = time.time()
	pre_total = total_func_stat.setdefault(func_id, {})
	cur_stat = frame_func_stat.get(func_id, {}).pop(frame_id, [])
	print "finish_one_call func_id %s frame_id %s cur detail %s " % (func_id, frame_id, cur_stat)

	if not cur_stat:
		return

	if len(cur_stat) == 1:
		return

	pre_time = cur_stat[0][0]
	pre_line = cur_stat[0][1]
	for one_stat in cur_stat:
		print "cur line info is  " , one_stat
		if one_stat[1] != pre_line + 1:
			pre_line = one_stat[1]
			continue
		one_time = one_stat[0]
		pre_line_info = pre_total.setdefault(pre_line, [0, 0])
		pre_line_info[0] += one_time - pre_time
		pre_line_info[1] += 1

		pre_line = one_stat[1]
		pre_time = one_time

	pre_line_info = pre_total.setdefault(pre_line, [0, 0])
	pre_line_info[0] += cur_time - pre_time
	pre_line_info[1] += 1


def add_line_stat(func_id, frame_id, line_no):
	print "add_line_stat func_id %s frame_id %s line_no %s cur_detail is %s" % (func_id, frame_id, line_no, frame_func_stat)
	cur_time = time.time()
	cur_stat = frame_func_stat.get(func_id, {}).get(frame_id, [])
	cur_stat.append((cur_time, line_no))

def dump_func_stat(func_id):
	return total_func_stat.get(func_id, [])
	


	

	

	
