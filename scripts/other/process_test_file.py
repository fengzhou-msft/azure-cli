#!/usr/bin/env python

import sys

def main():
    file = sys.argv[1]
    cmd = ""
    in_cmd = False
    process_kw = False
    kw_dict = {}
    for line in open(file):
        if (line.strip().startswith('#')):
            continue
        elif (line.strip().startswith('self.kwargs.update')):
            process_kw = True
        elif (line.strip().startswith("self.cmd")):
            if cmd != "":
                for k, v in kw_dict.items():
                    cmd = cmd.replace("{"+ k + "}", v)
                print(cmd + "\n")
                cmd = ""
            in_cmd = True
            process_kw = False
        elif process_kw:
            kv = line.strip().split(":")
            if len(kv) == 2:
                key = kv[0].strip().replace("'", "")
                value = kv[1].strip().replace("'", "").replace(",", "")
                kw_dict[key] = value
        if in_cmd and not line.strip().startswith("check"):
            words = line.split("'")
            if len(words) > 1:
                cmd += line.split("'")[1]
    if cmd != "":
        for k, v in kw_dict.items():
            cmd = cmd.replace("{"+ k + "}", v)
        print(cmd + "\n")
    

if __name__ == '__main__':
    main()
