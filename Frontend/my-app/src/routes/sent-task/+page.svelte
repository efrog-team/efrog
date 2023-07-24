<script>

    /*let id = 1;*/
    let name = "Task 1";
    let code = "";
    let language = "Python 3 (3.10)";

    function sent_form() {
        let tests = document.querySelector("input");
        tests.setAttribute("checked", "checked")

        let socket = new WebSocket("ws://localhost:8000/task");
        socket.onopen = function() {
            socket.send(code);
            socket.send(language);
            /*socket.send(id);*/
            document.getElementById('submit').disabled = true;
        };
        socket.onmessage = function(event) {
            let message = event.data;
            let messageElem = document.createElement('div');
            messageElem.textContent = message;
            document.getElementById('answer').append(messageElem);
        };
        socket.onclose = function() {
            document.getElementById('submit').disabled = false;
        };

    } 
</script>

<style>
    p{
        color:white;
        font-family: "e-Ukraine";
        font-size: 22px;
    }
    button{
        outline: none;
        border: none;
        display: inline;
        background-color: rgb(41, 44, 51);
        color: white;
        font-size: 22px;
        font-family: "e-Ukraine";

    }
    select{
        outline: none;
        border: none;
        background-color: rgb(57, 61, 69);
        width: 94vw;
        height: 60px;
        color: white;
        font-size: 22px;
        font-family: "e-Ukraine";
        resize: none;
        display:flex;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    textarea{
        outline: none;
        border: none;
        background-color: rgb(57, 61, 69);
        width: 94vw;
        height: 300px;
        color: white;
        font-size: 16px;
        font-family: "e-Ukraine";
        resize: none;
        display:flex;
    }
    .submit_button{
        width: 94vw;
        height: 50px;
        background-color: rgb(33, 121, 45);
        border: 4px solid rgb(33, 121, 45);
        margin-right: 4vw;
        margin-top: 15px;
        display:inline;
        float: left;
        color: white;
        font-size: 22px;
        font-family: "e-Ukraine";
        text-align: center;
    }
    .tests {
        display: none;
    }
    .tests + label {
        display: block;
    }
    .tests + label + div {
        display: none;
    }
    .tests:checked + label + div {
        display: block;
        padding:5px;    
        outline: none; 
        border: none; 
        color:white; 
        font-family: "e-Ukraine"; 
        font-size: 22px; 
        background-color: rgb(41, 44, 51);
    }
</style>

<svelte:head>
    <title>Create task</title>
</svelte:head>

<main>
    <div class="content">
        <div id="header" class="header">
            <div style="display: inline; float:left; margin-top: 6px; margin-left: 15px;"><a href="\main"><img src="logo.png" class="menu_photo" alt=" "></a></div>
            <div style="display: inline; float:right; margin-top: 6px;"><a href="\for-user"><img src="favicon.png" class="menu_photo" alt=" "></a></div>
            <div style="display: inline; float:right; margin-top: 30px;">   
                <a href="\finding-task" class="menu_text">Задачі</a>
                <a href="\olimpiad" class="menu_text">Олімпіади</a>
            </div>
        </div>
        <div style="padding: 3vw; padding-top: 0;">
            <p style="font-size: 32px;">{name}</p>
            <p>Мова програмування</p>
            <select name="language" id="language" bind:value={language}>
                <option value="Python 3 (3.10)">Python 3 (3.10)</option>
                <option value="C++ 17 (g++ 11.2)">C++ 17 (g++ 11.2)</option>
                <option value="C 17 (gcc 11.2)">C 17 (gcc 11.2)</option>
            </select>
            <p>Код</p>
            <textarea type="text" name="code" id="code" bind:value={code}></textarea>

            <input class="tests" id="tests" type="checkbox">
            <label for="tests"><p>Результати</p></label>
            <div id="answer">Відповідь сервера:</div>

            <button on:click={sent_form} class="submit_button" id="submit">Відправити</button>
        </div>
    </div>
</main>