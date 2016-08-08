<template>
    <div class="clearfix">
        <div class="col-xs-12 col-sm-6 col-md-8">
            <router-view></router-view>
        </div>
        <div class="col-xs-12 col-sm-6 col-md-4">
            <h3 style='color:#ccc'>
                资讯
            </h3>
            <article-list-group
                category="company"
                :other-params="{ limit: 10, fields: 'id,url,title,is_top,summary' }"
                :flush="true"
            >
            </article-list-group>
        </div>
    </div>
</template>

<style scoped>
    h3 {
        margin-bottom: 0.8rem;
    }
</style>

<script>
    import ArticleListGroup from 'articles/ArticleListGroup.vue'

    export default {
        components: { ArticleListGroup }
    }
</script>