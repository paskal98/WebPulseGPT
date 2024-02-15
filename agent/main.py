import os
import re

import requests
from openai import OpenAI

from agent.JS_parser import parse_ast_conditionally, find_function_by_name, \
    find_arrow_function_by_name, find_event_listeners_by_variable, parse_code_with_esprima_server, find_callbacks
from agent.core import Core
from agent.implemented_parser import parse_file_contents

core = Core()

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

code2 = """
document.addEventListener("DOMContentLoaded", function () {
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
    
    const abc = () => { 
        return 1 + 1; 
    }
    
    app.use(session({
        secret: "secret",
        resave: "false",
        saveUninitialized: "false"
    }));

    addTaskBtn.addEventListener("click", function () {
        const taskName = taskInput.value;
        if (taskName) {
            const newTask = document.createElement("li");
            newTask.innerText = taskName;
            taskList.appendChild(newTask);
            taskInput.value = "";
            setupTaskActions(newTask);
        }
        
        function setupTaskActions(taskItem) {
            taskItem.addEventListener("click", function () {
                taskItem.classList.toggle("completed");
            });
    
            taskItem.addEventListener("contextmenu", function (e) {
                e.preventDefault();
                taskItem.remove();
            });
        }
        
        
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
    
});

"""

code7 = '''


function setupTaskActions(taskItem) {
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

    function asd(taskItem) {
        taskItem.addEventListener("click", function () {
            taskItem.classList.toggle("completed");
        });

        taskItem.addEventListener("contextmenu", function (e) {
            e.preventDefault();
            taskItem.remove();
        });
    }
}
'''

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
mongoose.connect("mongodb://localhost/todo-app", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

// Define User schema and model
// ... (User schema and model setup)

// Passport local strategy setup
passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

// Authentication routes
app.post("/register", async (req, res) => {
    try {
        const { username, password } = req.body;
        const user = new User({ username });
        const registeredUser = await User.register(user, password);
        res.status(201).json(registeredUser);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

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




if __name__ == "__main__":
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
    # print("Merge...\n\n")
    # core.on_merge_updates()
    #
    # # print("Modularity...\n\n")
    # # core.on_check_modularity()
    #
    # print("Summary...\n\n")
    # core.on_summary()
    #
    # print("Generate Build File (build.sh)...\n\n")
    # core.generate_bash()



    # defined_v_f = parse_ast_conditionally(ast10)
    # print(defined_v_f)
    # print()



    # function_name = "setupTaskActions"
    # out = find_function_by_name(code4, function_name)
    # print(out)

    # arrow = "addTask"
    # out_arrow = find_arrow_function_by_name(code, arrow)
    # print(out_arrow)

    # print(find_event_listeners_by_variable(code4, "app"))



    # ast = parse_code_with_esprima_server(code7)
    #
    # defined_v_f = parse_ast_conditionally(ast)
    # print(defined_v_f)
    # print()

    ast = parse_code_with_esprima_server(server)
    defined_v_f = find_callbacks(ast)
    print(defined_v_f)
    print()