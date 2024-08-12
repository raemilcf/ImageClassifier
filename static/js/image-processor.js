
$(function() {
    var INDEX = 0; 
    $("#uploadImageButton").click(function(e) {
  
      ///avoid page to reload
      e.preventDefault();

      //var fileInput = $("#imageUploader-input").files;
      const imageUploader = document.getElementById('imageUploader-input');
      const fileInput = imageUploader.files;
      
      if (fileInput.length === 0) {
        alert('Please select images to upload!');
        return;
      }

      const fileToUpload = new FormData();
      for (let i = 0; i < fileInput.length; i++) {
          fileToUpload.append('images', fileInput[i]);
      }


    
    
      uploadPdfFile(fileToUpload)
      $("#imageUploader-input").val('');
        
    })
    
   
    function uploadPdfFile(fileInput){
      // Use $.ajax with the style of $.get
      $.ajax({
        url: '/upload_images',  // Your Flask route
        type: 'POST',
        data: fileInput,
        processData: false,
        contentType: false
      })
      .done(function(data) {
        
        console.log(data);
        results = data;


        $("#imageUploaded").html('<img width="450" height="450" src="' + results[0] + '" />');

        if (results[2].includes('Cancer Detected') ){
          $("#resultImages").html('<img width="450" height="450" src="'+results[1]+'" class="img-fluid" alt="">');
        }
        $("#cancerText").html('<p style="font-size:16px">'+results[2]+' </p>')

       

        console.log(msgText);
        alert('Images uploaded successfully!');
        resultImages
      })
      .fail(function(error) {
        const msgText = "Failed to upload the file, try later!";//data.response; // Adjust based on your server response structure
        console.log('Error:', error);
      });
    }
    

  })