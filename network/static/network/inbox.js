var script = document.createElement('script');
script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);


function w_set() {
  document.querySelector('h5').innerHTML = 'Post sent';
  setInterval(w_reset, 2000);


}

function w_reset() {
  document.querySelector('h5').innerHTML = '';
  window.location.reload(false);
  //document.getElementById("new_post").defaultValue = "";
  //document.querySelector('#new_post').innerHTML = '';

}


document.addEventListener('DOMContentLoaded', compose_post);


  function compose_post() {

    // Disable button by default:
    document.querySelector('#button').disabled = true;

    // Listen for input to be typed into the input field
    document.querySelector('#new_post').onkeyup = () => {
        if (document.querySelector('#new_post').value.length > 0) {
            document.querySelector('#button').disabled = false;
        }
        else {
            document.querySelector('#button').disabled = true;
        }
    }

    document.querySelector('#button').onclick = () =>  {

      const content = document.getElementById("new_post").value;
      console.log(content)
      fetch('/posts', {
      method: 'POST',
      timeout:3000,
      body: JSON.stringify({
          content : content,

      })
      })

    .then(response => response.json())
    .then(result => {
    // Print result
     console.log(result);
     //all_posts()
   })
   setInterval(w_set, 2000);
   //document.getElementById("new_post").innerHTML = "";
   //document.querySelector('#new_post').innerHTML = '';
   //setInterval(w_reset, 3000);
  }



}
