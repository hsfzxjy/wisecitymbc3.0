<template>
    <div>
        <vs-jumbotron fluid id="index-jumbotron">
            <img src="/static/logo.png" id="index-logo" />
            <h3 v-if="$root.user && $root.user.nickname">
                欢迎您，{{ $root.user.nickname }}
            </h3>
        </vs-jumbotron>
        <div class="container" id="index-container">
            <div class="col-xs-12 col-sm-6 col-md-3" v-for="title in articleOptions">
                <vs-card class="clearfix">
                    <a v-link="'/articles/'+$key+'/'" class="title">
                        <h2 class="card-block card-title text-xs-center">
                            {{title}}
                        </h2> 
                    </a>
                    <div class="content">
                        <article-list-group
                            :summary="false"
                            :category="$key"
                            :other-params="{limit: 3}"
                            flush>
                            <vs-list-group-item
                                slot="other-items"
                                class="read-more">
                                <a v-link="'/articles/'+$key+'/'">
                                    <span>了解更多</span>
                                </a> 
                            </vs-list-group-item>
                        </article-list-group>
                    </div>
                </vs-card>                    
            </div>
        </div>
    </div>
</template>

<style scoped>
    .no-padding {
        padding: 0!important;
    }
</style>

<script>
    import LoginForm from 'auth/LoginForm.vue'
    import ArticleListGroup from 'articles/ArticleListGroup.vue'

    export default {
        components: {
            LoginForm,
            ArticleListGroup
        },
        data: () => ({
            articleOptions: consts.article_type_verbose
        })
    }
</script>