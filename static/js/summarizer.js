// function to get text 

$(function() {
  var INDEX = 0; 
  $("#summaryButton").click(function(e) {

    ///avoid page to reload
    e.preventDefault();
    //get full text 
    var userInput = $("#fullText").val(); 
    if(userInput.trim() == ''){
      return false;
    }

    var minWords = $("#minWords").val(); 
 
    var maxWords = $("#maxWords").val(); 
   

    //generate response from bot
    getSummary(userInput,minWords,maxWords )

    //clean input bar
    $("#chat-input").val('');
  })
 
  
  function getSummary(rawText,minWords,maxWords) {
    // Bot Response
    $.get("/get", { fullText: rawText , minWords: minWords,maxWords: maxWords}).done(function (data) {
      const summary = data;
      $("#summaryText").val(summary)
    });
  }
  

})