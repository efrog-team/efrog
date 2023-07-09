<script>
</script>

<style>
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
        font-family: "e-Ukraine";

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
            <h1><a href="\Task">Тестове завдання</a></h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ac ante egestas, consequat nulla at, aliquam urna. Morbi dapibus hendrerit sagittis. Donec egestas quam in porta semper. Nullam interdum venenatis dolor, at laoreet metus lobortis et. Interdum et malesuada fames ac ante ipsum primis in faucibus. Fusce viverra venenatis sapien sed placerat. Integer est metus, hendrerit ut urna eget, commodo accumsan lectus. </p>
            <p>Praesent a tincidunt eros, et dignissim eros. Nullam ut elit in nisl vulputate cursus. Suspendisse ornare magna a justo lacinia, a luctus felis fringilla. Aliquam et enim aliquam tortor ultrices sollicitudin dapibus at velit. Integer vestibulum ligula eu diam fringilla, sit amet ultrices quam vulputate. Cras suscipit auctor felis sed fringilla.</p>
            <p>Aenean convallis est sem, sed iaculis nisi fermentum ac. Aliquam eleifend fringilla diam, vel luctus ipsum feugiat eu. Aenean vestibulum nec nisi non faucibus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Donec ut lacus ac eros rutrum pellentesque a non diam. Praesent a est sed est cursus iaculis. Cras tincidunt tincidunt massa non cursus. Proin consequat orci vitae risus feugiat porta. Integer sed lectus accumsan.</p>
        </div>
    </div>
</main>