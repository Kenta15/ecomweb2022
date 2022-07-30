var element = document.getElementById('country-btn')

if(element){
    element.addEventListener("click", function(){
        var country = document.getElementById("country")
        var selected_country = country.options[country.selectedIndex].value;
        if(user=='AnonymousUser'){
            addCookieCountry(selected_country)
            alert('Please login to change the country')
        }
        else{
            updateCountry(selected_country)
            alert('Country was changed')
        }
    })
}

function addCookieCountry(selected_country){

    country = selected_country

    location.reload()

    console.log('country:',country)

    document.cookie = 'country=' + JSON.stringify(country) + ";domain=;path=/"
}

function updateCountry(selected_country){

    var url = '/update_country/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'selected_country':selected_country})
    })
    // let .then = response => response.json()
    // let .then = data => console.log('data:',data)

    .then((response)=>{
        response.json()
    })

    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
}