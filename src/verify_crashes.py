import concurrent.futures
import os
import re
import sys
import subprocess
from tqdm import tqdm

max_workers = 5

# experiment
put = "/home/cas/chenxu/cxfuzz3/fuzz/verify_crashes/nm-new-asan"
args = "-C @@"
crash_dir = "/home/cas/chenxu/cxfuzz3/fuzz/verify_crashes/crashes"

# try vul
# put = "/home/cas/chenxu/cxfuzz3/try_vul/verify_crashes/MP4Box"
# args = "-dash 1000 -out /dev/null @@"
# crash_dir = "/home/cas/chenxu/cxfuzz3/try_vul/verify_crashes/crashes"

crash_file_list = []
timeout_file_list = []
asan_crashe_info_files_dict = {}
no_asan_crash_info_file_list = []
# with out asan info, try use gdb
gdb_crash_info_files_dict = {}
no_crash_info_file_list = []


def extract_asan_callstack(err_msg, max_func=5):
    patt = r'#\d+ 0x[0-9a-fA-F]+ in ([\w:]+)'
    match_list = re.findall(patt, err_msg)
    unwanted_functions = {
        '__asan_memcpy',
        '__interceptor_malloc',
        'strlen',
        '__sanitizer',
        'StackTrace',
        'BufferedStackTrace',
        'strstr',
        'xmalloc',
        'StrtolFixAndCheck',
        'fread',
        'strtol',
        'std::char_traits',
        'operator'
    }
    match_list = [
        func for func in match_list if func not in unwanted_functions]
    if match_list:
        first_func = match_list[0]
        search_string = 'in' + ' ' + first_func
        for line in err_msg.splitlines():
            if search_string in line:
                content = line.split(search_string, 1)[1].strip()
                file_line_match = content.split(
                    '/')[-1] if '/' in content else content
                if file_line_match:
                    file_name = file_line_match
                    match_list[0] += f' ({file_name})'
                    break
    if len(match_list) > max_func:
        match_list = match_list[:max_func]
    return match_list


def extract_gdb_callstack(err_msg, max_func=5):
    patt = r'#\d+\s+0x[0-9a-fA-F]+\s+in\s+([\w:]+)'
    match_list = re.findall(patt, err_msg)
    unwanted_functions = {
        '__GI_raise',
        '__GI_abort',
        '__assert_fail_base',
        '__GI___assert_fail',
        'std::terminate',
        '__cxa_throw'
    }
    match_list = [
        func for func in match_list if func not in unwanted_functions]
    if match_list:
        first_func = match_list[0]
        search_string = 'in' + ' ' + first_func
        for line in err_msg.splitlines():
            if search_string in line:
                content = line.split(search_string, 1)[1].strip()
                file_line_match = content.split(
                    '/')[-1] if '/' in content else content
                if file_line_match:
                    file_name = file_line_match
                    match_list[0] += f' ({file_name})'
                    break
    if len(match_list) > max_func:
        match_list = match_list[:max_func]
    return match_list


def process_asan_crash_info(file):
    if args.find('@@') == -1:
        _stdin_fd = open(file)
    else:
        _stdin_fd = subprocess.PIPE
    _cur_args = args.replace('@@', file)
    all_cmd = [put]
    all_cmd.extend(_cur_args.split(' '))
    try:
        p = subprocess.run(all_cmd, stdin=_stdin_fd,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
        err_msg = p.stderr.decode('utf-8', 'ignore')
        if err_msg.find('AddressSanitizer') == -1:
            no_asan_crash_info_file_list.append(file)
        else:
            lpos = err_msg.find('ERROR: AddressSanitizer: ')
            if lpos == -1 and err_msg.find('ERROR: LeakSanitizer: ') != -1:
                btype = 'mem-leak'
                err_msg = err_msg[err_msg.find('ERROR: LeakSanitizer: '):]
            else:
                btype = err_msg[lpos + 25:][:err_msg[lpos + 25:].find(' ')]
                err_msg = err_msg[lpos:]
            if btype == 'heap-use-after-free':
                free_pos = err_msg.find('freed by thread')
                alloc_pos = err_msg.find('previously allocated by')
                use_msg = err_msg[:free_pos]
                free_msg = err_msg[free_pos: alloc_pos]
                alloc_msg = err_msg[alloc_pos:]
                ret = extract_asan_callstack(use_msg)
                stack_trace = '->'.join(ret)
            elif btype == 'stack-overflow':
                ret = extract_asan_callstack(err_msg)
                stack_trace = '->'.join(ret)
            else:
                ret = extract_asan_callstack(err_msg)
                stack_trace = '->'.join(ret)
            type_stack_trace = btype + ' : ' + stack_trace
            if type_stack_trace not in asan_crashe_info_files_dict:
                asan_crashe_info_files_dict[type_stack_trace] = []
                asan_crashe_info_files_dict[type_stack_trace].append(file)
    except:
        timeout_file_list.append(file)


def process_gdb_crash_info(file):
    if args.find('@@') == -1:
        sys.exit(1)
    _cur_args = args.replace('@@', file)
    gdb_script = f"""
    set pagination off
    set args {_cur_args}
    run
    bt
    quit
    """
    try:
        gdb_process = subprocess.Popen(
            ['gdb', put], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False)
        stdout, stderr = gdb_process.communicate(
            gdb_script.encode('utf-8'), timeout=15)
        stdout_decoded = stdout.decode('utf-8')
        if "Segmentation fault" in stdout_decoded or "Aborted" in stdout_decoded:
            ret = extract_gdb_callstack(stdout_decoded)
            stack_trace = '->'.join(ret)
            if stack_trace not in gdb_crash_info_files_dict:
                gdb_crash_info_files_dict[stack_trace] = []
                gdb_crash_info_files_dict[stack_trace].append(file)
        else:
            no_crash_info_file_list.append(file)
    except subprocess.TimeoutExpired:
        timeout_file_list.append(file)


for root, dirs, files in os.walk(crash_dir):
    for file in files:
        crash_file_list.append(os.path.abspath(os.path.join(root, file)))

tasks = crash_file_list
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(process_asan_crash_info, task)
               for task in tasks]
    for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing files"):
        pass

tasks = no_asan_crash_info_file_list
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(process_gdb_crash_info, task) for task in tasks]
    for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing files"):
        pass


#  print

print("\n")

print_all = 1

if print_all == 1:
    for key, value in asan_crashe_info_files_dict.items():
        print(key)
        print(value[0])
        print("\n")
    print("----------\n")
    for key, value in gdb_crash_info_files_dict.items():
        print(key)
        print(value[0])
        print("\n")
    print("----------\n")
    print(len(asan_crashe_info_files_dict) +
          len(gdb_crash_info_files_dict), " different crash infos")
    if timeout_file_list:
        print(len(timeout_file_list), " timeout files")
    if no_crash_info_file_list:
        print(len(no_crash_info_file_list), " no crash info files")
else:
    print(len(asan_crashe_info_files_dict) +
          len(gdb_crash_info_files_dict), " different crash infos")
