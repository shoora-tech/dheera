fd = document.getElementsByTagName("fieldset")
ff = fd[1]
uu = ff.getElementsByClassName('form-row dynamic-sku')
for(var i=0; i<uu.length; i++){
    uu[i].cells[10].addEventListener('input', function (evt) {
        console.log(this.value)
    })
}