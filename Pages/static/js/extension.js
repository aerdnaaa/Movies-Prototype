function send_message(url, data){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true)
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() { // Call a function when the state changes.
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        // Request finished. Do processing here.
        location.reload();
        }
    }
    xhr.send(JSON.stringify(data))
}

function select_all(main_checkbox) {        
    var list_of_checkboxes = document.getElementsByClassName("form-check-input");
    if (!main_checkbox.checked) {
      for (var index=1;index<list_of_checkboxes.length;index++){                    
        var checkbox = list_of_checkboxes[index];                    
        if (checkbox.checked){
          checkbox.checked = false
        }
      }
    }
    else {
      for (var index=1;index<list_of_checkboxes.length;index++){                    
        var checkbox = list_of_checkboxes[index];                    
        if (!checkbox.checked){
          checkbox.checked = true
        }
      }
    }
}  