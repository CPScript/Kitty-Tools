readline = require('readline-sync');
const Kahoot = require("kahoot.js-latest");
var words = require('an-array-of-english-words')
const request = require('request');
var random = require('random-name')
var setTitle = require('console-title');
setTitle('flood.js');
var beep = require('beepbeep')

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getName() {
  ran = getRandomInt(1, 5)
  if (ran == 5) {
    request('https://apis.kahoot.it/namerator', function(error, response, body) {
      if (error) { console.log(error); }
      return JSON.parse(body).name
    });
  }
  if (ran == 4) {
    return words[getRandomInt(1, words.length)]
  }
  if (ran == 3) {
    return (random.first())
  }
  if (ran == 2) {
    return (random.first() + random.middle() + random.last())
  }
  if (ran == 1) {
    return (random.first() + random.last())
  }
}

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  while (0 !== currentIndex) {

    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

function getAnswerDelay() {
  const baseDelay = 7500; // Delay for promot - question time (DO NOT EDIT)
  const userDelay = answerdelay || 1500;
  const randomVariation = getRandomInt(-200, 500);
  
  const totalDelay = baseDelay + userDelay + randomVariation;
  return Math.max(1000, totalDelay);
}
function getAnswerCount(question) {
  try {
    if (question.type !== "quiz" && question.type !== "survey") {
      return 0;
    }
    
    if (question.numberOfAnswers && typeof question.numberOfAnswers === 'number') {
      return Math.max(1, Math.min(question.numberOfAnswers, 4));
    }
    
    if (question.quizQuestionAnswers && Array.isArray(question.quizQuestionAnswers) && 
        typeof question.questionIndex === 'number' && 
        question.questionIndex >= 0 && 
        question.questionIndex < question.quizQuestionAnswers.length &&
        question.quizQuestionAnswers[question.questionIndex] != null) {
      return Math.max(1, Math.min(question.quizQuestionAnswers[question.questionIndex], 4));
    }
    
    if (question.choices && Array.isArray(question.choices)) {
      return Math.max(1, Math.min(question.choices.length, 4));
    }
    
    if (question.answers && Array.isArray(question.answers)) {
      return Math.max(1, Math.min(question.answers.length, 4));
    }
    
    return 4;
  } catch (error) {
    console.log("Error getting answer count for " + question.type + ", using default of 4:", error.message);
    return 4;
  }
}

process.setMaxListeners(Number.POSITIVE_INFINITY)

function ads() {
  console.clear()
  console.log("==================================================")
  console.log("Made by ZaWarudo1")
  console.log("Enhancements by; CPScript")
  console.log("==================================================")
  console.log("My own version will be made soon with;\n")
  console.log("> Better answer handling")
  console.log("> Better error handling")
  console.log("> Better UI")
  console.log("==================================================\n")
}
ads()

antibotmode = readline.question('Use the new antibot mode? (y/n)> ');
if (antibotmode == "y") {
  console.log("NOTE: 2-factor brute forcing does not work with antibot.")
}

pin = readline.question('Enter Game PIN --> ');
bots = readline.question('Enter number of bots --> ');

answerdelay = readline.question('Answer delay in milliseconds (1-1000, recommended 500-2000) --> ');
if (answerdelay == "" || isNaN(answerdelay) || answerdelay < 1 || answerdelay > 10000) {
  answerdelay = 1500;
  console.log("Using default answer delay: 1500ms");
} else {
  answerdelay = parseInt(answerdelay);
  console.log("Answer delay set to: " + answerdelay + "ms");
}

if (antibotmode == "y") {
  ranname = true
  er = "n"
} else {
  ranname = readline.question('Use random name? (y/n) --> ');

  if (ranname == "y") {
    ranname = true
  } else {
    ranname = false
    botname = readline.question('Enter name --> ');
    botprefix = ""
  }
  er = readline.question('Use name bypass? (y/n) --> ');
}

usercontrolled = readline.question('Control the bots manually? (y/n) --> ');

if (usercontrolled == "y") {
  usercontrolled = true
  beepis = readline.question('Beep when the bots need controlling? (y/n) --> ');
} else {
  usercontrolled = false
  beepis = "n"
}

console.clear()

repeattimes = 0

function sendjoin(name, id) {
  if (ranname) {
    join(getName(), id)
  } else {
    join(name, id)
  }
}

function spam() {

  if (repeattimes == bots) {
    console.log("All join requests have finished.")
  } else {
    repeattimes++

    if (ranname) { rt = getRandomInt(90, 200) } else { rt = 15 }

    setTimeout(() => {
      spam()
    }, rt);
    setTimeout(() => {

      if (ranname) {
        sendjoin("This will become a random name!", bots - repeattimes - 1)
      } else {
        sendjoin(botname + (bots - repeattimes - 1), (bots - repeattimes - 1))
      }
    }, rt);
  }
}

process.setMaxListeners(Number.POSITIVE_INFINITY)

Arandomint = 0
todo = false
function join(name, idee) {
  while (name == undefined) {
    name = getName()
  }
  const client = new Kahoot();
  client.setMaxListeners(Number.POSITIVE_INFINITY)
  if (er == "y") {
    client.join(pin, name.replace(/a/g, 'ᗩ').replace(/b/g, 'ᗷ').replace(/c/g, 'ᑕ').replace(/d/g, 'ᗪ').replace(/e/g, 'E').replace(/f/g, 'ᖴ').replace(/g/g, 'G').replace(/h/g, 'ᕼ').replace(/i/g, 'I').replace(/j/g, 'ᒍ').replace(/k/g, 'K').replace(/l/g, 'ᒪ').replace(/m/g, 'ᗰ').replace(/n/g, 'ᑎ').replace(/o/g, 'O').replace(/p/g, 'ᑭ').replace(/q/g, 'ᑫ').replace(/r/g, 'ᖇ').replace(/s/g, 'ᔕ').replace(/t/g, 'T').replace(/u/g, 'ᑌ').replace(/v/g, 'ᐯ').replace(/w/g, 'ᗯ').replace(/x/g, '᙭').replace(/y/g, 'Y').replace(/z/g, 'ᘔ').replace(/A/g, 'ᗩ').replace(/B/g, 'ᗷ').replace(/C/g, 'ᑕ').replace(/D/g, 'ᗪ').replace(/E/g, 'E').replace(/F/g, 'ᖴ').replace(/G/g, 'G').replace(/H/g, 'ᕼ').replace(/I/g, 'I').replace(/J/g, 'ᒍ').replace(/K/g, 'K').replace(/L/g, 'ᒪ').replace(/M/g, 'ᗰ').replace(/N/g, 'ᑎ').replace(/O/g, 'O').replace(/P/g, 'ᑭ').replace(/Q/g, 'ᑫ').replace(/R/g, 'ᖇ').replace(/S/g, 'ᔕ').replace(/T/g, 'T').replace(/U/g, 'ᑌ').replace(/V/g, 'ᐯ').replace(/W/g, 'ᗯ').replace(/X/g, '᙭').replace(/Y/g, 'Y').replace(/Z/g, 'ᘔ'), [random.first(), random.last()]).catch(err => {
      if (err.description == "Duplicate name" & ranname) {
        sendjoin(name, idee)
      } else {
        console.log("Client " + idee + " failed to join with the error '" + err.description + "'")
        client.leave()
      }
    });
  } else {
    client.join(pin, name, [random.first(), random.last()]).catch(err => {
      if (err.description == "Duplicate name" & ranname) {
        sendjoin(name, idee)
      } else {
        console.log("Client " + idee + " failed to join with the error '" + err.description + "'")
        client.leave()
      }
    });
  }
  var list = [0, 1, 2, 3]
  todo = false
  client.on("Joined", info => {
    if (info.twoFactorAuth) {
      setInterval(() => {
        if (!todo == false) {
          client.answerTwoFactorAuth(todo)
        }
        shuffle(list)
        client.answerTwoFactorAuth(list)
      }, 1000);
    }
  });
  client.on("TwoFactorCorrect", function() {
    console.log(name + " Got 2-factor correct!")
    todo = list
  })

  client.on("QuestionReady", question => {
    try {
      if (idee == 1 & beepis == "y") {
        beep()
      }

      if (question.type !== "quiz" && question.type !== "survey" && question.type !== "word_cloud" && question.type !== "open_ended" && question.type !== "jumble") {
        console.log(name + " skipped question type: " + question.type + " (not supported)")
        return;
      }

      everyoneanswerthis = false
      
      if (question.type == "word_cloud") {
        if (usercontrolled) {
          if (idee == 1) {
            everyoneanswerthis = true
            answer = readline.question('type your answer> ');
            everyoneanswerthis = answer
            Arandomint = answer
            setTimeout(() => { client.answer(answer) }, getAnswerDelay());

          } else {
            var waittill = setInterval(() => {
              if (!everyoneanswerthis == false || !everyoneanswerthis == true) {
                clearInterval(waittill);
                setTimeout(() => {
                  client.answer(Arandomint)
                }, getAnswerDelay());
              }
            }, 100);
          }
        } else {
          console.log(name + " answered with 'kahootflood.weebly.com'")
          setTimeout(() => { client.answer("kahootflood.weebly.com") }, getAnswerDelay());
        }
      }

      if (question.type == "jumble") {
        console.log("User controlling is not currently available for jumbles. The bot " + name + " responded with a random answer.")
        const answerCount = getAnswerCount(question);
        if (answerCount > 0) {
          setTimeout(() => { client.answer(getRandomInt(0, answerCount - 1)) }, getAnswerDelay());
        } else {
          console.log(name + " skipped jumble question (no answer count available)")
        }
      }

      if (question.type == "quiz") {
        const answerCount = getAnswerCount(question);
        
        if (answerCount == 0) {
          console.log(name + " skipped quiz question (no answer count available)")
          return;
        }
        
        if (usercontrolled) {
          if (answerCount == 2) {
            if (idee == 1) {
              everyoneanswerthis = true
              answer = readline.question('t for triangle, d for diamond> ');
              answer = answer.replace('t', 1).replace('d', 2)
              everyoneanswerthis = answer
              Arandomint = answer
              setTimeout(() => { client.answer(answer - 1) }, getAnswerDelay());

            } else {
              var waittill = setInterval(() => {
                if (!everyoneanswerthis == false || !everyoneanswerthis == true) {
                  clearInterval(waittill);
                  setTimeout(() => {
                    client.answer(Arandomint - 1)
                  }, getAnswerDelay());
                }
              }, 100);
            }
          }

          if (answerCount == 3) {
            if (idee == 1) {
              everyoneanswerthis = true
              answer = readline.question('t for triangle, d for diamond, c for circle> ');
              answer = answer.replace('t', 1).replace('d', 2).replace('c', 3)
              everyoneanswerthis = answer
              Arandomint = answer
              setTimeout(() => { client.answer(answer - 1) }, getAnswerDelay());

            } else {
              var waittill = setInterval(() => {
                if (!everyoneanswerthis == false || !everyoneanswerthis == true) {
                  clearInterval(waittill);
                  setTimeout(() => {
                    client.answer(Arandomint - 1)
                  }, getAnswerDelay());
                }
              }, 100);
            }
          }

          if (answerCount == 4) {
            if (idee == 1) {
              everyoneanswerthis = true
              answer = readline.question('t for triangle, d for diamond, c for circle or s for square > ');
              answer = answer.replace('t', 1).replace('d', 2).replace('c', 3).replace('s', 4)
              everyoneanswerthis = answer
              Arandomint = answer
              setTimeout(() => { client.answer(answer - 1) }, getAnswerDelay());

            } else {
              var waittill = setInterval(() => {
                if (!everyoneanswerthis == false || !everyoneanswerthis == true) {
                  clearInterval(waittill);
                  setTimeout(() => {
                    client.answer(Arandomint - 1)
                  }, getAnswerDelay());
                }
              }, 100);
            }
          }
        } else {
          setTimeout(() => {
            try {
              toanswer = getRandomInt(0, answerCount - 1)
              console.log(name + " answered with option " + (toanswer + 1) + " after " + getAnswerDelay() + "ms delay")
              client.answer(toanswer)
            } catch (error) {
              console.log(name + " had an error answering: " + error.message)
            }
          }, getAnswerDelay());
        }
      }

      if (question.type == "survey") {
        const answerCount = getAnswerCount(question);
        
        if (answerCount == 0) {
          console.log(name + " skipped survey question (no answer count available)")
          return;
        }
        
        if (usercontrolled) {
          if (idee == 1) {
            everyoneanswerthis = true
            answer = readline.question('t for triangle, d for diamond, c for circle or s for square > ');
            answer = answer.replace('t', 1).replace('d', 2).replace('c', 3).replace('s', 4)
            everyoneanswerthis = answer
            Arandomint = answer
            setTimeout(() => { client.answer(answer - 1) }, getAnswerDelay());

          } else {
            var waittill = setInterval(() => {
              if (!everyoneanswerthis == false || !everyoneanswerthis == true) {
                clearInterval(waittill);
                setTimeout(() => {
                  client.answer(Arandomint - 1)
                }, getAnswerDelay());
              }
            }, 100);
          }
        } else {
          setTimeout(() => {
            try {
              toanswer = getRandomInt(0, answerCount - 1)
              console.log(name + " answered survey with option " + (toanswer + 1) + " after " + getAnswerDelay() + "ms delay")
              client.answer(toanswer)
            } catch (error) {
              console.log(name + " had an error answering: " + error.message)
            }
          }, getAnswerDelay());
        }
      }

      if (question.type == "open_ended") {
        if (usercontrolled) {
          if (idee == 1) {
            everyoneanswerthis = true
            answer = readline.question('type your answer> ');
            everyoneanswerthis = answer
            Arandomint = answer
            setTimeout(() => { client.answer(answer) }, getAnswerDelay());

          } else {
            var waittill = setInterval(() => {
              if (!everyoneanswerthis == false || !everyoneanswerthis == true) {
                clearInterval(waittill);
                setTimeout(() => {
                  client.answer(Arandomint)
                }, getAnswerDelay());
              }
            }, 100);
          }
        } else {
          console.log(name + " answered with 'kahootflood.weebly.com'")
          setTimeout(() => { client.answer("kahootflood.weebly.com") }, getAnswerDelay());
        }
      }
      
    } catch (error) {
      console.log(name + " had an error handling question: " + error.message)
    }
  });

  client.on("Disconnect", reason => {
    if (!reason == "Quiz Locked") {
      sendjoin(name, idee)
    }
  })

  client.on("QuestionEnd", data => {
    if (data.isCorrect) {
      console.log(name + " Got it correct!")
    } else {
      console.log(name + " Got it wrong.")
    }
  })
  client.on("QuizEnd", data => {
    console.log("The quiz has ended and " + name + " got rank " + data.rank)
  })
  process.on("SIGINT", function() {
    process.exit()
  });
}

console.clear()
console.log("Joining bots")
spam()
