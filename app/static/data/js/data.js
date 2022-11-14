

// The endpoint of the API runnngon docker
const URL_API = "http://localhost:5000/";

/**
 * Initialize the forms and lists
 * fetch all data from API
 */
function init() {
    hide('#data-form')
    hide('#data-batcher')
    show('#data-list')

    fetch(`${URL_API}/data`)
  .then(async (response) => {
    if(response.status === 200) {
        const json = await response.json();
        const listItems = json;
        loadList(listItems)
    }
  })
  .then((data) => console.log(data));
}

/**
 * Renders the data in the table
 * @param {List<Data>} data 
 */
function loadList(data) {
    const tab = document.getElementById('data-list-tab');
    const tbody = tab.querySelector('tbody');
    if (!data || !data.length) {
        tbody.innerHTML = '<tr><td colspan="5">No Data Available <br> you can add from importing the json or inserting one by one</td></tr>';
    } else {
        tbody.innerHTML = '';
        data.forEach((d)=> {
            tbody.innerHTML += `<tr>
                                    <td>
                                        ${d.id}
                                    </td>
                                    <td>
                                    ${d.url}
                                    </td>
                                    <td>
                                        ${d.title}
                                    </td>
                                    <td>
                                        ${d.date_added}
                                    </td>
                                    <td>
                                        <a href="javascript:edit(${d.id});" >Edit</a>
                                        <a href="javascript:remove(${d.id});">Remove</a>
                                    </td>
                                </tr>`;
        })
    }
}
/**
 * Calls the fileter pasingthe data from 
 */
function search() {

    const obj =  {
        "title": document.getElementById('filter-title').value ,
        "uri": document.getElementById('filter-url').value,
        "date_after": formatDateField(document.getElementById('filter-after').value),
        "date_before": formatDateField(document.getElementById('filter-before').value)
      }
      postData(`${URL_API}/data/filter`, obj, method='POST')
      .then(async (response) => {
        if(response.status === 200) {
            const json = await response.json();
            const listItems = json;
            loadList(listItems)
        }
      })
      .then((data) => console.log(data));
      ;
    

}

function formatDateField(d) {
    if(d) {
        return d;
    } else {
        return null;
    }
}


async function postData(url = '', data = {}, method = 'POST') {
    return fetch(url, {
      method: method, 
      mode: 'cors', 
      cache: 'no-cache',
      credentials: 'same-origin', 
      headers: {
        'Content-Type': 'application/json'
      },
      redirect: 'follow', 
      referrerPolicy: 'no-referrer', 
      body: JSON.stringify(data) 
    });
  }

function edit(id) {
    fetch(`${URL_API}/data/${id}`)
    .then(async (response) => {
      if(response.status === 200) {
          const json = await response.json();
          loadForm(json) 
      }
    })
    .then((data) => console.log(data));

}


function loadForm(obj) {
    show('#data-form');
    hide('#data-list');
    hide('#data-batcher')
    document.getElementById('save').onclick = ()=> save();
    document.getElementById('cancel').onclick = ()=> cancel();
    if (obj.id) {
        document.getElementById('form-id').value = obj.id;
    }
    document.getElementById('form-title').value = obj.title;
    document.getElementById('form-url').value = obj.url;
    document.getElementById('form-date').value = obj.date_added;
}
function newItem() {
    show('#data-form');
    hide('#data-list');
    hide('#data-batcher');
    document.getElementById('save').onclick = ()=> save();
    document.getElementById('cancel').onclick = ()=> cancel();

    document.getElementById('form-id').value = null;
    document.getElementById('form-title').value = null;
    document.getElementById('form-url').value = null;
    document.getElementById('form-date').value = null;
}

function dateToJs(d) {
    if (d) {
        const date = Date.parse(d);
        return date;
    }else {
        return d;
    }
}

function cancel() {
    init();
}


function save() {
    const obj =  {
        "id": document.getElementById('form-id').value ,
        "title": document.getElementById('form-title').value ,
        "uri": document.getElementById('form-url').value,
        "date": formatDateField(document.getElementById('form-date').value),
      }
    postData(`${URL_API}/data`, obj, method=(obj.id?'PUT':'POST'))
    .then(async (response) => {
      if(response.status === 201) {
            alert("Data created");
            init()
          
      } else if(response.status === 200) {
        alert("Data updated");
            init()
          
      } else if(response.status === 400) {
        alert(await response.text());
      }

    })
    .then((data) => console.log(data));
}

function hide(selector) {
    Array.from(document.querySelectorAll(selector)).forEach((a) => {
        a.style.display = 'none';
    });
}


function show(selector) {
    Array.from(document.querySelectorAll(selector)).forEach((a) => {
        a.style.display = 'block';
    });
}

function remove(id) {
    if (confirm("Are you sure you want to permanently remove this data?") == true) {
        postData(`${URL_API}/data/${id}`, null, method='DELETE')
        .then(async (response) => {
            if(response.status === 204) {
                    alert("Data deleted successfully");
                    init()
            } else if(response.status === 400) {
                alert(await response.text());
            }
        })
        .then((data) => console.log(data));
    }
}

async function openBatcher() {
    hide('#data-form');
    hide('#data-list');
    show('#data-batcher');
    const data = await fetch(`${URL_API}/static/input/data.json`)
    if(data.status===200) {
        document.getElementById('textarea-batch').value = await data.text();
    }

}
async function insertBatch() {
    let obj = null;
    try {
        obj = JSON.parse(document.getElementById('textarea-batch').value)
    }catch(e) {
        alert("JSON format invalid")
        return;
    }
    const errorsList = [];
    let counterOk = 0;
    // In this case it has to be synchronous
    for (const o of obj.items ) {
        try {
            const response = await postData(`${URL_API}/data`, o, method='POST')
            if(response.status === 201) {
                console.log("Created successfully");
                counterOk ++;
            } else if(response.status === 400) {
                console.log("ErrorBad request");
                errorsList.push(`Title ${o?.title} URI ${o?.uri} Date ${o?.date} failed to load: ${await response.text()}`)
            }
        }catch(e) {
            console.log("Error", e)
            errorsList.push(`Title ${o?.title} URI ${o?.uri} Date ${o?.date} failed to load`)
        }
    }
    alert("Import finalized")
    const el = document.getElementById("data-batchner-output");
    el.innerHTML = `${counterOk} Items created successfully <br>
                    <ul>
                        ${errorsList.map((a)=> `<li>${a}</li>`)}
                    </ul>
                        `
}