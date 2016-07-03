<template>
    <vs-navbar style='background-color:#191919' type="dark" fixed="top">
        <button class="navbar-toggler hidden-sm-up" type="button" data-toggle="collapse" data-target="#navbar-header" aria-controls="navbar-header">
            &#9776;
        </button>
        <vs-buttons class="hidden-sm-up pull-xs-right" type="button" link="/me/" variant="link">
            我
        </vs-buttons>
        <div id="navbar-header" class="collapse navbar-toggleable-xs">
            <a class="navbar-brand" href="#">WiseCity</a>
            <vs-nav type="navbar" class="pull-xs-left">
                <vs-nav-item link="/">主页</vs-nav-item>
                <vs-nav-item link="/articles/government/">文章</vs-nav-item>
                <vs-nav-item link="/finance/">交易</vs-nav-item>
            </vs-nav>
        </div>
    </vs-navbar>
</template>

<script>
    
</script>