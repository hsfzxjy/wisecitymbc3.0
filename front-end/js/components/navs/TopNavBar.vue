<template>
    <vs-navbar type="dark" id="top-nav-bar" style='background-color:#111;' fixed='top'>
        <vs-nav type="navbar" class="pull-xs-right">
            <vs-nav-item>
                <span class="fa fa-refresh fa-lg" @click="$root.refreshCurrentView()"></span>
            </vs-nav-item>
            <vs-nav-item link="/n/" v-if="$root.user" class="n-outer">
                <span 
                    class="fa fa-envelope-o fa-lg">
                </span>
                <span class="n-dot">{{ $root.nCount > 0 ? $root.nCount : ''}}</span>
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

<style>
    .n-outer {
        position: relative;
    }

    .n-dot {
        position: absolute;
        right: -1em;
        top: 1em;
        background-color: red;
        color: white;
        border-radius: 50%;
        font-size: .5em;
        padding: .2em .3em;
        line-height: 1;
    }
    .n-dot:empty {
        display: none;
    }
</style>