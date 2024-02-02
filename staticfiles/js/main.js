
//Get search form and page links
let searchForm = document.getElementById('searchForm')
let pageLink = document.getElementsByClassName('page-link')

//Check that search form exists
if(searchForm){
  for(let i=0; pageLink.length>i; i++){
    pageLink[i].addEventListener('click', function(e){
      e.preventDefault()

      //Get data attribute
      let page = this.dataset.page

      //Add hidden search input
      searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

      //Submit form
      searchForm.submit()
    })
  }
}



