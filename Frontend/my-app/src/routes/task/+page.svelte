<script>
    /*let id = 1;*/
    let task = {name: "Task1",
                time_limit: "12ms", 
                memory_limit: "256 mb", 
                term: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ac ante egestas, consequat nulla at, aliquam urna. Morbi dapibus hendrerit sa",
                input_term: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ac ante egestas, consequat nulla at, aliquam urna. Morbi dapibus hendrerit sa",
                outnput_term: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ac ante egestas, consequat nulla at, aliquam urna. Morbi dapibus hendrerit sa",
                note_term: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ac ante egestas, consequat nulla at, aliquam urna. Morbi dapibus hendrerit sa",};
    let open_tests = [{id: 1, input:"1", output:"1"}, {id: 2, input:"2", output:"4"}, {id: 3, input:"3", output:"9"}]
    let point = 0;


    function change_code() {
        point = 0
    }
    function change_res() {
        point = 1
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
    .term{
        outline: none;
        border: none;
        background-color: rgb(57, 61, 69);
        width: 92vw;
        color: white;
        font-size: 16px;
        font-family: "e-Ukraine";
        resize: none;
        padding: 1vw;
        padding-top: 1px;
    }
    .test{
        position: relative; 
        display:flex; 
        margin: 0px;
        color: white;
        font-size: 18px;
        font-family: "e-Ukraine";
    }
    .submit_button{
        width: 94vw;
        height: 50px;
        background-color: rgb(33, 121, 45);
        margin-top: 15px;
        float: left;
        color: white;
        font-size: 22px;
        font-family: "e-Ukraine";
        text-align: center;
        text-decoration: none;
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
            <p style="font-size: 32px;">{task.name}</p>
            <button on:click={change_code}>Умова</button>
            <button on:click={change_res}>Статистика</button>
            <hr>
            {#if point === 0}
                <div class="term">
                    <p>Ліміт часу: {task.time_limit}</p>
                    <p>Ліміт пам'яті: {task.memory_limit}</p>
                    <p>Умова</p>
                    {task.term}
                    <p>Умова до вхідних даних</p>
                    {task.input_term}
                    <p>Умова до вихідних даних</p>
                    {task.outnput_term}
                    <p>Примітки</p>
                    {task.note_term}
                    <p style="margin-bottom: 0px;">Приклади</p>
                    {#each open_tests as open_test}
                        <div class="test">
                            <div style="display: inline; float:left; margin-right: 30px; margin-top:0px;">
                                <p>Вхідні дані № {open_test.id}</p>
                                {open_test.input}
                            </div>
                            <div style="display: inline; float:left; margin-right: 30px; margin-top:0px;">
                                <p>Вихідні дані № {open_test.id}</p>
                                {open_test.output}
                            </div>
                            
                        </div>
                    {/each}
                </div>
                <a href="/sent-task" class="submit_button"><div style="margin-top: 10px;">Надіслати рішення</div></a>
            {:else}
                <div id="answer" class="tests">тут Статистика</div>
            {/if}
        </div>
    </div>
</main>