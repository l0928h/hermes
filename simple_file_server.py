import http.server
import socketserver

# 指定服务器地址和端口
HOST = '0.0.0.0'  # 监听所有可用的网络接口
PORT = 8000  # 端口号，可以根据需要更改

# 创建一个简单的 HTTP 服务器
Handler = http.server.SimpleHTTPRequestHandler

# 指定服务器地址和端口
with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print(f"文件服务器运行在 http://{HOST}:{PORT}/")
    try:
        # 保持服务器运行
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("^C 接收到中断信号，关闭服务器。")
