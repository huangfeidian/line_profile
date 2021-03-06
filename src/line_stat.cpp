#include <line_stat.h>
#include <chrono>
#include <iostream>


line_profile::line_profile()
{

}

line_profile& line_profile::instance()
{
	static line_profile the_one;
	return the_one;
}

void line_profile::begin_frame()
{
	PyFrameObject *frame = PyThreadState_Get()->frame;
	if (!frame)
	{
		return;
	}

	 //std::string func_name = (std::string)py::str(frame->f_code->co_name);
	 //std::cout << "begin_frame 1 at " << reinterpret_cast<std::size_t>(frame) << " function " << func_name << std::endl;

	auto& cur_line_ts = frame_infos[frame];
	cur_line_ts.line_info.line_no = 0;
	cur_line_ts.line_info.ts = std::chrono::steady_clock::now();
}

void line_profile::add_line()
{
	PyFrameObject *basic_frame = PyThreadState_Get()->frame;
	std::uint32_t line_no;
	if (!basic_frame)
	{
		std::cout << "fail to add_line 1" << std::endl;

		return;
	}
	

	PyFrameObject * frame = basic_frame->f_back;
	
	if (!frame)
	{
		std::cout << "fail to add_line 2" << std::endl;

		return;
	}
	//std::cout << "add_line lineno is " << line_no << " func is "<< func_name<< " frame id is "<< reinterpret_cast<std::size_t>(frame)<<std::endl;
	auto cur_frame_iter = frame_infos.find(frame);
	if(cur_frame_iter == frame_infos.end())
	{
		std::cout << "fail to add_line 3" << std::endl;
		return;
	}
	auto& cur_frame_stat = cur_frame_iter->second;
	if(cur_frame_stat.line_info.line_no == 0)
	{
		std::string func_name = (std::string)py::str(basic_frame->f_code->co_name);
		//std::cout << "link func_name " << func_name << " to frame " << reinterpret_cast<std::size_t>(frame) << std::endl;
		auto linked_func = func_line_stats[func_name];
		if (!linked_func)
		{
			linked_func = new function_stat();
			func_line_stats[func_name] = linked_func;

		}
		cur_frame_stat.link_func = linked_func;
	}
	if (basic_frame->f_trace)
	{
		line_no = basic_frame->f_lineno;
	}
	else
	{
		auto last_addr = basic_frame->f_lasti;
		auto& cur_cache_line_no = cur_frame_stat.link_func->address_to_line[last_addr];
		if (cur_cache_line_no == 0)
		{
			line_no = PyCode_Addr2Line(basic_frame->f_code, last_addr);
			cur_cache_line_no = line_no;
		}
		else
		{
			line_no = cur_cache_line_no;
		}

	}
	//std::cout << "add line_no 1 " << line_no << std::endl;

	//line_no = PyFrame_GetLineNumber(basic_frame);

	//std::cout << "add line_no 2 " << line_no << std::endl;
	if (cur_frame_stat.line_info.line_no + 2 != line_no)
	{
		cur_frame_stat.line_info.line_no = line_no;
		return;
	}
	auto diff_ts = std::chrono::steady_clock::now() - cur_frame_stat.line_info.ts;
	auto& cur_line_cost = cur_frame_stat.link_func->line_costs[line_no];
	cur_line_cost.durations += std::chrono::duration_cast<duration_t>(diff_ts);
	cur_line_cost.access_no++;
	cur_frame_stat.line_info.line_no = line_no;
	return;
}
void line_profile::end_frame()
{
	PyFrameObject *frame = PyThreadState_Get()->frame;
	std::string func_name;
	if (!frame)
	{
		std::cout << "fail to end_frame 1" << std::endl;

		return;
	}

	func_name = (std::string)py::str(frame->f_code->co_name);
	//std::cout << "end_frame 1 at " << reinterpret_cast<std::size_t>(frame) << " function " << func_name << std::endl;


	auto cur_ts = std::chrono::steady_clock::now();

	auto cur_frame_iter = frame_infos.find(frame);
	if (cur_frame_iter == frame_infos.end())
	{
		std::cout << "fail to end_frame 3" << std::endl;

		return;
	}
	
	auto& cur_frame_stat = cur_frame_iter->second;

	auto diff_ts = std::chrono::steady_clock::now() - cur_frame_stat.line_info.ts;
	auto& cur_line_cost = cur_frame_stat.link_func->line_costs[cur_frame_stat.line_info.line_no + 2];
	cur_line_cost.durations += std::chrono::duration_cast<duration_t>(diff_ts);
	cur_line_cost.access_no++;
	frame_infos.erase(cur_frame_iter);
}

std::map<std::uint32_t, std::pair<std::uint32_t, std::uint64_t>> line_profile::dump_stat(const std::string& func_name)
{
	std::map<std::uint32_t, std::pair<std::uint32_t, std::uint64_t>> result;
	auto cur_iter = func_line_stats.find(func_name);
	if (cur_iter == func_line_stats.end())
	{
		return result;
	}
	for (const auto& one_item : cur_iter->second->line_costs)
	{
		result[one_item.first - 1] = std::make_pair(one_item.second.access_no, one_item.second.durations.count());
	}
	func_line_stats.erase(cur_iter);
	return result;
}

void line_profile::clear_func(const std::string& func_name)
{
	auto cur_func_stat = func_line_stats[func_name];
	std::vector< PyFrameObject*> keys_to_remove;
	for (auto [k, v] : frame_infos)
	{
		if (v.link_func == cur_func_stat)
		{
			keys_to_remove.push_back(k);
		}
	}
	for (auto one_key : keys_to_remove)
	{
		frame_infos.erase(one_key);
	}
	func_line_stats.erase(func_name);
	if (cur_func_stat)
	{
		delete cur_func_stat;
	}
}
void begin_frame()
{
	auto& cur_ins = line_profile::instance();
	cur_ins.begin_frame();
}
void end_frame()
{
	auto& cur_ins = line_profile::instance();
	cur_ins.end_frame();
}

void add_line()
{
	auto& cur_ins = line_profile::instance();
	cur_ins.add_line();
}
void clear_func(const std::string& func_name)
{
	auto& cur_ins = line_profile::instance();
	cur_ins.clear_func(func_name);
}

void add_line_arg(int a)
{
	auto& cur_ins = line_profile::instance();
	cur_ins.add_line();
}
std::map<std::uint32_t, std::pair<std::uint32_t, std::uint64_t>> dump_stat(const std::string& func_name)
{
	auto& cur_ins = line_profile::instance();
	return cur_ins.dump_stat(func_name);
}

PYBIND11_MODULE(line_profile, m) {
	m.doc() = R"(line stat module)";
	m.def("begin_frame", &begin_frame, "begin to profile cur frame");
	m.def("end_frame", &end_frame, "end profile cur frame");
	m.def("add_line", &add_line, "add line cost");
	m.def("add_line_arg", &add_line_arg, "add line cost with arg");
	m.def("dump_stat", &dump_stat, "get cost statics for func");
	m.def("clear_func", &clear_func, "clear stat for func, stop trace");
}