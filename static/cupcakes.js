const BASE_URL = 'http://127.0.0.1:5000/api';

function generateCupcakeHTML(cupcake) {
    // Generate HTML page with given data.
    return `
    <div data-cupcake-id = ${cupcake.id}>
        <li>
        Flavor: ${cupcake.flavor},
        Size: ${cupcake.size},
        Rating: ${cupcake.rating}
        <button class='delete-button'>X</button>
        </li>
        <img class='Cupcake-img'
            src='${cupcake.image}'
            alt='(no image provided)'> 
    </div>
    `; 
}

async function showListCupcakes() {
    // List cupcakes.
    const res = await axios.get(`${BASE_URL}/cupcakes`);
    for (let data of res.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(data));
        $('#cupcakes-list').append(newCupcake); 
    }
}

$('#new-cupcake-form').on('submit', async function (e) {
    e.preventDefault();
    
})
