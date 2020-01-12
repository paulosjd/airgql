
const app = require('express')(),
    server = require('http').Server(app),
    io = require('socket.io')(server),
    bodyParser = require('body-parser');
    cors = require('cors');

// Echo the client's ID back to them when they connect.
io.on('connection', (client) => {
    client.emit('register', client.id);
});

// Accept URL-encoded body in POST request.
app.use(bodyParser.urlencoded({extended: true}));

// The /notify endpoint with the client ID as a POST parameter is called by background worker on task completion
app.post('/notify', (request, response) => {
    const {clientid, result} = request.body;
    const client = io.sockets.connected[clientid];  // Find the appropriate client to send the task result back to.
    client.emit('notify', result);
    response.type('text/plain');
    response.send('Result broadcast to client.');
});

server.listen(3000);