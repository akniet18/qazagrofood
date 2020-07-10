let name = []
let prices = []
let arr_plus = document.querySelectorAll('[id^="action_plus_"]')
let arr_minus = document.querySelectorAll('[id^="action_minus_"]')
let results = document.querySelectorAll('[id^="count_"]')

let namesh = "";
// let url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRNX6FcoIutGWY6VolvaL6GbCcRwj__YImi2EFAFEcLW4NL-pc9YAil8oxaB5-uaZfGgKIV5rMEPc8h/pubhtml?gid=62247483&single=true"
// fetch(url)
//     .then(r=>{
//         return r.text()
//     })
//     .then(r => {
//         var parser = new DOMParser();
//         var htmlDoc = parser.parseFromString(r, 'text/html');
//         let trs = htmlDoc.getElementsByTagName('tr')
//         // console.log(trs.length)
//         let html = ""
//         for (let i=3; i<=trs.length; i++){
//             if (trs[i]){
//                 // console.log(trs[i])
//                 let tds = trs[i].getElementsByTagName('td')
//                 if (tds[1].innerText != ""){
                    // html += `<div class="block_${i} block">
                    //                 <div class="action" >
                    //                     <div class="action_top">
                    //                         <div class="minus"  id="action_minus_${i}" onClick="minus()">-</div>
                    //                         <div class="count" id="count_${i}">0</div>
                    //                         <div class="plus" id="action_plus_${i}" onClick="plus()">+</div>
                    //                     </div>
                    //                     <div class="price">${tds[3].innerText}</div>
                    //                 </div>
                    //                 ${tds[1].innerText}
                    //             </div>`
//                     name.push(tds[1].innerText)
//                     // console.log(tds[5].innerText)
//                 }
//             }
//         }
//         document.querySelector('.gridLayout').innerHTML = html;
//         arr_plus = document.querySelectorAll('[id^="action_plus_"]')
//         arr_minus = document.querySelectorAll('[id^="action_minus_"]')
//         results = document.querySelectorAll('[id^="count_"]')
//     })

function minus(){
    let a = event.srcElement.parentNode.children[1]
    if (a.innerText != "0"){
        a.innerText = parseInt(a.innerText) - 1 
    }
}
function plus(){
    let a = event.srcElement.parentNode.children[1]
    a.innerText = parseInt(a.innerText) + 1 
}

// console.log(arr_plus)

arr_plus.forEach((e, i) => {
    e.addEventListener("click", function(){
        results[i].innerText = parseInt(results[i].innerText) + 1
    })
})

arr_minus.forEach((e, i) => {
    e.addEventListener("click", function(){
        if (results[i].innerText != 0){
            results[i].innerText = parseInt(results[i].innerText) - 1
        }       
    })
})

function doorder(){
    let modal = document.querySelector('.modal')
    let txt = ""
    let sumall = 0
    results.forEach((e, i) => {
        if (e.innerText != "0") {
            let ss = parseInt(e.innerText)*prices[i]
            sumall += ss
            txt += `<div>${name[i]} x ${e.innerText} = ${ss}</div>`
        }
    })
    txt += `<div style="text-align: right">${sumall}<?div>`
    document.querySelector('.myorder').innerHTML = txt
    modal.classList.toggle('show')
}


// function init() {
//     Papa.parse('https://docs.google.com/spreadsheets/d/1SKkUZPHRkUykdsfuRyFFT7LK_M8EFCqJDVi8UmQzi2c/edit#gid=0', {
//     download: true,
//     header: true,
//     complete: function(results) {
//       var data = results.data
//       console.log(data)
//     }
//   })
// }
// window.addEventListener('DOMContentLoaded', init)


// var CLIENT_ID = '314826407768-m68jb9ov3dknfc8ur6k071048qdllle5.apps.googleusercontent.com';
// var API_KEY = 'AIzaSyDImKps-3MuWR4p4vlyjf6ZOgsmwXfxQ9E';

// var SCOPES = "https://www.googleapis.com/auth/spreadsheets";
// var DISCOVERY_DOCS = ["https://sheets.googleapis.com/$discovery/rest?version=v4"];
// function handleClientLoad() {
//     gapi.load('client:auth2', initClient);
//   }

// function initClient() {
//     gapi.client.init({
//       apiKey: API_KEY,
//       clientId: CLIENT_ID,
//       discoveryDocs: DISCOVERY_DOCS,
//       scope: SCOPES
//     }).then(function () {
//         gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);
//         console.log("yes")
//         // gapi.auth2.getAuthInstance().signIn();
//         updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
//     }, function(error) {
//         console.log(error)
//     });
//   }

//   function listMajors() {
//     gapi.client.sheets.spreadsheets.values.get({
//       spreadsheetId: '1SKkUZPHRkUykdsfuRyFFT7LK_M8EFCqJDVi8UmQzi2c',
//       range: 'A2:E',
//     }).then(function(response) {
//       console.log(response.result)
//       var range = response.result;
    
//       if (range.values.length > 0) {
//         // appendPre('Name, Major:');
//         for (i = 0; i < range.values.length; i++) {
//           var row = range.values[i];
//           console.log(row)
//         //   appendPre(row[0] + ', ' + row[4]);
//         }
//     //   } else {
//         // appendPre('No data found.');
//       }
//     }, function(response) {
//         console.log(response)
//     //   appendPre('Error: ' + response.result.error.message);
//     });
//   }
//   function appendShets(name){
//       console.log(name)
//     gapi.client.sheets.spreadsheets.values.append({
//         spreadsheetId: '1SKkUZPHRkUykdsfuRyFFT7LK_M8EFCqJDVi8UmQzi2c',
//         range: `${name}!A1`,
//         valueInputOption:'RAW',
//         insertDataOption:'INSERT_ROWS',
//     }, {values: [["newsssss", "", "neww"]]}).then(r => {
//         console.log(r)
//     }, function(r){
//         console.log(r)
//     })
//   }
  

//   function getSheets(){
//     gapi.client.sheets.spreadsheets.get({
//         spreadsheetId: "1SKkUZPHRkUykdsfuRyFFT7LK_M8EFCqJDVi8UmQzi2c"
//     }).then(function(response) {
//         console.log(response.result.sheets)
//         namesh = response.result.sheets[1].properties.title
//         appendShets(namesh);
//     }, function(response) {
//         console.log('Error: ' + response.result.error.message);
//     });
//   }

//   function updateSigninStatus(isSignedIn) {
//     console.log(isSignedIn, "hh")
//     if (isSignedIn) {
//         getSheets()
        
//     }
//   }
//   gapi.load('client', initClient)