import os
import sys

def main():
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 添加Herodotus的src目录到Python路径
    herodotus_src = os.path.abspath(os.path.join(current_dir, '../../Herodotus/src'))
    sys.path.append(herodotus_src)
    
    # 添加当前目录到Python路径
    sys.path.append(current_dir)
    
    # 导入并运行Flask应用
    from app import app
    app.run(debug=True)

if __name__ == '__main__':
    main() 