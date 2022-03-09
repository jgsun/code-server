#!/usr/bin/python3
import os
import sys

def print_dir_files(file_path, root_path, file_suffix):
        file_list = []
        for file_path, sub_dirs, filenames in os.walk(file_path):
                if filenames:
                        # 如果是文件，则加append到list中
                        for filename in filenames:
                                file_map_path = file_path.replace(root_path, '')
                                if filename.endswith(file_suffix):
                                        file_list.append(os.path.join(file_map_path, filename))
        return file_list

def print_sub_dir(file_path, root_path):
        dir_list = []
        for file_path, sub_dirs, filenames in os.walk(file_path):
                if sub_dirs:
                        # 如果是目录，则加append到list中
                        for sub_dir in sub_dirs:
                                file_map_path = file_path.replace(root_path, '')
                                dir_list.append(os.path.join(file_map_path, sub_dir))
        return dir_list

if __name__ == '__main__':
        # Specific the src and build dir
        src_file_path = '/local/mnt/workspace/code_base/msm_linux/msm-5.4/'
        src_root_path = '/local/mnt/workspace/code_base/msm_linux/msm-5.4'
        obj_file_path = '/local/mnt/workspace/pre_fc1/poky/build/tmp-glibc/work/opsy_sa81x5-oe-linux/linux-msm/5.4-r0/build/'
        obj_root_path = '/local/mnt/workspace/pre_fc1/poky/build/tmp-glibc/work/opsy_sa81x5-oe-linux/linux-msm/5.4-r0/build'
        src_file_suffix = '.c'
        obj_file_suffix = '.o'

        final_obj_dir_list = []
        src_files = []
        exclude_dir = []
        exclude_file = []
        exclude_file_pick = []
        exclude_dir_pick = []
        exclude_dir_pick_l1 = []
        exclude_dir_pick_l2 = []
        exclude_dir_pick_l3 = []
        exclude_dir_pick_l4 = []
        exclude_dir_pick_l5 = []
        src_file_no_suffix = []
        obj_file_no_suffix = []
        final_exclude_file = []
        final_exclude_dir = []
        final_exclude_all = []

        # Retrieve the src and build dir list
        src_dir_list = print_sub_dir(src_file_path, src_root_path)
        print("len(src_dir_list)", len(src_dir_list))
        obj_dir_list = print_sub_dir(obj_file_path, obj_root_path)
        print("len(obj_dir_list)", len(obj_dir_list))

        # Move dir without .o file from object dir list
        for dir in obj_dir_list:
                file_name = obj_root_path + dir + '/built-in.a'
                if os.path.exists(file_name):
                        f = open(file_name, "r")
                        lines = f.readlines()
                        first_line=lines[0]
                        if first_line != '!<arch>\n':
                                final_obj_dir_list.append(dir)
                else:
                        final_obj_dir_list.append(dir)
        print("len(final_obj_dir_list)", len(final_obj_dir_list))
        # sys.exit()

        # Get the exclude object dir list
        for src_dir in src_dir_list:
                if final_obj_dir_list.count(src_dir) == 0:
                        exclude_dir.append(src_dir)
        print("len(exclude_dir)", len(exclude_dir))

        # Remove the overlap from the object dir
        for dir in exclude_dir:
                ltop = dir.rsplit("/", 1)[0]
                if dir.count("/") == 1:
                        exclude_dir_pick_l1.append(dir)
                elif dir.count("/") == 2:
                        if ltop not in exclude_dir_pick_l1:
                                exclude_dir_pick_l2.append(dir)
                elif dir.count("/") == 3:
                        l1 = '/{}'.format(dir.split("/")[1])
                        if l1 in exclude_dir_pick_l1:
                                continue
                        elif ltop not in exclude_dir_pick_l2:
                                exclude_dir_pick_l3.append(dir)
                elif dir.count("/") == 4:
                        l1 = '/{}'.format(dir.split("/")[1])
                        l2 = '/{}'.format(dir.split("/")[1]) + '/{}'.format(dir.split("/")[2])
                        if l1 in exclude_dir_pick_l1:
                                continue
                        elif l2 in exclude_dir_pick_l2:
                                continue
                        elif ltop not in exclude_dir_pick_l3:
                                exclude_dir_pick_l4.append(dir)
                elif dir.count("/") == 5:
                        l1 = '/{}'.format(dir.split("/")[1])
                        l2 = '/{}'.format(dir.split("/")[1]) + '/{}'.format(dir.split("/")[2])
                        l3 = '/{}'.format(dir.split("/")[1]) + '/{}'.format(dir.split("/")[2]) + '/{}'.format(dir.split("/")[3])
                        if l1 in exclude_dir_pick_l1:
                                continue
                        elif l2 in exclude_dir_pick_l2:
                                continue
                        elif l3 in exclude_dir_pick_l3:
                                continue
                        elif ltop not in exclude_dir_pick_l4:
                                exclude_dir_pick_l5.append(dir)
        exclude_dir_pick = exclude_dir_pick_l1 + exclude_dir_pick_l2 + exclude_dir_pick_l3 + exclude_dir_pick_l4 + exclude_dir_pick_l5
        print("len(exclude_dir_pick)", len(exclude_dir_pick))

        # sys.exit()
        # Retrieve the source and build file list
        src_file_list = print_dir_files(src_file_path, src_root_path, '.c')
        print("len(src_file_list)", len(src_file_list))
        obj_file_list = print_dir_files(obj_file_path, obj_root_path, '.o')
        print("len(obj_file_list)", len(obj_file_list))
        for src_file in src_file_list:
                src_file_no_suffix.append(src_file.split(".")[0])
        for obj_file in obj_file_list:
                obj_file_no_suffix.append(obj_file.split(".")[0])

        # Get the un-built source file
        for src_file in src_file_no_suffix:
                if obj_file_no_suffix.count(src_file) == 0:
                        exclude_file.append(src_file)

        # Remove un-built source files that get excluded by dir
        for src_file in exclude_file:
                ltop = src_file.rsplit("/", 1)[0]
                if src_file.count("/") == 1:
                        exclude_file_pick.append(src_file)
                elif src_file.count("/") == 2:
                        if ltop not in exclude_dir_pick:
                                exclude_file_pick.append(src_file)
                elif src_file.count("/") == 3:
                        l1 = '/{}'.format(src_file.split("/")[1])
                        if l1 in exclude_dir_pick:
                                continue
                        elif ltop not in exclude_dir_pick:
                                exclude_file_pick.append(src_file)
                elif src_file.count("/") == 4:
                        l1 = '/{}'.format(src_file.split("/")[1])
                        l2 = '/{}'.format(src_file.split("/")[1]) + '/{}'.format(src_file.split("/")[2])
                        if l1 in exclude_dir_pick:
                                continue
                        elif l2 in exclude_dir_pick:
                                continue
                        elif ltop not in exclude_dir_pick:
                                exclude_file_pick.append(src_file)
                elif dir.count("/") == 5:
                        l1 = '/{}'.format(src_file.split("/")[1])
                        l2 = '/{}'.format(src_file.split("/")[1]) + '/{}'.format(src_file.split("/")[2])
                        l3 = '/{}'.format(src_file.split("/")[1]) + '/{}'.format(src_file.split("/")[2]) + '/{}'.format(src_file.split("/")[3])
                        if l1 in exclude_dir_pick:
                                continue
                        elif l2 in exclude_dir_pick:
                                continue
                        elif l3 in exclude_dir_pick:
                                continue
                        elif ltop not in exclude_dir_pick:
                                exclude_file_pick.append(src_file)

        print("len(exclude_file_pick)", len(exclude_file_pick))

        # sys.exit()
        # Append format for setting.json
        for src_file in exclude_dir_pick:
                format_exclude_dir = '"**{}"'.format(src_file)
                final_exclude_dir.append(format_exclude_dir)


        for src_file in exclude_file_pick:
                format_exclude_file = '"**{}*"'.format(src_file)
                final_exclude_file.append(format_exclude_file)

        final_exclude_all = final_exclude_dir + final_exclude_file
        print("len(final_exclude_all)", len(final_exclude_all))

        format_final_exclude_all = ": true,\n".join(final_exclude_all)

        f = open("/local/mnt/workspace/tools/code-server/files_exclude.txt", "w")
        f.write(format_final_exclude_all)
        print("files to be excluded is available at /local/mnt/workspace/tools/code-server/files_exclude.txt")