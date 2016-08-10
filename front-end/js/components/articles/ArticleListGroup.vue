<template>
        <vs-list-group :flush="flush">
            <vs-list-group-item
                v-for="article in articles" class='ALGI'>
                <div class="wrapper">
                    <a
                        v-link="article.url">
                        {{ article.title }}
                    </a>
                    <label
                        v-if="summary"
                        :id="'collapse-article-'+article.id"
                        class="pull-xs-right pointer ALGB tag tag-success">
                        摘要
                    </label>
                    <label
                        class="pull-xs-right tag tag-danger"
                        v-if="article.is_top">
                        置顶
                    </label>
                </div>
                <vs-expansion 
                    v-if="summary"
                    :toggler-id="'collapse-article-'+article.id">
                     <div class="card card-block" slot="content">
                         {{ article.summary }}
                     </div>
                </vs-expansion>
            </vs-list-group-item>
            <slot name="other-items"></slot>
        </vs-list-group>   
        <list
            url="/api/articles/"
            :params="params"
            :model.sync="articles"
            type="once"
            autoload>
        </list>
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
    export default {
        data: () => ({
            articles: [],
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
            },
            summary: {
                type: Boolean,
                default: true
            }
        },
        computed: {
            params () {
                let params = _.cloneDeep(this.otherParams)

                params.article_type = this.category

                return params
            }
        }
    }
</script>