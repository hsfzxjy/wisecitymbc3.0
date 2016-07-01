<template>
    <div class="container">
        <article-item 
            v-for="article in objects" 
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
    import InfiniteLoading from 'vue-infinite-loading'

    export default {
        components: {ArticleItem, InfiniteLoading},
        mixins: [InfiniteLoadingMixin],
        data: () => ({
            objects: [],
            nextURL: ''
        }),
        computed: {
            baseURL: {
                get () {
                    return `/api/articles/?article_type=${consts.articles.ArticleType[this.category]}`
                }
            }
        },
        props: {
            category: {
                type: String,
                required: true
            }
        },
        ready () {
            this.$watch('category', () => {
                this.reset()
            })
        }
    }
</script>