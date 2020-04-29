function update(name) {
    form = document.getElementById('nameid')
    form.caller.value = name;
    form.submit();
}

function chociesGenerate() {
   var date = new Date(), dateArray = new Array(), i;
   curYear = date.getFullYear();
    for(i = 0; i<5; i++) {
        dateArray[i] = curYear+i;
    }
    return dateArray;
}

function addOption(divname) {
    var newDiv=document.createElement('div');
    var html = '<select>', choices = choicesGenerate(), i;
    for(i = 0; i < choices.length; i++) {
        html += "<option value='"+choices[i]+"</option>";
    }
    html += '</select>';
    newDiv.innerHTML= html;
    document.getElementById(divname).appendChild(newDiv);
}