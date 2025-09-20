// Enhanced Kahoot Flooder with improved error handling and module loading
console.log("Initializing Kahoot Flooder - Enhanced Version...");

// Required modules with error handling and fallbacks
const requiredModules = [
    { name: 'readline-sync', varName: 'readline' },
    { name: 'kahoot.js-updated', varName: 'Kahoot', fallback: 'kahoot.js' },
    { name: 'an-array-of-english-words', varName: 'words' },
    { name: 'request', varName: 'request' },
    { name: 'random-name', varName: 'random' },
    { name: 'console-title', varName: 'setTitle' },
    { name: 'beepbeep', varName: 'beep' }
];

// Object to store module references
const modules = {};
let initializationSuccess = true;

// Enhanced module loading with better error handling and fallbacks
function loadRequiredModules() {
    console.log("Loading required Node.js modules...");
    
    for (const module of requiredModules) {
        try {
            console.log(`Loading ${module.name}...`);
            modules[module.varName] = require(module.name);
            console.log(`Successfully loaded ${module.name}`);
        } catch (error) {
            console.error(`ERROR: Failed to load ${module.name}`);
            console.error(`Error details: ${error.message}`);
            
            // Try fallback if available
            if (module.fallback) {
                try {
                    console.log(`Trying fallback module: ${module.fallback}...`);
                    modules[module.varName] = require(module.fallback);
                    console.log(`Successfully loaded fallback module: ${module.fallback}`);
                    continue;
                } catch (fallbackError) {
                    console.error(`Fallback also failed: ${fallbackError.message}`);
                }
            }
            
            console.error("");
            console.error("SOLUTION:");
            console.error(`Run: npm install ${module.name}`);
            if (module.fallback) {
                console.error(`Or try: npm install ${module.fallback}`);
            }
            console.error("Or run: npm install (to install all dependencies)");
            console.error("");
            console.error("If the error persists:");
            console.error("1. Delete node_modules folder");
            console.error("2. Delete package-lock.json file");  
            console.error("3. Run: npm cache clean --force");
            console.error("4. Run: npm install --force");
            console.error("");
            initializationSuccess = false;
        }
    }
    
    if (!initializationSuccess) {
        console.error("MODULE LOADING FAILED!");
        console.error("Cannot proceed without required modules.");
        console.error("");
        console.error("QUICK FIX ATTEMPT:");
        console.error("Try running these commands in the terminal:");
        console.error("cd " + __dirname);
        console.error("rm -rf node_modules package-lock.json");
        console.error("npm cache clean --force");
        console.error("npm install --force");
        console.error("");
        console.error("Then run the flooder again.");
        process.exit(1);
    }
    
    console.log("All modules loaded successfully!");
    return true;
}

// Load modules and verify
if (!loadRequiredModules()) {
    process.exit(1);
}

// Extract modules for easier access
const { readline, Kahoot, words, request, random, setTitle, beep } = modules;

// Verify critical modules are functional
try {
    console.log("Verifying module functionality...");
    
    // Test readline-sync
    if (typeof readline.question !== 'function') {
        throw new Error("readline-sync module is not functioning correctly");
    }
    
    // Test Kahoot
    if (typeof Kahoot !== 'function') {
        throw new Error("kahoot.js-updated module is not functioning correctly");
    }
    
    // Test words array
    if (!Array.isArray(words) || words.length === 0) {
        throw new Error("an-array-of-english-words module is not functioning correctly");
    }
    
    // Test random name generator
    if (typeof random.first !== 'function') {
        throw new Error("random-name module is not functioning correctly");
    }
    
    console.log("Module functionality verification completed successfully!");
    
} catch (error) {
    console.error("MODULE FUNCTIONALITY TEST FAILED:");
    console.error(error.message);
    console.error("");
    console.error("Please try reinstalling the modules:");
    console.error("npm install --force");
    process.exit(1);
}

// Set console title
try {
    setTitle('Kahoot Flooder - Enhanced');
    console.log("Console title set successfully");
} catch (error) {
    console.log("Warning: Could not set console title, but continuing...");
}

// Enhanced utility functions
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Enhanced name generation with better error handling and validation
function getName() {
    const maxAttempts = 5;
    
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
        try {
            const method = getRandomInt(1, 5);
            let name = null;
            
            switch (method) {
                case 1:
                    // Random first + last name
                    name = `${random.first()}${random.last()}`;
                    break;
                    
                case 2:
                    // Random first + middle + last name
                    name = `${random.first()}${random.middle()}${random.last()}`;
                    break;
                    
                case 3:
                    // Random first name only
                    name = random.first();
                    break;
                    
                case 4:
                    // Random word from dictionary
                    if (words && words.length > 0) {
                        const word = words[getRandomInt(0, words.length - 1)];
                        if (word && word.length > 0 && word.length <= 15) {
                            name = word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
                        }
                    }
                    break;
                    
                case 5:
                    // Kahoot-style name with prefix
                    name = `Bot${random.first()}${getRandomInt(10, 99)}`;
                    break;
            }
            
            // Validate and clean the name
            if (name && typeof name === 'string' && name.trim().length > 0) {
                // Clean the name: remove special characters, limit length
                name = name.replace(/[^a-zA-Z0-9]/g, '').substring(0, 15);
                
                if (name.length >= 2) {
                    return name;
                }
            }
            
        } catch (error) {
            console.log(`Name generation attempt ${attempt + 1} failed: ${error.message}`);
        }
    }
    
    // Fallback name if all attempts fail
    const fallbackName = `Bot${getRandomInt(100, 999)}`;
    console.log(`Using fallback name: ${fallbackName}`);
    return fallbackName;
}

// Enhanced array shuffling with validation
function shuffle(array) {
    if (!Array.isArray(array) || array.length === 0) {
        console.error("Invalid array provided to shuffle function");
        return [0, 1, 2, 3]; // Return default array
    }
    
    const newArray = [...array]; // Create a copy to avoid modifying the original
    
    for (let currentIndex = newArray.length - 1; currentIndex > 0; currentIndex--) {
        const randomIndex = Math.floor(Math.random() * (currentIndex + 1));
        [newArray[currentIndex], newArray[randomIndex]] = [newArray[randomIndex], newArray[currentIndex]];
    }
    
    return newArray;
}

// Set up process listeners
process.setMaxListeners(Number.POSITIVE_INFINITY);

// Enhanced error handling for unhandled exceptions
process.on('uncaughtException', (error) => {
    console.error('UNCAUGHT EXCEPTION:', error.message);
    console.error('Stack trace:', error.stack);
    console.error('The flooder will attempt to continue...');
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('UNHANDLED REJECTION at:', promise);
    console.error('Reason:', reason);
    console.error('The flooder will attempt to continue...');
});

// UI and setup functions
function displayHeader() {
    console.clear();
    console.log("====================================");
    console.log("Kitty Tools - Enhanced Kahoot Flooder");
    console.log("Made by ImKTKota, Enhanced by CPScript");
    console.log("Version 2.1 (Enhanced with Error Handling)");
    console.log("====================================");
    console.log("");
    console.log("Use at your own risk!");
    console.log("This tool is for educational purposes only.");
    console.log("____________________________________");
    console.log("");
    console.log("Answer the following questions to begin:");
    console.log("");
}

// Display the header
displayHeader();

// Enhanced configuration with validation
function getValidatedInput(prompt, validator, errorMessage) {
    let attempts = 0;
    const maxAttempts = 3;
    
    while (attempts < maxAttempts) {
        try {
            const input = readline.question(prompt);
            
            if (validator(input)) {
                return input;
            } else {
                console.log(errorMessage);
                attempts++;
                
                if (attempts >= maxAttempts) {
                    console.log("Too many invalid attempts. Using default value.");
                    return null;
                }
            }
        } catch (error) {
            console.error(`Input error: ${error.message}`);
            attempts++;
        }
    }
    
    return null;
}

// Get user input for configuration with enhanced validation
try {
    const config = {};
    
    // Anti-bot mode
    const antibotInput = getValidatedInput(
        'Use the new antibot mode? (y/n)> ',
        (input) => input.toLowerCase() === 'y' || input.toLowerCase() === 'n',
        'Please enter "y" for yes or "n" for no.'
    );
    config.antibotMode = antibotInput ? antibotInput.toLowerCase() === 'y' : false;
    
    // Game PIN
    const pinInput = getValidatedInput(
        'Enter game pin = ',
        (input) => /^\d{3,8}$/.test(input),
        'Game PIN must be a number between 3-8 digits.'
    );
    
    if (!pinInput) {
        console.error("Invalid game PIN provided. Exiting.");
        process.exit(1);
    }
    config.pin = pinInput;
    
    // Number of bots
    const botsInput = getValidatedInput(
        'Enter number of bots (1-100) = ',
        (input) => {
            const num = parseInt(input);
            return !isNaN(num) && num >= 1 && num <= 100;
        },
        'Number of bots must be between 1 and 100.'
    );
    
    if (!botsInput) {
        console.log("Using default: 10 bots");
        config.bots = 10;
    } else {
        config.bots = parseInt(botsInput);
    }
    
    // Additional configuration based on antibot mode
    if (!config.antibotMode) {
        const rannameInput = getValidatedInput(
            'Use random generated names? (y/n)> ',
            (input) => input.toLowerCase() === 'y' || input.toLowerCase() === 'n',
            'Please enter "y" for yes or "n" for no.'
        );
        config.ranname = rannameInput ? rannameInput.toLowerCase() === 'y' : true;
        
        if (!config.ranname) {
            config.botname = readline.question('Enter bot name prefix = ') || 'Bot';
        }
        
        const bypassInput = getValidatedInput(
            'Use name bypass? (y/n)> ',
            (input) => input.toLowerCase() === 'y' || input.toLowerCase() === 'n',
            'Please enter "y" for yes or "n" for no.'
        );
        config.nameBypass = bypassInput ? bypassInput.toLowerCase() === 'y' : false;
    } else {
        config.ranname = true;
        config.nameBypass = false;
    }
    
    // Bot control configuration
    const controlInput = getValidatedInput(
        'Control the bots manually? (y/n)> ',
        (input) => input.toLowerCase() === 'y' || input.toLowerCase() === 'n',
        'Please enter "y" for yes or "n" for no.'
    );
    config.userControlled = controlInput ? controlInput.toLowerCase() === 'y' : false;
    
    if (config.userControlled) {
        const beepInput = getValidatedInput(
            'Beep when the bots need controlling? (y/n)> ',
            (input) => input.toLowerCase() === 'y' || input.toLowerCase() === 'n',
            'Please enter "y" for yes or "n" for no.'
        );
        config.beepEnabled = beepInput ? beepInput.toLowerCase() === 'y' : false;
    } else {
        config.beepEnabled = false;
    }
    
    console.log("");
    console.log("Configuration Summary:");
    console.log("=====================");
    console.log(`Game PIN: ${config.pin}`);
    console.log(`Number of bots: ${config.bots}`);
    console.log(`Anti-bot mode: ${config.antibotMode ? 'Enabled' : 'Disabled'}`);
    console.log(`Random names: ${config.ranname ? 'Enabled' : 'Disabled'}`);
    console.log(`Name bypass: ${config.nameBypass ? 'Enabled' : 'Disabled'}`);
    console.log(`User control: ${config.userControlled ? 'Enabled' : 'Disabled'}`);
    console.log(`Beep notifications: ${config.beepEnabled ? 'Enabled' : 'Disabled'}`);
    console.log("");
    
    const confirmInput = getValidatedInput(
        'Start flooder with these settings? (y/n)> ',
        (input) => input.toLowerCase() === 'y' || input.toLowerCase() === 'n',
        'Please enter "y" to start or "n" to cancel.'
    );
    
    if (!confirmInput || confirmInput.toLowerCase() !== 'y') {
        console.log("Flooder cancelled by user.");
        process.exit(0);
    }
    
} catch (error) {
    console.error(`Configuration error: ${error.message}`);
    console.error("Using default configuration...");
    
    // Default configuration
    config = {
        antibotMode: false,
        pin: '123456',
        bots: 10,
        ranname: true,
        nameBypass: false,
        userControlled: false,
        beepEnabled: false
    };
}

// Clear console before starting
console.clear();

// Tracking variables with enhanced monitoring
let repeattimes = 0;
let connectedBots = 0;
let activeBots = 0;
let everyoneanswerthis = false;
let Arandomint = 0;

// Enhanced connection tracking for detailed stats
const connectionStatus = {
    total: config.bots,
    connected: 0,
    failed: 0,
    active: 0,
    disconnected: 0,
    errors: []
};

// Enhanced status reporting
function reportStatus() {
    console.log(`\n[STATUS] Connected: ${connectionStatus.connected}/${connectionStatus.total} | Active: ${connectionStatus.active} | Failed: ${connectionStatus.failed}`);
    
    if (connectionStatus.errors.length > 0) {
        console.log(`[ERRORS] Recent: ${connectionStatus.errors.slice(-3).join(', ')}`);
    }
}

// Enhanced join function with better error handling
function sendjoin(name, id) {
    let botName;
    
    if (config.ranname) {
        botName = getName();
        // Ensure we have a valid name
        let attempts = 0;
        while ((!botName || botName.length === 0) && attempts < 3) {
            botName = getName();
            attempts++;
        }
        
        if (!botName || botName.length === 0) {
            botName = `FallbackBot${id}`;
        }
    } else {
        botName = `${config.botname}${id}`;
    }
    
    join(botName, id);
}

// Enhanced spam function with better timing and error handling
function spam() {
    if (repeattimes >= config.bots) {
        console.log(`\nAll ${config.bots} bots have been launched.`);
        reportStatus();
        
        // Set up periodic status reporting
        setInterval(() => {
            if (connectionStatus.active > 0) {
                reportStatus();
            }
        }, 10000); // Report every 10 seconds
        
        return;
    }
    
    repeattimes++;
    
    // Enhanced timing to avoid rate limiting
    const baseDelay = config.ranname ? getRandomInt(100, 300) : 50;
    const additionalDelay = Math.floor(repeattimes / 10) * 100; // Slow down as more bots are added
    const totalDelay = baseDelay + additionalDelay;
    
    setTimeout(() => {
        spam();
    }, totalDelay);
    
    setTimeout(() => {
        const botId = config.bots - repeattimes;
        
        try {
            if (config.ranname) {
                sendjoin("This will become a random name!", botId);
            } else {
                sendjoin(`${config.botname}${botId}`, botId);
            }
        } catch (error) {
            console.error(`Error launching bot ${botId}: ${error.message}`);
            connectionStatus.failed++;
            connectionStatus.errors.push(`Bot${botId}: ${error.message}`);
        }
    }, totalDelay);
}

// Set max listeners to avoid warnings
process.setMaxListeners(Number.POSITIVE_INFINITY);

// Enhanced bot tracking
const activeBotMap = new Map();

// Enhanced bot join and management with comprehensive error handling
function join(name, idee) {
    // Validate inputs
    if (!name || typeof name !== 'string' || name.trim().length === 0) {
        console.error(`Invalid name for bot ${idee}, generating new name...`);
        name = getName();
    }
    
    if (typeof idee !== 'number' || idee < 0) {
        console.error(`Invalid bot ID: ${idee}`);
        return;
    }
    
    // Ensure name is clean and valid
    name = name.trim().substring(0, 15);
    
    // Create Kahoot client instance with enhanced error handling
    let client;
    try {
        client = new Kahoot();
        client.setMaxListeners(Number.POSITIVE_INFINITY);
    } catch (error) {
        console.error(`Failed to create Kahoot client for bot ${idee}: ${error.message}`);
        connectionStatus.failed++;
        return;
    }
    
    // Enhanced logging functions
    const logConnection = (success, error = null) => {
        if (success) {
            connectionStatus.connected++;
            connectionStatus.active++;
            activeBotMap.set(idee, client);
            console.log(`[BOT ${idee}] ${name} connected successfully (${connectionStatus.connected}/${connectionStatus.total})`);
        } else {
            connectionStatus.failed++;
            const errorMsg = error || "Unknown error";
            console.error(`[BOT ${idee}] ${name} failed to connect: ${errorMsg}`);
            connectionStatus.errors.push(`${name}: ${errorMsg}`);
        }
    };
    
    // Enhanced disconnect handling
    const handleDisconnect = (reason) => {
        connectionStatus.active--;
        connectionStatus.disconnected++;
        activeBotMap.delete(idee);
        console.log(`[BOT ${idee}] ${name} disconnected: ${reason}`);
        
        // Attempt to reconnect if appropriate
        if (reason !== "Quiz Locked" && reason !== "Quiz Ended" && connectionStatus.active < connectionStatus.total * 0.8) {
            console.log(`[BOT ${idee}] Attempting to reconnect ${name}...`);
            setTimeout(() => {
                try {
                    sendjoin(name, idee);
                } catch (error) {
                    console.error(`[BOT ${idee}] Reconnection failed: ${error.message}`);
                }
            }, getRandomInt(2000, 5000));
        }
    };
    
    // Apply name bypass if enabled
    let joinName = name;
    if (config.nameBypass) {
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
    
    // Generate team names for two-factor authentication
    const randomTeamNames = [random.first(), random.last()];
    
    // Actually join the game with enhanced error handling
    client.join(config.pin, joinName, randomTeamNames).then(() => {
        logConnection(true);
    }).catch(err => {
        const errorDescription = err.description || err.message || 'Unknown error';
        
        if (errorDescription === "Duplicate name" && config.ranname) {
            // Try again with a different name
            console.log(`[BOT ${idee}] Duplicate name "${name}", trying different name...`);
            setTimeout(() => {
                sendjoin(getName(), idee);
            }, getRandomInt(500, 1500));
        } else {
            logConnection(false, errorDescription);
            try {
                client.leave();
            } catch (leaveError) {
                // Ignore leave errors
            }
        }
    });
    
    // Set up for two-factor authentication with enhanced handling
    const list = [0, 1, 2, 3];
    let todo = false;
    
    // Event handlers for the Kahoot client with enhanced error handling
    client.on("Joined", info => {
        try {
            if (info.twoFactorAuth) {
                console.log(`[BOT ${idee}] ${name} requires 2-factor authentication`);
                
                const twoFactorInterval = setInterval(() => {
                    try {
                        if (todo !== false) {
                            client.answerTwoFactorAuth(todo);
                            clearInterval(twoFactorInterval);
                        } else {
                            const shuffledList = shuffle(list);
                            client.answerTwoFactorAuth(shuffledList);
                        }
                    } catch (error) {
                        console.error(`[BOT ${idee}] 2-factor auth error: ${error.message}`);
                        clearInterval(twoFactorInterval);
                    }
                }, 1000);
                
                // Clear interval after timeout to prevent memory leaks
                setTimeout(() => {
                    clearInterval(twoFactorInterval);
                }, 30000);
            }
        } catch (error) {
            console.error(`[BOT ${idee}] Join event error: ${error.message}`);
        }
    });
    
    client.on("TwoFactorCorrect", function() {
        console.log(`[BOT ${idee}] ${name} passed 2-factor authentication!`);
        todo = list;
    });
    
    // Enhanced question handling with better error handling
    client.on("QuestionReady", question => {
        try {
            if (idee === 0 && config.beepEnabled) {
                try {
                    beep();
                } catch (beepError) {
                    // Ignore beep errors
                }
            }
            
            // Reset the answer flag for everyone
            everyoneanswerthis = false;
            
            // Enhanced random delay to appear more human-like
            const baseDelay = getRandomInt(1000, 3000);
            const userDelay = config.userControlled ? getRandomInt(2000, 5000) : 0;
            const answerDelay = baseDelay + userDelay;
            
            // Handle different question types with enhanced error handling
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
                    console.log(`[BOT ${idee}] ${name} received unknown question type: ${question.type}`);
                    // Try a random answer as fallback
                    setTimeout(() => {
                        try {
                            client.answer(getRandomInt(0, 3));
                        } catch (error) {
                            console.error(`[BOT ${idee}] Error answering unknown question: ${error.message}`);
                        }
                    }, answerDelay);
            }
        } catch (error) {
            console.error(`[BOT ${idee}] Question ready error: ${error.message}`);
        }
    });
    
    // Enhanced question type handlers with better error handling
    function handleWordCloudQuestion(client, name, idee, question, delay) {
        try {
            if (config.userControlled) {
                if (idee === 0) {
                    everyoneanswerthis = true;
                    const answer = readline.question('[WORD CLOUD] Type your answer> ');
                    everyoneanswerthis = answer;
                    Arandomint = answer;
                    setTimeout(() => {
                        try {
                            client.answer(answer);
                        } catch (error) {
                            console.error(`[BOT ${idee}] Error answering word cloud: ${error.message}`);
                        }
                    }, delay);
                } else {
                    waitForLeaderAnswer(client, name, idee, delay);
                }
            } else {
                console.log(`[BOT ${idee}] ${name} answered word cloud with 'BotResponse'`);
                setTimeout(() => {
                    try {
                        client.answer("BotResponse");
                    } catch (error) {
                        console.error(`[BOT ${idee}] Error answering word cloud: ${error.message}`);
                    }
                }, delay);
            }
        } catch (error) {
            console.error(`[BOT ${idee}] Word cloud handler error: ${error.message}`);
        }
    }
    
    function handleJumbleQuestion(client, name, idee, question, delay) {
        try {
            console.log(`[BOT ${idee}] ${name} answering jumble question randomly`);
            setTimeout(() => {
                try {
                    const maxAnswers = (question.quizQuestionAnswers && question.quizQuestionAnswers[question.questionIndex]) || 4;
                    client.answer(getRandomInt(0, maxAnswers - 1));
                } catch (error) {
                    console.error(`[BOT ${idee}] Error answering jumble: ${error.message}`);
                }
            }, delay);
        } catch (error) {
            console.error(`[BOT ${idee}] Jumble handler error: ${error.message}`);
        }
    }
    
    function handleQuizQuestion(client, name, idee, question, delay) {
        try {
            if (config.userControlled) {
                const choicesCount = (question.quizQuestionAnswers && question.quizQuestionAnswers[question.questionIndex]) || 4;
                
                if (idee === 0) {
                    everyoneanswerthis = true;
                    let promptText = '';
                    
                    if (choicesCount === 2) {
                        promptText = '[QUIZ] t for triangle, d for diamond> ';
                    } else if (choicesCount === 3) {
                        promptText = '[QUIZ] t for triangle, d for diamond, c for circle> ';
                    } else {
                        promptText = '[QUIZ] t for triangle, d for diamond, c for circle, s for square> ';
                    }
                    
                    let answer = readline.question(promptText);
                    answer = answer.replace('t', '1').replace('d', '2').replace('c', '3').replace('s', '4');
                    
                    const numAnswer = parseInt(answer);
                    if (isNaN(numAnswer) || numAnswer < 1 || numAnswer > choicesCount) {
                        console.log(`[BOT ${idee}] Invalid answer, defaulting to 1`);
                        answer = '1';
                    }
                    
                    everyoneanswerthis = answer;
                    Arandomint = answer;
                    
                    setTimeout(() => {
                        try {
                            client.answer(parseInt(answer) - 1);
                        } catch (error) {
                            console.error(`[BOT ${idee}] Error answering quiz: ${error.message}`);
                        }
                    }, delay);
                } else {
                    waitForLeaderAnswer(client, name, idee, delay);
                }
            } else {
                setTimeout(() => {
                    try {
                        const maxAnswers = (question.quizQuestionAnswers && question.quizQuestionAnswers[question.questionIndex]) || 4;
                        const answer = getRandomInt(0, maxAnswers - 1);
                        console.log(`[BOT ${idee}] ${name} answered quiz randomly (option ${answer + 1})`);
                        client.answer(answer);
                    } catch (error) {
                        console.error(`[BOT ${idee}] Error answering quiz: ${error.message}`);
                    }
                }, delay);
            }
        } catch (error) {
            console.error(`[BOT ${idee}] Quiz handler error: ${error.message}`);
        }
    }
    
    function handleSurveyQuestion(client, name, idee, question, delay) {
        try {
            if (config.userControlled) {
                if (idee === 0) {
                    everyoneanswerthis = true;
                    let answer = readline.question('[SURVEY] t for triangle, d for diamond, c for circle, s for square> ');
                    answer = answer.replace('t', '1').replace('d', '2').replace('c', '3').replace('s', '4');
                    everyoneanswerthis = answer;
                    Arandomint = answer;
                    
                    setTimeout(() => {
                        try {
                            client.answer(parseInt(answer) - 1);
                        } catch (error) {
                            console.error(`[BOT ${idee}] Error answering survey: ${error.message}`);
                        }
                    }, delay);
                } else {
                    waitForLeaderAnswer(client, name, idee, delay);
                }
            } else {
                setTimeout(() => {
                    try {
                        const maxAnswers = (question.quizQuestionAnswers && question.quizQuestionAnswers[question.questionIndex]) || 4;
                        const answer = getRandomInt(0, maxAnswers - 1);
                        console.log(`[BOT ${idee}] ${name} answered survey randomly (option ${answer + 1})`);
                        client.answer(answer);
                    } catch (error) {
                        console.error(`[BOT ${idee}] Error answering survey: ${error.message}`);
                    }
                }, delay);
            }
        } catch (error) {
            console.error(`[BOT ${idee}] Survey handler error: ${error.message}`);
        }
    }
    
    function handleOpenEndedQuestion(client, name, idee, question, delay) {
        try {
            if (config.userControlled) {
                if (idee === 0) {
                    everyoneanswerthis = true;
                    const answer = readline.question('[OPEN ENDED] Type your answer> ');
                    everyoneanswerthis = answer;
                    Arandomint = answer;
                    
                    setTimeout(() => {
                        try {
                            client.answer(answer);
                        } catch (error) {
                            console.error(`[BOT ${idee}] Error answering open-ended: ${error.message}`);
                        }
                    }, delay);
                } else {
                    waitForLeaderAnswer(client, name, idee, delay);
                }
            } else {
                console.log(`[BOT ${idee}] ${name} answered open-ended with 'Bot Response'`);
                setTimeout(() => {
                    try {
                        client.answer("Bot Response");
                    } catch (error) {
                        console.error(`[BOT ${idee}] Error answering open-ended: ${error.message}`);
                    }
                }, delay);
            }
        } catch (error) {
            console.error(`[BOT ${idee}] Open-ended handler error: ${error.message}`);
        }
    }
    
    // Enhanced leader answer waiting with timeout
    function waitForLeaderAnswer(client, name, idee, delay) {
        const startTime = Date.now();
        const timeout = 30000; // 30 second timeout
        
        const waitInterval = setInterval(() => {
            try {
                if (everyoneanswerthis !== false && everyoneanswerthis !== true) {
                    clearInterval(waitInterval);
                    
                    setTimeout(() => {
                        try {
                            if (typeof Arandomint === 'number' || !isNaN(parseInt(Arandomint))) {
                                client.answer(parseInt(Arandomint) - 1);
                            } else {
                                client.answer(Arandomint);
                            }
                        } catch (error) {
                            console.error(`[BOT ${idee}] Error following leader answer: ${error.message}`);
                        }
                    }, delay);
                } else if (Date.now() - startTime > timeout) {
                    clearInterval(waitInterval);
                    console.log(`[BOT ${idee}] ${name} timeout waiting for leader, answering randomly`);
                    
                    setTimeout(() => {
                        try {
                            client.answer(getRandomInt(0, 3));
                        } catch (error) {
                            console.error(`[BOT ${idee}] Error with timeout answer: ${error.message}`);
                        }
                    }, delay);
                }
            } catch (error) {
                console.error(`[BOT ${idee}] Wait interval error: ${error.message}`);
                clearInterval(waitInterval);
            }
        }, 100);
    }
    
    // Enhanced event handlers with error handling
    client.on("Disconnect", reason => {
        try {
            handleDisconnect(reason);
        } catch (error) {
            console.error(`[BOT ${idee}] Disconnect handler error: ${error.message}`);
        }
    });
    
    client.on("QuestionEnd", data => {
        try {
            if (data.isCorrect) {
                console.log(`[BOT ${idee}] ${name} got it correct! Score: ${data.points || 0}`);
            } else {
                const correctAnswers = data.correctAnswers ? data.correctAnswers.join(", ") : "Unknown";
                console.log(`[BOT ${idee}] ${name} got it wrong. Correct answer: ${correctAnswers}`);
            }
        } catch (error) {
            console.error(`[BOT ${idee}] Question end handler error: ${error.message}`);
        }
    });
    
    client.on("QuizEnd", data => {
        try {
            console.log(`[BOT ${idee}] Quiz ended - ${name} got rank ${data.rank || 'Unknown'}`);
            handleDisconnect("Quiz Ended");
        } catch (error) {
            console.error(`[BOT ${idee}] Quiz end handler error: ${error.message}`);
        }
    });
    
    // Enhanced cleanup on exit
    process.on("SIGINT", function() {
        console.log("\nShutting down bots gracefully...");
        try {
            client.leave();
        } catch (error) {
            // Ignore leave errors during shutdown
        }
        process.exit(0);
    });
}

// Start the flooding process with enhanced logging
console.clear();
console.log(`Starting to join ${config.bots} bots to game PIN: ${config.pin}`);
console.log(`Configuration:`);
console.log(`- Anti-Bot Mode: ${config.antibotMode ? 'Enabled' : 'Disabled'}`);
console.log(`- Random Names: ${config.ranname ? 'Enabled' : 'Disabled'}`);
console.log(`- Name Bypass: ${config.nameBypass ? 'Enabled' : 'Disabled'}`);
console.log(`- User Control: ${config.userControlled ? 'Enabled' : 'Disabled'}`);
console.log(`- Beep Notifications: ${config.beepEnabled ? 'Enabled' : 'Disabled'}`);
console.log("");
console.log("Please wait while bots connect...");
console.log("Press Ctrl+C to stop the flooder.");
console.log("");

// Begin the spam process
try {
    spam();
} catch (error) {
    console.error(`Failed to start flooder: ${error.message}`);
    console.error("Please check your configuration and try again.");
    process.exit(1);
}

// Enhanced status monitoring
setInterval(() => {
    if (connectionStatus.total > 0) {
        const connectedPercent = Math.round((connectionStatus.connected / connectionStatus.total) * 100);
        const activePercent = Math.round((connectionStatus.active / connectionStatus.total) * 100);
        
        if (connectionStatus.connected > 0 || connectionStatus.failed > 0) {
            console.log(`[MONITOR] Connected: ${connectedPercent}% (${connectionStatus.connected}/${connectionStatus.total}) | Active: ${activePercent}% (${connectionStatus.active}) | Failed: ${connectionStatus.failed}`);
        }
    }
}, 15000); // Monitor every 15 seconds

console.log("Kahoot Flooder started successfully!");
