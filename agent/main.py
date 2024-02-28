import os
import re

import requests
from openai import OpenAI

from agent.JS_parser import parse_ast_conditionally, find_function_by_name, \
    find_arrow_function_by_name, find_event_listeners_by_variable, get_ast_request, \
    parse_required_modules, find_callback_bodies, find_express_app_variable, get_skeleton_method, count_event_listeners, \
    split_event_listeners, extract_function
from agent.core import Core
from agent.implemented_parser import parse_file_contents
from agent.modularity import Modularity

API = ""

code = """
    document.addEventListener('DOMContentLoaded', () => {
  // JavaScript for dynamic interactions will be written here
  // Function to Add a Task
  const addTask = () => {
    // Code to add a new task
    const taskName = taskInput.value;
        if (taskName) {
            const newTask = document.createElement("li");
            newTask.innerText = taskName;
            taskList.appendChild(newTask);
            taskInput.value = "";
            setupTaskActions(newTask);
        }
        
        taskItem.addEventListener("contextmenu", function (e) {
            e.preventDefault();
            taskItem.remove();
        });
  }
  
  

  // Function to Display Tasks
  const displayTasks = () => {
    // Code to display the list of tasks with filters and sorting
  }

  // Function to Mark Task as Complete
  const markAsComplete = (taskId) => {
    // Code to mark the task as complete
  }

  // Function to Delete a Task
  const deleteTask = (taskId) => {
    // Code to delete the task
  }

  // Function to Edit a Task
  const editTask = (taskId) => {
    // Code to edit the details of the task
  }

  // Function to Handle User Authentication
  const handleAuthentication = () => {
    // Code to implement user authentication
  }

  // Function to Set Due Dates and Reminders
  const setDueDateAndReminders = (taskId) => {
    // Code to set due dates for tasks
  }

  // Function to Prioritize Tasks
  const prioritizeTasks = () => {
    // Code to prioritize tasks using colors or sorting
  }

  // Add Event Listeners for the Above Functions
  // E.g., document.getElementById('addTaskBtn').addEventListener('click', addTask);
});
    """


code3 = """
    const taskInput = document.getElementById("taskInput");
    const addTaskBtn = document.getElementById("addTaskBtn");
    const taskList = document.getElementById("taskList");
    

    addTaskBtn.addEventListener("click", function () {
        const taskName = taskInput.value;
        if (taskName) {
            const newTask = document.createElement("li");
            newTask.innerText = taskName;
            taskList.appendChild(newTask);
            taskInput.value = "";
            setupTaskActions(newTask);
        }

        if (taskName) {
            const newTask = document.createElement("li");
            newTask.innerText = taskName;
            taskList.appendChild(newTask);
            taskInput.value = "";
            setupTaskActions(newTask);
        }

        taskItem.addEventListener("click", function () {
            taskItem.classList.toggle("completed");
            taskItem.classList.toggle("asdasd");
        });
    });

    function setupTaskActions(taskItem) {
        taskItem.addEventListener("click", function () {
            taskItem.classList.toggle("completed");
        });

        taskItem.addEventListener("contextmenu", function (e) {
            e.preventDefault();
            taskItem.remove();
        });
    }
"""

code4 = """ 
document.addEventListener("DOMContentLoaded", function () {
    const taskInput = document.getElementById("taskInput");
    const addTaskBtn = document.getElementById("addTaskBtn");
    const taskList = document.getElementById("taskList");
    const addTaskBtn2 = document.getElementById("taskListQ");
    
    const abc = () => {
        return 1 + 1; 
    };

    const dba = async () => {
        return 2 + 2; 
    };

    addTaskBtn2.addEventListener("click", async function () {
        // Your asynchronous code here
    });
    
    addTaskBtn.addEventListener("click", function () {
        const taskName = taskInput.value;
    });
    
    
    function setupTaskActions(taskItem) {
            taskItem.addEventListener("click", function () {
                taskItem.classList.toggle("completed");
            });
    
            taskItem.addEventListener("contextmenu", function (e) {
                e.preventDefault();
                taskItem.remove();
            });
    }
    
    async function displayTasks(sortByValue) {
        try {
            const response = await fetch(`/tasks?sortBy=${sortByValue}`); // Assuming the server supports sorting based on query parameters
            const data = await response.json();
            taskList.innerHTML = ""; // Clear the task list before displaying the new sorted tasks
            data.forEach((task) => {
                const newTask = document.createElement("li");
                newTask.innerText = task.name;
                if (task.status === "Completed") {
                    newTask.classList.add("completed");
                }
                taskList.appendChild(newTask);
                setupTaskActions(newTask);
            });
        } catch (error) {
            console.error("Error fetching tasks:", error);
        }
    }
    
});

"""


server = """
 // app.js

const express = require("express");
const session = require("express-session");
const passport = require("passport");
const LocalStrategy = require("passport-local").Strategy;
const mongoose = require("mongoose");
const User = require("./models/user"); // User model

// Initialize Express app
const app = express();
app.use(express.json());

// Express session setup
app.use(session({
    secret: "secret",
    resave: false,
    saveUninitialized: false
}));

// Passport middleware setup
app.use(passport.initialize());
app.use(passport.session());

// Connect to MongoDB
mongoose.connect('mongodb://localhost/todoapp', { useNewUrlParser: true, useUnifiedTopology: true })
  
  
  
// Define User schema and model
// ... (User schema and model setup)

// Passport local strategy setup
passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

// Authentication routes
 

app.post("/login", passport.authenticate("local"), (req, res) => {
    res.json({ message: "Login successful" });
});

app.get("/logout", (req, res) => {
    req.logout();
    res.json({ message: "Logged out" });
});

app.get("/user", (req, res) => {
    res.json(req.user);
});

// Protected route (example)
app.get("/tasks", (req, res) => {
    if (req.isAuthenticated()) {
        // Handle fetching tasks for authenticated user
        res.json({ message: "Tasks fetched for authenticated user" });
    } else {
        res.status(401).json({ message: "User not authenticated" });
    }
});

// ... Additional routes for managing tasks

app.listen(3000, () => {
    console.log("Server is running on port 3000");
});
"""

code2_1 = """
// script.js

document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('taskForm');
    const taskInput = document.getElementById('taskInput');
    const taskList = document.getElementById('taskList');
    
    taskList.addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            toggleTaskCompletion(event.target); // Call function to toggle task completion
        }
    });

    taskForm.addEventListener('submit', function(event) {
        event.preventDefault();
        if (taskInput.value) {
            addNewTask(taskInput.value); // Call function to add new task
            taskInput.value = "";
        }
    });

    taskList.addEventListener('contextmenu', function(event) {
        event.preventDefault();
        if (event.target.tagName === 'LI') {
            deleteTask(event.target); // Call function to delete task
        }
    });

    // Function to add new task
    function addNewTask(taskName) {
        const newTask = document.createElement('li');
        newTask.innerText = taskName;
        taskList.appendChild(newTask);
    }

    // Function to toggle task completion
    function toggleTaskCompletion(task) {
        task.classList.toggle('completed');
    }

    // Function to delete task
    function deleteTask(task) {
        task.remove();
    }
}); 
"""

server2_1 = """
// server.js

const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');

const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://localhost/todoApp', { useNewUrlParser: true, useUnifiedTopology: true });

// Define task schema
const TaskSchema = new mongoose.Schema({
    name: String,
    completed: { type: Boolean, default: false }
});
const Task = mongoose.model('Task', TaskSchema);

// Middleware
app.use(bodyParser.json());

// API endpoints
app.get('/tasks', async (req, res) => {
    try {
        const tasks = await Task.find();
        res.json(tasks);
    } catch (error) {
        res.status(500).send(error.message);
    }
});

app.post('/tasks', async (req, res) => {
    const task = new Task({ name: req.body.name });
    try {
        const newTask = await task.save();
        res.json(newTask);
    } catch (error) {
        res.status(400).send(error.message);
    }
});

app.put('/tasks/:id', async (req, res) => {
    try {
        const updatedTask = await Task.findByIdAndUpdate(req.params.id, { completed: req.body.completed }, { new: true });
        res.json(updatedTask);
    } catch (error) {
        res.status(400).send(error.message);
    }
});

app.delete('/tasks/:id', async (req, res) => {
    try {
        await Task.findByIdAndDelete(req.params.id);
        res.send('Task deleted successfully');
    } catch (error) {
        res.status(400).send(error.message);
    }
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 
"""

project_files = """
server.js: // server.js

const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

// Middleware to parse JSON data
app.use(bodyParser.json());

// Sample data - to be replaced with MongoDB integration
let events = [
  { id: 1, title: 'Meeting', date: '2022-10-15', description: 'Discuss project timelines' },
  { id: 2, title: 'Lunch', date: '2022-10-20', description: 'Team lunch at the new restaurant' }
];

// Get all events
app.get('/api/events', (req, res) => {
  res.json(events);
});

// Get a specific event
app.get('/api/events/:id', (req, res) => {
  const eventId = parseInt(req.params.id);
  const event = events.find(event => event.id === eventId);
  if (!event) res.status(404).send('Event not found');
  res.json(event);
});

// Add a new event
app.post('/api/events', (req, res) => {
  const { title, date, description } = req.body;
  const newEvent = {
    id: events.length + 1,
    title,
    date,
    description
  };
  events.push(newEvent);
  res.json(newEvent);
});

// Update an event
app.put('/api/events/:id', (req, res) => {
  const eventId = parseInt(req.params.id);
  const event = events.find(event => event.id === eventId);
  if (!event) res.status(404).send('Event not found');
  event.title = req.body.title;
  event.date = req.body.date;
  event.description = req.body.description;
  res.json(event);
});

// Delete an event
app.delete('/api/events/:id', (req, res) => {
  const eventId = parseInt(req.params.id);
  const eventIndex = events.findIndex(event => event.id === eventId);
  if (eventIndex === -1) res.status(404).send('Event not found');
  const deletedEvent = events.splice(eventIndex, 1);
  res.json(deletedEvent[0]);
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});


===========================================
styles.css: ```styles.css: /* styles.css */

body {
  font-family: Arial, sans-serif;
  padding: 20px;
}

.calendar {
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
}

.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.calendar-body {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10px;
}

/* Responsive Design */
@media only screen and (max-width: 600px) {
  .calendar {
    width: 100%;
    max-width: none;
    border-radius: 0;
    padding: 10px;
  }
}```


===========================================
db.js: // db.js - Mongoose Database Connection

const mongoose = require('mongoose');

// Connect to the MongoDB database
mongoose.connect('mongodb://localhost:27017/calendar', { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Error connecting to MongoDB', err));

module.exports = mongoose.connection;


===========================================
index.html: ```index.html: <!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">  <!-- Responsive meta tag -->
  <link rel="stylesheet" href="styles.css">
  <title>Calendar App</title>
</head>
<body>
  <div class="calendar">
    <div class="calendar-header">
      <button id="prevBtn">Previous</button>
      <h1 id="currentDate">Month, Year</h1>
      <button id="nextBtn">Next</button>
    </div>
    <div class="calendar-body" id="calendarBody">
      <!-- Calendar grid will be dynamically generated here -->
    </div>
  </div>
  <script src="script.js"></script>
</body>
</html>```


===========================================
script.js: // script.js

// Sample JavaScript for adding, editing, and removing calendar events
// Add event
function addEvent(title, date, description) {
  // Add event to the calendar
}

// Edit event
function editEvent(eventId, newTitle, newDate, newDescription) {
  // Edit event in the calendar
}

// Remove event
function removeEvent(eventId) {
  // Remove event from the calendar
}

// Switch between calendar views
document.getElementById('prevBtn').addEventListener('click', function() {
  // Switch to the previous calendar view
});

document.getElementById('nextBtn').addEventListener('click', function() {
  // Switch to the next calendar view
});


===========================================
event.js: // event.js - Mongoose Schema for Calendar Events

const mongoose = require('mongoose');

// Define the Event Schema
const eventSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  startTime: {
    type: Date,
    required: true
  },
  endTime: {
    type: Date,
    required: true
  },
  attendees: {
    type: [String]  // Array of strings for attendee names
  }
});

// Create the Event Model
const Event = mongoose.model('Event', eventSchema);

module.exports = Event;


===========================================
event.js: // event.js - Mongoose Schema for Calendar Events

const mongoose = require('mongoose');
const { Schema } = mongoose;

// Define the Event Schema
const eventSchema = new Schema({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  startTime: {
    type: Date,
    required: true
  },
  endTime: {
    type: Date,
    required: true
  },
  attendees: {
    type: [String]  // Array of strings for attendee names
  },
  reminders: {
    type: [
      {
        method: {
          type: String,
          enum: ['email', 'notification']
        },
        timing: {
          type: Number,  // Value in minutes before the start time
          required: true
        }
      }
    ]
  }
});

// Create the Event Model
const Event = mongoose.model('Event', eventSchema);

module.exports = Event;


===========================================
event.js: // event.js - Mongoose Schema for Calendar Events

const mongoose = require('mongoose');
const { Schema } = mongoose;

// Define the Event Schema
const eventSchema = new Schema({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  startTime: {
    type: Date,
    required: true
  },
  endTime: {
    type: Date,
    required: true
  },
  attendees: {
    type: [String]  // Array of strings for attendee names
  },
  reminders: {
    type: [
      {
        method: {
          type: String,
          enum: ['email', 'notification']
        },
        timing: {
          type: Number,  // Value in minutes before the start time
          required: true
        }
      }
    ]
  },
  invitedUsers: {
    type: [String]  // Array of strings for usernames of invited users
  }
});

// Create the Event Model
const Event = mongoose.model('Event', eventSchema);

module.exports = Event;


===========================================
event.js: // event.js - Mongoose Schema for Calendar Events

const mongoose = require('mongoose');
const { Schema } = mongoose;

// Define the Event Schema
const eventSchema = new Schema({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  startTime: {
    type: Date,
    required: true
  },
  endTime: {
    type: Date,
    required: true
  },
  attendees: {
    type: [String]  // Array of strings for attendee names
  },
  reminders: {
    type: [
      {
        method: {
          type: String,
          enum: ['email', 'notification']
        },
        timing: {
          type: Number,  // Value in minutes before the start time
          required: true
        }
      }
    ]
  },
  invitedUsers: {
    type: [String]  // Array of strings for usernames of invited users
  },
  recurring: {
    type: {
      frequency: {
        type: String,
        enum: ['daily', 'weekly', 'monthly', 'yearly']
      },
      interval: {
        type: Number,
        min: 1
      }
    }
  }
});

// Create the Event Model
const Event = mongoose.model('Event', eventSchema);

module.exports = Event;


===========================================
user.js: // user.js - Mongoose Schema for User Accounts

const mongoose = require('mongoose');
const { Schema } = mongoose;

// Define the User Schema
const userSchema = new Schema({
  username: {
    type: String,
    required: true,
    unique: true
  },
  email: {
    type: String,
    required: true,
    unique: true
  },
  password: {
    type: String,
    required: true
  }
});

// Create the User Model
const User = mongoose.model('User', userSchema);

module.exports = User;


===========================================




- server.js
- styles.css
- db.js
- index.html
- script.js
- event.js
- event.js
- event.js
- event.js
- user.js

"""

project_details = """
Project Overview: To-Do App
1. Project Setup
Initialize a new Node.js project with npm init.
Install necessary Node.js packages like express for your server and mongoose for interacting with MongoDB.
Set up a MongoDB database, either locally or using a cloud service like MongoDB Atlas.
2. Front-End Development (HTML, CSS, JS)
Design a simple and intuitive user interface using HTML and CSS.
Use JavaScript for dynamic interactions on the client side, like adding, completing, or removing tasks.
3. Back-End Development (Node.js, Express)
Create a RESTful API using Express. This API will handle requests like retrieving, adding, updating, and deleting tasks.
Ensure your API communicates with the MongoDB database to store and retrieve tasks.
4. Database Integration (MongoDB)
Design your MongoDB schema for the to-do tasks. Typically, this includes fields like task name, status, priority, and timestamps.
Use Mongoose, an Object Data Modeling (ODM) library for MongoDB and Node.js, to interact with the database.
5. Features to Include
Basic Features:
Add Tasks: Users should be able to add new tasks to their to-do list.
View Tasks: Display a list of tasks. You might include filters or sorting (by date, completed status, priority).
Mark as Complete: Users can mark tasks as complete or toggle them back to incomplete.
Delete Tasks: Allow users to delete tasks from the list.
Advanced Features:
Edit Tasks: Implement functionality to edit the details of a task.
User Authentication: Allow users to create accounts and save their to-do lists.
Due Dates and Reminders: Users can set due dates for tasks and receive reminders.
Prioritization: Ability to prioritize tasks, possibly using different colors or sorting.
Responsive Design: Ensure the app is usable on various devices and screen sizes.
Data Persistence: Tasks should be stored in the MongoDB database to persist between sessions.
"""

project_plan = """
Development Plan for ToDo Web-App

- Project Setup
  - Task 1: Initialize a new Node.js project with npm init.
  - Task 2: Install Node.js packages necessary for the project such as express for the server and mongoose for interacting with MongoDB.
  - Task 3: Set up a MongoDB database, either locally or using a cloud service like MongoDB Atlas, to store calendar events.

- Front-End Development
  - Task 4: Design a user interface using HTML and CSS for displaying a calendar view (monthly, weekly, daily).
  - Task 5: Use JavaScript for dynamic interactions on the client side, such as adding, editing, or removing calendar events, and switching between calendar views.

- Back-End Development
  - Task 6: Create a RESTful API using Express to handle requests like retrieving, adding, updating, and deleting calendar events.

- Database Integration
  - Task 7: Design MongoDB schema for calendar events, including fields like event title, description, start time, end time, and attendees.
  - Task 8: Use Mongoose to interact with the database, leveraging its capabilities to manage event data effectively.

- Features
  - Task 9: Implement functionality for setting reminders for events, which could be sent via email or shown as notifications.
  - Task 10: Implement user authentication by allowing users to create accounts to manage their personal calendars.
  - Task 11: Enable functionality for users to invite others to events, possibly integrating with email services.
  - Task 12: Support for creating events that recur daily, weekly, monthly, or yearly.
  - Task 13: Ensure the calendar app is usable across various devices and screen sizes by implementing responsive design.
  - Task 14: Implement data persistence by storing events in the MongoDB database to persist between sessions and be available across devices for logged-in users.
"""

if __name__ == "__main__":
    # core = Core(API)
    #
    # print("START...\n\n")
    # core.on_start()
    #
    # print("Description...\n\n")
    # core.on_description()
    #
    # print("Technologies...\n\n")
    # core.on_technologies()
    #
    # print("Tasks...\n\n")
    # core.on_tasks()
    #
    # print("Planing...\n\n")
    # core.on_planing()
    #
    # print("Project Structure...\n\n")
    # core.on_project_structure()
    #
    # print("Implementing Tasks..\n\n")
    # core.on_developing_tasks()
    #
    # print("Merge Files...\n\n")
    # core.on_merge_files()
    #
    # print("Generate Build File (build.sh)...\n\n")
    # core.generate_bash()
    #
    # project_files, project_plan, project_details = core.get_total_project()
    #
    # with open('code.txt', 'w', encoding="utf-8") as file:
    #     file.write(f"{project_details}\n{project_plan}\n\{project_files}n")




    modularity = Modularity("code.txt")
    modularity.init_module()
    modularity.project_summary()

    # print("Modularity Files HTML JS...\n\n")
    # core.on_modularity_html_js()
    #
    # print("Modularity...\n\n")
    # core.on_check_modularity()
    #
    # print("Summary...\n\n")
    # core.on_summary()



