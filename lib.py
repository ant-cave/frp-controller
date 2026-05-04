import os

# ... existing code ...
def get_config() -> dict[str:str]:
    """获取所有配置文件路径映射
    
    返回:
        dict: 配置名称与文件路径的映射字典，格式为 {配置名: 配置文件路径}
        配置名格式规则:
        - 直接位于config目录下的文件: FRPAUTO_<文件名>
        - 位于子目录中的文件: FRPAUTO_<目录名>.<文件名>
    """
    main_dict = {}
    
    for item in os.listdir('./config'):
        item_path = os.path.join('./config', item)
        
        if os.path.isdir(item_path):
            # 处理子目录中的配置文件
            for config_file in os.listdir(item_path):
                if config_file.endswith('.toml'):
                    config_path = os.path.join(item_path, config_file)
                    config_name = f'FRPAUTO_{item}.{config_file[:-5]}'  # 去除.toml后缀
                    main_dict[config_name] = config_path
        elif item.endswith('.toml'):
            # 处理直接位于config目录下的配置文件
            config_name = f'FRPAUTO_{item[:-5]}'  # 去除.toml后缀
            main_dict[config_name] = os.path.join('./config', item)
    
    return main_dict
# ... existing code ...


import subprocess
import shlex
import sys

def start_screen(session_name: str, force_create: bool = False, sys_check: bool = True, cmd: str = None) -> bool:
    """
    在 Linux 系统中创建一个后台运行的 screen 会话，并可选择性地在会话中执行一条命令。

    :param session_name: 要创建的 screen 会话名称，如 "FRPAUTO_web"
    :param force_create: 是否强制创建（忽略同名会话）
    :param sys_check: 是否检查系统是否为 Linux
    :param cmd: 在 screen 会话中要执行的命令
    :return: True 如果成功创建会话并执行命令，否则返回 False
    """
    
    # 系统检查
    if sys_check and not sys.platform.startswith('linux'):
        print("错误：此函数仅支持 Linux 系统")
        return False
    
    # 检查 screen 是否安装
    try:
        subprocess.run(["screen", "-v"], check=True, 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误：screen 未安装或不可用")
        return False
    
    # 检查会话是否已存在
    check_session_cmd = f"screen -ls | grep -q {shlex.quote(session_name)}"
    session_exists = session_name in get_all_screens().values()
    
    if session_exists and not force_create:
        print(f"错误：会话 {session_name} 已存在")
        return False
    
    # 创建 screen 会话
    try:
        # 先创建分离的 screen 会话
        subprocess.run(["screen", "-dmS", session_name], check=True)
        
        # 如果有命令要执行
        if cmd:
            # 使用 screen -X 在会话中执行命令
            # 先发送回车确保在提示符下
            subprocess.run(["screen", "-S", session_name, "-X", "stuff", "\n"])
            # 发送命令并执行（末尾加回车）
            subprocess.run(["screen", "-S", session_name, "-X", "stuff", f"{cmd}\n"])
        
        return True
        
    except subprocess.CalledProcessError as e:
        return False

def stop_screen(session_name: str) -> int:
    """
    关闭指定名称的所有 screen 会话
    
    参数:
        session_name (str): 要关闭的 screen 会话名称（精确匹配）
    
    返回:
        int: 成功关闭的会话数量
    """
    success_count = 0  # 计数器，记录成功关闭的会话数量
    screen_dict = get_all_screens()

    for pid in screen_dict:
        name = screen_dict[pid]
        if name == session_name:
            #print(f"screen -X -S {pid}.{name} quit")
            os.system(f"screen -X -S {pid}.{name} quit")
            success_count += 1  # 每次成功关闭一个会话，计数器加一

    return success_count

    


def list_frpauto_screens() -> list[str]:
    """
    获取当前系统中所有以 'FRPAUTO_' 开头的 screen 会话名称
    
    返回:
        List[str]: 所有匹配的 screen 会话名称列表
    """
    try:
        # 获取所有 screen 会话并过滤出以 FRPAUTO_ 开头的名称
        cmd = "screen -list | grep -oP 'FRPAUTO_\\S+'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        
        if not result.stdout:
            return []
        
        return result.stdout.strip().splitlines()
    
    except (subprocess.CalledProcessError, OSError):
        return []

import subprocess


def get_all_screens() -> dict[int:str]:
    result = subprocess.run(["screen",'-ls'], capture_output=True, text=True)
    if result.stderr:
        raise NameError('Error')
    if not result.stdout:
        return {}
    else:
        resultList=result.stdout.split('\n')
        returnDict={}
        for i in resultList:
            if '\t' not in i:
                pass
            else:
                tmp=i[i.index('\t')+1:i.index('\t(')]
                pid=int(tmp.split('.')[0])

                returnDict.update({pid:tmp[tmp.index(str(pid))+len(str(pid))+1:]})
        return returnDict
    
