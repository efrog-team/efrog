<script>
</script>

<style>
    @font-face {
	font-family: "e-Ukraine"; 
	src: url("C:\Work\my-app\static\fonts\e-Ukraine\e-Ukraine-Light") format("truetype"); 
	font-style: normal; 
	font-weight: normal; 
    }
    .content{
        background-color: rgb(23, 22, 27);
        margin: 0px;
        height: 100vh;
    }
    .header{
        background-color: rgb(18, 18, 22);
        border-bottom: 5px solid rgb(34, 35, 39);
        height: 112px;
    }
    .header_text{
        color: white;
        font-size: 48px;
        font-family: "e-Ukraine";
        font-weight: bold;
        display: inline;
    }
    .menu_text{
        color: white;
        font-size: 20px;
        font-family: "e-Ukraine";
		text-align:right;
        text-decoration: none;   
        display: inline;
        margin: 5px;
    }
	.menu_photo{
		height: 100px;
		display:inline-block;
		margin:auto;
    }
    .main{
        background-color: rgb(34, 35, 39);
        color: white;
        font-size: 20px;
        margin: 50px;

    }
</style>

<svelte:head>
    <title>Create task</title>
</svelte:head>

<main>
    <div class="content">
        <div id="header" class="header">
            <div style="display: inline; float:left; margin-top: 25px; margin-left: 15px;"><p class="header_text">CodeMeister</p></div>
            <div style="display: inline; float:right; margin-top: 6px;"><a href="\ForUsers"><img src="favicon.png" class="menu_photo" alt=" "></a></div>
            <div style="display: inline; float:right; margin-top: 50px;">   
                <a href="\FindingTasks" class="menu_text">Пошук задач</a>
                <a href="\Olimpiad" class="menu_text">Олімпіади</a>
                <a href="\CreateTask" class="menu_text">Створити задачу</a>
                <a href="\CreateOlimpiad" class="menu_text">Створити олімпіаду</a>
                <a href="\ForCouthes" class="menu_text">Для коучів</a>
            </div>
        </div>
        <div class="main">
            <h1>Тестове завдання</h1>
            <p>Умова завдання: Напишіть функцію, що рахує квадрат числа</p>
            <form on:submit={() => {
                let socket = new WebSocket("ws://localhost:8000/task");
                socket.onopen = function() {
                    socket.send(document.getElementById("message").value);
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
                <textarea type="text" name="message" id="message" cols="30" rows="10" value="print(int(input()) ** 2)"></textarea>
                <input type="submit" id="submit" value="Відправити">
            </form>
            <div id="answer">Відповідь сервера:</div>
        </div>
    </div>
</main>