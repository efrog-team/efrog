<script>
</script>

<style>
    .content{
        text-align: center;
        margin-left: auto;
        margin-right: auto;
        width: max-content;
    }

    ul.menu {
        margin:0;
        padding:0;
        overflow: hidden;
        text-align: center;
    }

    ul.menu a{
        display: inline-block;
        position: relative;
        color: rgb(0, 0, 0); 
        background: rgb(142, 142, 150); 
        text-decoration: none;
        letter-spacing: 1px; 
        height: 2em; 
        
    }

    ul.menu li{
        display:inline;
        float: left;
        border: 2px solid black;
        width: 200px;
        text-align: center;
    }

</style>

<svelte:head>
    <title>Create task</title>
</svelte:head>

<main>
    <div id="content" class="content">   
        <h1 class="header">CodeMeister</h1>
        <ul class="menu">
            <li><a href="\">Головна</a></li>
            <li><a href="\FindingTasks">Пошук задач</a></li>
            <li><a href="\Olimpiad">Олімпіади</a></li>
            <li><a href="\CreateTask">Створити задачу</a></li>
            <li><a href="\CreateOlimpiad">Створити олімпіаду</a></li>
            <li><a href="\ForCouthes">Для коучів</a></li>
            <li><a href="\ForUsers">Для учасників</a></li>
        </ul>
    </div>
</main>