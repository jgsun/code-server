#!/usr/bin/python3

import os
# import glob 
# os.chdir("/local/mnt/workspace/code_base/msm-5.4/drivers/scsi")
# for file_lst in glob.glob("*.c"):
#         print(file_lst)


def print_dir_files(file_path, root_path, file_suffix):
        file_list = []
        for file_path, sub_dirs, filenames in os.walk(file_path):
                # print(sub_dirs)
                # print(filenames)
                # print(file_path)
                if filenames:
                        # 如果是文件，则加append到list中
                        for filename in filenames:
                                # if file_suffix in filename:
                                file_map_path = file_path.replace(root_path, '')
                                if filename.endswith(file_suffix):
                                        file_list.append(os.path.join(file_map_path, filename))
        # for file_list_item in file_list:
        #         print(file_list_item)
        return file_list

if __name__ == '__main__':
        src_files = []
        file_path = '/local/mnt/workspace/code_base/msm-5.4/'
        root_path = '/local/mnt/workspace/code_base/msm-5.4/'
        file_suffix = '.c'
        src_file_list = print_dir_files(file_path, root_path, file_suffix)
        # for src_file in src_file_list:
        #         print(src_file)

        file_path = '/local/mnt/workspace/pre_fc1/poky/build/tmp-glibc/work/opsy_sa81x5-oe-linux/linux-msm/5.4-r0/build/'
        root_path = '/local/mnt/workspace/pre_fc1/poky/build/tmp-glibc/work/opsy_sa81x5-oe-linux/linux-msm/5.4-r0/build/'
        file_suffix = '.o'
        obj_file_list = print_dir_files(file_path, root_path, file_suffix)
        for obj_file in obj_file_list:
                j = 0
                # print(obj_file)
                # print(len(src_file_list))
                for i in range(len(src_file_list)):
                        # print(i)
                        # print(src_file_list[i].split(".")[0])
                        # print(obj_file.split(".")[0])
                        if src_file_list[j].split(".")[0] == obj_file.split(".")[0]:
                                src_file_list.pop(j)
                                break
                        else:
                                j += 1
        for src_file in src_file_list:
                format_src_file = '"**/{}"'.format(src_file)
                # print(format_src_file)
                src_files.append(format_src_file)
                # file_map_path_wildcard = format_src_file[:-2] + '*"'
                # src_files.append(file_map_path_wildcard)
        # print(src_files)
        # os.mknod("/local/mnt/workspace/tools/code-server/files_exclude.txt")
        f = open("/local/mnt/workspace/tools/code-server/files_exclude.txt", "w")
        str_src_files = ": true,\n".join(src_files)
        f.write(str_src_files)
        print("files to be excluded is available at /local/mnt/workspace/tools/code-server/files_exclude.txt")
