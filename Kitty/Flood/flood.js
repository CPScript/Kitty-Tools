console.log("Loading...")
//requires
readline = require('readline-sync');
console.log("Connecting to Kahoot")
const Kahoot = require("kahoot.js-updated");
console.log("Downloading requirements...")
var words = require('an-array-of-english-words')
console.log("Scraping Proxies...")
const request = require('request');
console.log("Required request...")
var random = require('random-name')
console.log("Getting Random Names...")
var setTitle = require('console-title');
console.log("Console ready...")
setTitle('Flooder');
var beep = require('beepbeep')
console.log("Required beepbeep")

//stuff
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getName(){
    ran=getRandomInt(1,5)
    if(ran==5){
        request('https://apis.kahoot.it/namerator', function (error, response, body) {
        if (error) { console.log(error); }
            return JSON.parse(body).name
        });
    }
    if(ran==4){
        return words[getRandomInt(1,words.length)]
    }
    if(ran==3){
        return(random.first())
    }
    if(ran==2){
        return (random.first()+random.middle()+random.last())
    }
    if(ran==1){
        return (random.first()+random.last())
    }
}
function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
  
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
  
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
  
      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
  
    return array;
  }
  
process.setMaxListeners(Number.POSITIVE_INFINITY)

//ok lets go baby
function ads() {
    console.clear()
    console.log("------------------------------------")
    console.log("Kitty Tools, Kahoot flooder")
    console.log("Made by ImKTKota, reused by CPScript")
    console.log("Version 1.4")
    console.log("-------------------------------------\n")
    console.log("Use at your own risk!!!")
    console.log("_______________________________________")
 
    console.log("Answer the Following questions to begin")
}
ads()

//QUESTIONS TO START FLOODING
antibotmode=readline.question('Use the new antibot mode?  (y/n)> ');
if(antibotmode=="y"){
    console.log("NOTE: I do not take responsibilty or anything done with this bot")
}

pin = readline.question('Enter game pin = ');
bots = readline.question('Enter number of bots = ');
if(antibotmode=="y"){
    ranname=true
    er="n"
}else{
ranname = readline.question('Use random generated name? (y/n)> ');

if (ranname=="y"){
    ranname=true
}else{
    ranname=false
    botname = readline.question('Enter name = ');
    botprefix = ""
}
er = readline.question('Use name bypass? (y/n)> ');
}

usercontrolled = readline.question('Control the bots? (y/n)> ');

if (usercontrolled=="y"){
    usercontrolled =true
    beepis= readline.question('Beep when the bots need controlling? (y/n)> ');
}else{
    usercontrolled =false
    beepis="n"
}



//END QUESTIONS YAY
console.clear()

repeattimes=0

function sendjoin(name,id) {
    if(ranname){    
        join(getName(),id)
    }else{
        join(name,id)
    }
}

function spam() {
    
      if(repeattimes==bots){
        console.log("All bots have connected...")
      }else{
        repeattimes++

        if(ranname){rt=getRandomInt(90,200)}else{rt=15}

        setTimeout(() => {
            spam()
        }, rt);
        setTimeout(() => {
            
            if(ranname){
                sendjoin("This will become a random name!",bots-repeattimes-1)
            }else{
                sendjoin(botname+(bots-repeattimes-1),(bots-repeattimes-1))
            }
        }, rt);
      }
}

process.setMaxListeners(Number.POSITIVE_INFINITY)

Arandomint = 0
todo=false
function join(name,idee) {
    while (name==undefined) {
        name=getName()
    }
    const client = new Kahoot();
    client.setMaxListeners(Number.POSITIVE_INFINITY)
        if(er=="y"){
            client.join(pin, name.replace(/a/g, 'ᗩ').replace(/b/g, 'ᗷ').replace(/c/g, 'ᑕ').replace(/d/g, 'ᗪ').replace(/e/g, 'E').replace(/f/g, 'ᖴ').replace(/g/g, 'G').replace(/h/g, 'ᕼ').replace(/i/g, 'I').replace(/j/g, 'ᒍ').replace(/k/g, 'K').replace(/l/g, 'ᒪ').replace(/m/g, 'ᗰ').replace(/n/g, 'ᑎ').replace(/o/g, 'O').replace(/p/g, 'ᑭ').replace(/q/g, 'ᑫ').replace(/r/g, 'ᖇ').replace(/s/g, 'ᔕ').replace(/t/g, 'T').replace(/u/g, 'ᑌ').replace(/v/g, 'ᐯ').replace(/w/g, 'ᗯ').replace(/x/g, '᙭').replace(/y/g, 'Y').replace(/z/g, 'ᘔ').replace(/A/g, 'ᗩ').replace(/B/g, 'ᗷ').replace(/C/g, 'ᑕ').replace(/D/g, 'ᗪ').replace(/E/g, 'E').replace(/F/g, 'ᖴ').replace(/G/g, 'G').replace(/H/g, 'ᕼ').replace(/I/g, 'I').replace(/J/g, 'ᒍ').replace(/K/g, 'K').replace(/L/g, 'ᒪ').replace(/M/g, 'ᗰ').replace(/N/g, 'ᑎ').replace(/O/g, 'O').replace(/P/g, 'ᑭ').replace(/Q/g, 'ᑫ').replace(/R/g, 'ᖇ').replace(/S/g, 'ᔕ').replace(/T/g, 'T').replace(/U/g, 'ᑌ').replace(/V/g, 'ᐯ').replace(/W/g, 'ᗯ').replace(/X/g, '᙭').replace(/Y/g, 'Y').replace(/Z/g, 'ᘔ'),[random.first(),random.last()]).catch(err=>{
                if(err.description=="Duplicate name"&ranname){
                    sendjoin(name,idee)
                }else{
                    console.log("Client "+idee+" failed to join with the error '"+err.description+"'")
                    client.leave()
                }
            });
        }else{
            client.join(pin, name,[random.first(),random.last()]).catch(err=>{
                if(err.description=="Duplicate name"&ranname){
                    sendjoin(name,idee)
                }else{
                    console.log("Client "+idee+" failed to join with the error '"+err.description+"'")
                    client.leave()
                }
            });
        }
    var list=[0,1,2,3]
    todo=false
    client.on("Joined", info => {
        if (info.twoFactorAuth){
            setInterval(() => {
                if(!todo==false){
                    client.answerTwoFactorAuth(todo)
                }
                shuffle(list)
                client.answerTwoFactorAuth(list)
            }, 1000);
        }
    });
    client.on("TwoFactorCorrect", function () {
        console.log(name+" Got 2-factor correct!")
        todo=list
    })

    client.on("QuestionReady", question => {
        if (idee==1&beepis=="y"){
            beep()
        }

        everyoneanswerthis=false
        if (question.type == "word_cloud") {
            if(usercontrolled){

                if (idee==1){
                    everyoneanswerthis=true
                    answer = readline.question('type your answer> ');
                    everyoneanswerthis=answer
                    Arandomint=answer
                    setTimeout(() => {client.answer(answer-1)},getRandomInt(1,20000));

                }else{
                    var waittill=setInterval(() => {
                        if (!everyoneanswerthis==false || !everyoneanswerthis==true){
                            clearInterval(waittill);
                            setTimeout(() => {
                                client.answer(Arandomint)
                            },getRandomInt(1,20000));
                        }
                    }, 100);
                   
                }
            }else{
                console.log(name+" answered with 'External Server 1.1.1.1'")
                setTimeout(() => {client.answer("External Server")},getRandomInt(1,20000));
            }
        }

        if (question.type == "jumble") {
            console.log("User controlling is not currently available for jumbles. The bot "+name+" responded with a random generated answer.")
            setTimeout(() => {client.answer(getRandomInt(0,question.quizQuestionAnswers[question.questionIndex]-1))},getRandomInt(1,20000));
        }

        if (question.type == "quiz") {
            if(usercontrolled){
                if(question.quizQuestionAnswers[question.questionIndex]==2){

                    
                    if (idee==1){
                        everyoneanswerthis=true
                        answer = readline.question('t for triangle, d for diamond> ');
                        answer = answer.replace('t', 1).replace('d', 2)
                        everyoneanswerthis=answer
                        Arandomint=answer
                        setTimeout(() => {client.answer(answer-1)},getRandomInt(1,20000));

                    }else{
                        var waittill=setInterval(() => {
                            if (!everyoneanswerthis==false || !everyoneanswerthis==true){
                                clearInterval(waittill);
                                setTimeout(() => {
                                    client.answer(Arandomint-1)
                                },getRandomInt(1,20000));
                            }
                        }, 100);
                       
                    }


                }



                if(question.quizQuestionAnswers[question.questionIndex]==3){

                    if (idee==1){
                        everyoneanswerthis=true
                        answer = readline.question('t for triangle, d for diamond, c for circle> ');
                        answer = answer.replace('t', 1).replace('d', 2).replace('c', 3)
                        everyoneanswerthis=answer
                        Arandomint=answer
                        setTimeout(() => {client.answer(answer-1)},getRandomInt(1,20000));

                    }else{
                        var waittill=setInterval(() => {
                            if (!everyoneanswerthis==false || !everyoneanswerthis==true){
                                clearInterval(waittill);
                                setTimeout(() => {
                                    client.answer(Arandomint-1)
                                },getRandomInt(1,20000));
                            }
                        }, 100);
                       
                    }
                }



                if(question.quizQuestionAnswers[question.questionIndex]==4){

                    if (idee==1){
                        everyoneanswerthis=true
                        answer = readline.question('t for triangle, d for diamond, c for circle or s for square > ');
                        answer = answer.replace('t', 1).replace('d', 2).replace('c', 3).replace('s', 4)
                        everyoneanswerthis=answer
                        Arandomint=answer
                        setTimeout(() => {client.answer(answer-1)},getRandomInt(1,20000));

                    }else{
                        var waittill=setInterval(() => {
                            if (!everyoneanswerthis==false || !everyoneanswerthis==true){
                                clearInterval(waittill);
                                setTimeout(() => {
                                    client.answer(Arandomint-1)
                                },getRandomInt(1,20000));
                            }
                        }, 100);
                       
                    }


                }
            }else{


              
                setTimeout(() => {
                    toanswer=getRandomInt(0,question.quizQuestionAnswers[question.questionIndex]-1)
                    console.log(name+" answered with a random answer.")
                    client.answer(toanswer)
                },getRandomInt(1,20000));
                
            }
        } 


        if (question.type == "survey") {
            if(usercontrolled){
                if (idee==1){
                    everyoneanswerthis=true
                    answer = readline.question('t for triangle, d for diamond, c for circle or s for square > ');
                    answer = answer.replace('t', 1).replace('d', 2).replace('c', 3).replace('s', 4)
                    everyoneanswerthis=answer
                    Arandomint=answer
                    setTimeout(() => {client.answer(answer-1)},getRandomInt(1,20000));

                }else{
                    var waittill=setInterval(() => {
                        if (!everyoneanswerthis==false || !everyoneanswerthis==true){
                            clearInterval(waittill);
                            setTimeout(() => {
                                client.answer(Arandomint-1)
                            },getRandomInt(1,20000));
                        }
                    }, 100);
                   
                }
                
            }else{
                setTimeout(() => {
                    toanswer=getRandomInt(0,question.quizQuestionAnswers[question.questionIndex]-1)
                    console.log(name+" answered with a random answer.")
                    client.answer(toanswer)
                },getRandomInt(1,20000));
            }
        } 

        if (question.type == "open_ended") {
            if(usercontrolled){
                if (idee==1){
                    everyoneanswerthis=true
                    answer = readline.question('type your answer> ');
                    everyoneanswerthis=answer
                    Arandomint=answer
                    setTimeout(() => {client.answer(answer-1)},getRandomInt(1,20000));

                }else{
                    var waittill=setInterval(() => {
                        if (!everyoneanswerthis==false || !everyoneanswerthis==true){
                            clearInterval(waittill);
                            setTimeout(() => {
                                client.answer(Arandomint)
                            },getRandomInt(1,20000));
                        }
                    }, 100);
                   
                }
            }else{
                console.log(name+" answered with 'External Server'")
                setTimeout(() => {client.answer("External Server")},getRandomInt(1,20000));
            }
        }


    });

    //ON DISCONNECT
    client.on("Disconnect", reason => {
        if(!reason=="Quiz Locked"){
            sendjoin(name,idee)
        }
    })

    client.on("QuestionEnd", data => {
        if (data.isCorrect){
            console.log(name+ "Got it correct, Yay!")
        }else{
            console.log(name+" Got it wrong, Darn ")
        }
    })
    client.on("QuizEnd", data => {
        console.log("The quiz has ended and "+name+" got rank "+data.rank)
    })
    process.on("SIGINT", function () {
        process.exit()
    });
}

//INITIATE OF THE SPAM SPAM
console.clear()
console.log("Joining bots")
spam()//YAY WE DID IT
