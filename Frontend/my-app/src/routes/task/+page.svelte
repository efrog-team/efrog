<script>
    import { onMount } from "svelte";

    function sample() {
        if (document.getElementById('language').value == 'Python 3 (3.10)') {
            document.getElementById('code').value = 'print(int(input()))';
        }
        else if (document.getElementById('language').value == 'C++ 17 (g++ 11.2)') {
            document.getElementById('code').value = '#include <iostream>\nusing namespace std;\n\nint main() {\n    long long a;\n    cin >> a;\n    cout << a * a;\n}';
        }
        else if (document.getElementById('language').value == 'C 17 (gcc 11.2)') {
            document.getElementById('code').value = '#include <stdio.h>\n\nint main() {\n    long long a;\n    scanf("%lld", &a);\n    printf("%lld", a * a);\n}';
        }
    }

    onMount(() => sample());
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
                <textarea type="text" name="code" id="code" cols="30" rows="10"></textarea><br>
                <select name="language" id="language" on:change={sample}>
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