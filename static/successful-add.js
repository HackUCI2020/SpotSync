/* function taken from
    https://stackoverflow.com/questions/111529/how-to-create-query-parameters-in-javascript */
function encodeQueryData(data) {
   const ret = [];
   for (let d in data)
     ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
   return ret.join('&');
}

function redirect(url) {
    window.location.href = url;
}

function done()
{
    redirect('/');
}