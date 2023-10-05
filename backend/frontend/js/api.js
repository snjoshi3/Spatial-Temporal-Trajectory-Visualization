const BASE_URL = "http://localhost:8000/";

function parseJSON(response) {
    return new Promise(resolve =>
        response.json().then(json =>
        resolve({
            status: response.status,
            ok: response.ok,
            json
        })
        )
    );
}

async function load_data() {
    const url = BASE_URL + "load_data";

    return new Promise((resolve,reject)=>{
        fetch(url)
        .then(parseJSON)
        .then((response) => {
            if(response.ok){
                return resolve(response.json);
            }
            return reject(response.json.message);
        }).catch(error=>{
            console.log(error);
        });
    })
}

export{load_data};