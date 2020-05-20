#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <map>
#include <chrono>

namespace py = pybind11;
using duration_t = std::chrono::microseconds;
using ts_t = std::chrono::time_point<std::chrono::steady_clock>;

struct line_ts
{
	std::uint32_t line_no = 0;
	ts_t ts;
};
struct line_cost_stat
{
	std::uint32_t access_no = 0;
	duration_t durations;
};
struct function_stat
{
	std::unordered_map<std::uint32_t, line_cost_stat> line_costs;
	std::unordered_map<int, int> address_to_line;
};
struct frame_stat
{
	line_ts line_info;
	function_stat* link_func = nullptr;
};

class line_profile
{
public:
	std::unordered_map<std::string, function_stat*> func_line_stats;
	std::unordered_map<PyFrameObject*, frame_stat> frame_infos;

private:
	line_profile();
public:
	static line_profile& instance();
	void begin_frame();
	void end_frame();
	void add_line();
	void clear_func(const std::string& func_name);
	int get_line_number(PyFrameObject* frame, function_stat* func);
	std::map<std::uint32_t, std::pair<std::uint32_t, std::uint64_t>> dump_stat(const std::string& func_name);
};
void begin_frame();
void end_frame();
void add_line();
void add_line_arg(int a);
void clear_func(const std::string& func_name);
std::map<std::uint32_t, std::pair<std::uint32_t, std::uint64_t>> dump_stat(const std::string& func_name);