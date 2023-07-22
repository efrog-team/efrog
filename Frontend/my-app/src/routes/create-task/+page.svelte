<script>
    let test_amount = 1;
    let save = [];
    let tests = [];
    let files;

    function resize(_e) {
        let event = _e || event || window.event;
        let getElement = event.target || event.srcElement; 
        getElement.style.height = "92px"; 
        getElement.style.height = Math.max(getElement.scrollHeight, getElement.offsetHeight)+"px"
        console.log(1)
    }
    function create_test (){
        tests = save;
        if (document.getElementById("tests_amount").value != null){
            test_amount = Number(document.getElementById("tests_amount").value);
        }
        for(let i = 0; i <test_amount; i++){
        tests = tests.concat({id: i + 1});
        }
        console.log(tests);
    }
	 function send() {
        console.log(1)
     }
</script>

<style>
    p{
        color:white;
        font-family: "e-Ukraine";
        font-size: 22px;
    }
    input{
        outline: none;
        border: none;
        background-color: rgb(57, 61, 69);
        border-bottom: 4px solid rgb(33, 121, 45);
        width: 30vw;
        height: 50px;
        margin-top: 7px;
        margin-bottom: 44px;
        color: white;
        font-size: 22px;
        font-family: "e-Ukraine";
        display:flex;
    }
    .term{
        outline: none;
        border: none;
        background-color: rgb(57, 61, 69);
        border-bottom: 4px solid rgb(33, 121, 45);
        width: 53vw;
        height: 100px;
        color: white;
        font-size: 22px;
        font-family: "e-Ukraine";
        resize: none;
        display:flex;
    }
    .test_header{
        width: 88vw;
        height: 70px;
        background-color: rgb(57, 61, 69);
        border: 4px solid rgb(33, 121, 45);
        display:flex;
        margin-top: 15px;
        color: white;
        font-family: "e-Ukraine";
        text-align: justify;
    }
    .test_font{
        margin: auto;
    }
    .test{
        width: 88vw;
        height: 70px;
        background-color: rgb(41, 44, 51);
        border-bottom: 4px solid rgb(33, 121, 45);
        display:flex;
        margin-top: 15px;
        color: white;
        font-family: "e-Ukraine";
    }
    .test_area{
        outline: none;
        border: none;
        background-color: rgb(41, 44, 51);
        width: 25vw;
        height: 60px;
        color: white;
        font-size: 22px;
        font-family: "e-Ukraine";
        resize: none;
        display:flex;
    }
    .select{
        outline: none;
        border: none;
        background-color: rgb(41, 44, 51);
        width: 25vw;
        height: 60px;
        color: white;
        font-size: 22px;
        font-family: "e-Ukraine";
        resize: none;
        display:flex;
    }
    .number{
        margin: auto;
        margin-left: 6%;
        margin-right: 10%;
        margin-bottom: 30px;
        text-align: center;
    }
    .submit_button{
        width: 42vw;
        height: 70px;
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
        <div style="padding: 5vw;">
            <form>

                <div style="display: inline; float:left; margin-right: 5vw; margin-bottom:15px;">                
                    <p>Код задачі</p>
                    <input type="text" id="task_code">
                    <p>Назва</p>
                    <input type="text" id="task_name">
                    <p>Час виконання</p>
                    <input type="text" id="time_limit">
                    <p>Обсяг пам'яті</p>
                    <input type="text" id="memory_limit">
                    <p>Кількість тестів</p>
                    <input type="text" id="tests_amount"  on:change={create_test}>
                </div>
                <div style="display: inline; float:left; margin-bottom:15px;">                
                    <p>Умова</p>
                    <textarea name="term" id="term" class="term" on:input={resize}></textarea>
                    <p>Умова до вхідних даних</p>
                    <textarea name="input_term" id="input_term" class="term" on:input={resize}></textarea>
                    <p>Умова до вихідних даних</p>
                    <textarea name="outnput_term" id="outnput_term" class="term" on:input={resize}></textarea>
                    <p>Примітки</p>
                    <textarea name="notes" id="notes" class="term" on:input={resize}></textarea>
                </div>
                <div class="test_header">
                    <p class="test_font">№</p>
                    <p class="test_font">Вхідні дані</p>
                    <p class="test_font">Вихідні дані</p>
                    <p class="test_font">Статус тесту</p>
                </div>
                {#each tests as test}
                    <div class="test">
                        <p class="number">{test.id}</p>
                        <textarea name="input_value" id="input_value" class="test_area"></textarea>
                        <textarea name="outnput_value" id="outnput_value" class="test_area"></textarea>
                        <select class="select">
                            <option value="1">Opened</option>
                            <option value="2">Closed</option>
                        </select>
                    </div>
                {/each}
                <input bind:files id="many" multiple type="file" class="submit_button">
                <input type="submit" id="submit" value="Відправити" class="submit_button" style="margin-right: 0;" on:submit={send}>
            </form> 
        </div>
    </div>
</main>