"""PyCharm entry point. GUI sources are prebuilt; Node is not required to run."""
import argparse
import multiprocessing
import os
from pathlib import Path
import threading
import webbrowser
from backend.server import Bridge, serve
from backend.accounts import Accounts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--browser', action='store_true', help='在本机浏览器中测试，终端 Ctrl+C 结束')
    parser.add_argument('--data-dir', default=None)
    parser.add_argument('--no-open', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    frontend = root / 'frontend' / 'dist'
    if not (frontend / 'index.html').exists():
        raise SystemExit('缺少界面构建文件。请下载完整源码包，或在 frontend 中执行 npm install 和 npm run build。')
    service = Accounts(args.data_dir or os.environ.get('ZHIJUAN_DATA_DIR') or root / 'data')
    bridge = Bridge(service)
    server, url = serve(frontend, bridge)
    try:
        if args.browser:
            print(f'知卷工作台：{url}', flush=True)
            print('按 Ctrl+C 停止；资料会自动保存在 data 文件夹。', flush=True)
            if not args.no_open:
                webbrowser.open(url)
            threading.Event().wait()
        else:
            try:
                import webview
            except ImportError:
                raise SystemExit('缺少桌面依赖。请运行 python -m pip install -r requirements.txt\n也可先运行 python app.py --browser，测试无需桌面依赖的浏览器模式。')
            if os.name == 'nt':
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Zhijuan.Workbench.Desktop')
            webview.settings['ALLOW_DOWNLOADS'] = True
            window = webview.create_window('知卷 · 教学工作台', url, js_api=bridge, width=1380, height=900, min_size=(1000, 700), background_color='#F5F6F9', frameless=True, easy_drag=False)
            bridge._window=window
            webview.start(gui='edgechromium' if os.name == 'nt' else None, debug=False, icon=str(root / 'assets' / 'zhijuan.ico'))
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
        service.close()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
