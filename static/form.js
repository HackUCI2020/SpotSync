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

function submitClicked()
{
    var seedValue = document.getElementById("seed").value;
    var songsValue = document.getElementById("songs").value;
    var numSongsValue = document.getElementById("num").value;
    var params = {
        seed: seedValue,
        songs: songsValue,
        numSongs: numSongsValue
    };
    var url = "/song-request?"+encodeQueryData(params)
    console.log(url)
    redirect(url)
}

function addClicked()
{
    redirect("/playlist")
}