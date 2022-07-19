// to display the inputted image

window.onload = function(){

    var imageFile = document.getElementById("inputImage");
    var imageDisplayArea = document.getElementById("org-img");

    imageFile.addEventListener('change', function(e){
        var file = imageFile.files[0];
        var imageType = /image.*/;

        if(file.type.match(imageType)){
            var reader = new FileReader();

            reader.onload = function(e) {
                imageDisplayArea.innerHTML = "";

                var img = new Image();
                img.src = reader.result;

                imageDisplayArea.appendChild(img);

                // to make the image container visible
                document.getElementById("img-container").classList.remove("hidden");

                img.classList.add("img-sizing");
            }

            reader.readAsDataURL(file);

        }else{

            imageDisplayArea.innerHTML = "File not supported!";

        }
    });

}


// to submit the input to backend and display results

$("#formData").on("submit", (e) => {
    e.preventDefault();
    var form_data = new FormData();
    var files = $('#inputImage')[0].files[0];
    form_data.append('file[]', files);

    $.ajax({
      url: 'http://127.0.0.1:5000/detect_cancer_type',
      type: 'POST',
      dataType: 'json', // what to expect back from server
      cache: false,
      contentType: false,
      processData: false,
      data: form_data,
      success: function (response) {
        document.getElementById("result").classList.remove("hidden");
        document.getElementById("result").innerHTML=response.data
      },

    }).catch(err => {
      console.log("error", err)
      alert(err)
    });
  });