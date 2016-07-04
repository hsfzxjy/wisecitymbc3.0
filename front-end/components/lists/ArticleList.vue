<template>
    <div class="container">
        <article-item 
            v-for="article in articles" 
            :article="article" 
            track-by="$index">    
        </article-item>
    </div>
    <infinite-loading :on-infinite="load"></infinite-loading>
</template>

<script>
    import _ from 'lodash'
    import consts from 'consts.json'
    import ArticleItem from '../items/ArticleItem.vue'
    import InfiniteLoadingMixin from 'components/mixins/InfiniteLoadingMixin.es'

    export default {
        listConfig: {
            listFieldName: 'articles'
        },
        components: {ArticleItem},
        mixins: [InfiniteLoadingMixin],
        data: () => ({
            articles: [],
            nextURL: ''
        }),
        computed: {
            baseURL () {
                return `/api/articles/`
            },
            params () {
                let params = {}

                if (this.category) 
                    params.article_type = consts.articles.ArticleType[this.category]

                return _.assign(params, this.otherParams)
            }
        },
        props: {
            category: {
                type: String
            },
            otherParams: {
                type: Object
            }
        },
        ready () {
            this.$watch('category', () => {
                this.reset()
            })
        }
    }
</script>