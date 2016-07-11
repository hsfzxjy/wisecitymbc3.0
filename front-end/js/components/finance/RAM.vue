<template>
    <div class="clearfix">
        <div class="col-xs-12 col-sm-6 col-md-8">
            <h3 style="color:#ccc">原材料</h3>
            <ram-item
                v-if="page.results"
                v-for="item in page.results"
                :model="item">
            </ram-item>
            <pager
                :model.sync="page"
                url="/api/raw_materials/">
            </pager>
        </div>
        <div class="col-xs-12 col-sm-6 col-md-4">
            <h3 style='color:#ccc'>
                资讯
            </h3>
            <article-list-group
                category="energy_and_raw_materials"
                :other-params="{ limit: 10, fields: 'id,url,title,is_top,summary' }"
                :flush="true">
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
    import RAMItem from './RAMItem.vue'
    import Pager from 'misc/Pager.vue'

    export default {
        components: { ArticleListGroup, RAMItem, Pager },
        data: () => ({
            page: {}
        }),
        route: {
            data (transition) {
                this.$broadcast('ListLoader:reload')
            }
        }
    }
</script>