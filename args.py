def args_parser(sys_argvs):
    params = None    
    command = None
    args = sys_argvs[1:]

    try:
        command = args[0]
    except:
        print(" - You must insert a command")
        print(" - Try '--help' or '-h' to know more")
        exit()

    params = args[1:]
       
    return [command, params]     
    