<template>
    <div class="container">
        <article-item 
            v-for="article in articles" 
            :article="article" 
            track-by="$index">    
        </article-item>
    </div>
    <infinite-loading :on-infinite="onInfinite"></infinite-loading>
</template>

<script>
    import _ from 'lodash'
    import consts from 'consts.json'
    import ArticleItem from '../items/ArticleItem.vue'
    import InfiniteLoading from 'vue-infinite-loading'

    export default {
        components: {ArticleItem, InfiniteLoading},
        data: () => ({
            articles: [],
            nextURL: ''
        }),
        props: {
            category: {
                type: String,
                required: true
            }
        },
        ready () {
            this.$broadcast('$InfiniteLoading:reset')
            console.log(this.category)
        },
        methods: {
            onInfinite () {
                if (this.nextURL === '') 
                    this.nextURL = `/api/articles/?article_type=${consts.articles.ArticleType[this.category]}`
                this.$http.get(this.nextURL)
                    .then((res) => {
                        let data = res.data

                        this.nextURL = data.next
                        if (_.isNull(this.nextURL)) {
                            this.$broadcast('$InfiniteLoading:noMore')
                        }

                        this.articles = this.articles.concat(data.results)
                    }).then(() => {
                        this.$broadcast('$InfiniteLoading:loaded')
                    })
            }
        }
    }
</script>