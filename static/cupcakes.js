const BASE_URL = 'http://127.0.0.1:5000/api';

function generateCupcakeHTML(cupcake) {
    // Generate HTML page with given data.
    return `
    <div data-cupcake-id = ${cupcake.id}>
        <li>
        Flavor: ${cupcake.flavor} -- 
        Size: ${cupcake.size} --
        Rating: ${cupcake.rating}
        <button class='delete-button'>X</button>
        </li>
        <img class='cupcake-img'
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
    // Handle form for adding a new cupcake.
    e.preventDefault();
    let flavor = $('#flavor').val();
    let size = $('#size').val();
    let rating = $('#rating').val();
    let image = $('#image').val();

    const newData = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        size,
        rating,
        image
    });

    let newCupcake = $(generateCupcakeHTML(newData.data.cupcake));
    $('#cupcakes-list').append(newCupcake);
    $('#new-cupcake-form').trigger('reset'); 
});

$('#cupcakes-list').on('click', '.delete-button', async function (e) {
    e.preventDefault();
    let $cupcake = $(e.target).closest('div');
    let cupcakeId = $cupcake.attr('data-cupcake-id');

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});

$(showListCupcakes); 
