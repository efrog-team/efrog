<script>
</script>

<style>
</style>

<svelte:head>
    <title>Create task</title>
</svelte:head>
<main>
    <div class="content">
        <div id="header" class="header">
            <div style="display: inline; float:left; margin-top: 6px; margin-left: 15px;"><a href="\main"><img src="logo.png" class="menu_photo" alt=" "></a></div>
            <div style="display: inline; float:right; margin-top: 6px;"><a href="\for-user"><img src="favicon.png" class="menu_photo" alt=" "></a></div>
            <div style="display: inline; float:right; margin-top: 50px;">   
                <a href="\finding-task" class="menu_text">Задачі</a>
                <a href="\olimpiad" class="menu_text">Олімпіади</a>
            </div>
        </div>
        <div class="main">
            <h1>Тестове завдання</h1>
            <p>Умова завдання: Напишіть функцію, що рахує квадрат числа</p>
            <form on:submit={() => {
                let socket = new WebSocket("ws://localhost:8000/task");
                socket.onopen = function() {
                    socket.send(document.getElementById("code").value);
                    socket.send(document.getElementById("language").value);
                    document.getElementById('submit').disabled = true;
                    document.getElementById('answer').innerHTML = 'Відповідь сервера:';
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
            }}>
                <textarea type="text" name="code" id="code" cols="30" rows="10" value="print(int(input()) ** 2)"></textarea><br>
                <select name="language" id="language">
                    <option value="Python 3 (3.10)">Python 3 (3.10)</option>
                    <option value="C++ 17 (g++ 11.2)">C++ 17 (g++ 11.2)</option>
                    <option value="C 17 (gcc 11.2)">C 17 (gcc 11.2)</option>
                </select>
                <input type="submit" id="submit" value="Відправити">
            </form>
            <div id="answer">Відповідь сервера:</div>
        </div>
    </div>
</main>