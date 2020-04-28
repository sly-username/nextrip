const input = document.querySelector('input');

input.addEventListener('input', updateValue);


function updateValue(e) {
  return fetch('/autocomplete.py', {
      method: 'POST', 
      body: JSON.stringify(data)
    }).then(res => {
      console.log("Request complete! response:", res);
    });
  }