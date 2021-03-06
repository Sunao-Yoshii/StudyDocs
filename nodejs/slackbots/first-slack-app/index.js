const dotenv = require('dotenv');
dotenv.config();

// Initialize http
const http = require('http');

// Initialize the Slack Events API using signing secret from environment variables
const createEventAdapter = require('@slack/events-api').createEventAdapter;
const slackEvents = createEventAdapter(process.env.SLACK_SIGNING_SECRET);
const port = process.env.PORT || 3000;

// Initialize the Web API Client
const { WebClient } = require('@slack/client');
const token = process.env.SLACK_TOKEN;
const slackWeb = new WebClient(token);

// Setting Up Express to be used with the Events API
const express = require('express');
const bodyParser = require('body-parser');
const app = express();

// Setting up this route to be used with the Slack Events middleware
app.use('/slack/events', slackEvents.expressMiddleware());

// Attach listeners to events by Slack Event "type".
slackEvents.on('team_join', (event) => {
    console.log(`Received a team_join event: user ${event.user.name} has joined.`);
});

// Handle errors (see `errorCodes` export)
slackEvents.on('error', console.error);

// Start a basic HTTP server
http.createServer(app).listen(port, () => {
    console.log(`server listening on port ${port}`);
});