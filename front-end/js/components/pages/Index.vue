<template>
    <div>
        <vs-jumbotron fluid id="index-jumbotron">
            <img src="/static/logo.png" id="index-logo" />
            <h3 v-if="$root.user && $root.user.nickname">
                欢迎您，{{ $root.user.nickname }}
            </h3>
        </vs-jumbotron>
        <div class="container" id="index-container">
            <div class="col-xs-12 col-sm-6 col-md-3" v-for="options in articleOptions">
                <vs-card class="clearfix">
                    <a v-link="'/articles/'+$key+'/'" class="title">
                        <h2 class="card-block card-title text-xs-center">
                            {{options.title}}
                        </h2> 
                    </a>
                    <div class="content">
                        <article-list-group
                            :summary="false"
                            :category="$key"
                            :other-params="{limit: options.limit}"
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
            articleOptions: {
                government: {
                    title: '资讯·政府',
                    limit: 2
                },
                media: {
                    title: '资讯·媒体',
                    limit: 2
                },
                finance: {
                    title: '资讯 · 金融',
                    limit: 2
                },
                energy_and_raw_materials: {
                    title: '能源及原材料',
                    limit: 2
                },
                bank: {
                    title: '银行',
                    limit: 2
                },
                real_estate: {
                    title: '房地产',
                    limit: 2
                },
                electronic_technology: {
                    title: '电子科技',
                    limit: 2
                }
            }
        }),
        ready () {
            this.$broadcast('ListLoader:reload')
        }
    }
</script>