<template>
    <div>
        <vs-list-group :flush="flush">
            <vs-list-group-item
                v-for="article in articles" class='ALGI'>
                <div class="wrapper">
                    <a
                        v-link="article.url">
                        {{ article.title }}
                    </a>
                    <vs-collapse-toggle 
                        :target="`collapse-article-${article.id}`"
                        :target-group="`article-group-${category}`"
                        class="pull-xs-right">
                        <vs-badge
                            variant="success"
                            class="pull-xs-right pointer ALGB">
                            摘要
                        </vs-badge>
                    </vs-collapse-toggle>
                    <vs-badge
                        variant="danger"
                        class="pull-xs-right"
                        v-if="article.is_top">
                        置顶
                    </vs-badge>
                </div>
                <vs-collapse 
                    :id="`collapse-article-${article.id}`"
                    :group="`article-group-${category}`">
                     <div class="card card-block">
                         {{ article.summary }}
                     </div>
                </vs-collapse>
            </vs-list-group-item>
        </vs-list-group>   
        <list-loader
            url="/api/articles/"
            :params="params"
            :model.sync="articles">
        </list-loader>
    </div>   
</template>

<style scoped>
    li.list-group-item .wrapper {
        padding: .25em;
    }

    li.list-group-item .label {
        margin-left: .2em;
    }

    li.list-group-item .label.pointer {
        cursor: pointer;
    }
</style>

<script>
    import { articles } from 'consts.es'
    import ListLoader from 'misc/ListLoader.vue'

    export default {
        components: { ListLoader },
        data: () => ({
            articles: []
        }),
        props: {
            category: {
                type: String,
                required: true
            },
            flush: {
                type: Boolean,
                default: false
            },
            otherParams: {
                type: Object,
                default: {}
            }
        },
        computed: {
            params () {
                let params = _.cloneDeep(this.otherParams)

                params.article_type = articles.ArticleType[this.category]

                return params
            }
        }
    }
</script>