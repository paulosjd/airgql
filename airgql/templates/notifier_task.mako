<!doctype html>
<html>
<head>
	<meta charset="utf-8">
	<title>Task Example</title>
</head>
<body>
    <button type="button">Run Task</button>
    <br>
    Result: <span id="result"></span>
    <script src="${notifier_url}/socket.io/socket.io.js"></script>
    <script src="${request.static_url('airgql:static/client.js')}"></script>
</body>
</html>