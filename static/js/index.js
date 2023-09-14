const listDatos = async() => {
    try{
        const response = await fetch('./api/get_all_votantes/')
        const data = await response.json()

        let content = ``
        data.votantes.forEach( (votante,index) => {
            content += `
                <tr>
                    <td>${index+1}</td>
                    <td>${votante.name}</td>
                    <td>${votante.document_id}</td>
                    <td>${votante.mobile_phone}</td>
                    <td>${votante.municipio}</td>
                </tr>
            `
        })

        tableBody_votantes.innerHTML = content
    } catch (ex) {
        console.log(ex)
    }
};


window.addEventListener('load', async() => {
    await listDatos();
});