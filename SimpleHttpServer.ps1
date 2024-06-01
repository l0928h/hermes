# SimpleHttpServer.ps1

param (
    [int]$port = 8080
)

# 创建 HttpListener 对象
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://*: $port /")
$listener.Start()
Write-Host "HTTP Server started. Listening on port $port..."

while ($listener.IsListening) {
    # 等待并获取 HTTP 请求
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response

    # 处理请求并生成响应
    $responseString = "<html><body><h1>Hello, PowerShell HTTP Server!</h1></body></html>"
    $buffer = [System.Text.Encoding]::UTF8.GetBytes($responseString)
    $response.ContentLength64 = $buffer.Length
    $response.OutputStream.Write($buffer, 0, $buffer.Length)
    $response.OutputStream.Close()
}

# 停止 HttpListener 对象
$listener.Stop()
