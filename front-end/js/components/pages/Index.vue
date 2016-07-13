<template>
    <div>
        <vs-jumbotron fluid style="word-wrap: break-word;">
            <div class="col-md-8 col-sm-12">
                <h1 >
                    WiseCity
                </h1>
            </div>
            <div class="col-md-4 col-sm-12">
                <div v-show="!$root.hasLogined">
                    <login-form></login-form>    
                </div>
                <div v-else>
                    <h2>欢迎您，{{ $root.user.nickname }}</h2>
                </div>
            </div>
        </vs-jumbotron>
        <div class="container-fluid">
            <div class="col-sm-6 col-xs-12 no-padding">
                <div class="col-lg-6">
                    <vs-card>
                        <h4 class="card-block card-title text-xs-center">资讯·政府</h4>
                        <article-list-group
                            category="government"
                            :other-params="{limit:3}"
                            flush>
                            <div slot="no-results" class="card-block card-text">
                                空空如也～～
                            </div>
                        </article-list-group>
                    </vs-card>                    
                </div>
                <div class="col-lg-6">
                    <vs-card>
                        <h4 class="card-block card-title text-xs-center">资讯·媒体</h4>
                        <article-list-group
                            category="media"
                            :other-params="{limit:5}"
                            flush>
                            <div slot="no-results" class="card-block card-text">
                                空空如也～～
                            </div>
                        </article-list-group>
                    </vs-card>
                </div>
            </div>
            <div class="col-sm-6 col-xs-12 no-padding">
                <div class="col-lg-6">
                    <vs-card>
                        <h4 class="card-block card-title text-xs-center">金融</h4>
                        <article-list-group
                            category="finance"
                            :other-params="{limit:2}"
                            flush>
                            <div slot="no-results" class="card-block card-text">
                                空空如也～～
                            </div>
                        </article-list-group>
                    </vs-card>
                </div>
                <div class="col-lg-6">
                    <vs-card>
                        <h4 class="card-block card-title text-xs-center">能源及原材料</h4>
                        <article-list-group
                            category="energy_and_raw_materials"
                            :other-params="{limit:2}"
                            flush>
                            <div slot="no-results" class="card-block card-text">
                                空空如也～～
                            </div>
                        </article-list-group>
                    </vs-card>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
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
        ready () {
            this.$broadcast('ListLoader:reload')
        }
    }
</script>