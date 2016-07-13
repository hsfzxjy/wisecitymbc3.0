<template>
    <vs-navbar type="dark" id="top-nav-bar" style='background-color:#111;' fixed='top'>
        <vs-nav type="navbar" class="pull-xs-right">
            <vs-nav-item link="/n/" v-if="$root.user">
                <span class="fa fa-envelope-o fa-lg"></span>
            </vs-nav-item>
            <vs-nav-item>
                <span @click="$root.showSideBar = true" class="fa fa-bars fa-lg"></span>
            </vs-nav-item>
        </vs-nav>
        <div>
            <a class="navbar-brand" href="#">WiseCity</a>
            <vs-nav type="navbar" class="pull-xs-left hidden-xs-down">
                <vs-nav-item link="/articles/government/">资讯</vs-nav-item>
                <vs-nav-item link="/finance/">交易</vs-nav-item>
                <vs-nav-item link="/ram/">能源及原材料</vs-nav-item>
                <vs-nav-item link="/topics/" v-if="$root.perms.questions_topic_view_">Q&amp;A</vs-nav-item>
            </vs-nav>
        </div>
    </vs-navbar>
</template>

<script>

</script>