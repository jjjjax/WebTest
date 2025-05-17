import http.server
import socketserver
import os
import socket
import mimetypes

def get_local_ip():
    try:
        # 获取本机IP地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

PORT = 8000

# 允许跨域访问并处理APK文件
class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

    def do_GET(self):
        # 检查是否是APK文件
        if self.path.lower().endswith('.apk'):
            try:
                # 获取文件路径
                file_path = self.translate_path(self.path)
                # 获取文件大小
                file_size = os.path.getsize(file_path)
                
                # 设置响应头
                self.send_response(200)
                self.send_header('Content-Type', 'application/vnd.android.package-archive')
                self.send_header('Content-Length', str(file_size))
                self.send_header('Content-Disposition', 'attachment; filename="app.apk"')
                self.end_headers()
                
                # 发送文件内容
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
            except Exception as e:
                print(f"Error serving APK: {e}")
                self.send_error(500, f"Error serving APK: {e}")
                return
        
        # 对于其他文件使用默认处理
        return super().do_GET()

with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    local_ip = get_local_ip()
    print(f"服务器已启动!")
    print(f"请在浏览器中访问以下地址:")
    print(f"本机访问: http://localhost:{PORT}")
    print(f"局域网访问: http://{local_ip}:{PORT}")
    print("按 Ctrl+C 停止服务器")
    httpd.serve_forever()