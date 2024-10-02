// Variables to store user data and roles/questions
let users = [];
const adminUsername = 'admin';
const adminPassword = 'password';
let editedUserIndex = null;
let roleSelected = '';
let currentQuestionIndex = 0;

const rolesQuestions = {
    "Developer": [
        "Explain a challenging project you've worked on.",
        "How do you approach debugging code?",
        "What is your favorite programming language and why?"
    ],
    "Data Scientist": [
        "Explain a data analysis project you've worked on.",
        "What is your experience with machine learning?",
        "How do you handle missing data in a dataset?"
    ],
    "Project Manager": [
        "Describe your approach to managing a project.",
        "How do you handle team conflicts?",
        "What methodologies do you prefer for project management?"
    ],
    "QA": [
        "Explain a challenging project you've worked on.",
        "How do you approach debugging code?",
        "What is your favorite programming language and why?"
    ],
    "UI designer": [
        "Explain a challenging project you've worked on.",
        "How do you approach debugging code?",
        "What is your favorite programming language and why?"
    ],
    "ML Engineer": [
        "Explain a challenging project you've worked on.",
        "How do you approach debugging code?",
        "What is your favorite programming language and why?"
    ],
    "HR": [
        "Explain a challenging project you've worked on.",
        "What are the roles you interviewed the candidates?",
        "What is your favorite question you would like to ask and why?"
    ],
    "Intern": [
        "Explain a challenging project you've worked on.",
        "How do you approach debugging code?",
        "What is your favorite programming language and why?"
    ]
};

// Add a default admin user
users.push({ username: adminUsername, password: adminPassword });

// Function to display the login page
function showLoginPage() {
    document.getElementById('login-container').style.display = 'block';
    document.getElementById('signup-container').style.display = 'none';
    document.getElementById('signin-success-container').style.display = 'none';
    document.getElementById('admin-panel-container').style.display = 'none';
    document.getElementById('questions-container').style.display = 'none';
    document.getElementById('edit-user-container').style.display = 'none';
}

// Show login page on page load
showLoginPage();

// Function to handle user login
document.getElementById('login-button').addEventListener('click', () => {
    const username = document.getElementById('username-login').value;
    const password = document.getElementById('password-login').value;

    if (username === adminUsername && password === adminPassword) {
        showAdminPanel();
    } else {
        const user = users.find(user => user.username === username && user.password === password);
        if (user) {
            document.getElementById('login-container').style.display = 'none';
            document.getElementById('signin-success-container').style.display = 'block';
        } else {
            alert('Invalid username or password');
        }
    }
});

// Function to handle user registration
document.getElementById('register-button').addEventListener('click', () => {
    const username = document.getElementById('username-register').value;
    const password = document.getElementById('password-register').value;
    const confirmPassword = document.getElementById('password-confirm').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    users.push({ username, password });
    showLoginPage();
});

// Function to show admin panel
function showAdminPanel() {
    document.getElementById('admin-panel-container').style.display = 'block';
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('signin-success-container').style.display = 'none';
    populateUserTable();
}

// Logout buttons
document.getElementById('logout-button').addEventListener('click', showLoginPage);
document.getElementById('admin-logout-button').addEventListener('click', showLoginPage);
document.getElementById('logout-button-questions').addEventListener('click', showLoginPage);

// Redirect to sign-up page
document.getElementById('signup-redirect').addEventListener('click', () => {
    document.getElementById('signup-container').style.display = 'block';
    document.getElementById('login-container').style.display = 'none';
});

// Handle role selection and start interview
document.getElementById('start-interview').addEventListener('click', () => {
    roleSelected = document.getElementById('role-selection').value;
    currentQuestionIndex = 0;
    startInterviewProcess();
});

// Populate the user table in admin panel
function populateUserTable() {
    const userTable = document.getElementById('user-list');
    userTable.innerHTML = '';
    users.forEach((user, index) => {
        const row = `<tr>
            <td>${user.username}</td>
            <td>${user.password}</td>
            <td>
                <button onclick="editUser(${index})">Edit</button>
                <button onclick="removeUser(${index})">Remove</button>
            </td>
        </tr>`;
        userTable.innerHTML += row;
    });
}

// Edit user function
function editUser(index) {
    editedUserIndex = index;
    document.getElementById('edit-username').value = users[index].username;
    document.getElementById('edit-password').value = users[index].password;
    document.getElementById('edit-user-container').style.display = 'block';
    document.getElementById('admin-panel-container').style.display = 'none';
}

// Remove user function
function removeUser(index) {
    users.splice(index, 1);
    populateUserTable();
}

// Save edited user changes
document.getElementById('save-changes-button').addEventListener('click', () => {
    const username = document.getElementById('edit-username').value;
    const password = document.getElementById('edit-password').value;
    users[editedUserIndex] = { username, password };
    showAdminPanel();
});

// Cancel editing
document.getElementById('cancel-edit-button').addEventListener('click', showAdminPanel);

// Start interview process with questions
function startInterviewProcess() {
    document.getElementById('signin-success-container').style.display = 'none';
    document.getElementById('questions-container').style.display = 'block';
    showQuestion();
}

// Display question and timers
function showQuestion() {
    const questions = rolesQuestions[roleSelected];
    if (currentQuestionIndex >= questions.length) {
        alert("You've completed the interview. Thank you!");
        showLoginPage();
        return;
    }

    document.getElementById('question-text').textContent = `Question ${currentQuestionIndex + 1}: ${questions[currentQuestionIndex]}`;
    startPrepTimer();
}

// Handle preparation time timer
function startPrepTimer() {
    let prepTime = 30;
    document.getElementById('prep-time').textContent = prepTime;
    const prepInterval = setInterval(() => {
        prepTime--;
        document.getElementById('prep-time').textContent = prepTime;
        if (prepTime <= 0) {
            clearInterval(prepInterval);
            startRecording();
        }
    }, 1000);
}

// Start recording time and capture video
function startRecording() {
    let recordTime = 120;
    document.getElementById('record-time').textContent = recordTime;
    document.getElementById('start-recording-button').disabled = false;
    document.getElementById('stop-recording-button').disabled = false;

    const recordInterval = setInterval(() => {
        recordTime--;
        document.getElementById('record-time').textContent = recordTime;
        if (recordTime <= 0) {
            clearInterval(recordInterval);
            stopRecording();
        }
    }, 1000);

    // Start recording button click
    document.getElementById('start-recording-button').addEventListener('click', () => {
        startVideoCapture();
        document.getElementById('start-recording-button').disabled = true;
    });

    // Stop recording button click
    document.getElementById('stop-recording-button').addEventListener('click', () => {
        stopVideoCapture();
        document.getElementById('mark-done-button').disabled = false;
        clearInterval(recordInterval);
    });

    // Mark recording as done and move to next question
    document.getElementById('mark-done-button').addEventListener('click', () => {
        currentQuestionIndex++;
        showQuestion();
    });
}

// Video capture variables
let mediaRecorder;
let recordedBlobs;

// Start video capture function
async function startVideoCapture() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    document.getElementById('video-preview').srcObject = stream;

    const options = { mimeType: 'video/webm;codecs=vp9' };
    recordedBlobs = [];
    mediaRecorder = new MediaRecorder(stream, options);
    mediaRecorder.ondataavailable = event => recordedBlobs.push(event.data);
    mediaRecorder.start();
}

// Stop video capture function
function stopVideoCapture() {
    mediaRecorder.stop();
    document.getElementById('video-preview').srcObject.getTracks().forEach(track => track.stop());
}

// Function to stop recording
function stopRecording() {
    document.getElementById('stop-recording-button').disabled = true;
}
