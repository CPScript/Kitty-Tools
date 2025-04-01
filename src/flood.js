const requiredModules = [
    { name: 'readline-sync', varName: 'readline' },
    { name: 'kahoot.js-updated', varName: 'Kahoot' },
    { name: 'an-array-of-english-words', varName: 'words' },
    { name: 'request', varName: 'request' },
    { name: 'random-name', varName: 'random' },
    { name: 'console-title', varName: 'setTitle' },
    { name: 'beepbeep', varName: 'beep' }
];

// Object to store module references
const modules = {};

// Load required modules with error handling
console.log("Initializing Kahoot Flooder...");
try {
    for (const module of requiredModules) {
        try {
            console.log(`Loading ${module.name}...`);
            modules[module.varName] = require(module.name);
        } catch (error) {
            console.error(`Failed to load ${module.name}. Error: ${error.message}`);
            console.error("Please try reinstalling dependencies with 'npm install'");
            process.exit(1);
        }
    }
    
    // Extract modules for easier access
    const { readline, Kahoot, words, request, random, setTitle, beep } = modules;
    
    // Set console title
    console.log("Setting up console...");
    setTitle('Kahoot Flooder');
    
    // Utility functions
    function getRandomInt(min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    
    // Enhanced name generation with retry and validation
    function getName() {
        // Try to get a valid name up to 3 times
        for (let attempt = 0; attempt < 3; attempt++) {
            try {
                const ran = getRandomInt(1, 5);
                
                // Method 1: Kahoot namerator API
                if (ran === 5) {
                    // Use a synchronous method instead for consistency
                    // The API approach could cause issues since it's asynchronous
                    return `K_${random.first()}${getRandomInt(10, 99)}`;
                }
                
                // Method 2: Random word from dictionary
                if (ran === 4) {
                    const word = words[getRandomInt(0, words.length - 1)];
                    if (word && word.length > 0 && word.length <= 15) {
                        return word.charAt(0).toUpperCase() + word.slice(1);
                    }
                    // If word is invalid, try another method
                    continue;
                }
                
                // Method 3: Random first name
                if (ran === 3) {
                    return random.first();
                }
                
                // Method 4: Random full name
                if (ran === 2) {
                    return `${random.first()}${random.middle()}${random.last()}`.substring(0, 15);
                }
                
                // Method 5: Random first+last name
                if (ran === 1) {
                    return `${random.first()}${random.last()}`.substring(0, 15);
                }
            } catch (error) {
                console.log(`Name generation error: ${error.message}`);
                // If an error occurs, default to a basic name
                continue;
            }
        }
        
        // Fallback name if all attempts fail
        return `Bot${getRandomInt(100, 999)}`;
    }
    
    // Enhanced array shuffling
    function shuffle(array) {
        const newArray = [...array]; // Create a copy to avoid modifying the original
        for (let currentIndex = newArray.length - 1; currentIndex > 0; currentIndex--) {
            const randomIndex = Math.floor(Math.random() * (currentIndex + 1));
            [newArray[currentIndex], newArray[randomIndex]] = [newArray[randomIndex], newArray[currentIndex]];
        }
        return newArray;
    }
    
    // Allow more event listeners
    process.setMaxListeners(Number.POSITIVE_INFINITY);
    
    // UI and setup
    function displayHeader() {
        console.clear();
        console.log("------------------------------------");
        console.log("Kitty Tools, Kahoot flooder");
        console.log("Made by ImKTKota, reused by CPScript");
        console.log("Version 2.0 (Enhanced)");
        console.log("-------------------------------------\n");
        console.log("Use at your own risk!!!");
        console.log("_______________________________________");
        console.log("Answer the Following questions to begin");
    }
    
    // Display the header
    displayHeader();
    
    // Get user input for configuration
    const config = {
        antibotMode: readline.question('Use the new antibot mode? (y/n)> ').toLowerCase() === 'y',
        pin: readline.question('Enter game pin = '),
        bots: parseInt(readline.question('Enter number of bots = ')),
        ranname: true,
        userControlled: false,
        beepEnabled: false,
        nameBypass: false
    };
    
    // Additional configuration based on antibot mode
    if (!config.antibotMode) {
        config.ranname = readline.question('Use random generated name? (y/n)> ').toLowerCase() === 'y';
        
        if (!config.ranname) {
            config.botname = readline.question('Enter name = ');
            config.botprefix = "";
        }
        
        config.nameBypass = readline.question('Use name bypass? (y/n)> ').toLowerCase() === 'y';
    }
    
    // Bot control configuration
    config.userControlled = readline.question('Control the bots? (y/n)> ').toLowerCase() === 'y';
    
    if (config.userControlled) {
        config.beepEnabled = readline.question('Beep when the bots need controlling? (y/n)> ').toLowerCase() === 'y';
    }
    
    // Validate inputs
    if (!config.pin || isNaN(config.pin)) {
        console.error("Error: Game pin must be a number");
        process.exit(1);
    }
    
    if (isNaN(config.bots) || config.bots < 1 || config.bots > 500) {
        console.error("Error: Number of bots must be between 1 and 500");
        process.exit(1);
    }
    
    // Clear console before starting
    console.clear();
    
    // Tracking variables
    let repeattimes = 0;
    let connectedBots = 0;
    let activeBots = 0;
    let everyoneanswerthis = false;
    let Arandomint = 0;
    
    // Connection tracking for stats
    const connectionStatus = {
        total: config.bots,
        connected: 0,
        failed: 0,
        active: 0
    };
    
    // Enhanced join function with error handling
    function sendjoin(name, id) {
        let botName;
        
        if (config.ranname) {
            botName = getName();
            // Keep trying until we get a valid name
            while (!botName || botName.length === 0) {
                botName = getName();
            }
        } else {
            botName = `${config.botname}${id}`;
        }
        
        join(botName, id);
    }
    
    // Main function to manage bot creation
    function spam() {
        if (repeattimes >= config.bots) {
            console.log(`All ${config.bots} bots have been launched...`);
            console.log(`Successfully connected: ${connectionStatus.connected}`);
            console.log(`Failed to connect: ${connectionStatus.failed}`);
            
            // Display status update every 5 seconds
            setInterval(() => {
                console.log(`Status: ${connectionStatus.active}/${connectionStatus.connected} bots active`);
            }, 5000);
            
            return;
        }
        
        repeattimes++;
        
        // Randomized delay between bot spawns to avoid detection
        const spawnDelay = config.ranname ? getRandomInt(90, 200) : 15;
        
        setTimeout(() => {
            spam();
        }, spawnDelay);
        
        setTimeout(() => {
            const botId = config.bots - repeattimes;
            
            if (config.ranname) {
                sendjoin("This will become a random name!", botId);
            } else {
                sendjoin(`${config.botname}${botId}`, botId);
            }
        }, spawnDelay);
    }
    
    // Set max listeners to avoid warnings
    process.setMaxListeners(Number.POSITIVE_INFINITY);
    
    // Track bots for status reporting
    const activeBotMap = new Map();
    
    // Enhanced bot join and management
    function join(name, idee) {
        // Ensure name is valid
        while (!name || name.length === 0) {
            name = getName();
        }
        
        // Create Kahoot client instance with error handling
        const client = new Kahoot();
        client.setMaxListeners(Number.POSITIVE_INFINITY);
        
        // Function to log bot connection
        const logConnection = (success, error = null) => {
            if (success) {
                connectionStatus.connected++;
                connectionStatus.active++;
                activeBotMap.set(idee, client);
                console.log(`Bot ${idee} (${name}) connected successfully`);
            } else {
                connectionStatus.failed++;
                console.error(`Bot ${idee} (${name}) failed to connect: ${error || "Unknown error"}`);
            }
        };
        
        // Function to handle bot disconnection
        const handleDisconnect = (reason) => {
            connectionStatus.active--;
            activeBotMap.delete(idee);
            console.log(`Bot ${idee} (${name}) disconnected: ${reason}`);
            
            // Attempt to reconnect if not "Quiz Locked"
            if (reason !== "Quiz Locked" && connectionStatus.active < connectionStatus.total) {
                console.log(`Attempting to reconnect Bot ${idee}...`);
                setTimeout(() => {
                    sendjoin(name, idee);
                }, getRandomInt(1000, 3000));
            }
        };
        
        // Apply name bypass if enabled
        let joinName = name;
        if (config.nameBypass === true) {
            joinName = name.replace(/a/g, 'ᗩ').replace(/b/g, 'ᗷ').replace(/c/g, 'ᑕ')
                .replace(/d/g, 'ᗪ').replace(/e/g, 'E').replace(/f/g, 'ᖴ')
                .replace(/g/g, 'G').replace(/h/g, 'ᕼ').replace(/i/g, 'I')
                .replace(/j/g, 'ᒍ').replace(/k/g, 'K').replace(/l/g, 'ᒪ')
                .replace(/m/g, 'ᗰ').replace(/n/g, 'ᑎ').replace(/o/g, 'O')
                .replace(/p/g, 'ᑭ').replace(/q/g, 'ᑫ').replace(/r/g, 'ᖇ')
                .replace(/s/g, 'ᔕ').replace(/t/g, 'T').replace(/u/g, 'ᑌ')
                .replace(/v/g, 'ᐯ').replace(/w/g, 'ᗯ').replace(/x/g, '᙭')
                .replace(/y/g, 'Y').replace(/z/g, 'ᘔ')
                .replace(/A/g, 'ᗩ').replace(/B/g, 'ᗷ').replace(/C/g, 'ᑕ')
                .replace(/D/g, 'ᗪ').replace(/E/g, 'E').replace(/F/g, 'ᖴ')
                .replace(/G/g, 'G').replace(/H/g, 'ᕼ').replace(/I/g, 'I')
                .replace(/J/g, 'ᒍ').replace(/K/g, 'K').replace(/L/g, 'ᒪ')
                .replace(/M/g, 'ᗰ').replace(/N/g, 'ᑎ').replace(/O/g, 'O')
                .replace(/P/g, 'ᑭ').replace(/Q/g, 'ᑫ').replace(/R/g, 'ᖇ')
                .replace(/S/g, 'ᔕ').replace(/T/g, 'T').replace(/U/g, 'ᑌ')
                .replace(/V/g, 'ᐯ').replace(/W/g, 'ᗯ').replace(/X/g, '᙭')
                .replace(/Y/g, 'Y').replace(/Z/g, 'ᘔ');
        }
        
        // Team names for two-factor authentication
        const randomTeamNames = [random.first(), random.last()];
        
        // Actually join the game
        client.join(config.pin, joinName, randomTeamNames).then(() => {
            logConnection(true);
        }).catch(err => {
            if (err.description === "Duplicate name" && config.ranname) {
                // Try again with a different name
                sendjoin(getName(), idee);
            } else {
                logConnection(false, err.description);
                client.leave();
            }
        });
        
        // Set up for two-factor authentication
        const list = [0, 1, 2, 3];
        let todo = false;
        
        // Event handlers for the Kahoot client
        client.on("Joined", info => {
            if (info.twoFactorAuth) {
                // Handle two-factor auth by trying different combinations
                const twoFactorInterval = setInterval(() => {
                    if (todo !== false) {
                        client.answerTwoFactorAuth(todo);
                        clearInterval(twoFactorInterval);
                    } else {
                        const shuffledList = shuffle(list);
                        client.answerTwoFactorAuth(shuffledList);
                    }
                }, 1000);
            }
        });
        
        client.on("TwoFactorCorrect", function() {
            console.log(`${name} passed 2-factor authentication!`);
            todo = list;
        });
        
        // Handle question events
        client.on("QuestionReady", question => {
            if (idee === 0 && config.beepEnabled === "y") {
                beep();
            }
            
            // Reset the answer flag for everyone
            everyoneanswerthis = false;
            
            // Random delay before answering to appear more human-like
            const answerDelay = getRandomInt(1000, config.userControlled ? 3000 : 10000);
            
            // Handle different question types
            switch (question.type) {
                case "word_cloud":
                    handleWordCloudQuestion(client, name, idee, question, answerDelay);
                    break;
                
                case "jumble":
                    handleJumbleQuestion(client, name, idee, question, answerDelay);
                    break;
                
                case "quiz":
                    handleQuizQuestion(client, name, idee, question, answerDelay);
                    break;
                
                case "survey":
                    handleSurveyQuestion(client, name, idee, question, answerDelay);
                    break;
                
                case "open_ended":
                    handleOpenEndedQuestion(client, name, idee, question, answerDelay);
                    break;
                
                default:
                    console.log(`${name} received unknown question type: ${question.type}`);
                    // Try a random answer as fallback
                    setTimeout(() => {
                        try {
                            client.answer(getRandomInt(0, 3));
                        } catch (error) {
                            console.error(`Error answering question: ${error.message}`);
                        }
                    }, answerDelay);
            }
        });
        
        // Question type handlers
        function handleWordCloudQuestion(client, name, idee, question, delay) {
            if (config.userControlled) {
                if (idee === 0) {
                    everyoneanswerthis = true;
                    const answer = readline.question('Type your answer> ');
                    everyoneanswerthis = answer;
                    Arandomint = answer;
                    setTimeout(() => {
                        try {
                            client.answer(answer);
                        } catch (error) {
                            console.error(`Error answering word cloud: ${error.message}`);
                        }
                    }, delay);
                } else {
                    waitForLeaderAnswer(client, delay);
                }
            } else {
                console.log(`${name} answered with 'External Server 1.1.1.1'`);
                setTimeout(() => {
                    try {
                        client.answer("External Server");
                    } catch (error) {
                        console.error(`Error answering word cloud: ${error.message}`);
                    }
                }, delay);
            }
        }
        
        function handleJumbleQuestion(client, name, idee, question, delay) {
            console.log(`${name} received a jumble question. Answering randomly.`);
            setTimeout(() => {
                try {
                    // Get max possible answers
                    const maxAnswers = question.quizQuestionAnswers[question.questionIndex] || 4;
                    client.answer(getRandomInt(0, maxAnswers - 1));
                } catch (error) {
                    console.error(`Error answering jumble: ${error.message}`);
                }
            }, delay);
        }
        
        function handleQuizQuestion(client, name, idee, question, delay) {
            if (config.userControlled) {
                const choicesCount = question.quizQuestionAnswers[question.questionIndex] || 4;
                
                if (idee === 0) {
                    everyoneanswerthis = true;
                    let promptText = '';
                    
                    // Create appropriate prompt based on number of choices
                    if (choicesCount === 2) {
                        promptText = 't for triangle, d for diamond> ';
                    } else if (choicesCount === 3) {
                        promptText = 't for triangle, d for diamond, c for circle> ';
                    } else {
                        promptText = 't for triangle, d for diamond, c for circle or s for square > ';
                    }
                    
                    let answer = readline.question(promptText);
                    answer = answer.replace('t', 1).replace('d', 2).replace('c', 3).replace('s', 4);
                    
                    // Validate answer is within range
                    const numAnswer = parseInt(answer);
                    if (isNaN(numAnswer) || numAnswer < 1 || numAnswer > choicesCount) {
                        console.log(`Invalid answer, defaulting to 1`);
                        answer = 1;
                    }
                    
                    everyoneanswerthis = answer;
                    Arandomint = answer;
                    
                    setTimeout(() => {
                        try {
                            client.answer(answer - 1);
                        } catch (error) {
                            console.error(`Error answering quiz: ${error.message}`);
                        }
                    }, delay);
                } else {
                    waitForLeaderAnswer(client, delay);
                }
            } else {
                setTimeout(() => {
                    try {
                        const maxAnswers = question.quizQuestionAnswers[question.questionIndex] || 4;
                        const toanswer = getRandomInt(0, maxAnswers - 1);
                        console.log(`${name} answered with a random answer (${toanswer + 1})`);
                        client.answer(toanswer);
                    } catch (error) {
                        console.error(`Error answering quiz: ${error.message}`);
                    }
                }, delay);
            }
        }
        
        function handleSurveyQuestion(client, name, idee, question, delay) {
            if (config.userControlled) {
                if (idee === 0) {
                    everyoneanswerthis = true;
                    let answer = readline.question('t for triangle, d for diamond, c for circle or s for square > ');
                    answer = answer.replace('t', 1).replace('d', 2).replace('c', 3).replace('s', 4);
                    everyoneanswerthis = answer;
                    Arandomint = answer;
                    
                    setTimeout(() => {
                        try {
                            client.answer(answer - 1);
                        } catch (error) {
                            console.error(`Error answering survey: ${error.message}`);
                        }
                    }, delay);
                } else {
                    waitForLeaderAnswer(client, delay);
                }
            } else {
                setTimeout(() => {
                    try {
                        const maxAnswers = question.quizQuestionAnswers[question.questionIndex] || 4;
                        const toanswer = getRandomInt(0, maxAnswers - 1);
                        console.log(`${name} answered with a random answer (${toanswer + 1})`);
                        client.answer(toanswer);
                    } catch (error) {
                        console.error(`Error answering survey: ${error.message}`);
                    }
                }, delay);
            }
        }
        
        function handleOpenEndedQuestion(client, name, idee, question, delay) {
            if (config.userControlled) {
                if (idee === 0) {
                    everyoneanswerthis = true;
                    const answer = readline.question('Type your answer> ');
                    everyoneanswerthis = answer;
                    Arandomint = answer;
                    
                    setTimeout(() => {
                        try {
                            client.answer(answer);
                        } catch (error) {
                            console.error(`Error answering open-ended: ${error.message}`);
                        }
                    }, delay);
                } else {
                    waitForLeaderAnswer(client, delay);
                }
            } else {
                console.log(`${name} answered with 'External Server'`);
                setTimeout(() => {
                    try {
                        client.answer("External Server");
                    } catch (error) {
                        console.error(`Error answering open-ended: ${error.message}`);
                    }
                }, delay);
            }
        }
        
        // Wait for the leader's answer and then respond accordingly
        function waitForLeaderAnswer(client, delay) {
            const waittill = setInterval(() => {
                if (everyoneanswerthis !== false && everyoneanswerthis !== true) {
                    clearInterval(waittill);
                    
                    setTimeout(() => {
                        try {
                            // If the answer needs to be a number index, subtract 1
                            if (typeof Arandomint === 'number' || !isNaN(parseInt(Arandomint))) {
                                client.answer(parseInt(Arandomint) - 1);
                            } else {
                                client.answer(Arandomint);
                            }
                        } catch (error) {
                            console.error(`Error answering after leader: ${error.message}`);
                        }
                    }, delay);
                }
            }, 100);
            
            // Clear interval after timeout to prevent memory leaks
            setTimeout(() => {
                clearInterval(waittill);
            }, 30000);
        }
        
        // Handle disconnection
        client.on("Disconnect", reason => {
            handleDisconnect(reason);
        });
        
        // Handle question end events
        client.on("QuestionEnd", data => {
            if (data.isCorrect) {
                console.log(`${name} got it correct! Score: ${data.points || 0}`);
            } else {
                console.log(`${name} got it wrong. Correct answer was: ${data.correctAnswers.join(", ") || "Unknown"}`);
            }
        });
        
        // Handle quiz end
        client.on("QuizEnd", data => {
            console.log(`The quiz has ended and ${name} got rank ${data.rank}`);
            handleDisconnect("Quiz Ended");
        });
        
        // Cleanup on exit
        process.on("SIGINT", function() {
            console.log("Shutting down bots...");
            client.leave();
            process.exit();
        });
    }
    
    // Start the flooding
    console.clear();
    console.log(`Starting to join ${config.bots} bots to game pin: ${config.pin}`);
    console.log(`Anti-Bot Mode: ${config.antibotMode ? "Enabled" : "Disabled"}`);
    console.log(`User Control: ${config.userControlled ? "Enabled" : "Disabled"}`);
    console.log("Please wait while bots connect...");
    
    // Begin the spam process
    spam();
    
} catch (error) {
    console.error(`Fatal error: ${error.message}`);
    console.error(error.stack);
    process.exit(1);
}
